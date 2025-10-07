"""
RBAC Permission definitions for the banking feature store
This file defines granular access control policies for different user groups

GROUP-BASED ACCESS CONTROL:
The permissions use GroupBasedPolicy with group identities from your identity provider.
- For Kubernetes: Use Kubernetes groups (e.g., system:authenticated, custom groups)
- For OIDC: Use group claims from JWT tokens (configured in IdP)

GroupBasedPolicy is the proper way to define group-based permissions in Feast.
"""
from feast import Entity, FeatureView, FeatureService, Project
from feast.data_source import DataSource
from feast.permissions.action import AuthzedAction, READ, WRITE, CRUD
from feast.permissions.permission import Permission
from feast.permissions.policy import GroupBasedPolicy
from feast.on_demand_feature_view import OnDemandFeatureView

# =============================================================================
# GLOBAL PERMISSIONS (ALL USERS)
# =============================================================================

# All authenticated users need access to Project to interact with the feature store
# Using GroupBasedPolicy for proper group-based access control
project_access_all_users = Permission(
    name="project-access-all-users",
    types=[Project],
    policy=GroupBasedPolicy(groups=[
        # Common group for all authenticated users
        "system:authenticated",  # For Kubernetes - all authenticated users
        "authenticated-users",   # For OIDC - create this group and add all users
        
        # Also include specific groups as fallback
        "data-scientists-group",
        "data-engineers-group", 
        "analytics-team-group",
        "customer-engagement-team-group",
    ]),
    actions=[AuthzedAction.DESCRIBE],
)

# =============================================================================
# GROUP 1: DATA SCIENTISTS GROUP
# Access to features, feature-views, entities, and feature-services
# NO access to data sources
# Group Name: data-scientists-group
# =============================================================================

# Data Scientists Group - Read access to all Feature Views
data_scientist_feature_views = Permission(
    name="data-scientists-group-feature-views-reader",
    types=[FeatureView, OnDemandFeatureView],
    policy=GroupBasedPolicy(groups=["data-scientists-group"]),
    actions=[AuthzedAction.DESCRIBE, *READ],
)

# Data Scientists Group - Read access to all Feature Services
data_scientist_feature_services = Permission(
    name="data-scientists-group-feature-services-reader",
    types=[FeatureService],
    policy=GroupBasedPolicy(groups=["data-scientists-group"]),
    actions=[AuthzedAction.DESCRIBE, *READ],
)

# Data Scientists Group - Read access to all Entities
data_scientist_entities = Permission(
    name="data-scientists-group-entities-reader",
    types=[Entity],
    policy=GroupBasedPolicy(groups=["data-scientists-group"]),
    actions=[AuthzedAction.DESCRIBE],
)

# Data Scientists Group - Explicitly DENY access to Data Sources
# Note: In Feast RBAC, not defining a permission for a resource type means
# users without other permissions cannot access it, so we don't need explicit deny

# =============================================================================
# GROUP 2: DATA ENGINEERS GROUP
# Access to add all resources except permissions
# Includes CRUD operations on all resources
# Group Name: data-engineers-group
# =============================================================================

# Data Engineers Group - Full CRUD access to Feature Views
data_engineer_feature_views = Permission(
    name="data-engineers-group-feature-views-manager",
    types=[FeatureView, OnDemandFeatureView],
    policy=GroupBasedPolicy(groups=["data-engineers-group"]),
    actions=[*CRUD, *READ, *WRITE],
)

# Data Engineers Group - Full CRUD access to Feature Services
data_engineer_feature_services = Permission(
    name="data-engineers-group-feature-services-manager",
    types=[FeatureService],
    policy=GroupBasedPolicy(groups=["data-engineers-group"]),
    actions=[*CRUD, *READ],
)

# Data Engineers Group - Full CRUD access to Entities
data_engineer_entities = Permission(
    name="data-engineers-group-entities-manager",
    types=[Entity],
    policy=GroupBasedPolicy(groups=["data-engineers-group"]),
    actions=[*CRUD],
)

# Data Engineers Group - Full CRUD access to Data Sources
data_engineer_data_sources = Permission(
    name="data-engineers-group-data-sources-manager",
    types=[DataSource],  # Use abstract DataSource, not FileSource
    policy=GroupBasedPolicy(groups=["data-engineers-group"]),
    actions=[*CRUD, *READ, *WRITE],
)

# Note: Data Engineers Group explicitly DO NOT have access to Permission resources
# This is controlled by not creating a permission for Permission type

# =============================================================================
# GROUP 3: ANALYTICS TEAM GROUP
# Access to only customer and transaction related features, feature-views, 
# and feature-services
# Group Name: analytics-team-group
# =============================================================================

# Analytics Team Group - Customer related Feature Views
analytics_customer_feature_views = Permission(
    name="analytics-team-group-customer-features-reader",
    types=[FeatureView, OnDemandFeatureView],
    name_patterns=[
        "customer_demographics_fv",
        "customer_behavioral_profile",
        "customer_transaction_interaction",
        "customer_profile_.*",  # Any customer profile features
    ],
    policy=GroupBasedPolicy(groups=["analytics-team-group"]),
    actions=[AuthzedAction.DESCRIBE, *READ],
)

