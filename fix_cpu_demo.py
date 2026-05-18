import base64

def patch_cpu_demo():
    with open('src/imageezgen3d/adapters/cpu_demo.py', 'r') as f:
        src = f.read()

    b64_logic = """        with open(request.processed_image, "rb") as f:
            bimg = base64.b64encode(f.read()).decode("utf-8")
        mesh = make_box_mesh(
            width=aspect,
            depth=0.72 + view_bonus,
            height=quality_height,
            color=(red, green, blue, 1.0),
            b64_image=bimg,
        )"""

    curr_logic = """        mesh = make_box_mesh(
            width=aspect,
            depth=0.72 + view_bonus,
            height=quality_height,
            color=(red, green, blue, 1.0),
        )"""

    if curr_logic in src:
        src = src.replace(curr_logic, b64_logic)
        with open('src/imageezgen3d/adapters/cpu_demo.py', 'w') as f:
            f.write(src)
        print("Updated cpu_demo.py")
    else:
        print("Could not find logic")

patch_cpu_demo()
