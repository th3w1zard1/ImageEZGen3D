# Frontend Implementation Patterns 2026

This note captures implementation-level frontend decisions observed directly from the currently shared browser tabs, not just product-level feature summaries.

The goal is to identify what leading tools are doing well in their actual UI structure, control semantics, shell behavior, and interaction choreography, and to separate that from places where the implementation appears brittle, inaccessible, or overly dense.

## Source Basis

- [UI]{auth} Live browser inspection of the currently shared tabs for ChatGPT Images, Google Gemini, Grok Imagine, Adobe Firefly, and the ChatGPT login wall on 2026-05-16.
- [UI]{public} Live browser inspection of the currently shared tabs for Midjourney Explore, Pippit, and an empty `about:blank` control tab on 2026-05-16.
- [UI]{public} Safe interactive probing using `open_browser_page`, `read_page`, `click_element`, and `run_playwright_code` on each shared tab.
- [OFFICIAL] W3C WAI guidance for menu buttons, listboxes, and form labels from the ARIA Authoring Practices Guide and WAI Forms Tutorial.
- [OPEN] No prompts were submitted, no pages were reloaded, and no generation, upload, or credit-spending actions were performed.
- [OPEN] Shared-tab identifiers drifted from some attachment labels during live inspection, so conclusions below are based on the verified live page title and URL rather than the attachment label alone.

## Method

- [SYNTH] Verify the actual live title and URL for each shared tab before drawing conclusions.
- [SYNTH] Prefer safe clicks that expose menus, toggle shell regions, or focus inputs without starting a generation flow.
- [SYNTH] Use Playwright probes to inspect actual control structure, labels, roles, counts, and route changes, not only the visible text in snapshots.
- [SYNTH] Treat console and network errors as implementation evidence when they appear repeatedly on a live page, especially if the UI shell still renders.

## Cross-Surface Implementation Patterns

### 1. Persistent Shells Work Best When The Primary Action Stays Obvious

- [UI]{auth} Gemini, Grok, and Firefly all keep account shell, navigation, history, or suite routes visible around the main creative surface.
- [UI]{auth} ChatGPT Images also keeps the broader ChatGPT shell visible, but the actual prompt field was present in the DOM while not visible in the viewport during the probe.
- [SYNTH] Persistent workspace chrome is now standard, but it becomes a liability if the primary composer falls below the fold or competes with unrelated shell density.
- [SYNTH] ImageEZGen3D should keep a shell for history and reruns, but the upload and generate lane must remain visible without requiring a scroll hunt.

### 2. Explanatory Mode Pickers Outperform Opaque Speed Toggles

- [UI]{auth} Gemini exposes a mode menu with `Fast`, `Thinking`, and `Pro`, each paired with a short explanatory subtitle such as `Answers quickly` or `Solves complex problems`.
- [SYNTH] This is better than a bare speed toggle because it translates compute or reasoning tradeoffs into plain user outcomes.
- [SYNTH] ImageEZGen3D should prefer user-facing labels like `Draft`, `Quality`, or `Recommended`, plus one-line consequence labels, over backend-centric terms.

### 3. Grouped Model Pickers Need Provenance And Safety Context

- [UI]{auth} Firefly's expanded model picker groups choices into `Adobe models` and `Partner models`.
- [UI]{auth} The picker also exposes support links such as `Commercially safe` and `Models created by others` beside the grouped options.
- [OFFICIAL] W3C's listbox guidance says grouped options need accessible names and warns that long, repetitive option names degrade usability.
- [SYNTH] Firefly is doing the right high-level thing by grouping provenance, but a long model list still needs careful naming and navigation support.
- [SYNTH] ImageEZGen3D should group future runtime or adapter options by provenance and cost, keep names short, and expose why a category exists.

### 4. Route-Preserving Media Switches Reduce Context Loss

- [UI]{public} Clicking Midjourney's `Videos` tab changed the route from `/explore?tab=top` to `/explore?tab=video_top` while preserving the overall shell and social feed pattern.
- [UI]{public} The same layout family remains intact while the feed content and action affordances shift from images to videos.
- [SYNTH] This is a strong implementation pattern: use route or state changes to swap content classes without making the user feel they left the workspace.
- [SYNTH] ImageEZGen3D should keep draft mesh, quality mesh, turntable preview, and export inspection inside one coherent shell instead of bouncing users to unrelated pages.

