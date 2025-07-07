import os
import sys
import xml.etree.ElementTree as ET
import subprocess
from pathlib import Path

SHARED_LIBRARIES = [
    "Cl_Util",
    "Clpss_Common",
    "Clpss_Occupancy",
    "FireRating",
    "CSM",
    "Clpss_RateCLpolicy",
    "Clpss_ComposePrint"
]

# Helper to parse Maven pom.xml
def get_pom_lib_versions(pom_path):
    versions = {}
    if not Path(pom_path).exists():
        return versions
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
    return versions

# Helper to parse Ivy ivy.xml
def get_ivy_lib_versions(ivy_path):
    versions = {}
    if not Path(ivy_path).exists():
        return versions
    tree = ET.parse(ivy_path)
    root = tree.getroot()
    for dep in root.findall('.//dependency'):
        name = dep.attrib.get('name')
        rev = dep.attrib.get('rev')
        if name in SHARED_LIBRARIES and rev:
            versions[name] = rev
    return versions

def main():
    # Example paths (adjust as needed)
    repos = {
        'cl-clpss': {'type': 'maven', 'file': 'cl-clpss/pom.xml'},
        'cl-ccl1': {'type': 'maven', 'file': 'cl-ccl1/pom.xml'},
        'jobserver': {'type': 'ivy', 'file': 'jobserver/ivy.xml'},
        'jobschedular': {'type': 'ivy', 'file': 'jobschedular/ivy.xml'},
    }
    all_versions = {}
    for repo, info in repos.items():
        if info['type'] == 'maven':
            all_versions[repo] = get_pom_lib_versions(info['file'])
        elif info['type'] == 'ivy':
            all_versions[repo] = get_ivy_lib_versions(info['file'])

    mismatches = []
    for lib in SHARED_LIBRARIES:
        lib_versions = {repo: vers.get(lib) for repo, vers in all_versions.items() if lib in vers}
        if len(set(lib_versions.values())) > 1:
            mismatches.append((lib, lib_versions))

    if mismatches:
        print("LIB_VERSION_MISMATCH")
        for lib, vers in mismatches:
            print(f"Mismatch for {lib}:")
            for repo, v in vers.items():
                print(f"  {repo}: {v}")
    else:
        print("All shared library versions are aligned.")

if __name__ == "__main__":
    main()
