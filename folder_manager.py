"""
Folder Manager Desktop Application
A modern GUI application for managing folders with two main features:
1. Delete empty folder structures
2. Duplicate folder structures (folders only, no files)
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
from typing import List, Optional

from utils.folder_operations import (
    setup_logging, scan_empty_folder_structure, delete_empty_folders,
    scan_folder_structure, create_folder_structure, validate_path,
    count_files_recursive, count_files_root_only, flatten_to_root
)


class FolderManagerApp:
    """Main application class for the Folder Manager."""
    
    def __init__(self):
        # Setup logging
        self.log_file = setup_logging()
        
        # Initialize the main window
        self.root = ctk.CTk()
        self.setup_window()
        
        # Initialize variables
        self.selected_delete_path: Optional[Path] = None
        self.selected_source_path: Optional[Path] = None
        self.selected_dest_path: Optional[Path] = None
        self.empty_folders: List[Path] = []
        
        # Create the GUI
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window."""
        self.root.title("Folder Manager")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")  # Options: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"
        
        # Center the window
        self.center_window()
        
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main container with padding
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="📁 Folder Manager", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            main_frame, 
            text="Manage your folders efficiently", 
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Create tabview
        self.tabview = ctk.CTkTabview(main_frame, width=1300, height=700)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add("Delete Empty Folders")
        self.tabview.add("Duplicate Structure")
        self.tabview.add("Root Tools")
        
        # Configure tab appearance
        self.tabview.tab("Delete Empty Folders").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Duplicate Structure").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Root Tools").grid_columnconfigure(0, weight=1)
        
        # Create tab contents
        self.create_delete_tab()
        self.create_duplicate_tab()
        self.create_root_tools_tab()
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_delete_tab(self):
        """Create the Delete Empty Folders tab."""
        tab = self.tabview.tab("Delete Empty Folders")
        
        # Instructions
        instructions = ctk.CTkLabel(
            tab,
            text="Select a folder to scan for empty folder structures that can be safely deleted.",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        instructions.pack(pady=(10, 20))
        
        # Path selection frame
        path_frame = ctk.CTkFrame(tab)
        path_frame.pack(fill="x", padx=10, pady=10)
        
        path_label = ctk.CTkLabel(path_frame, text="Select Folder:", font=ctk.CTkFont(size=14, weight="bold"))
        path_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Path display and browse button
        path_display_frame = ctk.CTkFrame(path_frame)
        path_display_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.delete_path_var = tk.StringVar()
        self.delete_path_entry = ctk.CTkEntry(
            path_display_frame, 
            textvariable=self.delete_path_var,
            placeholder_text="Click 'Browse' to select a folder",
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.delete_path_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        browse_delete_btn = ctk.CTkButton(
            path_display_frame,
            text="Browse",
            command=self.browse_delete_folder,
            width=100,
            height=35
        )
        browse_delete_btn.pack(side="right", padx=(5, 10), pady=10)
        
        # Action buttons frame
        action_frame = ctk.CTkFrame(tab)
        action_frame.pack(fill="x", padx=10, pady=10)
        
        self.scan_btn = ctk.CTkButton(
            action_frame,
            text="🔍 Scan for Empty Folders",
            command=self.scan_empty_folders,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.scan_btn.pack(side="left", padx=(10, 5), pady=10)
        
        self.delete_btn = ctk.CTkButton(
            action_frame,
            text="🗑️ Delete Selected",
            command=self.delete_empty_folders,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="red",
            hover_color="darkred",
            state="disabled"
        )
        self.delete_btn.pack(side="left", padx=5, pady=10)
        
        # Results frame
        results_frame = ctk.CTkFrame(tab)
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        results_label = ctk.CTkLabel(
            results_frame, 
            text="Scan Results:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        results_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Results text area - using CustomTkinter Text widget for better scaling
        self.delete_results_text = ctk.CTkTextbox(
            results_frame,
            wrap="word",
            height=400,
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="white"
        )
        self.delete_results_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def create_root_tools_tab(self):
        """Create the Root Tools tab (count files, flatten)."""
        tab = self.tabview.tab("Root Tools")

        # Instructions
        instructions = ctk.CTkLabel(
            tab,
            text="Select a root folder to count files or move all nested files into it (flatten).",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        instructions.pack(pady=(10, 20))

        # Path selection frame
        path_frame = ctk.CTkFrame(tab)
        path_frame.pack(fill="x", padx=10, pady=10)

        path_label = ctk.CTkLabel(path_frame, text="Root Folder:", font=ctk.CTkFont(size=14, weight="bold"))
        path_label.pack(anchor="w", padx=10, pady=(10, 5))

        path_display_frame = ctk.CTkFrame(path_frame)
        path_display_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.root_tools_path_var = tk.StringVar()
        self.root_tools_path_entry = ctk.CTkEntry(
            path_display_frame,
            textvariable=self.root_tools_path_var,
            placeholder_text="Click 'Browse' to select a folder",
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.root_tools_path_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)

        browse_btn = ctk.CTkButton(
            path_display_frame,
            text="Browse",
            command=self.browse_root_tools_folder,
            width=100,
            height=35
        )
        browse_btn.pack(side="right", padx=(5, 10), pady=10)

        # Action buttons
        action_frame = ctk.CTkFrame(tab)
        action_frame.pack(fill="x", padx=10, pady=10)

        self.count_btn = ctk.CTkButton(
            action_frame,
            text="📊 Count Files",
            command=self.count_files_action,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.count_btn.pack(side="left", padx=(10, 5), pady=10)

        self.flatten_btn = ctk.CTkButton(
            action_frame,
            text="🧹 Flatten to Root",
            command=self.flatten_to_root_action,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="orange",
            hover_color="#9a5b00"
        )
        self.flatten_btn.pack(side="left", padx=5, pady=10)

        # Results
        results_frame = ctk.CTkFrame(tab)
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        results_label = ctk.CTkLabel(
            results_frame,
            text="Results:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        results_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.root_tools_results = ctk.CTkTextbox(
            results_frame,
            wrap="word",
            height=400,
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="white"
        )
        self.root_tools_results.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def browse_root_tools_folder(self):
        folder = filedialog.askdirectory(title="Select root folder")
        if folder:
            self.root_tools_path_var.set(folder)

    # Root Tools: Count files
    def count_files_action(self):
        path_str = self.root_tools_path_var.get().strip()
        valid, err, path = validate_path(path_str)
        if not valid:
            messagebox.showerror("Error", err)
            return
        self.count_btn.configure(state="disabled", text="⏳ Counting...")
        self.status_var.set("Counting files...")

        def worker():
            try:
                root_only = count_files_root_only(path)
                total, _ = count_files_recursive(path)
                self.root.after(0, lambda: self._count_files_complete(path, root_only, total))
            except Exception as e:
                self.root.after(0, lambda: self._count_files_error(str(e)))

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def _count_files_complete(self, path: Path, root_only: int, total: int):
        self.count_btn.configure(state="normal", text="📊 Count Files")
        self.root_tools_results.delete("1.0", "end")
        self.root_tools_results.insert("end", f"Folder: {path}\n\n")
        self.root_tools_results.insert("end", f"Files in root only: {root_only}\n")
        self.root_tools_results.insert("end", f"Files in all subfolders: {total}\n")
        self.status_var.set("Count complete.")

    def _count_files_error(self, msg: str):
        self.count_btn.configure(state="normal", text="📊 Count Files")
        messagebox.showerror("Count Error", f"Error counting files: {msg}")
        self.status_var.set("Count failed.")

    # Root Tools: Flatten
    def flatten_to_root_action(self):
        path_str = self.root_tools_path_var.get().strip()
        valid, err, path = validate_path(path_str)
        if not valid:
            messagebox.showerror("Error", err)
            return

        confirm = messagebox.askyesno(
            "Confirm Flatten",
            "This will move ALL files from nested folders into the selected root folder,\n"
            "handle name conflicts, and remove empty folders.\n\n"
            "Proceed?"
        )
        if not confirm:
            return

        self.flatten_btn.configure(state="disabled", text="⏳ Flattening...")
        self.status_var.set("Flattening folder...")

        def worker():
            try:
                result = flatten_to_root(path, conflict_mode='rename')
                self.root.after(0, lambda: self._flatten_complete(result))
            except Exception as e:
                self.root.after(0, lambda: self._flatten_error(str(e)))

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def _flatten_complete(self, result):
        self.flatten_btn.configure(state="normal", text="🧹 Flatten to Root")
        self.root_tools_results.delete("1.0", "end")
        self.root_tools_results.insert("end", "Flatten completed!\n\n")
        self.root_tools_results.insert("end", f"Files moved: {result.get('moved', 0)}\n")
        self.root_tools_results.insert("end", f"Name conflicts skipped: {result.get('skipped_conflicts', 0)}\n")
        self.root_tools_results.insert("end", f"Empty folders removed: {result.get('removed_folders', 0)}\n")
        errors = result.get('errors', [])
        if errors:
            self.root_tools_results.insert("end", f"\nErrors: {len(errors)}\n")
            for e in errors[:50]:  # cap output
                self.root_tools_results.insert("end", f"- {e}\n")
        self.status_var.set("Flatten complete.")

    def _flatten_error(self, msg: str):
        self.flatten_btn.configure(state="normal", text="🧹 Flatten to Root")
        messagebox.showerror("Flatten Error", f"Error flattening folders: {msg}")
        self.status_var.set("Flatten failed.")
        
    def create_duplicate_tab(self):
        """Create the Duplicate Folder Structure tab."""
        tab = self.tabview.tab("Duplicate Structure")
        
        # Instructions
        instructions = ctk.CTkLabel(
            tab,
            text="Select source and destination folders to duplicate the folder structure (folders only, no files).",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        instructions.pack(pady=(10, 20))
        
        # Source path selection
        source_frame = ctk.CTkFrame(tab)
        source_frame.pack(fill="x", padx=10, pady=10)
        
        source_label = ctk.CTkLabel(source_frame, text="Source Folder:", font=ctk.CTkFont(size=14, weight="bold"))
        source_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        source_display_frame = ctk.CTkFrame(source_frame)
        source_display_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.source_path_var = tk.StringVar()
        self.source_path_entry = ctk.CTkEntry(
            source_display_frame, 
            textvariable=self.source_path_var,
            placeholder_text="Click 'Browse' to select source folder",
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.source_path_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        browse_source_btn = ctk.CTkButton(
            source_display_frame,
            text="Browse",
            command=self.browse_source_folder,
            width=100,
            height=35
        )
        browse_source_btn.pack(side="right", padx=(5, 10), pady=10)
        
        # Destination path selection
        dest_frame = ctk.CTkFrame(tab)
        dest_frame.pack(fill="x", padx=10, pady=10)
        
        dest_label = ctk.CTkLabel(dest_frame, text="Destination Folder:", font=ctk.CTkFont(size=14, weight="bold"))
        dest_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        dest_display_frame = ctk.CTkFrame(dest_frame)
        dest_display_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.dest_path_var = tk.StringVar()
        self.dest_path_entry = ctk.CTkEntry(
            dest_display_frame, 
            textvariable=self.dest_path_var,
            placeholder_text="Click 'Browse' to select destination folder",
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.dest_path_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        browse_dest_btn = ctk.CTkButton(
            dest_display_frame,
            text="Browse",
            command=self.browse_dest_folder,
            width=100,
            height=35
        )
        browse_dest_btn.pack(side="right", padx=(5, 10), pady=10)
        
        # Action buttons frame
        action_frame = ctk.CTkFrame(tab)
        action_frame.pack(fill="x", padx=10, pady=10)
        
        self.preview_btn = ctk.CTkButton(
            action_frame,
            text="👁️ Preview Structure",
            command=self.preview_structure,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.preview_btn.pack(side="left", padx=(10, 5), pady=10)
        
        self.create_btn = ctk.CTkButton(
            action_frame,
            text="📁 Create Structure",
            command=self.create_folder_structure,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="green",
            hover_color="darkgreen",
            state="disabled"
        )
        self.create_btn.pack(side="left", padx=5, pady=10)
        
        # Results frame
        results_frame = ctk.CTkFrame(tab)
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        results_label = ctk.CTkLabel(
            results_frame, 
            text="Preview/Results:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        results_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Results text area - using CustomTkinter Text widget for better scaling
        self.duplicate_results_text = ctk.CTkTextbox(
            results_frame,
            wrap="word",
            height=400,
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="white"
        )
        self.duplicate_results_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
    def create_status_bar(self, parent):
        """Create the status bar at the bottom."""
        status_frame = ctk.CTkFrame(parent)
        status_frame.pack(fill="x", pady=(10, 0))
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ctk.CTkLabel(
            status_frame, 
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12)
        )
        status_label.pack(side="left", padx=10, pady=5)
        
        # Log file info
        log_info = ctk.CTkLabel(
            status_frame,
            text=f"Log: {Path(self.log_file).name}",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        log_info.pack(side="right", padx=10, pady=5)
        
    # File browsing methods
    def browse_delete_folder(self):
        """Browse for folder to delete empty folders from."""
        folder = filedialog.askdirectory(title="Select folder to scan for empty folders")
        if folder:
            self.selected_delete_path = Path(folder)
            self.delete_path_var.set(str(self.selected_delete_path))
            
    def browse_source_folder(self):
        """Browse for source folder."""
        folder = filedialog.askdirectory(title="Select source folder")
        if folder:
            self.selected_source_path = Path(folder)
            self.source_path_var.set(str(self.selected_source_path))
            
    def browse_dest_folder(self):
        """Browse for destination folder."""
        folder = filedialog.askdirectory(title="Select destination folder")
        if folder:
            self.selected_dest_path = Path(folder)
            self.dest_path_var.set(str(self.selected_dest_path))
            
    # Delete empty folders methods
    def scan_empty_folders(self):
        """Scan for empty folders in a separate thread."""
        if not self.selected_delete_path:
            messagebox.showerror("Error", "Please select a folder first.")
            return
            
        # Disable button during scan
        self.scan_btn.configure(state="disabled", text="🔍 Scanning...")
        self.status_var.set("Scanning for empty folders...")
        
        # Run in separate thread
        thread = threading.Thread(target=self._scan_empty_folders_thread)
        thread.daemon = True
        thread.start()
        
    def _scan_empty_folders_thread(self):
        """Thread function for scanning empty folders."""
        try:
            self.empty_folders = scan_empty_folder_structure(self.selected_delete_path)
            
            # Update UI in main thread
            self.root.after(0, self._scan_empty_folders_complete)
            
        except Exception as e:
            self.root.after(0, lambda: self._scan_empty_folders_error(str(e)))
            
    def _scan_empty_folders_complete(self):
        """Handle scan completion."""
        self.scan_btn.configure(state="normal", text="🔍 Scan for Empty Folders")
        
        # Display results
        self.delete_results_text.delete("1.0", "end")
        
        if self.empty_folders:
            self.delete_results_text.insert("end", f"Found {len(self.empty_folders)} empty folder structures:\n\n")
            
            for folder in sorted(self.empty_folders, key=lambda p: len(p.parts)):
                self.delete_results_text.insert("end", f"📁 {folder}\n")
                
            self.delete_btn.configure(state="normal")
            self.status_var.set(f"Found {len(self.empty_folders)} empty folders. Ready to delete.")
            
        else:
            self.delete_results_text.insert("end", "No empty folder structures found.\n")
            self.delete_btn.configure(state="disabled")
            self.status_var.set("No empty folders found.")
            
    def _scan_empty_folders_error(self, error_msg):
        """Handle scan error."""
        self.scan_btn.configure(state="normal", text="🔍 Scan for Empty Folders")
        messagebox.showerror("Scan Error", f"Error scanning folders: {error_msg}")
        self.status_var.set("Scan failed.")
        
    def delete_empty_folders(self):
        """Delete the empty folders."""
        if not self.empty_folders:
            messagebox.showwarning("Warning", "No empty folders to delete.")
            return
            
        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {len(self.empty_folders)} empty folder structures?\n\n"
            "This action cannot be undone."
        )
        
        if not result:
            return
            
        # Disable button during deletion
        self.delete_btn.configure(state="disabled", text="🗑️ Deleting...")
        self.status_var.set("Deleting empty folders...")
        
        # Run in separate thread
        thread = threading.Thread(target=self._delete_empty_folders_thread)
        thread.daemon = True
        thread.start()
        
    def _delete_empty_folders_thread(self):
        """Thread function for deleting empty folders."""
        try:
            success_count, errors = delete_empty_folders(self.empty_folders)
            self.root.after(0, lambda: self._delete_empty_folders_complete(success_count, errors))
            
        except Exception as e:
            self.root.after(0, lambda: self._delete_empty_folders_error(str(e)))
            
    def _delete_empty_folders_complete(self, success_count, errors):
        """Handle deletion completion."""
        self.delete_btn.configure(state="disabled", text="🗑️ Delete Selected")
        self.scan_btn.configure(state="normal", text="🔍 Scan for Empty Folders")
        
        # Display results
        self.delete_results_text.delete("1.0", "end")
        self.delete_results_text.insert("end", f"Deletion completed!\n\n")
        self.delete_results_text.insert("end", f"Successfully deleted: {success_count} folders\n")
        
        if errors:
            self.delete_results_text.insert("end", f"\nErrors encountered: {len(errors)}\n")
            for error in errors:
                self.delete_results_text.insert("end", f"⚠️ {error}\n")
                
        self.empty_folders = []
        self.status_var.set(f"Deleted {success_count} folders successfully.")
        messagebox.showinfo("Success", f"Successfully deleted {success_count} empty folders!")
        
    def _delete_empty_folders_error(self, error_msg):
        """Handle deletion error."""
        self.delete_btn.configure(state="normal", text="🗑️ Delete Selected")
        messagebox.showerror("Deletion Error", f"Error deleting folders: {error_msg}")
        self.status_var.set("Deletion failed.")
        
    # Duplicate structure methods
    def preview_structure(self):
        """Preview the folder structure to be created."""
        if not self.selected_source_path or not self.selected_dest_path:
            messagebox.showerror("Error", "Please select both source and destination folders.")
            return
            
        # Disable button during preview
        self.preview_btn.configure(state="disabled", text="👁️ Previewing...")
        self.status_var.set("Generating preview...")
        
        # Run in separate thread
        thread = threading.Thread(target=self._preview_structure_thread)
        thread.daemon = True
        thread.start()
        
    def _preview_structure_thread(self):
        """Thread function for previewing structure."""
        try:
            folders = scan_folder_structure(self.selected_source_path)
            self.root.after(0, lambda: self._preview_structure_complete(folders))
            
        except Exception as e:
            self.root.after(0, lambda: self._preview_structure_error(str(e)))
            
    def _preview_structure_complete(self, folders):
        """Handle preview completion."""
        self.preview_btn.configure(state="normal", text="👁️ Preview Structure")
        
        # Display preview
        self.duplicate_results_text.delete("1.0", "end")
        self.duplicate_results_text.insert("end", f"Folder structure preview:\n\n")
        self.duplicate_results_text.insert("end", f"Source: {self.selected_source_path}\n")
        self.duplicate_results_text.insert("end", f"Destination: {self.selected_dest_path}\n\n")
        self.duplicate_results_text.insert("end", f"Will create {len(folders)} folders:\n\n")
        
        for folder in sorted(folders, key=lambda p: len(p.parts)):
            relative_path = folder.relative_to(self.selected_source_path)
            self.duplicate_results_text.insert("end", f"📁 {relative_path}\n")
            
        self.create_btn.configure(state="normal")
        self.status_var.set(f"Preview ready. {len(folders)} folders will be created.")
        
    def _preview_structure_error(self, error_msg):
        """Handle preview error."""
        self.preview_btn.configure(state="normal", text="👁️ Preview Structure")
        messagebox.showerror("Preview Error", f"Error generating preview: {error_msg}")
        self.status_var.set("Preview failed.")
        
    def create_folder_structure(self):
        """Create the folder structure."""
        if not self.selected_source_path or not self.selected_dest_path:
            messagebox.showerror("Error", "Please select both source and destination folders.")
            return
            
        # Confirm creation
        result = messagebox.askyesno(
            "Confirm Creation",
            "Are you sure you want to create the folder structure at the destination?"
        )
        
        if not result:
            return
            
        # Disable button during creation
        self.create_btn.configure(state="disabled", text="📁 Creating...")
        self.status_var.set("Creating folder structure...")
        
        # Run in separate thread
        thread = threading.Thread(target=self._create_folder_structure_thread)
        thread.daemon = True
        thread.start()
        
    def _create_folder_structure_thread(self):
        """Thread function for creating folder structure."""
        try:
            folders = scan_folder_structure(self.selected_source_path)
            success_count, errors = create_folder_structure(folders, self.selected_dest_path)
            self.root.after(0, lambda: self._create_folder_structure_complete(success_count, errors))
            
        except Exception as e:
            self.root.after(0, lambda: self._create_folder_structure_error(str(e)))
            
    def _create_folder_structure_complete(self, success_count, errors):
        """Handle creation completion."""
        self.create_btn.configure(state="normal", text="📁 Create Structure")
        
        # Display results
        self.duplicate_results_text.delete("1.0", "end")
        self.duplicate_results_text.insert("end", f"Folder structure creation completed!\n\n")
        self.duplicate_results_text.insert("end", f"Successfully created: {success_count} folders\n")
        
        if errors:
            self.duplicate_results_text.insert("end", f"\nErrors encountered: {len(errors)}\n")
            for error in errors:
                self.duplicate_results_text.insert("end", f"⚠️ {error}\n")
                
        self.status_var.set(f"Created {success_count} folders successfully.")
        messagebox.showinfo("Success", f"Successfully created {success_count} folders!")
        
    def _create_folder_structure_error(self, error_msg):
        """Handle creation error."""
        self.create_btn.configure(state="normal", text="📁 Create Structure")
        messagebox.showerror("Creation Error", f"Error creating folders: {error_msg}")
        self.status_var.set("Creation failed.")
        
    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    """Main entry point."""
    app = FolderManagerApp()
    app.run()


if __name__ == "__main__":
    main()
