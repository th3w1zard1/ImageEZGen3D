# Failure-Mode Playbook

| Symptom | Likely Cause | Suggested Recovery |
| --- | --- | --- |
| Missing or wrong back side | Single image has no rear evidence | Add labeled back/side views or accept draft geometry |
| Blobby silhouette | Low resolution, crop, motion blur | Retake sharper image with full object visible |
| Holes or loose parts | Thin structures or segmentation errors | Use mesh repair and simplify settings; retake on clean background |
| Stretched texture | UV/bake limitations or occluded surfaces | Lower texture expectation; add more coherent views |
| Reflective/transparent failure | Material violates common model assumptions | Use matte proxy, diffuse lighting, or manual cleanup |
| Bad topology | Generative mesh is not retopologized | Retopologize in DCC tools for production/game assets |

Community notes from Reddit-like sources are treated as anecdotal signals. They are useful for finding failure classes, not for benchmark claims.
