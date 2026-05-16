# Prompt Behavior Investigations 2026

This note captures a deeper, per-page prompt-behavior pass across the current 2026 consumer creator surfaces already opened in the user's browser.

The goal is not to guess hidden product behavior from marketing pages. The goal is to document what the currently visible surfaces teach about prompting, intuitive UI components, workspace continuity, auth gating, and how creator tools reduce the cost of the next action.

## Source Basis

- [UI]{auth} Live extracted authenticated surfaces from the user's existing tabs on 2026-05-15 and 2026-05-16 for ChatGPT Images, Gemini, Grok Imagine, Adobe Firefly, CapCut home, and two CapCut agent surfaces.
- [UI]{public} Live extracted public or partially public surfaces from the user's existing tabs on 2026-05-15 and 2026-05-16 for Midjourney Explore and Pippit.
- [SYNTH] Each page below was analyzed through three prompt investigations using subagents against the visible surface state only.
- [OPEN] No prompts were submitted, no tabs were reloaded, and no credit-spending or state-mutating actions were taken during this pass.
- [OPEN] Where a surface exposed hidden routes, result cards, or premium controls that were visible only by label, this note treats them as surface evidence, not end-to-end workflow verification.

## Method

- [SYNTH] Treat signed-in tabs as read-only research surfaces unless the user explicitly asks for destructive or credit-spending exploration.
- [SYNTH] For each page, derive exactly three prompt investigations from the visible placeholder text, example chips, template labels, route structure, mode toggles, and cost or failure messaging.
- [SYNTH] For each investigation, record a concrete example prompt, the likely intuitive path, what the page teaches about the product mental model, and what ImageEZGen3D should borrow or avoid.
- [SYNTH] Separate workspace-shell observations from one-shot composer observations because they teach different product lessons.

## Cross-Surface Stable Conclusions

- [SYNTH] The best current creator tools do not treat the prompt box as the whole product. They surround it with starter flows, history, templates, example chips, and artifact-local next actions.
- [SYNTH] `Auto`, `Fast`, starter chips, template cards, and preselected default models all serve the same UX purpose: reduce first-run decision load without hiding that more control exists.
- [SYNTH] History, projects, recents, spaces, boards, and asset drawers are now central trust features, not secondary productivity extras.
- [SYNTH] Branching from an existing artifact is often more important than blank-state generation. Image-to-image, image-to-video, and card-local follow-up chips make iteration feel safer and more obvious.
- [SYNTH] When expensive generation is involved, the better products surface the transaction model directly with cost, failure, and refund language rather than hiding it.
- [SYNTH] Authentication is most defensible when the product is truly a persistent workspace shell. Even then, the best surfaces still teach the user the next action immediately after login.

## Page Investigations

### ChatGPT Images

- [UI]{auth} Surface classification: authenticated workspace shell inside the broader ChatGPT product.
- [UI]{auth} Visible evidence: sidebar with recents, projects, and chat history; `Describe a new image`; upload affordance; recipe examples such as `Improve Your Desk Setup`, `Wanderlust`, `Scribble`, `Chibi stickers`, `App design`, `Blueprint poster`, `Cross-section`, and `Studio headshot`.
- [SYNTH] Mental model: image generation is one persistent multimodal lane inside a broader assistant workspace rather than a detached image app.

#### Investigation 1: Real-Photo Transformation

- [UI]{auth} Example prompt: `Improve this desk setup into a cleaner walnut-and-black workspace with hidden cables, softer lamp light, and a minimal pegboard wall.`
- [SYNTH] Likely intuitive path: drop a reference photo into the upload area, use `Improve Your Desk Setup` as the cognitive scaffold, refine in `Describe a new image`, and compare against prior results through recents or personal image history.
- [SYNTH] Product lesson: transformation is first-class without forcing the user into a separate edit mode.
- [SYNTH] ImageEZGen3D implication: keep upload, preprocessing visibility, run history, and rerun actions on one surface for the single-image draft path.

