#!/usr/bin/env python3
import os
import yaml
import sys
from pathlib import Path

# DataEngOS v2.0 Gatekeeper
# Enforces:
# 1. Existence of ODCS Contracts for every project.
# 2. Presence of 'owner' in contracts.
# 3. Security Plan if PII is detected (simulated check).

PROJECTS_DIR = Path("projects")
GOVERNANCE_FILE = Path("core/global_governance/classification.yaml")

def load_yaml(path):
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

def check_project(project_path):
    print(f"Checking project: {project_path.name}")
    errors = []
    
    # Check 1: Contracts Existence
    contracts_dir = project_path / "contracts"
    if not contracts_dir.exists():
        errors.append("Missing 'contracts' directory.")
    else:
        # Check 2: Contract Validity (Owner)
        has_contracts = False
        for contract_file in contracts_dir.rglob("*.yaml"):
            has_contracts = True
            data = load_yaml(contract_file)
            if not data:
                continue
                
            # Check 2: Contract Validity (Owner)
            # Support both ODCS v2.x (spec.dataset.owners) and v3/Simple (metadata.owner)
            owner_found = False
            
            # Check v2.x format
            if 'spec' in data and 'dataset' in data['spec'] and 'owners' in data['spec']['dataset']:
                owners = data['spec']['dataset']['owners']
                if isinstance(owners, list) and len(owners) > 0:
                    owner_found = True
            
            # Check Simple/v3 format fallback
            if not owner_found and 'metadata' in data and 'owner' in data['metadata']:
                owner_found = True
                
            if not owner_found:
                errors.append(f"Contract {contract_file.name} missing 'spec.dataset.owners' or 'metadata.owner'.")
        
        if not has_contracts:
            errors.append("No contracts found in 'contracts' directory.")

    # Check 3: Security Plan (Basic existence check for v2)
    security_plan = project_path / "security_privacy" / "project_plan.yaml"
    if not security_plan.exists():
        # Ideally check if PII is actually used, but for v2 strictness we demand the plan folder
        errors.append("Missing 'security_privacy/project_plan.yaml'.")

    return errors

def main():
    if not PROJECTS_DIR.exists():
        print("Projects directory not found.")
        sys.exit(1)

    all_errors = {}
    for project in PROJECTS_DIR.iterdir():
        if project.is_dir() and project.name not in ["__pycache__", ".git"]:
            # Skip non-project dirs if any, strictly checking formatted dirs
            if not (project / "dbt").exists() and not (project / "contracts").exists():
                 # likely not a project
                 continue
            
            errs = check_project(project)
            if errs:
                all_errors[project.name] = errs

    if all_errors:
        print("\n=== GATEKEEPER FAILED ===")
        for p, errs in all_errors.items():
            print(f"\nProject: {p}")
            for e in errs:
                print(f"  - {e}")
        sys.exit(1)
    else:
        print("\n=== GATEKEEPER PASSED ===")
        sys.exit(0)

if __name__ == "__main__":
    main()
