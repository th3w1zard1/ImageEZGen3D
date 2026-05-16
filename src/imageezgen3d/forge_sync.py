from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote, urlencode, urlparse, urlunparse
from urllib.request import Request, urlopen


class ForgeSyncError(RuntimeError):
    pass


@dataclass(frozen=True)
class ForgeRepoStatus:
    provider: str
    slug: str
    http_url: str
    exists: bool
    created: bool
    auth_username: str = ""


def _request_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str],
    payload: dict[str, Any] | None = None,
) -> tuple[int, dict[str, Any] | list[dict[str, Any]] | None]:
    request_headers = dict(headers)
    body = None
    if payload is not None:
        request_headers["Content-Type"] = "application/json"
        body = json.dumps(payload).encode("utf-8")
    request = Request(url, data=body, method=method, headers=request_headers)
    try:
        with urlopen(request) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw) if raw else None
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        if exc.code == 404:
            return exc.code, None
        raise ForgeSyncError(f"{method} {url} failed with {exc.code}: {raw}") from exc


def _encoded_project_slug(slug: str) -> str:
    return quote(slug, safe="")


def _authenticated_git_url(base_url: str, slug: str, *, username: str, password: str) -> str:
    parsed = urlparse(base_url.rstrip("/"))
    netloc = f"{quote(username, safe='')}:{quote(password, safe='')}@{parsed.netloc}"
    return urlunparse((parsed.scheme, netloc, f"/{slug}.git", "", "", ""))


def build_gitlab_remote_url(base_url: str, slug: str, token: str) -> str:
    return _authenticated_git_url(base_url, slug, username="oauth2", password=token)


def build_forgejo_remote_url(base_url: str, slug: str, username: str, token: str) -> str:
    return _authenticated_git_url(base_url, slug, username=username, password=token)


def _gitlab_headers(token: str) -> dict[str, str]:
    return {"PRIVATE-TOKEN": token, "Accept": "application/json"}


def _forgejo_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"token {token}",
        "Accept": "application/json",
    }


def _gitlab_namespace_id(base_url: str, owner: str, token: str) -> int | None:
    if not owner.strip():
        return None
    query = urlencode({"search": owner, "full_path_search": "true"})
    status, payload = _request_json(
        "GET",
        f"{base_url.rstrip('/')}/api/v4/namespaces?{query}",
        headers=_gitlab_headers(token),
    )
    if status != 200 or not isinstance(payload, list):
        return None
    for namespace in payload:
        if not isinstance(namespace, dict):
            continue
        if namespace.get("full_path") == owner or namespace.get("path") == owner:
            namespace_id = namespace.get("id")
            if isinstance(namespace_id, int):
                return namespace_id
    return None


def ensure_gitlab_repository(
    *,
    base_url: str,
    slug: str,
    token: str,
    visibility: str,
) -> ForgeRepoStatus:
    owner, repo = slug.split("/", 1)
    project_url = f"{base_url.rstrip('/')}/api/v4/projects/{_encoded_project_slug(slug)}"
    status, payload = _request_json("GET", project_url, headers=_gitlab_headers(token))
    if status == 200 and isinstance(payload, dict):
        return ForgeRepoStatus(
            provider="gitlab",
            slug=slug,
            http_url=str(payload.get("http_url_to_repo", f"{base_url.rstrip('/')}/{slug}.git")),
            exists=True,
            created=False,
            auth_username="oauth2",
        )
    namespace_id = _gitlab_namespace_id(base_url, owner, token)
    create_payload: dict[str, Any] = {
        "name": repo,
        "path": repo,
        "visibility": visibility,
        "initialize_with_readme": False,
    }
    if namespace_id is not None:
        create_payload["namespace_id"] = namespace_id
    elif owner.strip():
        raise ForgeSyncError(
            f"GitLab namespace '{owner}' was not found; set IMAGEEZ_RELEASE_GITLAB_OWNER or create the namespace first."
        )
    _, created = _request_json(
        "POST",
        f"{base_url.rstrip('/')}/api/v4/projects",
        headers=_gitlab_headers(token),
        payload=create_payload,
    )
    if not isinstance(created, dict):
        raise ForgeSyncError("GitLab create project response was empty.")
    return ForgeRepoStatus(
        provider="gitlab",
        slug=slug,
        http_url=str(created.get("http_url_to_repo", f"{base_url.rstrip('/')}/{slug}.git")),
        exists=False,
        created=True,
        auth_username="oauth2",
    )


def _forgejo_user(base_url: str, token: str) -> dict[str, Any]:
    _, payload = _request_json(
        "GET",
        f"{base_url.rstrip('/')}/api/v1/user",
        headers=_forgejo_headers(token),
    )
    if not isinstance(payload, dict):
        raise ForgeSyncError("Forgejo user lookup returned no payload.")
    return payload


def ensure_forgejo_repository(
    *,
    base_url: str,
    slug: str,
    token: str,
    visibility: str,
) -> ForgeRepoStatus:
    owner, repo = slug.split("/", 1)
    current_user = _forgejo_user(base_url, token)
    current_login = str(current_user.get("login") or current_user.get("username") or "")
    repo_url = f"{base_url.rstrip('/')}/api/v1/repos/{owner}/{repo}"
    status, payload = _request_json("GET", repo_url, headers=_forgejo_headers(token))
    if status == 200 and isinstance(payload, dict):
        return ForgeRepoStatus(
            provider="codeberg",
            slug=slug,
            http_url=str(payload.get("clone_url", f"{base_url.rstrip('/')}/{slug}.git")),
            exists=True,
            created=False,
            auth_username=current_login,
        )
    create_payload = {
        "name": repo,
        "private": visibility != "public",
        "auto_init": False,
    }
    if owner == current_login:
        create_url = f"{base_url.rstrip('/')}/api/v1/user/repos"
    else:
        create_url = f"{base_url.rstrip('/')}/api/v1/orgs/{owner}/repos"
    _, created = _request_json(
        "POST",
        create_url,
        headers=_forgejo_headers(token),
        payload=create_payload,
    )
    if not isinstance(created, dict):
        raise ForgeSyncError("Forgejo create repository response was empty.")
    return ForgeRepoStatus(
        provider="codeberg",
        slug=slug,
        http_url=str(created.get("clone_url", f"{base_url.rstrip('/')}/{slug}.git")),
        exists=False,
        created=True,
        auth_username=current_login,
    )


def sync_git_repository(remote_url: str, branch: str) -> None:
    subprocess.run(
        ["git", "push", "--force", remote_url, f"HEAD:refs/heads/{branch}"],
        check=True,
    )
    subprocess.run(["git", "push", remote_url, "--tags"], check=True)