#### Investigation 2: Identity-Preserving Stylization

- [UI]{auth} Example prompt: `Turn this selfie into a chibi sticker pack with 6 expressions, white die-cut borders, and bright pastel accents.`
- [SYNTH] Likely intuitive path: upload an identity reference, start from `Chibi stickers` or `Mini me`, then iterate within the same workspace instead of restarting the prompt.
- [SYNTH] Product lesson: recipe chips act as understandable deliverable types, not just inspiration.
- [SYNTH] ImageEZGen3D implication: offer starter chips like `Toy figurine draft`, `Avatar bust`, and `Stylized collectible` rather than only abstract mode names.

#### Investigation 3: Structured Explanatory Graphic

- [UI]{auth} Example prompt: `Create a blueprint poster of a retro instant camera with labeled exploded parts, white annotation lines, and navy technical-paper styling.`
- [SYNTH] Likely intuitive path: start from `Blueprint poster` or `Cross-section`, then remain in the same workspace shell so the output can live beside adjacent text or design work.
- [SYNTH] Product lesson: ChatGPT Images is positioned for diagrams, guides, and UI concepts as much as art or photography.
- [SYNTH] ImageEZGen3D implication: the app should support technical or explanatory outputs near generation, such as normalized-input previews, turntable sheets, and mesh-quality explainer cards.

- [UI]{auth} Key intuitive components: persistent sidebar history, upload plus prompt in one lane, recipe chips, and recoverable continuity through recents and projects.
- [OPEN] Generation states, moderation behavior, and exact result review flows were not exercised in this pass.

### Google Gemini Image Surface

- [UI]{auth} Surface classification: authenticated conversational workspace with the image tool active.
- [UI]{auth} Visible evidence: `Enter a prompt for Gemini`, `Create image`, upload/file entry, `Fast` mode, and style chips such as `Monochrome`, `Color block`, `Runway`, `Risograph`, `Technicolor`, `Steampunk`, and `Oil painting`.
- [SYNTH] Mental model: stay in chat, flip into image mode, and use styles or uploads to reduce prompting complexity.

#### Investigation 1: Style-Led Blank-Canvas Ideation

- [UI]{auth} Example prompt: `A city marathon at sunrise, limited ink palette, layered paper texture, bold geometric shadows.`
- [SYNTH] Likely intuitive path: tap a style such as `Risograph`, keep `Create image` active, leave `Fast` on, and send a short prompt.
- [SYNTH] Product lesson: the style strip lets users begin from recognition rather than recall.
- [SYNTH] ImageEZGen3D implication: surface 3D-oriented starter styles or intent chips before exposing advanced settings.

#### Investigation 2: Reference-Guided Transformation

- [UI]{auth} Example prompt: `Turn this uploaded dog photo into an enamel pin badge with thick metal edging and flat bold colors.`
- [SYNTH] Likely intuitive path: upload a source, keep the same composer, choose an accessible style handle such as `Enamel pin`, and send without switching products.
- [SYNTH] Product lesson: evidence input and generation share one visible lane.
- [SYNTH] ImageEZGen3D implication: upload, evidence-role labeling, and generation intent should stay in one block rather than split across distant panels.

#### Investigation 3: Fast Conversational Concept Iteration

- [UI]{auth} Example prompt: `Front three-quarter view of a steampunk owl courier with brass lenses, folded leather satchel, and workshop lighting.`
- [SYNTH] Likely intuitive path: choose `Steampunk`, trust the visible `Fast` default, and expect to refine in chat if the first image is close but not final.
- [SYNTH] Product lesson: visible speed modes turn generation into a lightweight turn instead of a high-stakes submission.
- [SYNTH] ImageEZGen3D implication: expose `Draft` versus `Quality` explicitly and tie those labels to runtime and evidence expectations.