### 5. Template Systems Need Strong Taxonomy And Eventual Compression

- [UI]{auth} Grok exposed approximately 58 template buttons during the live probe.
- [UI]{auth} The visible names are short, noun-driven, and outcome-oriented: `Chibi`, `Professional Headshot`, `Object Remover`, `Product Showcase`, `Pulp Cover`, `3D Animation`, and many more.
- [SYNTH] This helps first-run activation because the names encode deliverable types, not internal mechanics.
- [SYNTH] The tradeoff is scale pressure: as the starter system grows, search, grouping, or curation becomes mandatory.
- [SYNTH] ImageEZGen3D should adopt semantic starter flows, but keep the early set tight and curated.

### 6. Auth Walls Work Better With Redundant Entry Paths And Clean Hierarchy

- [UI]{public} The current ChatGPT login wall offers `Continue with Google`, `Continue with Apple`, `Continue with phone`, an `OR` divider, and an email field with a `Continue` button.
- [OFFICIAL] W3C labeling guidance recommends explicit labels for form controls and warns against relying on placeholders or `title` alone.
- [SYNTH] This is a clean auth wall composition: multiple identity providers, one clear fallback path, and a low-cognitive-load stack.
- [SYNTH] If ImageEZGen3D ever adds sign-in, it should preserve that clarity and keep visible labels or explicit field identification instead of placeholder-only auth forms.

### 7. Semantic Quality Is A Real Product Feature

- [UI]{public} On Pippit, live probing found the visible `Video`, `Image`, and `Home` controls rendered as plain `div` elements with no button role, while `Assets` appeared as a `menuitem`.
- [UI]{public} The same page reported `buttonCount: 0` in the live DOM probe despite clearly visual interactive affordances.
- [OFFICIAL] W3C's menu button guidance expects a real button with `aria-haspopup` and `aria-expanded`; the forms guidance expects properly identified controls.
- [SYNTH] Weak semantics make a UI harder to automate, less predictable for assistive tech, and more fragile under keyboard use.
- [SYNTH] ImageEZGen3D should use actual buttons, menus, listboxes, and labeled inputs for all core actions, not div-based lookalikes.

### 8. Reliability Debt Shows Up In The Shell Before It Breaks The Flow

- [UI]{auth} Firefly exposed repeated console and request failures during the live probe, including top-app-bar errors, aborted requests, and repeated preload warnings, while the main workspace still rendered.
- [UI]{public} Pippit earlier exposed runtime and CORS failures while the core prompt surface still rendered.
- [SYNTH] These products demonstrate a useful lesson even when they are misbehaving: graceful partial rendering matters, but noisy or brittle shell infrastructure undermines trust.
- [SYNTH] ImageEZGen3D should keep optional shell surfaces non-critical and ensure failures degrade into explicit, local recoverable states.

## Per-Page Implementation Notes

### ChatGPT Images

- [UI]{auth} The `Describe a new image` composer exists in the DOM, but the live probe reported it as not currently visible in the viewport.
- [UI]{auth} The page keeps a dense persistent shell with recents, projects, and chat history around the image mode.
- [SYNTH] Good: strong workspace continuity. Risk: the image-mode primary action can become visually secondary to the broader assistant shell.
- [SYNTH] ImageEZGen3D should borrow continuity, not the above-the-fold ambiguity.

### Google Gemini

- [UI]{auth} The primary prompt lane is extremely legible: style strip, prompt field, upload affordance, active `Create image` tool, and a descriptive mode picker.
- [UI]{auth} The clicked mode picker clearly exposed `Fast`, `Thinking`, `Pro`, and an inline `Upgrade` path.
- [SYNTH] Good: progressive disclosure with explanatory menu copy. ImageEZGen3D should imitate this shape closely.

### Grok Imagine

- [UI]{auth} The shell keeps search, projects, history, and the `Imagine` lane persistently visible.
- [UI]{auth} The starter system is large, noun-driven, and centered on recognizable outcomes rather than internal parameters.
- [SYNTH] Good: prompt activation via outcome taxonomy. Risk: starter overgrowth without search or grouping.

