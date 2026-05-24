from __future__ import annotations

import math
from typing import Any

from .exporters import SimpleMesh


def _face_area(mesh: SimpleMesh, face: tuple[int, int, int]) -> float:
    vertices = [mesh.vertices[index] for index in face]
    ax, ay, az = (vertices[1][i] - vertices[0][i] for i in range(3))
    bx, by, bz = (vertices[2][i] - vertices[0][i] for i in range(3))
    cx, cy, cz = ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx
    return 0.5 * math.sqrt(cx * cx + cy * cy + cz * cz)


def subdivide_mesh(mesh: SimpleMesh, levels: int = 1) -> SimpleMesh:
    """Subdivide each triangle into four (loop-style midpoint split) for demo densification."""
    if levels < 1:
        return mesh
    vertices = list(mesh.vertices)
    faces = list(mesh.faces)
    edge_cache: dict[tuple[int, int], int] = {}

    def midpoint(a: int, b: int) -> int:
        key = (a, b) if a < b else (b, a)
        cached = edge_cache.get(key)
        if cached is not None:
            return cached
        ax, ay, az = vertices[a]
        bx, by, bz = vertices[b]
        vertices.append(((ax + bx) / 2, (ay + by) / 2, (az + bz) / 2))
        edge_cache[key] = len(vertices) - 1
        return edge_cache[key]

    for _ in range(levels):
        next_faces: list[tuple[int, int, int]] = []
        for face in faces:
            a, b, c = face
            ab = midpoint(a, b)
            bc = midpoint(b, c)
            ca = midpoint(c, a)
            next_faces.extend(
                [
                    (a, ab, ca),
                    (b, bc, ab),
                    (c, ca, bc),
                    (ab, bc, ca),
                ]
            )
        faces = next_faces
    return SimpleMesh(
        vertices=tuple(vertices),
        faces=tuple(faces),
        color=mesh.color,
        b64_image=mesh.b64_image,
    )


def decimate_mesh(
    mesh: SimpleMesh,
    target_faces: int,
) -> tuple[SimpleMesh, dict[str, Any]]:
    """Reduce face count to at most target_faces (smallest-area removal MVP)."""
    faces_before = len(mesh.faces)
    if faces_before <= target_faces or target_faces < 1:
        return mesh, {
            "decimation_applied": False,
            "faces_before": faces_before,
            "faces_after": faces_before,
        }

    ranked = sorted(
        mesh.faces,
        key=lambda face: _face_area(mesh, face),
        reverse=True,
    )
    kept = tuple(ranked[:target_faces])

    return (
        SimpleMesh(
            vertices=mesh.vertices,
            faces=kept,
            color=mesh.color,
            b64_image=mesh.b64_image,
        ),
        {
            "decimation_applied": True,
            "faces_before": faces_before,
            "faces_after": len(kept),
        },
    )
