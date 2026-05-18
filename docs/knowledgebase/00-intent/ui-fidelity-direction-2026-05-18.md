# UI Fidelity Direction 2026-05-18

## Why This Exists

- [REPO] ImageEZGen3D already values truthful outputs, visible runtime decisions, preserved history, and auditable manifests.
- [UI]{auth} The strongest current creator tools pair those trust mechanics with a more decisive creation hierarchy.
- [SYNTH] The repo needs a higher-fidelity shell, not a looser truth contract.

## Direction

### 1. Make The Composer Win The Page

- [SYNTH] The first screen should read as `here is where you create`, not `here are several related panels about creation`.
- [SYNTH] Brief entry, hero-image upload, essential mode controls, and the primary generate action should read as one dominant system.

### 2. Keep Visual Starters Above Fold

- [SYNTH] Templates and starter captures should be visibly image-led and nearby, so the page teaches possibility without requiring the user to parse long copy blocks.

### 3. Keep Memory Adjacent, Not Dominant

- [SYNTH] History, projects, and recent runs should remain visible enough to support iteration, but secondary to the active composer.

### 4. Compress Controls

- [SYNTH] Mode, quality, route choice, and similar levers should read as short, chip-scale decisions whenever possible.
- [SYNTH] Long-form explanations should move to helper panels, post-selection guidance, or the Guide tab.

### 5. Shrink Empty Artifact States

- [SYNTH] Blank export surfaces should stay compact until real files exist. They should not visually outweigh the creation path.

### 6. Preserve Truthful Timing

- [REPO] The repo already established that previews and downloads must remain empty until verified artifacts exist.
- [SYNTH] This rule survives every future UI rewrite. Borrow the references' polish, not any illusion of instant results.

## Prefer / Defer / Avoid

- [SYNTH] Prefer premium composition, stronger contrast, image-led discovery, and fewer top-level panels.
- [SYNTH] Prefer creator-tool language over admin-tool language.
- [SYNTH] Defer social feeds, collaboration shells, and quota-heavy complexity until the core creation surface feels excellent.
- [SYNTH] Avoid beige report-panel sprawl, giant empty file cards, and explanatory text that competes with the start path.

## Immediate Repo Implications

- [REPO] The current shell in [app.py](/home/brunner56/Workspaces/ImageEZGen3D/app.py) should continue moving toward a single composer plus compact rail model.
- [SYNTH] Future UI passes should be judged against the reference questions below:
  - does one composer clearly dominate the page?
  - are visual starters more prominent than helper prose?
  - is history adjacent but secondary?
  - do blank outputs stay compact?
  - does the page still tell the truth about runtime and artifacts?

- [OPEN] The latest in-repo redesign edits still need redeploy and hosted browser verification after this documentation pass.
