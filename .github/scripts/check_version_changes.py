#!/usr/bin/env python3
"""
Script to check for shared library version changes in PR and send notifications.
This script is designed to run in GitHub Actions CI/CD pipeline.
"""

import os
import sys
import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Optional

SHARED_LIBRARIES = [
    "Util",           # CL_Util
    "common",         # Clpss_Common
    "occupancy",      # Clpss_Occupancy
    "fire-rating",    # FireRating
    "csm",            # CSM
    "rating",         # Clpss_RateCLPolicy
    "compose-print"   # Clpss_ComposePrint
]

def get_pom_versions(pom_path: Path) -> Dict[str, str]:
    """Parse Maven pom.xml file for dependency versions"""
    versions = {}
    if not pom_path.exists():
        return versions
    
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
        ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
        
        for dep in root.findall('.//m:dependency', ns):
            artifact_id = dep.find('m:artifactId', ns)
            version = dep.find('m:version', ns)
            if artifact_id is not None and version is not None:
                aid = artifact_id.text.strip()
                if aid in SHARED_LIBRARIES:
                    versions[aid] = version.text.strip()
    except ET.ParseError as e:
        print(f"Error parsing {pom_path}: {e}")
    
    return versions

def get_changed_libraries() -> List[Tuple[str, str, str]]:
    """
    Compare current branch with base branch to find changed shared libraries.
    Returns list of (library_name, old_version, new_version) tuples.
    """
    changed_libs = []
    
    # Get current versions
    current_versions = get_pom_versions(Path('pom.xml'))
    
    # Get base branch versions
    base_ref = os.environ.get('GITHUB_BASE_REF', 'main')
    try:
        # Checkout base branch temporarily
        subprocess.run(['git', 'checkout', f'origin/{base_ref}', '--', 'pom.xml'], 
                      check=True, capture_output=True)
        
        base_versions = get_pom_versions(Path('pom.xml'))
        
        # Restore current pom.xml
        subprocess.run(['git', 'checkout', 'HEAD', '--', 'pom.xml'], 
                      check=True, capture_output=True)
        
        # Find changes
        for lib in SHARED_LIBRARIES:
            current_ver = current_versions.get(lib)
            base_ver = base_versions.get(lib)
            
            if current_ver and base_ver and current_ver != base_ver:
                changed_libs.append((lib, base_ver, current_ver))
            elif current_ver and not base_ver:
                changed_libs.append((lib, "NOT_FOUND", current_ver))
            elif not current_ver and base_ver:
                changed_libs.append((lib, base_ver, "REMOVED"))
                
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")
    
    return changed_libs

def generate_notification_message(changed_libs: List[Tuple[str, str, str]]) -> str:
    """Generate notification message for changed libraries"""
    message = "🚨 **Shared Library Version Changes Detected** 🚨\n\n"
    message += "The following shared libraries have been updated in `pom.xml`:\n\n"
    
    for lib, old_ver, new_ver in changed_libs:
        message += f"• **{lib}**: `{old_ver}` → `{new_ver}`\n"
    
    message += "\n⚠️ **Action Required:**\n"
    message += "Please ensure you also update the corresponding versions in:\n"
    message += "- **cl-ccl1** (pom.xml)\n"
    message += "- **cl-jobserver** (ivy.xml)\n"
    message += "- **cl-jobschedular** (ivy.xml)\n\n"
    message += "Keeping these aligned prevents runtime incompatibilities.\n"
    message += "Thank you for keeping our dependencies in sync! 🙏\n\n"
    message += "---\n"
    message += "*This is an automated notification from the CI/CD pipeline.*"
    
    return message

def generate_email_body(changed_libs: List[Tuple[str, str, str]], pr_author: str, pr_url: str) -> str:
    """Generate email body for notifications"""
    body = f"Hello Team,\n\n"
    body += f"Shared library versions have been updated in the cl-clpss repository.\n\n"
    body += f"PR Author: {pr_author}\n"
    body += f"PR URL: {pr_url}\n\n"
    body += f"Changed Libraries:\n"
    
    for lib, old_ver, new_ver in changed_libs:
        body += f"• {lib}: {old_ver} → {new_ver}\n"
    
    body += f"\nPlease update the corresponding versions in:\n"
    body += f"- cl-ccl1 (pom.xml)\n"
    body += f"- cl-jobserver (ivy.xml)\n"
    body += f"- cl-jobschedular (ivy.xml)\n\n"
    body += f"Keeping these aligned prevents runtime incompatibilities.\n\n"
    body += f"Best regards,\n"
    body += f"Automated CI/CD System"
    
    return body

def get_pr_info() -> Tuple[str, str]:
    """Get PR author and URL from GitHub environment"""
    pr_author = os.environ.get('GITHUB_ACTOR', 'Unknown')
    repo = os.environ.get('GITHUB_REPOSITORY', 'unknown/unknown')
    pr_number = os.environ.get('GITHUB_PR_NUMBER', '0')
    pr_url = f"https://github.com/{repo}/pull/{pr_number}"
    
    return pr_author, pr_url

def main():
    """Main function to check for changes and output results"""
    changed_libs = get_changed_libraries()
    
    if not changed_libs:
        print("No shared library version changes detected.")
        return 0
    
    print("LIB_VERSION_CHANGED")
    print(f"Found {len(changed_libs)} changed libraries:")
    
    for lib, old_ver, new_ver in changed_libs:
        print(f"  {lib}: {old_ver} → {new_ver}")
    
    # Generate notification content
    pr_author, pr_url = get_pr_info()
    notification_message = generate_notification_message(changed_libs)
    email_body = generate_email_body(changed_libs, pr_author, pr_url)
    
    # Output for GitHub Actions
    print(f"\n--- PR Comment ---")
    print(notification_message)
    
    print(f"\n--- Email Body ---")
    print(email_body)
    
    # Set GitHub Actions outputs
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"pr_comment<<EOF\n{notification_message}\nEOF\n")
            f.write(f"email_body<<EOF\n{email_body}\nEOF\n")
    
    return 1  # Return 1 to indicate changes were found

if __name__ == "__main__":
    sys.exit(main())