- [UI]{auth} Key intuitive components: style chips, upload access, explicit `Create image` mode state, visible speed mode, disabled send until prompt entry.
- [OPEN] Post-generation comparison, failure, and quota behavior were not verified.

### Grok Imagine

- [UI]{auth} Surface classification: authenticated workspace shell with prompting, templates, projects, and history in one place.
- [UI]{auth} Visible evidence: Search, New Chat, Imagine, Projects, History, and template buttons such as `Professional Headshot`, `Background Generator`, `Virtual Try-On`, `Object Remover`, `Style Transfer`, `3D Animation`, `Product Showcase`, and `Glossy Product Shot`.
- [SYNTH] Mental model: image creation is a creator mode inside a broader AI workspace, with templates doing much of the onboarding work.

#### Investigation 1: Portrait Or Identity Styling

- [UI]{auth} Example prompt: `Professional headshot of me with soft studio lighting, clean gray background, subtle skin retouching, image mode, 4:5.`
- [SYNTH] Likely intuitive path: start from `Professional Headshot`, optionally upload a source image, then refine rather than author the entire visual recipe from scratch.
- [SYNTH] Product lesson: plain-language templates lower the barrier to advanced outcomes.
- [SYNTH] ImageEZGen3D implication: use named starter lanes such as `Clean Product Turntable`, `Single Photo Draft Mesh`, and `Stylized Figurine` instead of technical jargon alone.

#### Investigation 2: Product Or Commercial Cleanup

- [UI]{auth} Example prompt: `Glossy product shot of this sneaker on a reflective white pedestal, remove background clutter, premium studio lighting, square image.`
- [SYNTH] Likely intuitive path: begin from `Glossy Product Shot`, `Product Photography`, or `Object Remover`, then branch from uploaded evidence toward a cleaned commercial output.
- [SYNTH] Product lesson: practical commerce tasks sit alongside expressive art tasks in the same template system.
- [SYNTH] ImageEZGen3D implication: include capture-improvement and object-centering helpers adjacent to core reconstruction.

#### Investigation 3: Narrative Or Genre Remix

- [UI]{auth} Example prompt: `Pulp cover poster of a spaghetti-western hero in Roman Empire armor during a laser fight, dramatic dust and sunset, wide image.`
- [SYNTH] Likely intuitive path: combine recognizable genre templates rather than learn technical camera or style syntax.
- [SYNTH] Product lesson: memorable template nouns encourage playful recombination.
- [SYNTH] ImageEZGen3D implication: semantic starter flows can guide non-experts into meaningful output categories such as `Game prop`, `Museum bust`, or `Hero object render`.

- [UI]{auth} Key intuitive components: projects and history beside the composer, template-first starts, and a single workspace shell for diverse creative tasks.
- [OPEN] The exact behavior of upload, aspect-ratio, and speed/quality controls on this specific state remains partially inferred from prior visible snapshots.

### Midjourney Explore

- [UI]{public} Surface classification: public browse plus gated creation.
- [UI]{public} Visible evidence: routes for `explore`, `imagine`, `editor`, `organize`, `personalize`, `moodboards`, and `tasks`; disabled prompt input with `Log in to start creating...`; visible controls such as `Stylization`, `Weirdness`, `Variety`, `Version`, `Raw`, `Speed`, `Video Resolution`, and `Video Batch Size`.
- [SYNTH] Mental model: learn the product through public exploration and parameter vocabulary before crossing the auth gate into creation.

#### Investigation 1: Cinematic Character Portrait

- [UI]{public} Example prompt: `Cinematic editorial portrait of a futuristic violinist in silver silk, moody rim lighting, dramatic fog, highly detailed face, elegant color grading.`
- [SYNTH] Likely intuitive path after login: browse Explore first, then use Imagine plus portrait framing, stylization, weirdness, variety, rawness, and speed controls.
- [SYNTH] Product lesson: Midjourney teaches users a compact control vocabulary before they create.
- [SYNTH] ImageEZGen3D implication: make a small set of high-leverage user-facing controls legible instead of burying all differences inside undocumented backend choices.

