# Reference Creator Workspace Audit 2026-05-18

## Observation Boundary

- [UI]{auth} `ChatGPT Images`, `Gemini`, and `Grok Imagine` were observed from already-authenticated shared browser pages on 2026-05-18.
- [UI]{public} `Midjourney Explore`, `Pippit`, and `ImageEZGen3D` were observed from public or non-destructively accessible pages on 2026-05-18.
- [UI]{public} Existing shared pages were reused for all observations; no new browser pages were opened for this audit.
- [UI]{public|auth} Screenshots were captured in-session for all six shared tabs.
- [OPEN] This audit focuses on layout, control density, and creation-surface hierarchy. It does not claim billing, quota, or deeper post-generation editing behavior beyond what was directly visible.

## Surfaces Reviewed

- [UI]{auth} ChatGPT Images 2.0 | AI Image Generator
- [UI]{auth} Google Gemini image-creation surface
- [UI]{auth} Grok Imagine
- [UI]{public} Midjourney Explore
- [UI]{public} Pippit AI home / composer surface
- [UI]{public} Hosted ImageEZGen3D app

## Per-Product Findings

### ChatGPT Images

- [UI]{auth} The first screen places one large composer near the top, with `Create an image` and `My images` on the same page rather than splitting create and history into different routes.
- [UI]{auth} The left rail is visually quiet: icon-first navigation, low ornament, and little copy competing with the main composer.
- [UI]{auth} The `Create an image` row uses image-led starter cards with short labels like `Improve Your Desk Setup`, `Wanderlust`, and `Scribble` instead of long instructional copy.
- [UI]{auth} Scrolling confirms that the page keeps prompt entry, starter ideas, and prior outputs within the same broad surface.
- [SYNTH] ChatGPT's strength is not novelty. It is restraint: one dominant prompt lane, one nearby inspiration row, and one nearby personal history region.

### Gemini

- [UI]{auth} Gemini leads with a large style wall under the heading `Pick a style for your image`, making style selection the main visual action before any deeper settings.
- [UI]{auth} The visible style options are concise and image-led: `Monochrome`, `Color block`, `Runway`, `Risograph`, `Technicolor`, `Gothic clay`, and `Dynamite` were directly visible during inspection.
- [UI]{auth} The composer sits at the bottom of the viewport with a stable prompt field, upload affordance, a `Create image` mode chip, and a mode picker showing `Thinking`.
- [UI]{auth} The page proves a useful composition pattern: inspiration and entry remain in the same viewport, but the inspiration is visual while the composer stays mechanically obvious.
- [SYNTH] Gemini feels strong because it turns style selection into a gallery, then anchors the actual creation control in one consistent place.

### Grok Imagine

- [UI]{auth} Grok combines a left workspace shell (`Projects`, `History`) with a main canvas that exposes `Featured Templates`, `Discover`, and a bottom composer in the same view.
- [UI]{auth} The bottom composer exposes compact mode chips such as `Agent (Beta)`, `Image`, `Video`, plus smaller controls like `Speed`, `Quality`, and an aspect-ratio chip.
- [UI]{auth} The top content region uses tall, visual template cards like `Background Generator`, `70s Street Style`, and `Virtual Try-On` before the user even touches the prompt field.
- [UI]{auth} The history list remains close enough to creation that the shell feels like a persistent workspace rather than a separate admin area.
- [SYNTH] Grok's most borrowable pattern is the three-layer stack: persistent memory on the side, visual starters above, compact creation controls below.

### Midjourney Explore

- [UI]{public} Midjourney Explore is browse-first and dense. The page foregrounds media over explanation, with filters such as `Top Day`, `Likes`, `Styles`, `Images`, and `Videos` visible at the top of the feed.
- [UI]{public} Clicking `Styles` confirmed that the page keeps content-type and sorting controls in a tight top band instead of scattering settings across separate panels.
- [UI]{public} The image grid is the product. The shell is thin, the filter vocabulary is short, and the browsing surface does most of the work.
- [SYNTH] Midjourney's strongest contribution here is density: less tutorial prose, more visual ranking and curation.

### Pippit

- [UI]{public} Pippit uses a bold, dark hero with a centered brand moment and a large premium-looking composer.
- [UI]{public} The composer exposes mode chips such as `Model` and `Image`, a large `Generate` call to action, and supporting language that reads like an agent prompt rather than a settings form.
- [UI]{public} Scrolling confirmed a visible follow-up prompt section (`No idea? Try the following ideas`) beneath the main composer.
- [UI]{public} The overall contrast model is aggressive: the page makes the composer feel like the product and everything else feel secondary.
- [SYNTH] Pippit's strongest pattern is tonal clarity. The page feels opinionated because one dramatic composer wins the hierarchy immediately.

### Hosted ImageEZGen3D

