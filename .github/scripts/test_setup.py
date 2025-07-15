#!/usr/bin/env python3
"""
Test script to verify the shared library version alert system.
This script simulates the workflow locally for testing purposes.
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Test shared libraries (same as in the real script)
SHARED_LIBRARIES = [
    "Util",           # CL_Util
    "common",         # Clpss_Common
    "occupancy",      # Clpss_Occupancy
    "fire-rating",    # FireRating
    "csm",            # CSM
    "rating",         # Clpss_RateCLPolicy
    "compose-print"   # Clpss_ComposePrint
]

def test_pom_parsing():
    """Test if pom.xml can be parsed correctly"""
    pom_path = Path('pom.xml')
    
    if not pom_path.exists():
        print("❌ pom.xml not found in current directory")
        return False
    
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
        print("✅ pom.xml parsed successfully")
        
        # Check namespace
        ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
        dependencies = root.findall('.//m:dependency', ns)
        print(f"✅ Found {len(dependencies)} dependencies")
        
        # Check for shared libraries
        found_libs = []
        for dep in dependencies:
            artifact_id = dep.find('m:artifactId', ns)
            version = dep.find('m:version', ns)
            if artifact_id is not None and version is not None:
                aid = artifact_id.text.strip()
                if aid in SHARED_LIBRARIES:
                    found_libs.append((aid, version.text.strip()))
        
        print(f"✅ Found {len(found_libs)} shared libraries:")
        for lib, version in found_libs:
            print(f"   - {lib}: {version}")
        
        if not found_libs:
            print("⚠️  No shared libraries found in pom.xml")
            print("   Make sure the library names match exactly:")
            for lib in SHARED_LIBRARIES:
                print(f"   - {lib}")
        
        return True
        
    except ET.ParseError as e:
        print(f"❌ Error parsing pom.xml: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_workflow_files():
    """Test if workflow files exist and are properly configured"""
    workflow_path = Path('.github/workflows/shared-libs.yml')
    
    if not workflow_path.exists():
        print("❌ Workflow file not found: .github/workflows/shared-libs.yml")
        return False
    
    print("✅ Workflow file exists")
    
    # Check scripts
    scripts = [
        '.github/scripts/check_version_changes.py',
        '.github/scripts/compare_shared_lib_versions.py',
        '.github/scripts/check_shared_lib_versions.py'
    ]
    
    for script in scripts:
        script_path = Path(script)
        if script_path.exists():
            print(f"✅ Script exists: {script}")
        else:
            print(f"❌ Script missing: {script}")
            return False
    
    return True

def test_git_setup():
    """Test git configuration for the workflow"""
    import subprocess
    
    try:
        # Check if in git repo
        result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Not in a git repository")
            return False
        
        print("✅ Git repository detected")
        
        # Check current branch
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            branch = result.stdout.strip()
            print(f"✅ Current branch: {branch}")
        
        # Check if there are commits
        result = subprocess.run(['git', 'log', '--oneline', '-1'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git history available")
        else:
            print("⚠️  No git history found")
        
        return True
        
    except FileNotFoundError:
        print("❌ Git not available")
        return False
    except Exception as e:
        print(f"❌ Git error: {e}")
        return False

def main():
    """Run all tests"""
    print("🔧 Testing Shared Library Version Alert System")
    print("=" * 50)
    
    tests = [
        ("Parsing pom.xml", test_pom_parsing),
        ("Workflow files", test_workflow_files),
        ("Git setup", test_git_setup)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system should work correctly.")
    else:
        print("⚠️  Some tests failed. Please fix the issues before using the system.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
