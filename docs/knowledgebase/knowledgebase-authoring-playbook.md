# Knowledgebase Authoring Playbook

This note captures what this repository now appears to consider a good knowledgebase, based on the repo's existing docs and the research workflow used to expand them.

The intended downstream use is to seed a future skill, agent, or prompt that can build or extend a knowledgebase in one autonomous pass without collapsing into shallow summaries, generic link dumps, or ungrounded speculation.

## Purpose

The goal is not to write "documentation" in the abstract.

The goal is to create a research-backed operating memory for a project that:

- reflects repo intent and user customizations;
- captures current theory, product patterns, and implementation constraints;
- separates facts, inferences, and aspirations;
- captures user process preferences, not just domain content preferences;
- stays actionable for future implementation work.

## What A Good Knowledgebase Means Here

For this repo and this user workflow, a good knowledgebase is:

- evidence-first;
- current rather than stale;
- structured by decision surface, not by random topic accumulation;
- explicit about uncertainty and source quality;
- useful for implementation, UX design, architecture, runtime, legal, and verification work;
- broad enough to include adjacent research that may matter soon, not only what the code already does.

It is not:

- a giant unstructured paper dump;
- a shallow summary of marketing pages;
- a generic best-practices guide detached from the repo;
- a single mega-file that mixes theory, UX, runtime, and roadmap without boundaries.

## What Counts As Relevant

The working definition of relevance in this project is intentionally broad.

Something is relevant if it can influence any of the following:

- implementation architecture;
- user experience and workflow;
- runtime or deployment strategy;
- failure handling and recovery;
- evaluation and verification;
- legal, licensing, or operational safety;
- future roadmap decisions;
- how a future skill or agent should reason about the project.

This includes material that is only vaguely adjacent when it could reasonably affect future product choices, terminology, research direction, or implementation boundaries.

## Relevance Tiers

To keep "exhaustive" from becoming shapeless, use three tiers.

### Tier 1: Directly Actionable

Include anything that directly changes what should be built, validated, or avoided now.

Examples:

- runtime constraints such as ZeroGPU rules;
- library-specific behavior;
- capture guidance;
- export requirements;
- failure-mode recovery;
- UX patterns that clearly map to the app.

### Tier 2: Strongly Directional

Include anything that strongly influences near-term product or architecture choices.

Examples:

- competitive UX patterns from major end-user apps;
- representation tradeoffs such as mesh versus splat;
- multi-view versus single-image framing;
- evaluation frameworks;
- configuration and manifest strategy.

### Tier 3: Frontier Or Adjacent

Include emerging or adjacent research if it may matter soon, but label it as frontier tracking rather than current product truth.

Examples:

- new 3D representations;
- active view selection;
- relightable materials;
- WebGPU-native delivery;
- new creator-tool interaction models.

## Source Priority

When building a knowledgebase in one shot, sources should be weighted in this order.

1. User customizations, instructions, preferences, and memory.
 This includes user-provided planning artifacts, cross-repo operating plans, and explicit preferences about validation, vertical slices, or documentation maintenance.
2. Existing knowledgebase docs.
3. Repo-local evidence such as README, config, tests, tasks, launch configs, scripts, and git history.
4. Current official docs for libraries, frameworks, SDKs, CLIs, and platforms.
5. Direct observation of official product surfaces for UX and workflow research.
6. Current external research and comparison sources.
7. Community anecdotes and social discussion.

Lower-priority sources can inform exploration, but they should not overrule higher-priority evidence.

## Evidence Rules

Every serious knowledgebase pass should distinguish among these categories:

- observed repo facts;
- observed product or UI facts;
- official claims from current docs or vendor pages;
- synthesized conclusions;
- open questions or caveats.

Do not blur them together.

If a page is auth-gated or partially inaccessible, say so and separate what was actually observed from what was claimed elsewhere.

## Auth-Gated Terminology

Use the common industry terms instead of inventing local names.

- `login wall`: the clearest and most widely recognized UX term for a page or flow that forces users to log in or register before they can access meaningful content or functionality;
- `sign-in wall`: a close synonym, often used when the emphasis is on the entry screen itself;
- `auth gate` or `authentication gate`: common product and engineering terms for a feature or surface that is conditionally blocked behind authentication;
- `gated experience` or `gated surface`: umbrella terms for any experience where access is restricted until some condition, often authentication, is met;
- `hard auth gate`: no meaningful value before login;
- `soft gate` or `post-value auth`: users can inspect, preview, or partially use the product before auth is required.

For knowledgebase work, `login wall` should be the default UX term and `auth gate` the useful systems term.

## Single-Shot Research Workflow

"Single shot" should mean autonomous end-to-end completion in one session, not superficiality.

Recommended workflow:

