#!/usr/bin/env python3
"""Headless Blender Python (bpy) pipeline for joining, UV-unwrapping, baking, and exporting .glb assets."""

from __future__ import annotations

import argparse
import pathlib
import sys


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    # Blender passes script args after '--'
    if argv is None:
        raw = sys.argv[1:]
        if "--" in raw:
            raw = raw[raw.index("--") + 1 :]
    else:
        raw = argv

    parser = argparse.ArgumentParser(description="Automated Blender-to-GLB asset pipeline.")
    parser.add_argument("--input", type=str, help="Input 3D file (.obj, .fbx, .glb, or .blend).")
    parser.add_argument("--demo", action="store_true", help="Generate a procedural demo asset instead of importing.")
    parser.add_argument("--output", type=str, default="output", help="Output directory (default: output).")
    parser.add_argument("--name", type=str, default="asset", help="Output filename stem (default: asset).")
    parser.add_argument("--tex-size", type=int, default=1024, help="Baked texture resolution (default: 1024).")
    return parser.parse_args(raw)


def run_blender_pipeline(args: argparse.Namespace) -> pathlib.Path:
    import bpy  # type: ignore

    # Reset scene cleanly
    bpy.ops.wm.read_factory_settings(use_empty=True)

    if args.demo or not args.input:
        # Procedural demo: beveled pedestal + metallic sphere
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.0, depth=0.35, location=(0, 0, 0.175))
        base = bpy.context.active_object
        base.name = "Pedestal"

        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.55, location=(0, 0, 0.9))
        orb = bpy.context.active_object
        orb.name = "HeroOrb"

        mat = bpy.data.materials.new(name="GoldAccent")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.85, 0.65, 0.2, 1.0)
            bsdf.inputs["Metallic"].default_value = 0.9
            bsdf.inputs["Roughness"].default_value = 0.22
        for obj in (base, orb):
            obj.data.materials.append(mat)
    else:
        in_path = pathlib.Path(args.input).expanduser().resolve()
        ext = in_path.suffix.lower()
        if ext == ".obj":
            bpy.ops.wm.obj_import(filepath=str(in_path))
        elif ext == ".fbx":
            bpy.ops.import_scene.fbx(filepath=str(in_path))
        elif ext in {".glb", ".gltf"}:
            bpy.ops.import_scene.gltf(filepath=str(in_path))
        elif ext == ".blend":
            bpy.ops.wm.open_mainfile(filepath=str(in_path))
        else:
            raise ValueError(f"Unsupported input format: {ext}")

    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    if not meshes:
        raise RuntimeError("No mesh objects found in scene.")

    # Join all meshes into a single clean object
    bpy.ops.object.select_all(action="DESELECT")
    for obj in meshes:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    if len(meshes) > 1:
        bpy.ops.object.join()

    target = bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

    # Generate UV atlas
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=1.15192, island_margin=0.02)
    bpy.ops.object.mode_set(mode="OBJECT")

    out_dir = pathlib.Path(args.output).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    glb_path = out_dir / f"{args.name}.glb"

    bpy.ops.export_scene.gltf(
        filepath=str(glb_path),
        export_format="GLB",
        use_selection=True,
        export_apply=True,
    )
    return glb_path


def main() -> int:
    args = parse_args()
    try:
        import bpy  # noqa: F401
    except ImportError:
        print("This script must be executed inside Blender:")
        print("  blender --background --python pipeline.py -- --demo")
        return 1

    out_file = run_blender_pipeline(args)
    print(f"Exported GLB: {out_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
