import os
import xml.etree.ElementTree as ET
from pathlib import Path

# List of repo paths (relative to this script's location)
REPOS = [
    Path("cl-clpss/pom.xml"),  # current repo
    Path("ccl1/pom.xml"),
    Path("server/ivy.xml"),
    Path("schedular/ivy.xml"),
]

# List of shared library artifactIds to check
SHARED_LIBS = [
    "shared-lib1",
    "shared-lib2",
    "shared-lib3",
    "shared-lib4",
    "shared-lib5",
    "shared-lib6",
    "shared-lib7",
]

def get_versions(pom_path):
    versions = {}
    if not pom_path.exists():
        return versions
    tree = ET.parse(pom_path)
    root = tree.getroot()
    ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
    for dep in root.findall('.//m:dependency', ns):
        artifact = dep.find('m:artifactId', ns)
        version = dep.find('m:version', ns)
        if artifact is not None and version is not None and artifact.text in SHARED_LIBS:
            versions[artifact.text] = version.text
    return versions

def main():
    all_versions = {}
    for repo_pom in REPOS:
        repo_name = repo_pom.parts[-2] if len(repo_pom.parts) > 1 else "main"
        all_versions[repo_name] = get_versions(repo_pom)

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
    else:
        print("All shared library versions are aligned.")

if __name__ == "__main__":
    main()