# Analytics Team Group - Transaction related Feature Views
analytics_transaction_feature_views = Permission(
    name="analytics-team-group-transaction-features-reader",
    types=[FeatureView],
    name_patterns=[
        "transaction_7d_aggregations",
        "transaction_30d_aggregations",
        "transaction_90d_patterns",
        "transaction_details",
        "transaction_.*",  # Any transaction features
    ],
    policy=GroupBasedPolicy(groups=["analytics-team-group"]),
    actions=[AuthzedAction.DESCRIBE, *READ],
)

# Analytics Team Group - Customer related Feature Services
analytics_customer_feature_services = Permission(
    name="analytics-team-group-customer-services-reader",
    types=[FeatureService],
    name_patterns=[
        "customer_charter_service",
        "customer_behavior_service",
    ],
    policy=GroupBasedPolicy(groups=["analytics-team-group"]),
    actions=[AuthzedAction.DESCRIBE, *READ],
)

# Analytics Team Group - Transaction related Feature Services
analytics_transaction_feature_services = Permission(
    name="analytics-team-group-transaction-services-reader",
    types=[FeatureService],
    name_patterns=[
        "transaction_prediction_service",
        "risk_compliance_service",
        "simple_ondemand_risk_service",
    ],
    policy=GroupBasedPolicy(groups=["analytics-team-group"]),
    actions=[AuthzedAction.DESCRIBE, *READ],
)

# Analytics Team Group - Customer Entity access
analytics_customer_entity = Permission(
    name="analytics-team-group-customer-entity-reader",
    types=[Entity],
    name_patterns=["customer"],
    policy=GroupBasedPolicy(groups=["analytics-team-group"]),
    actions=[AuthzedAction.DESCRIBE],
)

# Analytics Team Group - Transaction Entity access
analytics_transaction_entity = Permission(
    name="analytics-team-group-transaction-entity-reader",
    types=[Entity],
    name_patterns=["transaction"],
    policy=GroupBasedPolicy(groups=["analytics-team-group"]),
    actions=[AuthzedAction.DESCRIBE],
)

# =============================================================================
# GROUP 4: CUSTOMER ENGAGEMENT TEAM GROUP
# Access to branch, ATM, and call-center features, feature-views, and 
# feature-services
# Group Name: customer-engagement-team-group
# =============================================================================

# Customer Engagement Team Group - Branch related Feature Views
engagement_branch_feature_views = Permission(
    name="customer-engagement-team-group-branch-features-reader",
    types=[FeatureView],
    name_patterns=[
        "branch_visits_90d",
        "branch_service_preferences",
        "branch_performance",
        "customer_branch_interaction",
        "branch_.*",  # Any branch features
    ],
    policy=GroupBasedPolicy(groups=["customer-engagement-team-group"]),
    actions=[AuthzedAction.DESCRIBE, *READ],
)

# Customer Engagement Team Group - ATM related Feature Views
engagement_atm_feature_views = Permission(
    name="customer-engagement-team-group-atm-features-reader",
    types=[FeatureView],
    name_patterns=[
        "atm_usage_30d",
        "atm_time_patterns",
        "atm_location_performance",
        "customer_atm_interaction",
        "atm_.*",  # Any ATM features
    ],
    policy=GroupBasedPolicy(groups=["customer-engagement-team-group"]),
    actions=[AuthzedAction.DESCRIBE, *READ],
)

# Customer Engagement Team Group - Call Center related Feature Views
engagement_call_center_feature_views = Permission(
    name="customer-engagement-team-group-call-center-features-reader",
    types=[FeatureView],
    name_patterns=[
        "call_center_90d",
        "call_center_predictive",
        "call_.*",  # Any call center features
    ],
    policy=GroupBasedPolicy(groups=["customer-engagement-team-group"]),
    actions=[AuthzedAction.DESCRIBE, *READ],
)

# Customer Engagement Team Group - Branch related Feature Services
engagement_branch_feature_services = Permission(
    name="customer-engagement-team-group-branch-services-reader",
    types=[FeatureService],
    name_patterns=[
        "branch_optimization_service",
    ],
    policy=GroupBasedPolicy(groups=["customer-engagement-team-group"]),
    actions=[AuthzedAction.DESCRIBE, *READ],
)

# Customer Engagement Team Group - ATM related Feature Services
engagement_atm_feature_services = Permission(
    name="customer-engagement-team-group-atm-services-reader",
    types=[FeatureService],
    name_patterns=[
        "atm_optimization_service",
    ],
    policy=GroupBasedPolicy(groups=["customer-engagement-team-group"]),
    actions=[AuthzedAction.DESCRIBE, *READ],
)

# Customer Engagement Team Group - Call Center related Feature Services
engagement_call_center_feature_services = Permission(
    name="customer-engagement-team-group-call-center-services-reader",
    types=[FeatureService],
    name_patterns=[
        "call_prediction_service",
    ],
    policy=GroupBasedPolicy(groups=["customer-engagement-team-group"]),
    actions=[AuthzedAction.DESCRIBE, *READ],
)

