import os
import sys
import xml.etree.ElementTree as ET
import subprocess

SHARED_LIBRARIES = [
    "Util",
    "common",
    "occupancy",
    "fire-rating",
    "csm",
    "rating",
    "compose-print"
]

def get_pom_lib_versions(pom_path):
    tree = ET.parse(pom_path)
    root = tree.getroot()
    ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
    versions = {}
    for dep in root.findall(".//m:dependency", ns):
        artifact_id = dep.find("m:artifactId", ns)
        version = dep.find("m:version", ns)
        if artifact_id is not None and version is not None:
            aid = artifact_id.text.strip()
            if aid in SHARED_LIBRARIES:
                versions[aid] = version.text.strip()
    return versions

def get_base_and_head_files():
    # Get the base and head commit SHAs
    result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True)
    head_sha = result.stdout.strip()
    result = subprocess.run(['git', 'rev-parse', 'origin/' + os.environ.get('GITHUB_BASE_REF', 'main')], capture_output=True, text=True)
    base_sha = result.stdout.strip()
    return base_sha, head_sha

def main():
    # Get the diff of pom.xml in this PR
    result = subprocess.run(['git', 'diff', 'origin/' + os.environ.get('GITHUB_BASE_REF', 'main'), 'pom.xml'], capture_output=True, text=True)
    diff = result.stdout
    changed = False
    for lib in SHARED_LIBRARIES:
        if f"<artifactId>{lib}</artifactId>" in diff and "<version>" in diff:
            print(f"LIB_VERSION_CHANGED: {lib}")
            changed = True
    if changed:
        print("LIB_VERSION_CHANGED")
    else:
        print("NO_VERSION_CHANGE")

if __name__ == "__main__":
    main()
