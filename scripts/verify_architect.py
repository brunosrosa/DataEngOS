import sys
import os

# Add project root to sys.path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from dataeng_os.ui.architect import architect

print("--- Verifying Catalog Indexing ---")
architect._index_catalog()
print(f"Contracts found: {len(architect.catalog_index)}")
for name, meta in architect.catalog_index.items():
    print(f" - {name}: {meta['domain']}")

print("\n--- Verifying Context Injection ---")
context = architect._get_catalog_context()
print("Context Summary:")
print(context[:500] + "..." if len(context) > 500 else context)

if len(architect.catalog_index) == 0:
    print("\n[WARN] No contracts found. Please ensure 'projects/**/contracts/**/*.yaml' exists for full test.")
else:
    print("\n[SUCCESS] Indexing working.")