#### Investigation 2: Product Object Or Concept Render

- [UI]{public} Example prompt: `Minimal studio render of a compact field camera made of brushed aluminum and smoked glass, soft shadow, centered composition, premium product photography look.`
- [SYNTH] Likely intuitive path after login: inspect examples, use square or landscape framing, lower weirdness, and bias toward raw adherence when the object itself matters.
- [SYNTH] Product lesson: art direction plus production settings are visible as separate dimensions.
- [SYNTH] ImageEZGen3D implication: offer output-shaping choices such as `shape-faithful` versus `stylized draft` without forcing users into low-level parameters immediately.

#### Investigation 3: Motion-Ready Scene Or Video Batch

- [UI]{public} Example prompt: `Sweeping aerial view of a neon-lit desert festival at dusk, flowing dust trails, kinetic crowd motion, cinematic scale, vivid atmosphere.`
- [SYNTH] Likely intuitive path after login: use landscape, stylization, speed, and video settings, then rely on `tasks` and `editor` as follow-up workflow stages.
- [SYNTH] Product lesson: queue and task management are visible parts of the creative workflow.
- [SYNTH] ImageEZGen3D implication: long-running work should expose queue state, compare paths, and follow-up actions rather than disappear into a spinner.

- [UI]{public} Key intuitive components: public explore feed, explicit route segmentation, disabled prompt that still teaches the entry point, and visible parameter vocabulary before auth.
- [OPEN] Authenticated post-login layout, defaults, and result workflows were not exercised.

### Adobe Firefly

- [UI]{auth} Surface classification: account-linked creative workspace shell with a live generation cockpit and adjacent suite routes.
- [UI]{auth} Visible evidence: `Describe what you want to generate`; `Image`; account menu; routes for `Create`, `Generate`, `Boards`, `AI Assistant Beta`, `Production`, `Quick actions`, `Your stuff`, `Custom models`, and `Gallery`; model selector currently showing `Gemini 3.1 (w/ Nano Banana 2)` with alternatives from Firefly, GPT Image, Gemini, FLUX, Imagen, Ideogram, and Runway.
- [SYNTH] Mental model: generation happens inside a broader suite shell where organization, comparison, and downstream editing are always nearby.

#### Investigation 1: Fast Blank-Canvas Ideation

- [UI]{auth} Example prompt: `Generate a premium studio image of a translucent portable speaker floating above brushed aluminum, soft sunset rim light, clean hero composition.`
- [SYNTH] Likely intuitive path: start from the main prompt box, keep `Image` selected, trust the preselected model, and move quickly from idea to result.
- [SYNTH] Product lesson: first action friction is minimized by preselected defaults.
- [SYNTH] ImageEZGen3D implication: one obvious first-run lane should be instantly usable before the user touches advanced runtime or export settings.

#### Investigation 2: Polished Asset With Downstream Production Intent

- [UI]{auth} Example prompt: `Using Firefly Image 4, create a high-end ecommerce hero image of a matte black running shoe suspended above cobalt paper, sharp shadow, premium studio lighting, copy space on the left.`
- [SYNTH] Likely intuitive path: switch models only if needed, generate in place, then think in terms of downstream `Production`, `Photoshop`, or `Adobe Express` steps.
- [SYNTH] Product lesson: generation is presented as the start of an asset pipeline, not the end.
- [SYNTH] ImageEZGen3D implication: preview, inspect, export, and next-stage actions should stay visible as a connected asset workflow.

#### Investigation 3: Cross-Model Comparative Testing

