# Knowledgebase Builder Agent Spec

This note turns the authoring playbook into a more operational blueprint for a future skill or agent that can build or extend a knowledgebase in one autonomous pass.

## Mission

Create a layered, research-backed, repo-aware knowledgebase that reflects:

- the user's customizations and preferences;
- the target repository's actual intent and constraints;
- current official documentation;
- product-surface and workflow research where relevant;
- broader theory, domain, and frontier context when it materially affects decisions.

## Primary Success Criteria

The agent succeeds when it leaves behind a knowledgebase that future implementation work can rely on directly.

That means the output must be:

- current;
- auditable;
- structured;
- decision-oriented;
- explicit about caveats;
- validated before completion.

## Inputs

The agent should expect these inputs when available:

- repository path;
- existing knowledgebase folder or docs set;
- user customization files, instructions, memory, and planning artifacts;
- specific user requests about scope, depth, or priorities;
- access to browser and documentation tools;
- optional existing research notes or prior session memories.

## Required Behavioral Contract

### 1. Read Preference Signals First

Before broad repo or web research, read:

- user instructions;
- memory or saved preferences;
- existing knowledgebase intent docs;
- any user-provided planning or methodology documents.

This ensures the agent reflects customizations instead of acting like a generic summarizer.

### 2. Treat The Repo As Evidence

The agent should inspect:

- README;
- architecture and configuration files;
- tests and validation scripts;
- tasks and launch configs;
- docs and runbooks;
- git history when useful.

It should not invent historical trends when the repo history is shallow.

### 3. Expand Research Outward In Controlled Layers

Recommended order:

1. repo-local truth;
2. official docs;
3. official product surfaces;
4. broader external research;
5. frontier or adjacent material.

### 4. Distinguish Evidence Types

The agent must clearly separate:

- observed repo facts;
- observed product/UI facts;
- official claims;
- synthesized conclusions;
- open questions;
- speculative or frontier notes.

### 5. Prefer Focused Docs Over A Mega-File

When the topic is large, the agent should create a focused doc network with links rather than one giant markdown file.

### 6. Integrate Back Into Intent

New docs should not remain isolated. The agent should update the main intent or index layer so the knowledgebase remains navigable.

## Tool Requirements

### Documentation Tools

- always use current official docs for named libraries, frameworks, SDKs, CLIs, or platforms;
- do not rely on stale model memory for recent APIs or platform constraints.

### Browser Tools

- use browser inspection for official product surfaces when UX, flow, or feature discoverability matters;
- inspect both public and authenticated surfaces when available;
- avoid reloading or disrupting active user sessions unnecessarily.

When the user asks for deeper product-surface analysis instead of a light benchmark:

- perform at least three prompt-behavior investigations per relevant page;
- keep each investigation grounded in visible prompts, chips, template labels, route structure, mode toggles, and any visible credit or failure language;
- record one concrete example prompt, likely intuitive path, key UI components, observation boundary, and repo implication for each investigation;
- use subagents when the number of pages is large enough that per-page reasoning would otherwise become shallow.

### Search And Research Tools

- use search or research tools to identify candidate products or sources before deep inspection;
- compress large result sets into stable themes and ranked signals.

### Repo Tools

- use targeted file reads and searches to find the nearest relevant context;
- prefer narrow, local context over broad repo wandering.

## Output Package

At minimum, the agent should produce:

1. an updated intent or index document;
2. focused companion docs for major knowledge surfaces;
3. explicit caveats where evidence is partial;
4. validation output proving the docs patch is clean.

When the user goal is to create a reusable process, the agent should also produce:

1. a playbook or methodology doc;
2. a skill or agent spec, or both.

## Preferred Knowledge Surfaces

The agent should usually cover these layers when relevant:

- intent and cleanup patterns;
- architecture and runtime;
- theory and methodology;
- product and UX patterns;
- failure, verification, and operational risk;
- roadmap or execution implications;
- meta authoring or agent behavior guidance.

## Validation Contract

The agent must validate documentation changes before finishing.

Minimum:

- `git diff --check` on touched docs;
- `git status` or equivalent to confirm touched scope.

If code or runnable assets were changed:

- run the narrowest relevant executable validations first;
- when runtime and built assets can drift, validate the runtime-facing surface too.

## Process Preferences To Preserve

If user-provided plans or customizations reveal these preferences, the agent should preserve them:

- vertical-slice completeness instead of isolated edits;
- validation immediately after first substantive edits;
- source-versus-runtime parity checks;
- docs and runbook parity with actual behavior;
- explicit graceful degradation and fallback reasoning;
- removal or collapse of stale guidance;
- living-plan maintenance after each pass.

## Failure Behaviors

If the agent cannot fully inspect a surface, it should:

- say whether the barrier was auth, sharing, or missing tool access;
- continue with the best available higher-confidence evidence;
- avoid overstating conclusions drawn from incomplete observation.

If research is broad and conflicting, it should:

- prioritize the source hierarchy;
- record disagreement as an open question or frontier note;
- still synthesize stable conclusions where possible.

## Anti-Patterns

The future agent should avoid:

- generating a long but shapeless markdown dump;
- confusing marketing copy with observed behavior;
- treating another repo's planning preferences as target-repo product facts;
- ignoring runtime or hosted behavior in favor of source-only confidence;
- leaving behind disconnected docs with no index or intent integration;
- finishing without validation.

## Definition Of Done

The agent is done when:

- the repo's current intent is clear;
- the user's customization signals are reflected;
- relevant official docs and external research were incorporated;
- product and UX patterns are synthesized meaningfully;
- failure, verification, and operational constraints are represented;
- the knowledgebase is organized as a usable doc system;
- the documentation patch has been validated.

## Practical Use

This spec is meant to be the bridge between a general authoring playbook and an actual reusable skill or agent definition.

If a future implementation turns this into `SKILL.md`, `.agent.md`, or a prompt file, this document should serve as the operational contract.