### Midjourney Explore

- [UI]{public} The clicked `Videos` tab changed the route while preserving the explore shell.
- [UI]{public} Visible control clusters include feed scope, media type, aspect presets, quality/speed controls, and social actions like follow and like.
- [SYNTH] Good: public browse teaches the product vocabulary before subscription. ImageEZGen3D can borrow the browse-before-commit mental model without copying the gate.

### Adobe Firefly

- [UI]{auth} The model picker exposes a long grouped radio-style choice list, provenance grouping, and adjacent explanatory links.
- [UI]{auth} The broader shell also keeps `Create`, `Generate`, `Boards`, `AI Assistant Beta`, `Production`, `Quick actions`, `Your stuff`, `Custom models`, and `Gallery` visible.
- [SYNTH] Good: clear multi-model disclosure and suite continuity. Risk: large-shell brittleness and too many adjacent routes near the main prompt lane.

### Pippit

- [UI]{public} The prompt-first lane is clear and the composer copy is strong.
- [UI]{public} The DOM semantics are weak for several visually interactive elements, which is a concrete frontend implementation warning sign.
- [SYNTH] Good: multimodal evidence conditioning. Risk: low semantic quality and earlier runtime instability.

### ChatGPT Login Wall

- [UI]{public} The sign-in wall is structurally simple: three provider buttons, an `OR` divider, a focused email field, and a single fallback action.
- [SYNTH] Good: auth wall clarity without heavy surrounding chrome. If auth is ever added, ImageEZGen3D should prefer this kind of clean hierarchy.

### Blank Tab

- [UI]{public} The shared `about:blank` tab had no product content and served only as a control surface during the investigation.
- [SYNTH] No product implications.

## Official Best-Practice Overlay

### Menu Buttons

- [OFFICIAL] W3C's menu button pattern expects a real button, `aria-haspopup`, and `aria-expanded`, with keyboard entry through `Enter`, `Space`, and optionally arrow keys.
- [SYNTH] Gemini's mode picker and Firefly's model picker are directionally aligned with this pattern; Pippit's div-based mode chips are not.

### Listboxes And Long Option Menus

- [OFFICIAL] W3C warns that listboxes should not contain interactive elements inside options, grouped options need accessible names, and long repetitive option names degrade usability.
- [OFFICIAL] W3C strongly recommends `Home`, `End`, and type-ahead support for longer lists.
- [SYNTH] Firefly's model list should be treated as a strong pattern for grouped provenance disclosure, but the longer the list gets, the more keyboard and naming discipline matter.

### Labels And Prompt Inputs

- [OFFICIAL] W3C recommends explicit labels for form controls whenever possible and does not recommend relying on `title` as a replacement.
- [OFFICIAL] Visible labels above fields often work better for mobile and low-vision users than unlabeled placeholder-only fields.
- [SYNTH] ImageEZGen3D should keep the main prompt or instruction field visibly identified and should not rely on placeholder text alone to explain purpose.

## What To Prefer In ImageEZGen3D

- [SYNTH] Keep the primary upload-and-generate lane above the fold even when history and shell chrome are visible.
- [SYNTH] Use real button, menu button, listbox, and labeled field semantics for all critical actions.
- [SYNTH] Keep route or mode changes inside one persistent shell instead of fragmenting the workflow.
- [SYNTH] Use short, outcome-oriented starter flows and grow them carefully.
- [SYNTH] Group future model, adapter, or runtime options by provenance and cost with explicit naming.
- [SYNTH] Expose descriptive mode labels like `Draft`, `Quality`, and `Recommended`, not opaque infrastructure terms.
- [SYNTH] Preserve artifact-local next actions so refinement starts from a result rather than a blank form.

## What To Avoid In ImageEZGen3D

- [SYNTH] Letting workspace chrome push the main composer out of view.
- [SYNTH] Div-based faux controls for primary actions or mode switches.
- [SYNTH] Unbounded template growth without grouping or curation.
- [SYNTH] A multi-model picker that lacks provenance, safety context, or short option names.
- [SYNTH] Telemetry-heavy or shell-heavy UI wiring that can fail noisily while the core flow depends on it.
