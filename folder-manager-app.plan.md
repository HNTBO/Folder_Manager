<!-- a24bc0e6-6ff2-405a-89ac-296243277ef3 9881d273-81f1-4cb0-9a01-f77f77d4145c -->
# Folder Manager Desktop Application

## Overview

Create a Python-based desktop application with a modern GUI that provides two key features:

1. Scan and delete folders containing only empty folders
2. Duplicate folder structure (folders only, no files) to another location

## Technology Stack

- **Python 3.x** - Programming language
- **CustomTkinter** - Modern, polished GUI framework
- **PyInstaller** - Convert Python to standalone .exe file
- **pathlib/os** - Folder operations

## Implementation Steps

### 1. Project Setup

- Create project structure with proper folders
- Create `requirements.txt` with dependencies: customtkinter, pillow
- Create main application file `folder_manager.py`

### 2. Core Backend Logic

- **Empty folder deletion module** (`utils/folder_operations.py`):
- Function to recursively scan folders and identify empty folder trees
- Function to safely delete empty folder structures
- Function to generate preview list of folders to be deleted

- **Folder structure duplication module** (`utils/folder_operations.py`):
- Function to recursively scan source folder structure
- Function to recreate folder hierarchy at destination (folders only, no files)

### 3. GUI Implementation

- **Main window** with modern CustomTkinter styling:
- Title bar and app branding
- Tab-based interface for two main features

- **Tab 1 - Delete Empty Folders**:
- Folder browser button with file explorer dialog
- Display selected path
- "Scan" button to preview empty folders
- Scrollable list showing folders that will be deleted
- "Delete" confirmation button (disabled until scan completes)
- Status messages and progress indicators

- **Tab 2 - Duplicate Folder Structure**:
- Source folder browser button
- Destination folder browser button
- Display both selected paths
- "Preview" button to show folder structure that will be created
- Scrollable preview list
- "Create Structure" button to execute
- Status messages and progress indicators

### 4. User Experience Features

- Modern dark/light theme support
- Clear error messages for invalid paths or permissions
- Success/completion notifications
- Preview before any destructive operations
- Log file creation for both operations showing what was done

### 5. Build .exe Application

- Create `build.bat` script for easy building
- Configure PyInstaller with proper settings:
- Single .exe file output
- Include all dependencies
- Add application icon (optional)
- Windows-only build
- Test the generated .exe file

### 6. Documentation

- Create `README.md` with:
- How to use the application
- What each feature does
- Safety notes
- How to rebuild from source

## Key Files

- `folder_manager.py` - Main application entry point and GUI
- `utils/folder_operations.py` - Backend logic for folder operations
- `requirements.txt` - Python dependencies
- `build.bat` - Script to build the .exe file
- `README.md` - User documentation

### To-dos

- [ ] Create project structure and requirements.txt with dependencies
- [ ] Implement folder scanning, deletion, and duplication logic in utils/folder_operations.py
- [ ] Build main GUI window with CustomTkinter and tab-based interface
- [ ] Implement Delete Empty Folders tab with preview and confirmation
- [ ] Implement Duplicate Folder Structure tab with source/destination selection
- [ ] Create build script and configure PyInstaller to generate .exe file
- [ ] Create README.md with usage instructions and safety notes