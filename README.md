# 📁 Folder Manager

A modern desktop application for managing folders on your computer. Built with Python and CustomTkinter, this application provides two powerful features to help you organize and clean up your file system.

## ✨ Features

### 1. Delete Empty Folder Structures
- **Purpose**: Clean up your file system by removing unnecessary empty folder hierarchies
- **How it works**: Scans a selected folder and identifies folders that contain only empty folders or are empty themselves
- **Safety**: Always shows a preview of what will be deleted before performing any deletions
- **Logging**: Creates detailed logs of all operations

### 2. Duplicate Folder Structure
- **Purpose**: Create an identical folder structure at a new location without copying files
- **Use case**: Set up project templates, organize new work areas, or create backup folder structures
- **Preview**: Shows exactly which folders will be created before execution
- **Flexible**: Works with any folder depth and structure

### 3. Root Tools (New)
- **Count Files**: See how many files are directly in the selected root folder and how many exist across all subfolders.
- **Flatten to Root**: Move all files from nested subfolders into the selected root folder, then remove empty subfolders.
- **Safe conflicts**: Existing filenames are not overwritten; they are auto-renamed to "name (n).ext".

## 🚀 Getting Started

### Prerequisites
- **Windows 10/11** (tested on Windows 10)
- **Python 3.7 or higher** (if building from source)

### Installation Options

#### Option 1: Use the Pre-built Executable (Recommended)
1. Download the `FolderManager.exe` file from the `dist` folder
2. Double-click to run the application
3. No installation required!

