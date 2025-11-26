import os
import json
import argparse

def create_data_files(data_json: dict = None, data_json_path=None, use_relative_paths=False, server_root=None, num_samples=None):
    """
    Generate data_files.json containing OBJ file paths.
    
    Args:
        use_relative_paths: If True, converts absolute paths to relative paths for browser use
        server_root: Base directory to make paths relative to (if use_relative_paths=True)
    """

    if data_json is not None:
        if data_json_path is not None:
            raise ValueError("Cannot provide both data_json and data_json_path")

    if not data_json:
        data_json = data_json_path if data_json_path else "data.json"
        assert os.path.exists(data_json), f"{data_json} does not exist"
        
        with open(data_json, "r") as f:
            data = json.load(f)
    else:
        data = data_json

    data_files = {}
    
    for dataset_name in data:
        dataset_path = data[dataset_name]
        if not os.path.exists(dataset_path):
            continue
        all_files = []
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith('.obj'):
                    file_path = os.path.join(root, file)
                    
                    # Convert to relative path if requested
                    if use_relative_paths and server_root:
                        try:
                            # Make path relative to the server root
                            rel_path = os.path.relpath(file_path, server_root)
                            file_path = rel_path
                        except ValueError:
                            print(f"Warning: Could not make path relative: {file_path}")
                    
                    all_files.append(file_path)
        
        num_samples = num_samples if num_samples is not None else len(all_files)
        all_files = all_files[:num_samples]
        data_files[dataset_name] = all_files
    
    # Save the data_files.json
    with open("data_files.json", "w") as f:
        json.dump(data_files, f, indent=4)
    
    print(f"Created data_files.json with {sum(len(files) for files in data_files.values())} total OBJ files")
    
    # Output info about datasets
    for dataset_name, files in data_files.items():
        print(f"  - {dataset_name}: {len(files)} OBJ files")
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate data_files.json containing paths to OBJ files")
    parser.add_argument("--data_path", default=None, help="Data Json path")
    parser.add_argument("--relative", action="store_true", help="Generate relative paths instead of absolute paths")
    parser.add_argument("--server-root", type=str, default=os.getcwd(),
                        help="Server root directory to use for relative path calculation (default: current dir)")
    parser.add_argument("--num_samples", type=int, default=None, help="Number of samples to generate (default: 100)")
    
    args = parser.parse_args()
    
    print(f"Generating data_files.json...")
    if args.relative:
        print(f"Using relative paths relative to: {args.server_root}")
    else:
        print("Using absolute paths (may not work in browser)")
    
    create_data_files(
        data_json_path=args.data_path, 
        use_relative_paths=args.relative, 
        server_root=args.server_root, 
        num_samples=args.num_samples
    )