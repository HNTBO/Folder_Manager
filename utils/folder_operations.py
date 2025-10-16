"""
Folder operations module for the Folder Manager application.
Provides functions for scanning, deleting empty folders, and duplicating folder structures.
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple, Dict
import logging
from datetime import datetime


def setup_logging() -> str:
    """Setup logging and return the log file path."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"folder_manager_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return str(log_file)


def is_folder_empty(folder_path: Path) -> bool:
    """
    Check if a folder is completely empty (no files, no folders).
    
    Args:
        folder_path: Path to the folder to check
        
    Returns:
        True if folder is empty, False otherwise
    """
    try:
        return not any(folder_path.iterdir())
    except (PermissionError, OSError):
        return False


def scan_empty_folder_structure(root_path: Path) -> List[Path]:
    """
    Recursively scan a folder structure and identify folders that contain
    only empty folders or are empty themselves. A folder is considered empty
    if it contains no files (only folders), and all nested folders also contain no files.
    
    This function checks each folder individually, regardless of parent folder contents.
    
    Args:
        root_path: Root path to start scanning from
        
    Returns:
        List of paths that can be safely deleted (empty folder structures)
    """
    empty_folders = []
    
    if not root_path.exists() or not root_path.is_dir():
        return empty_folders
    
    try:
        # Get all items in the current directory
        items = list(root_path.iterdir())
        
        # If folder is completely empty, it's empty
        if not items:
            empty_folders.append(root_path)
            return empty_folders
        
        # Check if this folder contains any files
        has_files = any(item.is_file() for item in items)
        
        # If folder contains files, it's not empty - but still check subdirectories
        if has_files:
            # Even if this folder has files, check if any subdirectories are empty
            subdirectories = [item for item in items if item.is_dir()]
            for subdir in subdirectories:
                empty_folders.extend(scan_empty_folder_structure(subdir))
            return empty_folders
        
        # Folder contains only directories - check if all subdirectories are empty
        subdirectories = [item for item in items if item.is_dir()]
        all_subdirs_empty = True
        
        for subdir in subdirectories:
            subdir_empty_folders = scan_empty_folder_structure(subdir)
            empty_folders.extend(subdir_empty_folders)
            
            # If the subdirectory itself is not in the empty list, it's not empty
            if subdir not in subdir_empty_folders:
                all_subdirs_empty = False
        
        # If all subdirectories are empty, this folder is also empty
        if all_subdirs_empty:
            empty_folders.append(root_path)
        
    except (PermissionError, OSError) as e:
        logging.warning(f"Permission error accessing {root_path}: {e}")
    
    return empty_folders


def delete_empty_folders(folder_paths: List[Path]) -> Tuple[int, List[str]]:
    """
    Delete a list of empty folder paths.
    
    Args:
        folder_paths: List of folder paths to delete
        
    Returns:
        Tuple of (success_count, error_messages)
    """
    success_count = 0
    errors = []
    
    # Sort paths by depth (deepest first) to avoid deleting parent before child
    sorted_paths = sorted(folder_paths, key=lambda p: len(p.parts), reverse=True)
    
    for folder_path in sorted_paths:
        try:
            if folder_path.exists() and folder_path.is_dir():
                # Double-check the folder is still empty before deleting
                if is_folder_empty(folder_path):
                    folder_path.rmdir()
                    success_count += 1
                    logging.info(f"Deleted empty folder: {folder_path}")
                else:
                    error_msg = f"Folder not empty, skipping: {folder_path}"
                    errors.append(error_msg)
                    logging.warning(error_msg)
            else:
                error_msg = f"Path does not exist or is not a directory: {folder_path}"
                errors.append(error_msg)
                logging.warning(error_msg)
                
        except (PermissionError, OSError) as e:
            error_msg = f"Error deleting {folder_path}: {e}"
            errors.append(error_msg)
            logging.error(error_msg)
    
    return success_count, errors


def scan_folder_structure(source_path: Path) -> List[Path]:
    """
    Scan a folder and return all directory paths in the structure.
    
    Args:
        source_path: Root path to scan
        
    Returns:
        List of all directory paths found
    """
    directories = []
    
    if not source_path.exists() or not source_path.is_dir():
        return directories
    
    try:
        for item in source_path.rglob('*'):
            if item.is_dir():
                directories.append(item)
        
        # Ensure root path is included
        if source_path not in directories:
            directories.insert(0, source_path)
            
    except (PermissionError, OSError) as e:
        logging.warning(f"Permission error scanning {source_path}: {e}")
    
    return directories