#### Option 2: Build from Source
1. **Install Python** from [python.org](https://python.org) if not already installed
2. **Clone or download** this project to your computer
3. **Open Command Prompt** in the project folder
4. **Run the build script**:
   ```cmd
   build.bat
   ```
5. The executable will be created in the `dist` folder

Tip: To speed up subsequent builds (when dependencies are already installed), run:
```cmd
build.bat --skip-pip
```
The build script auto-detects Python (`python` or `py -3`).

## 📖 How to Use

### Delete Empty Folders

1. **Launch** the application
2. **Go to** the "Delete Empty Folders" tab
3. **Click "Browse"** and select the folder you want to scan
4. **Click "Scan for Empty Folders"** to analyze the folder structure
5. **Review the results** in the preview area
6. **Click "Delete Selected"** to remove the empty folders
7. **Confirm** the deletion when prompted

**Example scenario**: You have a downloads folder with many empty subfolders from old projects. This feature will clean them up automatically.

### Duplicate Folder Structure

1. **Launch** the application
2. **Go to** the "Duplicate Structure" tab
3. **Select source folder** (the folder whose structure you want to copy)
4. **Select destination folder** (where you want the new structure created)
5. **Click "Preview Structure"** to see what will be created
6. **Click "Create Structure"** to execute the duplication
7. **Confirm** the creation when prompted

**Example scenario**: You want to set up a new project with the same folder structure as an existing project, but without copying the files.

### Root Tools

1. Go to the "Root Tools" tab
2. Select the folder you want to analyze or flatten
3. Click "Count Files" to see:
   - Files directly in the root folder
   - Total files including all subfolders
4. Click "Flatten to Root" to move every file from subfolders into the root and remove empty folders
5. Confirm when prompted

Notes:
- Name conflicts are handled safely by auto-renaming as "name (n).ext".
- A summary shows moved files, skipped conflicts, removed empty folders, and errors.

## ⚠️ Safety Features

- **Preview before action**: Both features show exactly what will happen before doing anything
- **Confirmation dialogs**: You must confirm destructive operations
- **Detailed logging**: All operations are logged with timestamps
- **Error handling**: Clear error messages if something goes wrong
- **Threading**: Operations run in background threads so the interface stays responsive

## 📁 Log Files

The application creates detailed log files in the `logs` folder:
- **Location**: `logs/folder_manager_YYYYMMDD_HHMMSS.log`
- **Contents**: Timestamps, operations performed, errors encountered
- **Purpose**: Track what was done and troubleshoot any issues

## 🛠️ Technical Details

### Built With
- **Python 3.x** - Core programming language
- **CustomTkinter** - Modern GUI framework
- **PyInstaller** - Creates standalone executable
- **pathlib** - Modern file system operations

### File Structure
```
FolderManager/
├── folder_manager.py          # Main application
├── utils/
│   └── folder_operations.py   # Backend logic
├── requirements.txt           # Dependencies
├── build.bat                 # Build script
├── README.md                 # This documentation
├── logs/                     # Log files (created at runtime)
├── dist/                     # Built executable (created during build)
└── build/                    # Build artifacts (created during build)
```

## 🔧 Troubleshooting

### Common Issues

**"Python is not installed" error when running build.bat**
- Download and install Python from [python.org](https://python.org)
- Make sure to check "Add Python to PATH" during installation

**"Permission denied" errors**
- Run the application as administrator
- Make sure the target folders are not in use by other programs

**Application won't start**
- Check that all files are in the same folder
- Try running from Command Prompt to see error messages

**Executable doesn't show new features**
- Rebuild using `build.bat` (or `build.bat --skip-pip` if dependencies are already installed)
- Make sure you launch the newly built `dist\FolderManager.exe`

**Scan finds no empty folders**
- This is normal if your folder structure doesn't contain empty folders
- The application only deletes folders that are completely empty or contain only empty subfolders

### Getting Help

If you encounter issues:
1. Check the log files in the `logs` folder
2. Try running the application as administrator
3. Make sure your antivirus isn't blocking the application

## 📝 Notes

- The application only works with **folders**, not individual files
- **Empty folder deletion** removes folders that contain no files and only empty subfolders
- **Folder structure duplication** creates only the folder hierarchy, no files are copied
- All operations are **logged** for your reference
- The application is **safe** and will always ask for confirmation before making changes

## 🎯 Use Cases

### For Personal Organization
- Clean up old project folders with empty subdirectories
- Organize downloads folder by removing empty category folders
- Set up new project structures based on existing templates

### For Professional Use
- Clean up shared network drives
- Set up consistent folder structures for team projects
- Organize client work folders

## 🔄 Updates

To update the application:
1. Download the new version
2. Replace the old files
3. Run `build.bat` to rebuild the executable
4. Your log files will be preserved

Recent changes:
- Added "Root Tools" tab with "Count Files" and "Flatten to Root" features
- Improved `build.bat` to auto-detect Python and support `--skip-pip`
- Enhanced `count_files.bat` to run from any folder and detect Python reliably

## Test Data Generator

- Purpose: Quickly create a realistic folder tree for safe testing.
- Location: Creates `Test_Folder_Structure` in the current working folder. If it already exists, it is removed and recreated each run.
- Mix: Generates a random nested structure plus a few fixed subtrees (some empty, some with sample files) to exercise different scenarios.

### Using the batch script (recommended on Windows)

1. Run `create_test_data.bat` (double-click or from Command Prompt).
2. When prompted, enter a seed for deterministic generation, or press Enter for a new random structure each time.
   - With a seed, the folder structure, file choices, and the `{timestamp}` content placeholder are reproducible.
3. The script prints a summary of folders/files created.

Examples:
```cmd
create_test_data.bat
```
(leave seed blank for random)

Then run again and enter the same seed (e.g., `my-seed-123`) to reproduce identical output later.

### Using Python directly

```cmd
python create_test_data.py               # random each run
python create_test_data.py --seed 42     # deterministic for seed 42
python create_test_data.py --seed "acme"  # deterministic for seed "acme"
```

### Notes

- Deterministic mode: Using the same seed reproduces the nested structure, file names, and timestamp placeholder values.
- Random mode: Leaving the seed blank creates a different structure each time.
- Contents overview:
  - Random nested folders up to depth 4; ~30% of folders empty; 0–5 files added otherwise.
  - Fixed empty nested subtrees for testing empty-folder deletion.
  - Fixed mixed subtrees with some files for testing duplication and preservation.
- Safe to re-run: The generator removes any existing `Test_Folder_Structure` before creating a new one.
- Next steps: Use `Test_Folder_Structure` with the app’s "Delete Empty Folders" and "Duplicate Structure" features for end-to-end testing.

---

## License

- Copyright (c) 2025 Frederic Pons
- Licensed under the MIT License. See `LICENSE`.
- Third-party components and their licenses are listed in `THIRD_PARTY_NOTICES.md`.

**Enjoy using Folder Manager to keep your file system organized!** 📁✨
# Folder_Manager
# Folder_Manager
