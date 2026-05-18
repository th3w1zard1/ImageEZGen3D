def patch_exporters_uvs():
    with open('src/imageezgen3d/exporters.py', 'r') as f:
        src = f.read()

    # Modify gltf payload to include TEXCOORD_0
    texcoord_code = '''        "meshes": [{"primitives": [{"attributes": {"POSITION": 0, "TEXCOORD_0": 2}, "indices": 1, "material": 0}]}],'''
    
    src = src.replace('        "meshes": [{"primitives": [{"attributes": {"POSITION": 0}, "indices": 1, "material": 0}]}],', texcoord_code)

    # Now add the uv buffer logic.
    uv_logic = '''
    if mesh.b64_image:
        gltf["images"] = [{"uri": "data:image/jpeg;base64," + mesh.b64_image}]
        gltf["samplers"] = [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}]
        gltf["textures"] = [{"sampler": 0, "source": 0}]
        mat["pbrMetallicRoughness"]["baseColorTexture"] = {"index": 0}
        mat["pbrMetallicRoughness"]["baseColorFactor"] = [1.0, 1.0, 1.0, 1.0]

    # Generate UVs (simple box mapping)
    # The box has 8 vertices. Left: x=-w, Right: x=w. Bottom: z=-h, Top: z=h
    uvs = []
    for x, y, z in mesh.vertices:
        u = (x - mins[0]) / (maxs[0] - mins[0] + 1e-9)
        v = (z - mins[2]) / (maxs[2] - mins[2] + 1e-9)
        uvs.append((u, 1.0 - v))
    
    uv_bytes = b"".join(struct.pack("<2f", *uv) for uv in uvs)
    uv_padded = _pad4(uv_bytes, b"\\x00")
    uv_offset = len(positions_padded) + len(indices)
    uv_offset = uv_offset + ((4 - (uv_offset % 4)) % 4) # manually pad
    
    bin_blob = _pad4(positions_padded + _pad4(indices, b"\\x00") + uv_padded, b"\\x00")
    
    gltf["bufferViews"].append({
        "buffer": 0, "byteOffset": uv_offset, "byteLength": len(uv_bytes), "target": 34962
    })
    gltf["accessors"].append({
        "bufferView": 2, "componentType": 5126, "count": len(mesh.vertices), "type": "VEC2"
    })
    
    json_blob = _pad4(json.dumps(gltf, separators=(",", ":")).encode("utf-8"), b'''
    
    import re
    # We replace from "if mesh.b64_image:" down to "json_blob ="
    src = re.sub(r'    if mesh\.b64_image:.*?    json_blob = _pad4\(json\.dumps\(gltf, separators=\(",", ":"\)\)\.encode\("utf-8"\), b', uv_logic, src, flags=re.DOTALL)
    
    with open('src/imageezgen3d/exporters.py', 'w') as f:
        f.write(src)
    print("Updated UVs")

patch_exporters_uvs()