def create_folder_structure(source_paths: List[Path], destination_root: Path) -> Tuple[int, List[str]]:
    """
    Create a folder structure at the destination based on the source structure.
    
    Args:
        source_paths: List of source directory paths to recreate
        destination_root: Root destination path
        
    Returns:
        Tuple of (success_count, error_messages)
    """
    success_count = 0
    errors = []
    
    # Create destination root if it doesn't exist
    try:
        destination_root.mkdir(parents=True, exist_ok=True)
    except (PermissionError, OSError) as e:
        error_msg = f"Cannot create destination root {destination_root}: {e}"
        errors.append(error_msg)
        logging.error(error_msg)
        return success_count, errors
    
    # Sort paths by depth to create parent directories first
    sorted_paths = sorted(source_paths, key=lambda p: len(p.parts))
    
    for source_path in sorted_paths:
        try:
            # Calculate relative path from the first source path
            if len(source_paths) > 0:
                relative_path = source_path.relative_to(source_paths[0].parent)
                destination_path = destination_root / relative_path
            else:
                destination_path = destination_root / source_path.name
            
            # Create the directory
            destination_path.mkdir(parents=True, exist_ok=True)
            success_count += 1
            logging.info(f"Created folder: {destination_path}")
            
        except (PermissionError, OSError) as e:
            error_msg = f"Error creating {destination_path}: {e}"
            errors.append(error_msg)
            logging.error(error_msg)
    
    return success_count, errors


def validate_path(path_str: str) -> Tuple[bool, str, Path]:
    """
    Validate a path string and return validation results.
    
    Args:
        path_str: String path to validate
        
    Returns:
        Tuple of (is_valid, error_message, path_object)
    """
    if not path_str or not path_str.strip():
        return False, "Path cannot be empty", Path()
    
    try:
        path = Path(path_str.strip())
        
        if not path.exists():
            return False, "Path does not exist", path
        
        if not path.is_dir():
            return False, "Path is not a directory", path
        
        return True, "", path
        
    except Exception as e:
        return False, f"Invalid path: {e}", Path()


def count_files_recursive(root_path: Path) -> Tuple[int, List[Path]]:
    """
    Count all files under root_path recursively.

    Returns (count, list_of_files). If the path is invalid, returns (0, []).
    """
    if not root_path.exists() or not root_path.is_dir():
        return 0, []

    files: List[Path] = []
    try:
        for item in root_path.rglob('*'):
            if item.is_file():
                files.append(item)
    except (PermissionError, OSError) as e:
        logging.warning(f"Error scanning files under {root_path}: {e}")

    return len(files), files


def count_files_root_only(root_path: Path) -> int:
    """
    Count files directly inside root_path (non-recursive).
    """
    if not root_path.exists() or not root_path.is_dir():
        return 0
    try:
        return sum(1 for p in root_path.iterdir() if p.is_file())
    except (PermissionError, OSError) as e:
        logging.warning(f"Error listing {root_path}: {e}")
        return 0


def _unique_destination(root: Path, name: str) -> Path:
    """Return a non-conflicting destination path inside root by appending (n) before extension."""
    base = name
    stem = Path(name).stem
    suffix = Path(name).suffix
    candidate = root / base
    counter = 1
    while candidate.exists():
        candidate = root / f"{stem} ({counter}){suffix}"
        counter += 1
    return candidate


def flatten_to_root(root_path: Path, conflict_mode: str = 'rename') -> Dict[str, object]:
    """
    Move all files from nested subfolders into root_path and remove empty subfolders.

    conflict_mode:
      - 'rename': auto-rename conflicting files as "name (n).ext"
      - 'skip': do not move a file if a conflict exists

    Returns dict with keys: moved, skipped_conflicts, removed_folders, errors, moves
    """
    result: Dict[str, object] = {
        'moved': 0,
        'skipped_conflicts': 0,
        'removed_folders': 0,
        'errors': [],
        'moves': []  # list of (src, dest)
    }

    if not root_path.exists() or not root_path.is_dir():
        result['errors'].append(f"Invalid root folder: {root_path}")
        return result

    # Move files up to root
    try:
        # Collect files first to avoid modifying iterables while traversing
        all_files: List[Path] = []
        for p in root_path.rglob('*'):
            if p.is_file() and p.parent != root_path:
                all_files.append(p)

        for src in all_files:
            try:
                dest = root_path / src.name
                if dest.exists():
                    if conflict_mode == 'skip':
                        result['skipped_conflicts'] += 1
                        logging.info(f"Skip due to conflict: {src} -> {dest}")
                        continue
                    dest = _unique_destination(root_path, src.name)

                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dest))
                result['moved'] += 1
                result['moves'].append((str(src), str(dest)))
                logging.info(f"Moved file: {src} -> {dest}")
            except (PermissionError, OSError, shutil.Error) as e:
                msg = f"Error moving {src}: {e}"
                logging.error(msg)
                result['errors'].append(msg)
    except (PermissionError, OSError) as e:
        msg = f"Error scanning {root_path}: {e}"
        logging.error(msg)
        result['errors'].append(msg)

    # Remove empty directories (deepest first)
    try:
        dirs = [d for d in root_path.rglob('*') if d.is_dir()]
        for d in sorted(dirs, key=lambda p: len(p.parts), reverse=True):
            try:
                if is_folder_empty(d):
                    d.rmdir()
                    result['removed_folders'] += 1
                    logging.info(f"Removed empty folder: {d}")
            except (PermissionError, OSError) as e:
                msg = f"Error removing {d}: {e}"
                logging.warning(msg)
                result['errors'].append(msg)
    except (PermissionError, OSError) as e:
        msg = f"Error enumerating directories in {root_path}: {e}"
        logging.warning(msg)
        result['errors'].append(msg)

    return result
