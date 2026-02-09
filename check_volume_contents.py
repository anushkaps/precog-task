"""
Check what's actually in the Modal volume.
"""
import modal

app = modal.App("check-volume")

volume = modal.Volume.from_name("lazy-artist-outputs", create_if_missing=False)

@app.function(
    volumes={"/check": volume},
    timeout=60,
)
def list_volume_contents():
    """List everything in the volume."""
    import os
    from pathlib import Path
    
    check_dir = Path("/check")
    
    print("="*60)
    print("VOLUME CONTENTS")
    print("="*60)
    
    if not check_dir.exists():
        print("ERROR: /check does not exist")
        return {"error": "check dir not found"}
    
    # List root
    print(f"\nRoot directory (/check):")
    for item in sorted(check_dir.iterdir()):
        if item.is_dir():
            print(f"  DIR:  {item.name}/")
        else:
            size = item.stat().st_size
            print(f"  FILE: {item.name} ({size} bytes)")
    
    # Check for outputs directory
    outputs_path = check_dir / "outputs"
    if outputs_path.exists():
        print(f"\n/outputs directory exists!")
        print(f"Contents of /outputs:")
        for root, dirs, files in os.walk(outputs_path):
            level = root.replace(str(outputs_path), '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in sorted(files)[:10]:  # First 10 files per dir
                filepath = Path(root) / file
                size = filepath.stat().st_size
                print(f"{subindent}{file} ({size} bytes)")
            if len(files) > 10:
                print(f"{subindent}... and {len(files) - 10} more files")
    else:
        print("\n/outputs directory does NOT exist")
    
    # Also check if files are directly in root
    print(f"\n\nAll files in volume root:")
    all_files = []
    for root, dirs, files in os.walk(check_dir):
        for file in files:
            rel_path = Path(root).relative_to(check_dir) / file
            filepath = Path(root) / file
            size = filepath.stat().st_size
            all_files.append((str(rel_path), size))
    
    for path, size in sorted(all_files)[:50]:  # First 50 files
        print(f"  {path} ({size} bytes)")
    
    if len(all_files) > 50:
        print(f"  ... and {len(all_files) - 50} more files")
    
    return {
        "total_files": len(all_files),
        "outputs_exists": outputs_path.exists()
    }

@app.local_entrypoint()
def main():
    result = list_volume_contents.remote()
    print("\n" + "="*60)
    print("Result:")
    print("="*60)
    print(result)

