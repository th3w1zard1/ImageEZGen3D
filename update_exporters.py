import math, sys
from pathlib import Path
content = Path('src/imageezgen3d/exporters.py').read_text()
# Ensure we don't break existing tests, add image_path to SimpleMesh optionally
if 'image_path: Path | None = None' not in content:
    content = content.replace(
        'color: tuple[float, float, float, float]\n',
        'color: tuple[float, float, float, float]\n    image_path: Path | None = None\n    uvs: tuple[tuple[float, float], ...] | None = None\n'
    )
    # Box UVs roughly wrapping a texture, or just a simple quad. Let's change make_box_mesh to a plane if image_path is there.
Path('src/imageezgen3d/exporters.py').write_text(content)
