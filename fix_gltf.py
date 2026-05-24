from __future__ import annotations

import json, base64

def patch_exporters():
    with open('src/imageezgen3d/exporters.py', 'r') as f:
        src = f.read()
    
    if 'b64_image: str | None = None' not in src:
        # Add b64_image to SimpleMesh
        src = src.replace('color: tuple[float, float, float, float]\n', 'color: tuple[float, float, float, float]\n    b64_image: str | None = None\n')
        
        # update make_box_mesh signature
        src = src.replace('color: tuple[float, float, float, float]) -> SimpleMesh:', 'color: tuple[float, float, float, float], b64_image: str | None = None) -> SimpleMesh:')
        src = src.replace('return SimpleMesh(vertices=vertices, faces=faces, color=color)', 'return SimpleMesh(vertices=vertices, faces=faces, color=color, b64_image=b64_image)')
        
        # update write_glb
        # Find where gltf dict is created
        import re
        gltf_code = """    gltf = {
        "asset": {"version": "2.0", "generator": "ImageEZGen3D CPU demo"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": "ImageEZGen3D Draft"}],
        "materials": [{"pbrMetallicRoughness": {"baseColorFactor": list(mesh.color), "metallicFactor": 0.0, "roughnessFactor": 0.72}}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0}, "indices": 1, "material": 0}]}],
"""
        
        new_gltf_code = """
    mat = {"pbrMetallicRoughness": {"baseColorFactor": list(mesh.color), "metallicFactor": 0.0, "roughnessFactor": 0.72}}
    gltf = {
        "asset": {"version": "2.0", "generator": "ImageEZGen3D CPU demo"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": "ImageEZGen3D Draft"}],
        "materials": [mat],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0}, "indices": 1, "material": 0}]}],
"""
        
        src = src.replace(gltf_code, new_gltf_code)
        
        tex_logic = """
    if mesh.b64_image:
        gltf["images"] = [{"uri": "data:image/jpeg;base64," + mesh.b64_image}]
        gltf["samplers"] = [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}]
        gltf["textures"] = [{"sampler": 0, "source": 0}]
        mat["pbrMetallicRoughness"]["baseColorTexture"] = {"index": 0}
        mat["pbrMetallicRoughness"]["baseColorFactor"] = [1.0, 1.0, 1.0, 1.0]

    json_blob = _pad4(json.dumps(gltf, separators=(",", ":")).encode("utf-8"), b"""
        
        src = src.replace('    json_blob = _pad4(json.dumps(gltf, separators=(",", ":")).encode("utf-8"), b', tex_logic)
        
        with open('src/imageezgen3d/exporters.py', 'w') as f:
            f.write(src)
        print("Updated exporters.py")

patch_exporters()
