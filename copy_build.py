# copy_build.py
import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Create static directory if it doesn't exist
static_dir = os.path.join(BASE_DIR, 'static')
os.makedirs(static_dir, exist_ok=True)

# Source directory
source_dir = os.path.join(BASE_DIR, 'bingo-frontend', 'build')

# Check if source directory exists
if os.path.exists(source_dir):
    print(f"Copying files from {source_dir} to {static_dir}...")
    
    # Copy static directory
    source_static = os.path.join(source_dir, 'static')
    if os.path.exists(source_static):
        for item in os.listdir(source_static):
            source_item = os.path.join(source_static, item)
            dest_item = os.path.join(static_dir, item)
            
            if os.path.isdir(source_item):
                shutil.copytree(source_item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy2(source_item, dest_item)
    
    # Copy index.html to templates
    templates_dir = os.path.join(BASE_DIR, 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    source_index = os.path.join(source_dir, 'index.html')
    if os.path.exists(source_index):
        shutil.copy2(source_index, os.path.join(templates_dir, 'index.html'))
    
    print("Copy complete!")
else:
    print(f"Source directory {source_dir} does not exist.")