- [UI]{auth} Example prompt: `Using Ideogram 3.0, make a black-background festival poster for "SOLAR NOISE" with large chrome lettering, neon orange accents, editorial layout, dramatic contrast.`
- [SYNTH] Likely intuitive path: reuse the same workspace and prompt box while changing models inside the selector, then rely on boards or personal history for comparison.
- [SYNTH] Product lesson: model choice is a mode switch inside one shell rather than a separate product boundary.
- [SYNTH] ImageEZGen3D implication: draft, quality, CPU fallback, and heavier adapters should feel like modes inside one workspace with recorded provenance.

- [UI]{auth} Key intuitive components: central prompt cockpit, preselected media type and model, boards/history-like routes, and suite continuity with Photoshop and Adobe Express.
- [OPEN] Result review, export, credits, and save semantics were not exercised during this pass.

### Pippit

- [UI]{public} Surface classification: prompt-first creative agent home with commerce-creative framing.
- [UI]{public} Visible evidence: `Hi, what will we create today?`; `Video` and `Image`; `Tell me what you want. Add media or docs to generate more precise results.`; `Pippit Standard`; `9:16`; `Home`, `Space`, and `Assets`.
- [UI]{public} Reliability evidence: visible console/runtime issues, including CORS failures and page errors, while the main composer still rendered.
- [SYNTH] Mental model: one multimodal command center for short-form commerce creative, where text, media, and documents all serve as grounding evidence.

#### Investigation 1: Single-Asset Social Ad Video

- [UI]{public} Example prompt: `Create a 9:16 product ad video from this skincare bottle photo with clean studio lighting, ingredient callouts, soft motion, and a final shop-now end card.`
- [SYNTH] Likely intuitive path: choose `Video`, keep the visible aspect ratio, attach a source image, and use the prompt box as the central control surface.
- [SYNTH] Product lesson: the first-run lane is reduced to a few high-signal choices.
- [SYNTH] ImageEZGen3D implication: one source artifact plus one clear intent should be enough to begin a draft run.

#### Investigation 2: Image-Based Commerce Variant

- [UI]{public} Example prompt: `Turn this coffee bag packshot into a premium 9:16 launch visual with warm morning light, floating beans, clean headline space, and ecommerce-ready composition.`
- [SYNTH] Likely intuitive path: switch to `Image` while staying inside the same composer and workspace shell.
- [SYNTH] Product lesson: modality switching is handled inside one stable entry surface.
- [SYNTH] ImageEZGen3D implication: draft versus quality, or image input versus multi-view input, should not feel like changing products.

#### Investigation 3: Brief-Guided Creative Generation

- [UI]{public} Example prompt: `Using the attached product brief and bottle photo, generate a 9:16 launch video for a vitamin C serum focused on brightening, dermatologist-tested trust cues, and a clean premium aesthetic.`
- [SYNTH] Likely intuitive path: attach a document plus media, then rely on the same composer to blend intent and evidence.
- [SYNTH] Product lesson: the prompt box is framed as a multimodal evidence hub rather than pure text entry.
- [SYNTH] ImageEZGen3D implication: capture notes, reference boards, and labeled extra views should feel like precision add-ons next to the main create action.

- [UI]{public} Key intuitive components: mode chips, central prompt area, model and aspect defaults, and clear mention of media/doc grounding.
- [OPEN] Access state was not independently verified, and the visible runtime issues limit confidence in deeper workflow claims.

### CapCut Home Workspace

- [UI]{auth} Surface classification: authenticated creator-suite home shell.
- [UI]{auth} Visible evidence: spaces and invitation controls, templates/projects/inspiration grouping, visible credits, and a partially loaded surface that included `Couldn't load` text.
- [SYNTH] Mental model: not one generator page, but a creative operating system where templates, projects, inspiration, and collaboration surround prompting.

#### Investigation 1: Template-Led Social Output

