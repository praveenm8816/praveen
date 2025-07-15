import os
import xml.etree.ElementTree as ET
from pathlib import Path

# List of repo paths (relative to this script's location)
REPOS = [
    Path("cl-clpss/pom.xml"),  # current repo
    Path("cl-ccl1/pom.xml"),
    Path("cl-jobserver/ivy.xml"),
    Path("cl-jobschedular/ivy.xml"),
]

# List of shared library artifactIds to check
SHARED_LIBS = [
    "Util",           # CL_Util
    "common",         # Clpss_Common
    "occupancy",      # Clpss_Occupancy
    "fire-rating",    # FireRating
    "csm",            # CSM
    "rating",         # Clpss_RateCLPolicy
    "compose-print",  # Clpss_ComposePrint
]

def get_versions(file_path):
    """Get versions from either pom.xml or ivy.xml files"""
    versions = {}
    if not file_path.exists():
        return versions
    
    if file_path.name == "pom.xml":
        return get_pom_versions(file_path)
    elif file_path.name == "ivy.xml":
        return get_ivy_versions(file_path)
    
    return versions

def get_pom_versions(pom_path):
    """Parse Maven pom.xml file for dependency versions"""
    versions = {}
    tree = ET.parse(pom_path)
    root = tree.getroot()
    ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
    
    for dep in root.findall('.//m:dependency', ns):
        artifact = dep.find('m:artifactId', ns)
        version = dep.find('m:version', ns)
        if artifact is not None and version is not None and artifact.text in SHARED_LIBS:
            versions[artifact.text] = version.text
    return versions

def get_ivy_versions(ivy_path):
    """Parse Ivy ivy.xml file for dependency versions"""
    versions = {}
    tree = ET.parse(ivy_path)
    root = tree.getroot()
    
    for dep in root.findall('.//dependency'):
        name = dep.attrib.get('name')
        rev = dep.attrib.get('rev')
        if name in SHARED_LIBS and rev:
            versions[name] = rev
    return versions

def main():
    all_versions = {}
    for repo_file in REPOS:
        repo_name = repo_file.parts[-2] if len(repo_file.parts) > 1 else "main"
        all_versions[repo_name] = get_versions(repo_file)

    mismatches = []
    for lib in SHARED_LIBS:
        lib_versions = {repo: vers.get(lib) for repo, vers in all_versions.items() if lib in vers}
        if len(set(lib_versions.values())) > 1:
            mismatches.append((lib, lib_versions))

    if mismatches:
        print("LIB_VERSION_MISMATCH")
        for lib, vers in mismatches:
            print(f"Mismatch for {lib}:")
            for repo, v in vers.items():
                print(f"  {repo}: {v}")
        return 1
    else:
        print("All shared library versions are aligned.")
        return 0

if __name__ == "__main__":
    main()
