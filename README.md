# bpy-glb-pipeline

An automated, headless **Blender Python (`bpy`)** CLI pipeline that imports or procedurally generates 3D meshes, joins geometry, applies transforms, creates a UV atlas (`smart_project`), and exports web-ready `.glb` assets.

## Features

- **Headless Execution:** Runs via `blender --background --python pipeline.py` with zero GUI overhead.
- **Multi-Format Input:** Supports `.obj`, `.fbx`, `.glb`/`.gltf`, `.blend`, or `--demo` procedural generation.
- **Clean Mesh Prep:** Joins multi-part meshes, applies rotation/scale transforms, and generates UV islands automatically.
- **Web-Ready Export:** Outputs compressed binary `.glb` files into `output/`.

## Quick Start

```bash
# Run the procedural demo on macOS
chmod +x run_demo.sh
./run_demo.sh

# Or convert an existing 3D model
/Applications/Blender.app/Contents/MacOS/Blender --background --python pipeline.py -- \
  --input model.obj --output output --name product_mesh
```

## Repository Structure

```text
.
├── pipeline.py       # Headless Blender Python automation script
├── run_demo.sh       # macOS/Linux demo runner
├── requirements.txt  # Runtime notes (uses Blender's bundled bpy)
├── README.md         # Documentation and CLI usage
├── CHANGELOG.md      # Release history
├── CONTRIBUTING.md   # Contribution guidelines
├── LICENSE           # MIT License
└── .gitignore        # Python, Blender (.blend1), and output/ ignores
```

## License

MIT License — see [`LICENSE`](LICENSE).
