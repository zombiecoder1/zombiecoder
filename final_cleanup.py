#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Final Cleanup Script for Shaon AI Advanced System
"সবকিছু clean করে দেয়, সবকিছু organize করে দেয়"
"""

import os
import shutil
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def final_cleanup():
    """Final cleanup and organization"""
    base_dir = Path("D:/Alhamdullha")
    
    logger.info("🧹 Starting Final Cleanup...")
    
    # Create organized directories
    directories = {
        "docs": ["*.md", "*.html"],
        "tests": ["test_*.py", "TEST_*.py", "*_test.py"],
        "tools": ["fix_*.py", "optimize_*.py", "quick_*.py", "create_*.py"],
        "config": ["*.json", "*.config", "requirements.txt"],
        "backup": ["*.zip", "backup_*.json", "RESTORATION_*.md"],
        "logs": ["*.log"]
    }
    
    # Keep important files in root
    important_files = [
        "README.md", "SYSTEM_DOCUMENTATION.md", "GLOBAL_LAUNCHER.bat",
        "power-switch.bat", "optimized_port_routing.py", "final_solution.py",
        "run.py", ".gitignore", "optimize_everything.py", "final_cleanup.py"
    ]
    
    # Organize files
    for dir_name, patterns in directories.items():
        dir_path = base_dir / dir_name
        dir_path.mkdir(exist_ok=True)
        
        moved_files = 0
        for pattern in patterns:
            for file_path in base_dir.glob(pattern):
                if file_path.is_file() and file_path.parent == base_dir:
                    # Skip important files
                    if file_path.name in important_files:
                        continue
                        
                    try:
                        shutil.move(str(file_path), str(dir_path / file_path.name))
                        moved_files += 1
                        logger.info(f"📁 Moved: {file_path.name} -> {dir_name}/")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not move {file_path.name}: {e}")
                        
        logger.info(f"📁 {dir_name}: {moved_files} files organized")
    
    # Remove unnecessary files
    unnecessary_files = [
        "tatus",  # Corrupted file
        "*.tmp",
        "*.bak"
    ]
    
    removed_files = 0
    for pattern in unnecessary_files:
        for file_path in base_dir.glob(pattern):
            if file_path.is_file() and file_path.parent == base_dir:
                try:
                    file_path.unlink()
                    removed_files += 1
                    logger.info(f"🗑️ Removed: {file_path.name}")
                except Exception as e:
                    logger.warning(f"⚠️ Could not remove {file_path.name}: {e}")
    
    logger.info(f"🗑️ Removed {removed_files} unnecessary files")
    
    # Create final structure report
    create_structure_report(base_dir)
    
    logger.info("🎉 Final Cleanup Complete!")
    
def create_structure_report(base_dir):
    """Create final directory structure report"""
    report_content = """# 📁 Final Directory Structure

## 🎯 Root Directory (Important Files)
"""
    
    important_files = [
        "README.md", "SYSTEM_DOCUMENTATION.md", "GLOBAL_LAUNCHER.bat",
        "power-switch.bat", "optimized_port_routing.py", "final_solution.py",
        "run.py", ".gitignore", "optimize_everything.py", "final_cleanup.py"
    ]
    
    for file_name in important_files:
        file_path = base_dir / file_name
        if file_path.exists():
            report_content += f"- ✅ {file_name}\n"
        else:
            report_content += f"- ❌ {file_name} (missing)\n"
    
    report_content += """
## 📂 Organized Directories

### 📚 docs/
- Documentation files (.md, .html)

### 🧪 tests/
- Test files (test_*.py, *_test.py)

### 🔧 tools/
- Utility scripts (fix_*.py, optimize_*.py, quick_*.py)

### ⚙️ config/
- Configuration files (.json, .config, requirements.txt)

### 💾 backup/
- Backup files (.zip, backup_*.json)

### 📋 logs/
- Log files (.log)

## 🎉 Clean and Organized!

The directory is now properly organized and optimized.
"""
    
    report_path = base_dir / "FINAL_STRUCTURE_REPORT.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    logger.info(f"📋 Structure report saved to: {report_path}")

if __name__ == "__main__":
    final_cleanup()
