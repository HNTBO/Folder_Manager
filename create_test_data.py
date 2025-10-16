"""
Test Data Generator for Folder Manager
Creates a realistic folder structure with empty folders and folders containing files
for testing the Folder Manager application.
"""

import os
import random
import argparse
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


def create_test_folder_structure(seed: Optional[str] = None):
    """Create a comprehensive test folder structure.

    If a seed is provided, the generation is fully deterministic for the same seed,
    including the timestamp placeholder used in file contents.
    """
    
    # Base test directory
    test_dir = Path("Test_Folder_Structure")
    
    # Remove existing test directory if it exists
    if test_dir.exists():
        import shutil
        shutil.rmtree(test_dir)
        print(f"Removed existing {test_dir}")
    
    # Apply seed for deterministic behavior (if provided)
    if seed is not None:
        random.seed(seed)

    # Create base directory
    test_dir.mkdir()
    print(f"Created test directory: {test_dir}")
    if seed is not None:
        print(f"Using seed: {seed}")
    
    # Sample folder names
    folder_names = [
        "Projects", "Documents", "Downloads", "Photos", "Videos", "Music",
        "Work", "Personal", "Archive", "Backup", "Temp", "Cache",
        "Reports", "Presentations", "Spreadsheets", "Images", "Screenshots",
        "Old_Files", "New_Files", "Drafts", "Final", "Review", "Approved",
        "Client_A", "Client_B", "Client_C", "Project_X", "Project_Y", "Project_Z",
        "2023", "2024", "2025", "January", "February", "March", "April", "May",
        "Q1", "Q2", "Q3", "Q4", "Weekly", "Monthly", "Yearly",
        "Alpha", "Beta", "Production", "Development", "Testing", "Staging"
    ]
    
    # Sample file names
    file_names = [
        "readme.txt", "notes.txt", "todo.txt", "ideas.txt", "summary.txt",
        "report.docx", "presentation.pptx", "data.xlsx", "config.json",
        "settings.ini", "log.txt", "error.log", "debug.log", "info.txt",
        "document.pdf", "manual.pdf", "guide.txt", "instructions.txt",
        "contact.txt", "address.txt", "phone.txt", "email.txt",
        "budget.xlsx", "expenses.xlsx", "income.xlsx", "balance.txt",
        "meeting_notes.txt", "agenda.txt", "minutes.txt", "action_items.txt"
    ]
    
    # Sample file contents
    file_contents = [
        "This is a test file for the Folder Manager application.",
        "Sample content to test file operations.",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Testing folder structure generation for Folder Manager.",
        "This file was created by the test data generator.",
        "Sample text content for testing purposes.",
        "Empty folders and files with content for testing.",
        "Folder Manager test data - file with content.",
        "Test file created on {timestamp}",
        "This is sample data for testing the application."
    ]

    # Determine timestamp replacement value (deterministic when seeded)
    if seed is not None:
        # Derive a stable timestamp from the seed within a 5-year window after 2020-01-01
        h = int(hashlib.md5(str(seed).encode("utf-8")).hexdigest(), 16)
        base_dt = datetime(2020, 1, 1, 0, 0, 0)
        ts_dt = base_dt + timedelta(seconds=h % (5 * 365 * 24 * 3600))
        timestamp_value = ts_dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        timestamp_value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    created_folders = 0
    created_files = 0
    empty_folders = 0
    
    # Create nested folder structure
    def create_nested_structure(parent_path, depth=0, max_depth=4):
        nonlocal created_folders, created_files, empty_folders
        
        if depth >= max_depth:
            return
        
        # Determine how many subfolders to create (random 1-4)
        num_folders = random.randint(1, 4)
        
        for i in range(num_folders):
            # Select random folder name
            folder_name = random.choice(folder_names)
            
            # Create unique folder name if it already exists
            folder_path = parent_path / folder_name
            counter = 1
            while folder_path.exists():
                folder_path = parent_path / f"{folder_name}_{counter}"
                counter += 1
            
            # Create the folder
            folder_path.mkdir()
            created_folders += 1
            
            # Randomly decide if this folder should be empty (30% chance)
            should_be_empty = random.random() < 0.3
            
            if should_be_empty:
                empty_folders += 1
                print(f"Created empty folder: {folder_path}")
            else:
                # Add some files to this folder (random 0-5 files)
                num_files = random.randint(0, 5)
                
                for j in range(num_files):
                    file_name = random.choice(file_names)
                    
                    # Create unique file name if it already exists
                    file_path = folder_path / file_name
                    counter = 1
                    while file_path.exists():
                        name_part = file_path.stem
                        ext_part = file_path.suffix
                        file_path = folder_path / f"{name_part}_{counter}{ext_part}"
                        counter += 1
                    
                    # Create file with random content
                    content = random.choice(file_contents)
                    if "{timestamp}" in content:
                        content = content.replace("{timestamp}", timestamp_value)
                    
                    file_path.write_text(content)
                    created_files += 1
                
                print(f"Created folder with {num_files} files: {folder_path}")
            
            # Recursively create subfolders (70% chance)
            if random.random() < 0.7:
                create_nested_structure(folder_path, depth + 1, max_depth)
    
    # Create the main structure
    print("\nCreating nested folder structure...")
    create_nested_structure(test_dir, 0, 4)
    
    # Create some additional empty folder structures (nested empty folders)
    print("\nCreating nested empty folder structures...")
    
    empty_structures = [
        ["Old_Projects", "Project_2022", "Client_Work", "Abandoned"],
        ["Temp_Files", "Cache", "Browser_Cache", "System_Cache"],
        ["Backup_Old", "Archive_2023", "Documents", "Drafts"],
        ["Empty_Structure_1", "Level_2", "Level_3", "Level_4"],
        ["Test_Empty", "Nested_Empty", "Deep_Empty"]
    ]
    
    for structure in empty_structures:
        current_path = test_dir
        for folder_name in structure:
            current_path = current_path / folder_name
            current_path.mkdir(exist_ok=True)
            created_folders += 1
            empty_folders += 1
        
        print(f"Created empty nested structure: {current_path}")
    
    # Create some mixed structures (some empty, some with files)
    print("\nCreating mixed structures...")
    
    mixed_structures = [
        {
            "path": ["Mixed_Folder", "Has_Files"],
            "files": ["file1.txt", "file2.txt", "readme.txt"]
        },
        {
            "path": ["Mixed_Folder", "Empty_Sub"],
            "files": []
        },
        {
            "path": ["Project_Structure", "Source", "Code"],
            "files": ["main.py", "utils.py", "config.json"]
        },
        {
            "path": ["Project_Structure", "Empty_Docs"],
            "files": []
        },
        {
            "path": ["Project_Structure", "Tests", "Unit"],
            "files": ["test_main.py", "test_utils.py"]
        }
    ]
    
    for structure in mixed_structures:
        current_path = test_dir
        for folder_name in structure["path"]:
            current_path = current_path / folder_name
            current_path.mkdir(exist_ok=True)
            created_folders += 1
        
        # Add files if specified
        for file_name in structure["files"]:
            file_path = current_path / file_name
            content = f"Test file: {file_name}\nCreated for Folder Manager testing."
            file_path.write_text(content)
            created_files += 1
        
        if structure["files"]:
            print(f"Created folder with files: {current_path} ({len(structure['files'])} files)")
        else:
            print(f"Created empty folder: {current_path}")
            empty_folders += 1
    
    # Summary
    print("\n" + "="*60)
    print("TEST DATA GENERATION COMPLETE!")
    print("="*60)
    print(f"Total folders created: {created_folders}")
    print(f"Total files created: {created_files}")
    print(f"Empty folders: {empty_folders}")
    print(f"Folders with files: {created_folders - empty_folders}")
    print(f"Test directory: {test_dir.absolute()}")
    print("\nThis structure is perfect for testing:")
    print("- Empty folder deletion feature")
    print("- Folder structure duplication feature")
    print("- Mixed scenarios (some empty, some with files)")
    print("\nYou can now run your Folder Manager application and test it with this data!")
    print("="*60)


def main():
    """Main function to run the test data generator."""
    parser = argparse.ArgumentParser(description="Generate test folder structure for Folder Manager.")
    parser.add_argument("--seed", help="Seed for deterministic generation (string or number)", default=None)
    args = parser.parse_args()

    print("Folder Manager - Test Data Generator")
    print("="*50)
    print("This script will create a realistic folder structure")
    print("with empty folders and folders containing files")
    print("for testing the Folder Manager application.")
    if args.seed is not None:
        print(f"\nDeterministic mode enabled with seed: {args.seed}")
    print()

    try:
        create_test_folder_structure(seed=args.seed)
    except Exception as e:
        print(f"\nError creating test data: {e}")
        return

    print("\nTest data generation completed successfully!")
    print("\nNext steps:")
    print("1. Run your Folder Manager application")
    print("2. Test the 'Delete Empty Folders' feature on the Test_Folder_Structure")
    print("3. Test the 'Duplicate Structure' feature with the test data")
    print("\nThe test structure contains a good mix of:")
    print("- Empty folders that should be deleted")
    print("- Folders with files that should be preserved")
    print("- Nested empty folder structures")
    print("- Mixed scenarios for comprehensive testing")


if __name__ == "__main__":
    main()
