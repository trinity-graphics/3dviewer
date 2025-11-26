import os
import argparse
import json

from construct import create_data_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create data_files.json from datasets")
    parser.add_argument('--ori_dir', type=str, default=None, help='Path to origin *obj file')
    parser.add_argument('--pred_dir', type=str, default=None, help='Path to prediction *obj file')
    parser.add_argument('--ori_key', type=str, required=True, help='Key name for origin dataset in data_files.json')
    parser.add_argument('--pred_key', type=str, required=True, help='Key name for prediction dataset in data_files.json')
    parser.add_argument('--relative', action='store_true', help='Use relative paths in data_files.json')
    parser.add_argument('--server-root', type=str, default=os.getcwd(),
                        help="Server root directory to use for relative path calculation (default: current dir)")
    parser.add_argument('--num_samples', type=int, default=None,
                        help="Number of samples to include from each dataset (default: all)")
    
    args = parser.parse_args()

    print(f"Generating data_files.json...")
    if args.relative:
        print(f"Using relative paths relative to: {args.server_root}")
    else:
        print("Using absolute paths (may not work in browser)")

    data_json = {
        args.ori_key: args.ori_dir,
        args.pred_key: args.pred_dir
    }

    create_data_files(
        data_json=data_json, 
        use_relative_paths=args.relative, 
        server_root=args.server_root, 
        num_samples=args.num_samples
    )

    with open("data_files.json", "r") as f:
        data_files = json.load(f)
    
    # Sorting the files for consistent ordering by filename
    for key in data_files:
        files = data_files[key]
        files = sorted(files, key=lambda x: os.path.basename(x))
        data_files[key] = files
    
    with open("data_files.json", "w") as f:
        json.dump(data_files, f, indent=4)