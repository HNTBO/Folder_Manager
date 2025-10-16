"""
File Counter Script for Folder Manager
Counts all files in a folder structure, diving deep into every branch.
Folders are not counted as files - only actual files are counted.
"""

import os
from pathlib import Path
import argparse
import time


def count_files_in_folder(root_path: Path) -> tuple[int, list[Path]]:
    """
    Recursively count all files in a folder structure.
    Dives deep into every branch, counting only files (not folders).
    
    Args:
        root_path: Root path to start counting from
        
    Returns:
        Tuple of (total_file_count, list_of_all_files)
    """
    file_count = 0
    all_files = []
    
    if not root_path.exists() or not root_path.is_dir():
        print(f"Error: {root_path} does not exist or is not a directory")
        return file_count, all_files
    
    try:
        # Get all items in the current directory
        items = list(root_path.iterdir())
        
        for item in items:
            if item.is_file():
                # Count actual files
                file_count += 1
                all_files.append(item)
            elif item.is_dir():
                # Recursively count files in subdirectories
                sub_count, sub_files = count_files_in_folder(item)
                file_count += sub_count
                all_files.extend(sub_files)
        
    except (PermissionError, OSError) as e:
        print(f"Permission error accessing {root_path}: {e}")
    
    return file_count, all_files


def count_files_with_details(root_path: Path) -> dict:
    """
    Count files with detailed breakdown by folder structure.
    
    Args:
        root_path: Root path to start counting from
        
    Returns:
        Dictionary with detailed file count information
    """
    details = {
        'total_files': 0,
        'total_folders': 0,
        'files_by_type': {},
        'files_by_folder': {},
        'all_files': [],
        'empty_folders': [],
        'folders_with_files': []
    }
    
    def analyze_folder(folder_path: Path, current_depth: int = 0) -> tuple[int, int]:
        """Analyze a single folder and return (file_count, folder_count)"""
        if not folder_path.exists() or not folder_path.is_dir():
            return 0, 0
        
        try:
            items = list(folder_path.iterdir())
            files = [item for item in items if item.is_file()]
            dirs = [item for item in items if item.is_dir()]
            
            local_file_count = len(files)
            local_folder_count = len(dirs)
            
            # Count files by type
            for file in files:
                extension = file.suffix.lower() or 'no_extension'
                details['files_by_type'][extension] = details['files_by_type'].get(extension, 0) + 1
                details['all_files'].append(file)
            
            # Track folder information
            if local_file_count == 0 and local_folder_count == 0:
                details['empty_folders'].append(folder_path)
            elif local_file_count > 0:
                details['folders_with_files'].append(folder_path)
                details['files_by_folder'][str(folder_path)] = local_file_count
            
            # Recursively analyze subdirectories
            for subdir in dirs:
                sub_files, sub_folders = analyze_folder(subdir, current_depth + 1)
                local_file_count += sub_files
                local_folder_count += sub_folders
            
            details['total_files'] += local_file_count
            details['total_folders'] += local_folder_count
            
            return local_file_count, local_folder_count
            
        except (PermissionError, OSError) as e:
            print(f"Permission error accessing {folder_path}: {e}")
            return 0, 0
    
    # Start analysis
    analyze_folder(root_path)
    return details


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def get_file_size_info(all_files: list[Path]) -> dict:
    """Get file size information for all files."""
    total_size = 0
    size_by_type = {}
    
    for file_path in all_files:
        try:
            size = file_path.stat().st_size
            total_size += size
            
            extension = file_path.suffix.lower() or 'no_extension'
            if extension not in size_by_type:
                size_by_type[extension] = {'count': 0, 'size': 0}
            size_by_type[extension]['count'] += 1
            size_by_type[extension]['size'] += size
            
        except (PermissionError, OSError):
            continue
    
    return {
        'total_size': total_size,
        'size_by_type': size_by_type
    }


def main():
    """Main function to run the file counter."""
    parser = argparse.ArgumentParser(description='Count all files in a folder structure')
    parser.add_argument('folder', nargs='?', default='.', 
                       help='Folder to count files in (default: current directory)')
    parser.add_argument('--detailed', '-d', action='store_true',
                       help='Show detailed breakdown by file type and folder')
    parser.add_argument('--size', '-s', action='store_true',
                       help='Show file size information')
    
    args = parser.parse_args()
    
    folder_path = Path(args.folder).resolve()
    
    print("="*60)
    print("FILE COUNTER - Folder Manager")
    print("="*60)
    print(f"Scanning folder: {folder_path}")
    print()
    
    start_time = time.time()
    file_count = 0
    
    if args.detailed:
        print("Running detailed analysis...")
        details = count_files_with_details(folder_path)
        file_count = details['total_files']
        
        print(f"DETAILED FILE ANALYSIS")
        print("-" * 40)
        print(f"Total files found: {details['total_files']}")
        print(f"Total folders found: {details['total_folders']}")
        print(f"Empty folders: {len(details['empty_folders'])}")
        print(f"Folders with files: {len(details['folders_with_files'])}")
        
        if details['files_by_type']:
            print(f"\nFILES BY TYPE:")
            print("-" * 20)
            sorted_types = sorted(details['files_by_type'].items(), key=lambda x: x[1], reverse=True)
            for ext, count in sorted_types[:10]:  # Show top 10 file types
                ext_display = ext if ext != 'no_extension' else '(no extension)'
                print(f"  {ext_display:<15}: {count:>6} files")
        
        if args.size:
            size_info = get_file_size_info(details['all_files'])
            print(f"\nSIZE INFORMATION:")
            print("-" * 20)
            print(f"Total size: {format_file_size(size_info['total_size'])}")
            
            if size_info['size_by_type']:
                print(f"\nSize by file type (top 10):")
                sorted_sizes = sorted(size_info['size_by_type'].items(), 
                                    key=lambda x: x[1]['size'], reverse=True)
                for ext, info in sorted_sizes[:10]:
                    ext_display = ext if ext != 'no_extension' else '(no extension)'
                    avg_size = info['size'] / info['count'] if info['count'] > 0 else 0
                    print(f"  {ext_display:<15}: {format_file_size(info['size']):>8} "
                          f"({info['count']} files, avg: {format_file_size(avg_size)})")
    
    else:
        # Simple count
        print("Counting files...")
        file_count, all_files = count_files_in_folder(folder_path)
        
        print(f"RESULTS:")
        print("-" * 20)
        print(f"Total files found: {file_count}")
        
        if args.size and all_files:
            size_info = get_file_size_info(all_files)
            print(f"Total size: {format_file_size(size_info['total_size'])}")
    
    end_time = time.time()
    scan_time = end_time - start_time
    
    print(f"\nScan completed in {scan_time:.2f} seconds")
    print("="*60)
    
    if file_count == 0:
        print("No files found in the specified folder.")
    else:
        print(f"Successfully counted {file_count} files!")


if __name__ == "__main__":
    main()