- [UI]{public} The hosted app still exposes multiple separate regions for creation, prompt templates, capture, preview, validation, and outputs.
- [UI]{public} The current surface makes heavy use of default Gradio block anatomy. Large empty artifact states and text-heavy cards visually outweigh the actual creation path.
- [UI]{public} Screenshots from this audit show that empty `Manifest`, `GLB`, `OBJ`, `PLY`, `STL`, and ZIP states consume too much rail area when no run exists yet.
- [UI]{public} The shell already has some of the right ingredients: history nearby, template cards, sample packs, and a hero. The current issue is composition quality rather than missing concepts.
- [REPO] The current implementation in [app.py](/home/brunner56/Workspaces/ImageEZGen3D/app.py) still relies on Gradio-native `File`, `Markdown`, `Examples`, `Image`, and `Group` surfaces for much of the visible layout.
- [SYNTH] ImageEZGen3D is currently concept-complete but composition-weak.

## Cross-Surface Design Reasons These References Feel Strong

### 1. One Dominant Creation Surface

- [UI]{auth} ChatGPT, Gemini, and Pippit each make one composer visually dominant.
- [UI]{auth} Grok still uses one dominant composer even though templates and history surround it.
- [SYNTH] Strong creator tools choose a primary action zone first, then make everything else subordinate to it.

### 2. Visual Starters Beat Explanatory Text

- [UI]{auth} ChatGPT uses image-led starter cards.
- [UI]{auth} Gemini uses a style wall with thumbnails.
- [UI]{auth} Grok uses featured templates with visual previews.
- [UI]{public} Midjourney makes the browse grid itself the visual starter system.
- [SYNTH] These products do not explain possibility first. They show it first.

### 3. History And Memory Stay Adjacent To Creation

- [UI]{auth} ChatGPT keeps `My images` on the same page as creation.
- [UI]{auth} Grok keeps `Projects` and `History` in the same shell as templates and the composer.
- [SYNTH] Persistence is not pushed into a separate admin tool. It remains close enough to support iteration.

### 4. Controls Are Short, Chip-Like, And Dense

- [UI]{auth} Gemini keeps mode and prompt controls compact.
- [UI]{auth} Grok uses chip-scale toggles for mode, speed, quality, and aspect ratio.
- [UI]{public} Midjourney uses compact top filters instead of long setting explanations.
- [SYNTH] The strongest creator surfaces compress control language until it becomes scannable.

### 5. Empty States Are Compact, Not Dominant

- [UI]{auth} The reference apps do not let blank download states dominate the page before creation.
- [UI]{public} Midjourney and Pippit avoid large dead boxes entirely on first load.
- [SYNTH] Large empty export tiles create a trust tax because they look like unfinished tooling rather than a polished creator surface.

### 6. The Browse Layer Serves The Composer

- [UI]{auth} ChatGPT, Gemini, and Grok use inspiration to accelerate creation rather than distract from it.
- [UI]{public} Midjourney proves that dense browse can work, but only because the browse layer is visually coherent.
- [SYNTH] Browse content should shorten time-to-start, not replace the start path.

### 7. Typography Carries Confidence

- [UI]{public} Pippit uses bold, dramatic branding and high contrast.
- [UI]{auth} ChatGPT and Gemini use large headings with restrained supporting text.
- [SYNTH] The common win is not a specific font. It is decisive hierarchy: short headings, short supporting lines, strong contrast, and fewer paragraphs.

## Repo Implications

- [REPO] ImageEZGen3D already has the correct functional primitives in [app.py](/home/brunner56/Workspaces/ImageEZGen3D/app.py): starter flows, prompt templates, sample packs, history, validation, preview, and exports.
- [SYNTH] The repo should consolidate the brief, hero upload, runtime lane, and generate action into one unmistakable composer instead of several sequential panels.
- [SYNTH] Prompt templates should become visibly differentiated cards, not mostly text blocks with a button attached.
- [SYNTH] Sample packs should be image-led by default. Text labels can remain secondary metadata.
- [SYNTH] The rail should keep preview, status, and history nearby, but empty export states should shrink until real artifacts exist.
- [SYNTH] Long explanatory paragraphs belong in a guide layer or in collapsible helper panels, not as the primary visual surface.
- [SYNTH] The right lesson to borrow is `workspace continuity`, not `fake immediacy`. Truthful output timing remains non-negotiable.

## What To Prefer / Defer / Avoid

- [SYNTH] Prefer one dominant composer, visual starter cards, compact control chips, and adjacent history.
- [SYNTH] Prefer image-led discovery over prose-led discovery.
- [SYNTH] Prefer compact artifact shells before generation and richer artifact cards only after files exist.
- [SYNTH] Defer deeper route trees, community browsing, or public sharing features until the core create surface feels premium.
- [SYNTH] Avoid report-style section stacking where every concept gets its own beige panel.
- [SYNTH] Avoid giant empty `File` placeholders and long help paragraphs above the fold.
- [SYNTH] Avoid copying auth walls, credit systems, or public feed mechanics just because the references use them.

## Open Questions

- [OPEN] The shared browser session did not include destructive or account-risky actions inside the reference tools, so deeper generation-state transitions were not probed.
- [OPEN] Some authenticated surfaces likely expose additional follow-up or editing states that were not explored in this pass.
- [OPEN] The latest local `app.py` redesign edits were not yet redeployed and revalidated in the hosted app during this documentation pass.
