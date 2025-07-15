#!/usr/bin/env python3
"""
Demo script to simulate a version change and show how the alert system works.
This creates a test scenario where a shared library version changes.
"""

import sys
import tempfile
import shutil
from pathlib import Path
import xml.etree.ElementTree as ET

def create_demo_scenario():
    """Create a demo scenario with version changes"""
    
    print("🎬 Demo: Shared Library Version Change Alert")
    print("=" * 50)
    
    # Read current pom.xml
    pom_path = Path('pom.xml')
    if not pom_path.exists():
        print("❌ pom.xml not found")
        return
    
    # Parse current pom.xml
    tree = ET.parse(pom_path)
    root = tree.getroot()
    ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
    
    print("📋 Current versions:")
    dependencies = root.findall('.//m:dependency', ns)
    for dep in dependencies:
        artifact_id = dep.find('m:artifactId', ns)
        version = dep.find('m:version', ns)
        if artifact_id is not None and version is not None:
            print(f"  - {artifact_id.text}: {version.text}")
    
    print("\n🔄 Simulating version change...")
    print("   Changing 'common' from 3.0.5 to 3.1.0")
    print("   Changing 'fire-rating' from 4.2.0 to 4.3.0")
    
    # Create modified version
    for dep in dependencies:
        artifact_id = dep.find('m:artifactId', ns)
        version = dep.find('m:version', ns)
        if artifact_id is not None and version is not None:
            if artifact_id.text == 'common':
                version.text = '3.1.0'
            elif artifact_id.text == 'fire-rating':
                version.text = '4.3.0'
    
    # Save modified pom.xml to temporary file
    temp_pom = tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False)
    tree.write(temp_pom.name, encoding='utf-8', xml_declaration=True)
    temp_pom.close()
    
    print(f"\n📝 Modified pom.xml saved to: {temp_pom.name}")
    
    # Show what the notification would look like
    print("\n📧 This would trigger the following notification:")
    print("=" * 50)
    
    notification = """🚨 **Shared Library Version Changes Detected** 🚨

The following shared libraries have been updated in `pom.xml`:

• **common**: `3.0.5` → `3.1.0`
• **fire-rating**: `4.2.0` → `4.3.0`

⚠️ **Action Required:**
Please ensure you also update the corresponding versions in:
- **cl-ccl1** (pom.xml)
- **cl-jobserver** (ivy.xml)
- **cl-jobschedular** (ivy.xml)

Keeping these aligned prevents runtime incompatibilities.
Thank you for keeping our dependencies in sync! 🙏

---
*This is an automated notification from the CI/CD pipeline.*"""
    
    print(notification)
    
    print("\n📨 Email would be sent to:")
    print("  - madanipyla@gmail.com")
    print("  - Other configured team members")
    
    print("\n💬 Teams notification would be posted to configured channels")
    
    # Cleanup
    Path(temp_pom.name).unlink()
    
    print("\n✅ Demo completed successfully!")
    print("\n💡 To test in real scenario:")
    print("   1. Create a new branch")
    print("   2. Modify versions in pom.xml")
    print("   3. Create a Pull Request")
    print("   4. The workflow will automatically detect changes and notify")

if __name__ == "__main__":
    create_demo_scenario()