1. Load user customizations and relevant instruction files.
2. Read the existing knowledgebase before creating new docs.
3. Inspect repo-local anchors: README, config, tests, tasks, scripts, architecture, and git history.
4. Determine what the project is trying to be, what it is avoiding, and what it treats as a definition of done.
5. Identify gaps in the current knowledgebase.
6. Use current official docs for any named library, framework, SDK, CLI, or cloud platform.
7. Use direct website or product-surface inspection when the task involves UX, feature sets, or end-user workflow patterns.
 When authenticated surfaces are available, inspect both public and logged-in states if possible and label which observations came from which state.
8. Expand outward into theory, science, competitive analysis, and adjacent research.
9. Synthesize stable conclusions and clearly mark frontier or speculative material.
10. Write or update a focused set of docs rather than one giant file.
11. Integrate the new docs back into the main intent layer.
12. Validate the documentation patch.

## Tool Strategy For A Future Skill Or Agent

A future knowledgebase-builder skill or agent should prefer this tool strategy.

### Repo Understanding

- use file and text search to map the repo quickly;
- read the nearest existing docs before creating new ones;
- inspect git history, but do not pretend shallow history contains patterns it does not.

### Current Documentation

- use current official documentation tools for libraries and platforms;
- do not rely on stale training memory for API details or platform behavior.

### Product And UX Research

- use browser tools for official product pages when the user asks about interface, flows, or visible features;
- use search and web-fetch tools to identify candidate products before inspecting them;
- distinguish public landing-page behavior from logged-in product behavior.
- do not reload or mutate signed-in tabs unnecessarily when the user is actively using them; prefer read-only inspection first.

When the user asks for deeper page-by-page product analysis, prefer a repeated investigation format instead of one broad summary:

- run at least three prompt-behavior investigations per page;
- keep each investigation grounded in the visible placeholder text, example chips, template labels, mode toggles, route structure, and credit or failure messaging;
- record one concrete example prompt, the likely intuitive path, the key UI components, and repo implications for each investigation;
- use subagents when the surface set is large enough that per-page reasoning would otherwise collapse into shallow notes;
- preserve the non-destructive rule unless the user explicitly authorizes submissions, reloads, or credit-spending actions.

When the request is specifically about frontend implementation quality rather than only product behavior, extend the pass with safe live probes:

- verify the actual page title and URL for each shared tab before trusting the attachment label;
- use `read_page` for the structural snapshot and `run_playwright_code` for control semantics, role quality, option counts, and route changes;
- prefer safe clicks that open menus, focus fields, or switch tabs over actions that submit, upload, or spend credits;
- document whether key controls are real buttons, menu buttons, listboxes, or unlabeled divs, because this materially affects accessibility and automation.

### Broad Research

- use broad web search or a research subagent when the space is large and open-ended;
- compress findings into stable themes, not a raw source dump.

### Validation

- validate documentation edits with `git diff --check` at minimum;
- use status or diff output to confirm touched scope;
- if code was changed, run the narrowest relevant executable checks.
- when a request spans source, runtime, docs, or built artifacts, verify source-versus-runtime parity instead of assuming the repo and the served experience match.

For research-heavy passes, also validate the evidence boundary explicitly:

- label whether the observation came from a public or authenticated surface;
- state whether prompts were submitted or not;
- state whether runtime, quota, or failure handling was directly observed or only inferred from visible UI.

## Process Preferences From User Planning Artifacts

User-provided plans, even from other repositories, can reveal durable operating preferences.

Treat them as preference evidence when they consistently emphasize:

- vertical-slice completeness across source, runtime, tests, static assets, and docs;
- a validation ladder that runs the narrowest useful check immediately after edits;
- source-versus-runtime drift detection;
- docs, runbooks, and instruction parity as part of product quality;
- graceful degradation and explicit fallback behavior for optional capabilities;
- active pruning of stale guidance instead of layering conflicting instructions forever;
- living-plan maintenance after each implementation pass.

These should inform how the future knowledgebase-builder agent works, but they should not be misrepresented as repo-local product facts unless the target repo itself shows the same pattern.

## Recommended Knowledgebase Taxonomy

The current repository suggests a useful structure for future knowledgebases.

### Intent Layer

- project intent;
- cleanup patterns;
- goals and non-goals;
- stable conclusions.

### Architecture And Runtime Layer

- architecture decisions;
- configuration;
- runtime strategy;
- deployment constraints.

### Domain And Theory Layer

- science and math;
- representation tradeoffs;
- methodology;
- frontier research.

### Product And UX Layer

- creator product patterns;
- competitive product benchmark;
- auth-gated UX patterns;
- frontend UX blueprint;
- workflow guidance.

### Operational Risk Layer

- failure modes;
- verification;
- license and dependency audit;
- security or secret-handling constraints.

### Execution Layer

- roadmap;
- workflow docs;
- implementation implications;
- editor and deployment instructions.

### Meta Layer

- authoring playbooks such as this one;
- future skill or agent specifications;
- curation rules for keeping the knowledgebase coherent over time.

