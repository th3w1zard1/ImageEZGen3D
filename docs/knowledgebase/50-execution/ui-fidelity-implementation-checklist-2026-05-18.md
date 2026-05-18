# UI Fidelity Implementation Checklist 2026-05-18

## Purpose

- [REPO] This checklist translates the 2026-05-18 creator-workspace audit into implementation checks for ImageEZGen3D.
- [SYNTH] Use this when reviewing future UI changes so `better looking` is measured against specific outcomes instead of taste alone.

## Checklist

### Composer

- [SYNTH] One dominant composer is visible above the fold on common desktop widths.
- [SYNTH] Project brief, hero upload, key mode controls, and primary action feel like one system.
- [SYNTH] The first-run path does not require reading multiple long paragraphs before acting.

### Starter Systems

- [SYNTH] Prompt templates are visually distinct from one another.
- [SYNTH] Sample packs are image-led, not button-led, by default.
- [SYNTH] Starter choices remain usable on hosted and local paths without hidden asset assumptions.

### Workspace Memory

- [SYNTH] Recent runs stay visible close to creation.
- [SYNTH] History remains reopenable without leaving the shell.
- [SYNTH] The memory surface does not outrank the active composer.

### Outputs

- [SYNTH] Empty artifact states are compact.
- [SYNTH] Verified artifacts become visually richer only after files actually exist.
- [REPO] Truthful-output behavior remains intact for preview, manifest, GLB, OBJ, PLY, STL, and ZIP outputs.

### Typography And Density

- [SYNTH] Headings are short and high-contrast.
- [SYNTH] Helper text is secondary in both color and volume.
- [SYNTH] The page avoids large low-information beige regions.

### Validation

- [REPO] Browser verification must confirm the updated shell visually on the hosted app, not only in local screenshots.
- [REPO] Pre-run state must still show no fake outputs.
- [REPO] Post-run state must still show real artifacts and the executed runtime path.

## Stop Conditions

- [SYNTH] Do not call the UI pass done if the page still reads like stacked documentation instead of a creator workspace.
- [SYNTH] Do not call the UI pass done if empty export boxes still dominate the rail.
- [SYNTH] Do not call the UI pass done if improving visual polish weakened truthful runtime or artifact signaling.
