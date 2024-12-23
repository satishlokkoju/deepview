#!/usr/bin/env python3

import os
import re
from pathlib import Path

BETTERWITHDATA_LICENSE = '''#
# Copyright 2024 BetterWithData
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This file contains code that is part of Apple's DNIKit project, licensed
# under the Apache License, Version 2.0:
#'''

def update_file_header(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file already has Apple's copyright notice
    if "Copyright" in content and "Apple Inc." in content:
        # Find the start of the Apple copyright notice
        apple_start = content.find("# Copyright")
        if apple_start == -1:
            return False
        
        # Don't modify if BetterWithData license is already present
        if "BetterWithData" in content:
            return False
        
        # Insert the new license before Apple's
        new_content = content[:apple_start] + BETTERWITHDATA_LICENSE + "\n" + content[apple_start:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    project_root = Path(__file__).parent.parent
    source_dirs = [
        project_root / "src/deepview",
        # Excluding deepview_canvas as requested
        project_root / "src/deepview_tensorflow",
        project_root / "src/deepview_torch"
    ]
    
    python_files = []
    for source_dir in source_dirs:
        if source_dir.exists():
            print(f"Processing directory: {source_dir}")
            for root, _, files in os.walk(source_dir):
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(os.path.join(root, file))
    
    updated_count = 0
    for file_path in python_files:
        if update_file_header(file_path):
            print(f"Updated license header in: {file_path}")
            updated_count += 1
    
    print(f"\nUpdated {updated_count} files")

if __name__ == "__main__":
    main()