## Authoring Rules

### Prefer Focused Companion Docs

When a topic becomes large, split it into a focused companion doc and link it from the intent layer.

Do not keep stuffing everything into one document.

### Start With Source Basis

When practical, state what the document is based on.

That makes the note auditable and easier to update later.

### Tie Research Back To The Repo

Do not stop at "here is what the field says."

Every substantial research note should answer some version of:

- what does this mean for this repo;
- what should be preferred;
- what should be deferred;
- what should be avoided.

### Preserve Caveats

A good knowledgebase says when:

- the git history is shallow;
- the product page is auth-gated;
- the evidence is anecdotal;
- the platform rules may change;
- the conclusion is provisional.
- the observation came from a signed-in or signed-out product state.

### Prefer Stable Conclusions Over Exhaustive Naming

Enumerate products, papers, or tools when they matter, but prioritize stable themes that survive vendor and branding churn.

### Include Failure And Verification

Knowledgebases should not only describe ideals.

They should also explain:

- how things fail;
- how the user recovers;
- how the team verifies claims.

### Separate Product Surface States

When a product behaves differently before and after login, document both states.

- public browse state;
- authenticated workspace state;
- where the auth gate actually sits;
- whether creation, editing, history, collaboration, or export is gated.

### Keep Speculation Labeled

When something is a future direction rather than current truth, label it explicitly.

## Gotchas

### Shallow History Trap

If the repo has little git history, do not invent cleanup trends. Say that the history is shallow and derive patterns from current structure and docs instead.

### Marketing Trap

Product pages are useful for feature framing and UX patterns, but they are not neutral sources. Separate observed behavior from vendor claims.

### Auth Wall Trap

Some of the most popular apps gate core UX behind login. Public pages can still teach useful patterns, but the knowledgebase should note the observation boundary.

### Source-Versus-Runtime Drift Trap

A repo can look coherent in source while shipped behavior, built assets, hosted routes, or runtime docs say something different. A serious knowledgebase pass should notice and record that drift.

### Stale Guidance Layering Trap

When a newer plan, handbook, or runbook supersedes an older one, do not preserve both as if they are equally current. Collapse or clearly rank authority.

### Mega-File Trap

One huge file feels exhaustive but is usually less useful than a network of linked, focused notes.

### Generic Summary Trap

A knowledgebase is not good just because it is long. If it does not influence implementation or product judgment, it is probably noise.

### Staleness Trap

Library docs, platform rules, and product UIs change quickly. Date external research when it matters.

### Confused Evidence Trap

Do not mix:

- repo facts;
- external research;
- user preference;
- aspirational roadmap;
- agent inference.

Keep those layers legible.

### Overfitting Trap

Do not turn one competitor into the product template. Borrow patterns, not identity.

## What This Repo Seems To Value Most

From the current conversation and knowledgebase, the strongest recurring values are:

- explicit intent over hidden magic;
- inspectable runs over black-box behavior;
- staged workflows over one-click mystique;
- mesh-first creator utility over novelty-first representations;
- current research translated into product decisions;
- direct UX usefulness, not just model fascination;
- source, runtime, validation, and documentation staying in sync;
- vertical-slice completeness over isolated patches;
- verification and recoverability as part of product quality.

Any future knowledgebase-building skill should optimize for those values.

## Suggested Output Contract For A Future Skill Or Agent

A future one-shot knowledgebase builder should, at minimum:

1. read customizations, memory, and existing docs first;
2. determine project intent and non-goals;
3. identify missing knowledgebase surfaces;
4. gather current official docs and external research;
5. inspect relevant product UIs when UX patterns are part of the request;
6. create or update a structured doc set, not just one mega-summary;
7. integrate the new docs into the intent layer;
8. record caveats, evidence limits, and frontier material clearly;
9. validate the documentation patch before finishing;
10. distinguish public versus authenticated product observations when relevant;
11. update or prune superseded meta guidance when a better plan replaces it.

## Definition Of Done

A knowledgebase pass should count as complete only when:

- the project's current intent is captured accurately;
- repo-local constraints and risks are represented;
- relevant theory and research are translated into repo implications;
- product and UX patterns are synthesized, not just listed;
- failure, verification, and operational concerns are covered;
- new notes are organized coherently within the knowledgebase;
- public and authenticated product behaviors are not conflated;
- source-versus-runtime drift has been checked where relevant;
- documentation changes are validated.

## Practical Bottom Line

The right future skill or agent is not "a thing that writes lots of markdown."

It is a system that:

- reads the user's customizations and preferences first;
- treats the repo as evidence, not just code;
- researches widely but filters by relevance;
- builds a layered, auditable knowledgebase;
- preserves the distinction between public product surfaces and authenticated workspace surfaces;
- keeps plans, docs, and runtime claims in sync;
- leaves behind documents that directly help future implementation work.