# Customer Engagement Team Group - Related Entities access
engagement_entities = Permission(
    name="customer-engagement-team-group-entities-reader",
    types=[Entity],
    name_patterns=[
        "branch",
        "atm_location",
        "customer",  # May need customer context
    ],
    policy=GroupBasedPolicy(groups=["customer-engagement-team-group"]),
    actions=[AuthzedAction.DESCRIBE],
)

# =============================================================================
# SUMMARY OF PERMISSIONS
# =============================================================================
"""
Permission Groups Summary:

GROUP-BASED ACCESS CONTROL:
The GroupBasedPolicy uses group identities from your identity provider.
Configure your IdP to pass group memberships in the groups claim.

GLOBAL PERMISSIONS (ALL USER GROUPS):
   - DESCRIBE access to Project (required for all feature store interactions)
   - Applies to: data-scientists-group, data-engineers-group, analytics-team-group, 
     customer-engagement-team-group

1. Data Scientists Group (group: data-scientists-group)
   - READ access to all Feature Views
   - READ access to all Feature Services  
   - DESCRIBE access to all Entities
   - NO access to Data Sources

2. Data Engineers Group (group: data-engineers-group)
   - Full CRUD + READ + WRITE access to Feature Views
   - Full CRUD + READ access to Feature Services
   - Full CRUD access to Entities
   - Full CRUD + READ + WRITE access to Data Sources
   - NO access to Permissions (reserved for admins)

3. Analytics Team Group (group: analytics-team-group)
   - READ access to customer-related Feature Views
   - READ access to transaction-related Feature Views
   - READ access to customer-related Feature Services
   - READ access to transaction-related Feature Services
   - DESCRIBE access to customer and transaction Entities

4. Customer Engagement Team Group (group: customer-engagement-team-group)
   - READ access to branch-related Feature Views
   - READ access to ATM-related Feature Views
   - READ access to call-center-related Feature Views
   - READ access to branch, ATM, and call-center Feature Services
   - DESCRIBE access to branch, atm_location, and customer Entities

HOW TO CONFIGURE GROUPS:

For Kubernetes RBAC:
  Create Kubernetes groups and RoleBindings that map users to groups.
  The group name will be passed as the identity to Feast.

For OIDC (Keycloak, Auth0, Okta):
  1. Create groups in your IdP (e.g., "data-scientists-group")
  2. Configure your IdP to include group memberships in JWT tokens
  3. Configure Feast to read the group claim (usually "groups" or "roles")
  4. Example feature_store.yaml:
     auth:
       type: oidc
       client_id: feast-banking
       roles_claim: groups  # or 'roles' depending on your IdP

Actions Available:
- DESCRIBE: View resource metadata
- READ: Read from online and offline stores
- READ_ONLINE: Read from online store only
- READ_OFFLINE: Read from offline store only
- WRITE: Write to stores
- CREATE: Create new resources
- UPDATE: Modify existing resources
- DELETE: Remove resources
- CRUD: Shorthand for CREATE, UPDATE, DELETE, DESCRIBE

Usage:
To apply these permissions to your feature store, run:
    from feast import FeatureStore
    from permissions import *
    
    store = FeatureStore(repo_path=".")
    store.apply([
        data_scientist_feature_views,
        data_scientist_feature_services,
        data_scientist_entities,
        data_engineer_feature_views,
        data_engineer_feature_services,
        data_engineer_entities,
        data_engineer_data_sources,
        analytics_customer_feature_views,
        analytics_transaction_feature_views,
        analytics_customer_feature_services,
        analytics_transaction_feature_services,
        analytics_customer_entity,
        analytics_transaction_entity,
        engagement_branch_feature_views,
        engagement_atm_feature_views,
        engagement_call_center_feature_views,
        engagement_branch_feature_services,
        engagement_atm_feature_services,
        engagement_call_center_feature_services,
        engagement_entities,
    ])

Note: 
- These permissions are enforced when using Feast servers (REST, Arrow Flight, gRPC)
- No enforcement occurs when using local provider
- Ensure your feature_store.yaml has proper auth configuration (OIDC or Kubernetes RBAC)
"""

# Export all permissions for easy importing
__all__ = [
    # Global permissions (all users)
    "project_access_all_users",
    
    # Data Scientists
    "data_scientist_feature_views",
    "data_scientist_feature_services",
    "data_scientist_entities",
    
    # Data Engineers
    "data_engineer_feature_views",
    "data_engineer_feature_services",
    "data_engineer_entities",
    "data_engineer_data_sources",
    
    # Analytics Team
    "analytics_customer_feature_views",
    "analytics_transaction_feature_views",
    "analytics_customer_feature_services",
    "analytics_transaction_feature_services",
    "analytics_customer_entity",
    "analytics_transaction_entity",
    
    # Customer Engagement Team
    "engagement_branch_feature_views",
    "engagement_atm_feature_views",
    "engagement_call_center_feature_views",
    "engagement_branch_feature_services",
    "engagement_atm_feature_services",
    "engagement_call_center_feature_services",
    "engagement_entities",
]