- [UI]{auth} Example prompt: `Turn these three skincare clips into a 12-second promo reel with clean captions, punchy cuts, and a final shop-now card.`
- [SYNTH] Likely intuitive path: start from a template or inspiration lane, then land inside a project workflow where AI prompting accelerates a scaffold rather than replacing it.
- [SYNTH] Product lesson: prompts are accelerants inside structured workflows, not the whole workflow.
- [SYNTH] ImageEZGen3D implication: expose starter lanes such as `Single Image Draft`, `Multi-View Quality`, and `Cleanup / Export` rather than leading with one blank form.

#### Investigation 2: Continue Or Repair An Existing Draft

- [UI]{auth} Example prompt: `Tighten pacing, add bold subtitles, and make this travel montage feel more cinematic without changing the ending.`
- [SYNTH] Likely intuitive path: open a recent project or space and use an inline assist inside the existing draft context.
- [SYNTH] Product lesson: persistence and revision history are treated as first-class.
- [SYNTH] ImageEZGen3D implication: every run should behave like a revisitable project with rerun-from-settings and comparison built in.

#### Investigation 3: Inspiration-To-Create Jump

- [UI]{auth} Example prompt: `Use this trending neon-glitch intro style for my gaming clip, but keep the text readable and the pacing under 8 seconds.`
- [SYNTH] Likely intuitive path: browse inspiration, then jump directly into a prefilled prompt or template workflow.
- [SYNTH] Product lesson: discovery and execution are intentionally adjacent.
- [SYNTH] ImageEZGen3D implication: example capture sets, retake hints, and successful run presets should be executable launch points, not static documentation only.

- [UI]{auth} Key intuitive components: clear entry modes through templates, projects, and inspiration; visible credits; and collaboration-aware spaces.
- [OPEN] The exact scope of the visible load failure was not confirmed.

### CapCut Agent Draft Thread

- [UI]{auth} Surface classification: authenticated draft-thread workspace with existing conversation and artifact history.
- [UI]{auth} Visible evidence: prior Mario-pet prompt context, generated image cards, follow-up suggestion chips, `Generating 1 item will consume 1 credit`, `Credits returned`, and adjacent `Image to video` / `Image to image` branching controls.
- [SYNTH] Mental model: start from an existing artifact, then branch, refine, or transform it inside the same thread.

#### Investigation 1: In-Thread Refinement

- [UI]{auth} Example prompt: `Keep the current Mario-pet draft, clean up the face, make the colors richer, and place it in a polished toy-poster scene.`
- [SYNTH] Likely intuitive path: choose a visible result card, use a suggestion chip or follow-up prompt, notice credit cost before acting, and compare new results against prior cards.
- [SYNTH] Product lesson: the product teaches refinement from success states instead of prompt reset.
- [SYNTH] ImageEZGen3D implication: each generated artifact should expose actionable next steps such as `improve silhouette`, `retry with stronger structure`, or `keep current shape and refine texture`.

#### Investigation 2: Image-To-Image Variation

- [UI]{auth} Example prompt: `Use the current Mario-pet result as the input and make an image-to-image version in a rainy neon street while keeping the same character identity.`
- [SYNTH] Likely intuitive path: branch from a result card into `Image to image`, preserving context and history.
- [SYNTH] Product lesson: transformation is adjacent to generation rather than isolated in another tool.
- [SYNTH] ImageEZGen3D implication: place follow-up branches such as `image to draft mesh`, `draft mesh to refined texture`, and `mesh to turntable preview` directly on artifact cards.

#### Investigation 3: Image-To-Video Motion Extension

- [UI]{auth} Example prompt: `Use this Mario-pet image as the source and make a short video where it waves, blinks, and does a small hop toward the camera.`
- [SYNTH] Likely intuitive path: pick the best card, switch to `Image to video`, add a light motion directive, and keep the result in the same project thread.
- [SYNTH] Product lesson: successful artifacts become launchpads into neighboring media modes.
- [SYNTH] ImageEZGen3D implication: successful draft meshes should branch cleanly into refinement, inspection, and export subflows without losing provenance.

