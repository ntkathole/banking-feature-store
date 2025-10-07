#!/usr/bin/env python3
"""
Script to apply RBAC permissions to the banking feature store

This script applies all defined permissions to the feature store registry.
Run this after applying your feature definitions to set up access control.

Usage:
    python apply_permissions.py

Requirements:
    - Feature store must be initialized (feast apply run first)
    - Auth configuration must be set in feature_store.yaml
"""

from feast import FeatureStore
from feature_repo.permissions import (
    # Global permissions (all users)
    project_access_all_users,
    
    # Data Scientists permissions
    data_scientist_feature_views,
    data_scientist_feature_services,
    data_scientist_entities,
    
    # Data Engineers permissions
    data_engineer_feature_views,
    data_engineer_feature_services,
    data_engineer_entities,
    data_engineer_data_sources,
    
    # Analytics Team permissions
    analytics_customer_feature_views,
    analytics_transaction_feature_views,
    analytics_customer_feature_services,
    analytics_transaction_feature_services,
    analytics_customer_entity,
    analytics_transaction_entity,
    
    # Customer Engagement Team permissions
    engagement_branch_feature_views,
    engagement_atm_feature_views,
    engagement_call_center_feature_views,
    engagement_branch_feature_services,
    engagement_atm_feature_services,
    engagement_call_center_feature_services,
    engagement_entities,
)

def main():
    """Apply all permissions to the feature store"""
    
    print("Initializing Feature Store...")
    store = FeatureStore(repo_path="feature_repo")
    
    print("\nApplying RBAC permissions...")
    
    # Collect all permissions
    all_permissions = [
        # Global permissions (all users)
        project_access_all_users,
        
        # Data Scientists group
        data_scientist_feature_views,
        data_scientist_feature_services,
        data_scientist_entities,
        
        # Data Engineers group
        data_engineer_feature_views,
        data_engineer_feature_services,
        data_engineer_entities,
        data_engineer_data_sources,
        
        # Analytics Team group
        analytics_customer_feature_views,
        analytics_transaction_feature_views,
        analytics_customer_feature_services,
        analytics_transaction_feature_services,
        analytics_customer_entity,
        analytics_transaction_entity,
        
        # Customer Engagement Team group
        engagement_branch_feature_views,
        engagement_atm_feature_views,
        engagement_call_center_feature_views,
        engagement_branch_feature_services,
        engagement_atm_feature_services,
        engagement_call_center_feature_services,
        engagement_entities,
    ]
    
    # Apply permissions
    try:
        store.apply(all_permissions)
        print(f"\n✓ Successfully applied {len(all_permissions)} permissions!")
        
        # List current permissions
        print("\n" + "="*80)
        print("Current Permissions in Registry:")
        print("="*80)
        
        permissions = store.list_permissions()
        if permissions:
            for i, perm in enumerate(permissions, 1):
                print(f"\n{i}. {perm.name}")
                print(f"   Types: {[t.__name__ for t in perm.types]}")
                print(f"   Actions: {[a.value for a in perm.actions]}")
                print(f"   Policy: {perm.policy}")
                if perm.name_patterns:
                    print(f"   Name Patterns: {perm.name_patterns}")
                if perm.required_tags:
                    print(f"   Required Tags: {perm.required_tags}")
        else:
            print("No permissions found in registry.")
        
        print("\n" + "="*80)
        print("\nPermission Groups:")
        print("="*80)
        print("1. data_scientist        - Read access to features, entities, services (NO data sources)")
        print("2. data_engineer         - Full CRUD access to all resources (EXCEPT permissions)")
        print("3. analytics_team        - Read access to customer & transaction features/services")
        print("4. customer_engagement_team - Read access to branch, ATM & call center features/services")
        
        print("\n" + "="*80)
        print("Next Steps:")
        print("="*80)
        print("1. Configure authentication in feature_store.yaml (OIDC or Kubernetes)")
        print("2. Assign appropriate roles to users in your identity provider")
        print("3. Test access with different user roles")
        print("4. Use 'feast permissions describe' to validate permissions")
        
    except Exception as e:
        print(f"\n✗ Error applying permissions: {str(e)}")
        print("\nTroubleshooting:")
        print("- Ensure you've run 'feast apply' first to register features")
        print("- Check that auth is configured in feature_store.yaml")
        print("- Verify you have permission to modify the registry")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
