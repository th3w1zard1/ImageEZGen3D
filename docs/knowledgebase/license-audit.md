# License Audit

No third-party source code, model weights, sample assets, or generated outputs from Hunyuan3D, TRELLIS, or Pixal3D are vendored in this scaffold.

Before enabling a heavy adapter, record:

- Source repository and exact revision.
- Model repository and revision.
- License text and usage restrictions.
- Commercial, region, attribution, and redistribution limits.
- Whether weights are gated or require an access token.
- Whether dependency wheels can be redistributed.
- Whether generated outputs have any special terms.

## Known Initial Concerns

- Hunyuan3D-2.1 uses a community license with commercial and regional constraints.
- TRELLIS/Pixal dependencies include CUDA-only wheels and third-party model licenses that must be checked independently.
- Hugging Face tokens must never be stored in source.
