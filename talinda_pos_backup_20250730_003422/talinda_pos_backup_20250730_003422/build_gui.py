#!/usr/bin/env python3
"""
Talinda POS Installer Builder - GUI Tool
========================================

A simple GUI tool for building the Talinda POS installer.
"""

import sys
import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
import queue

class InstallerBuilderGUI:
    """GUI for building the Talinda POS installer."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Talinda POS Installer Builder")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Message queue for thread communication
        self.message_queue = queue.Queue()
        
        self.setup_ui()
        self.check_python()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Talinda POS Installer Builder", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Python status
        self.python_status = ttk.Label(main_frame, text="Checking Python...", 
                                      foreground="orange")
        self.python_status.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Build Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)
        
        # Build method
        ttk.Label(options_frame, text="Build Method:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.build_method = tk.StringVar(value="cx_Freeze")
        build_method_combo = ttk.Combobox(options_frame, textvariable=self.build_method, 
                                         values=["cx_Freeze", "PyInstaller", "Auto-detect"], 
                                         state="readonly", width=15)
        build_method_combo.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Create installer
        self.create_installer = tk.BooleanVar(value=True)
        installer_check = ttk.Checkbutton(options_frame, text="Create Windows Installer", 
                                         variable=self.create_installer)
        installer_check.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Create portable package
        self.create_portable = tk.BooleanVar(value=True)
        portable_check = ttk.Checkbutton(options_frame, text="Create Portable Package", 
                                        variable=self.create_portable)
        portable_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Clean build directories
        self.clean_build = tk.BooleanVar(value=True)
        clean_check = ttk.Checkbutton(options_frame, text="Clean previous builds", 
                                     variable=self.clean_build)
        clean_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Build button
        self.build_button = ttk.Button(main_frame, text="Start Build", 
                                      command=self.start_build, state="disabled")
        self.build_button.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Log output
        log_frame = ttk.LabelFrame(main_frame, text="Build Log", padding="5")
        log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
    def check_python(self):
        """Check if Python is available."""
        try:
            result = subprocess.run([sys.executable, "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.python_status.config(text=f"✓ Python found: {version}", 
                                        foreground="green")
                self.build_button.config(state="normal")
                self.log_message(f"Python found: {version}")
            else:
                self.python_status.config(text="✗ Python not found", 
                                        foreground="red")
                self.log_message("ERROR: Python not found")
        except Exception as e:
            self.python_status.config(text="✗ Python check failed", 
                                    foreground="red")
            self.log_message(f"ERROR: Python check failed: {e}")
            
    def log_message(self, message):
        """Add a message to the log."""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_status(self, message):
        """Update the status bar."""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def start_build(self):
        """Start the build process in a separate thread."""
        self.build_button.config(state="disabled")
        self.progress.start()
        self.log_text.delete(1.0, tk.END)
        self.update_status("Building...")
        
        # Start build thread
        build_thread = threading.Thread(target=self.build_process)
        build_thread.daemon = True
        build_thread.start()
        
        # Start message processing
        self.process_messages()
        
    def build_process(self):
        """The actual build process."""
        try:
            # Install dependencies
            self.message_queue.put(("log", "Installing build dependencies..."))
            self.message_queue.put(("status", "Installing dependencies..."))
            
            build_deps = ["cx_Freeze", "pyinstaller", "pyinstaller-hooks-contrib"]
            for dep in build_deps:
                try:
                    self.message_queue.put(("log", f"Installing {dep}..."))
                    subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                                 check=True, capture_output=True, text=True)
                    self.message_queue.put(("log", f"✓ Installed {dep}"))
                except subprocess.CalledProcessError as e:
                    self.message_queue.put(("log", f"✗ Failed to install {dep}: {e}"))
                    
            # Build executable
            self.message_queue.put(("log", "Building executable..."))
            self.message_queue.put(("status", "Building executable..."))
            
            build_method = self.build_method.get()
            success = False
            
            if build_method == "cx_Freeze" or build_method == "Auto-detect":
                try:
                    self.message_queue.put(("log", "Trying cx_Freeze..."))
                    subprocess.run([sys.executable, "setup.py", "build"], 
                                 check=True, capture_output=True, text=True)
                    self.message_queue.put(("log", "✓ cx_Freeze build completed"))
                    success = True
                except subprocess.CalledProcessError as e:
                    self.message_queue.put(("log", f"✗ cx_Freeze failed: {e}"))
                    
            if not success and (build_method == "PyInstaller" or build_method == "Auto-detect"):
                try:
                    self.message_queue.put(("log", "Trying PyInstaller..."))
                    subprocess.run([sys.executable, "-m", "PyInstaller", 
                                  "--onefile", "--windowed", "--name", "Talinda_POS", 
                                  "src/main.py"], check=True, capture_output=True, text=True)
                    self.message_queue.put(("log", "✓ PyInstaller build completed"))
                    success = True
                except subprocess.CalledProcessError as e:
                    self.message_queue.put(("log", f"✗ PyInstaller failed: {e}"))
                    
            if not success:
                self.message_queue.put(("log", "✗ All build methods failed"))
                self.message_queue.put(("status", "Build failed"))
                self.message_queue.put(("done", None))
                return
                
            # Create installer if requested
            if self.create_installer.get():
                self.message_queue.put(("log", "Creating installer..."))
                self.message_queue.put(("status", "Creating installer..."))
                
                try:
                    cmd = [sys.executable, "build_installer.py"]
                    if not self.create_portable.get():
                        cmd.append("--no-portable")
                    subprocess.run(cmd, check=True, capture_output=True, text=True)
                    self.message_queue.put(("log", "✓ Installer created successfully"))
                except subprocess.CalledProcessError as e:
                    self.message_queue.put(("log", f"⚠ Installer creation failed: {e}"))
                    
            # Create portable package if requested
            if self.create_portable.get():
                self.message_queue.put(("log", "Creating portable package..."))
                self.message_queue.put(("status", "Creating portable package..."))
                
                try:
                    cmd = [sys.executable, "build_installer.py"]
                    if not self.create_installer.get():
                        cmd.append("--no-installer")
                    subprocess.run(cmd, check=True, capture_output=True, text=True)
                    self.message_queue.put(("log", "✓ Portable package created successfully"))
                except subprocess.CalledProcessError as e:
                    self.message_queue.put(("log", f"⚠ Portable package creation failed: {e}"))
                    
            self.message_queue.put(("log", "Build completed successfully!"))
            self.message_queue.put(("status", "Build completed"))
            
        except Exception as e:
            self.message_queue.put(("log", f"ERROR: {e}"))
            self.message_queue.put(("status", "Build failed"))
            
        finally:
            self.message_queue.put(("done", None))
            
    def process_messages(self):
        """Process messages from the build thread."""
        try:
            while True:
                try:
                    msg_type, message = self.message_queue.get_nowait()
                    
                    if msg_type == "log":
                        self.log_message(message)
                    elif msg_type == "status":
                        self.update_status(message)
                    elif msg_type == "done":
                        self.progress.stop()
                        self.build_button.config(state="normal")
                        if message is None:
                            messagebox.showinfo("Build Complete", 
                                              "Build process completed successfully!")
                        return
                        
                except queue.Empty:
                    break
                    
        except Exception as e:
            self.log_message(f"Error processing messages: {e}")
            
        # Schedule next check
        self.root.after(100, self.process_messages)
        
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()


def main():
    """Main entry point."""
    app = InstallerBuilderGUI()
    app.run()


if __name__ == "__main__":
    main() 