- [UI]{auth} Key intuitive components: explicit credit preflight, explicit refund feedback on failure, card-local history, suggestion chips, and transformation branches.
- [OPEN] Credit timing, hidden settings, and export behavior were not verified through interaction.

### CapCut Agent Fresh Entry Surface

- [UI]{auth} Surface classification: authenticated prompt-first creator surface with both fresh-start and resume-state cues.
- [UI]{auth} Visible evidence: `Hi, what will we create today?`, `Try Dreamina Seedance 2.0`, example chip `a stunning 80s Japanese anime-style MV`, a textbox already containing a previous prompt, and an `Auto` combobox.
- [SYNTH] Mental model: a single-entry-lane assistant surface where users can either start from inspiration or continue unfinished work.

#### Investigation 1: First-Pass Anime MV Ideation

- [UI]{auth} Example prompt: `Auto: create a stunning 80s Japanese anime-style MV intro with neon Tokyo streets, windblown hair, film-grain glow, and dramatic camera movement.`
- [SYNTH] Likely intuitive path: use the anime-style example chip, leave `Auto` selected, and trust the system to pick an appropriate route.
- [SYNTH] Product lesson: example chips plus a recommended mode absorb early complexity.
- [SYNTH] ImageEZGen3D implication: provide high-signal starter chips and a clearly recommended default path for first-run 3D generation.

#### Investigation 2: Resume And Refine Previous Intent

- [UI]{auth} Example prompt: `Auto: refine my anime-style MV concept into a cleaner 12-second opening with one heroine silhouette, rain-soaked alley lighting, and stronger scene continuity.`
- [SYNTH] Likely intuitive path: edit the preloaded textbox rather than rebuilding from zero.
- [SYNTH] Product lesson: preserved in-progress intent is a continuity feature, not accidental state.
- [SYNTH] ImageEZGen3D implication: preserve unsent instructions, recent settings, and recoverable prior evidence on the main page.

#### Investigation 3: Delegate Mode Choice To The System

- [UI]{auth} Example prompt: `Auto: turn this 80s Japanese anime-style MV idea into a social-ready visual concept with cinematic keyframe energy and a polished cover frame.`
- [SYNTH] Likely intuitive path: trust `Auto` together with the nearby `Seedance 2.0` promo to route the user toward a capable flow without exposing every model or media distinction first.
- [SYNTH] Product lesson: possibility is often taught before manual control.
- [SYNTH] ImageEZGen3D implication: an `Auto` or `Recommended` path should explain what it chose and why after the run finishes, so convenience does not become hidden magic.

- [UI]{auth} Key intuitive components: greeting plus remembered state, high-signal example chip, and a visible `Auto` default that lowers decision load.
- [OPEN] Actual `Auto` choices, create-action behavior, and cost semantics were not exercised.

## What ImageEZGen3D Should Prefer

- [SYNTH] One stable workspace surface that keeps upload, validation, runtime status, preview, history, and export visibly connected.
- [SYNTH] Starter flows and prompt or intent chips that name deliverable types instead of forcing users to learn internal pipeline terminology.
- [SYNTH] Artifact-local next actions so users branch from a result instead of starting over.
- [SYNTH] A visible `Draft`, `Quality`, or `Recommended` mode choice with runtime implications explained in plain language.
- [SYNTH] Cost or runtime preflight messaging when heavier hosted or ZeroGPU paths are in play.
- [SYNTH] Failure and refund semantics that are explicit if future remote generation introduces scarce runtime or billing.

## What ImageEZGen3D Should Avoid

- [SYNTH] A bare upload form that leaves the user guessing what to do next.
- [SYNTH] Hidden mode or runtime routing that changes outcomes without explanation.
- [SYNTH] Forcing the user onto a new page just to see the main preview, history, or comparison state.
- [SYNTH] Treating generation as a one-shot event instead of a revisable asset lifecycle.
- [SYNTH] Mixing inspiration, history, and follow-up actions so loosely that the first-run path disappears.
