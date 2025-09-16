"""
Simple On-Demand Feature View Example

This module demonstrates a basic on-demand feature transformation for banking.
"""

import pandas as pd
from feast import Field
from feast.on_demand_feature_view import on_demand_feature_view
from feast.types import Float64

# Import existing feature views for transformations
from .customer_features import customer_demographics_fv


@on_demand_feature_view(
    sources=[customer_demographics_fv],
    schema=[
        Field(name="risk_score", dtype=Float64),
    ],
    description="Simple risk score calculation based on credit score",
    tags={
        "team": "risk_management",
        "owner": "risk_management_team@bank.com",
        "use_case": "simple_risk_scoring",
        "model_type": "regression",
        "target": "risk_score",
        "business_impact": "medium",
        "sla": "real_time",
        "transformation_type": "on_demand"
    },
)
def calculate_simple_risk_score(customer_features: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate a simple risk score based on credit score.
    Higher credit score = lower risk (higher score)
    """
    df = pd.DataFrame()
    
    # Get credit score from customer features
    credit_score = customer_features.get('credit_score', pd.Series([0.0])).fillna(0.0)
    
    # Simple risk calculation: credit score as percentage (0-100)
    # Higher credit score = lower risk = higher risk score
    risk_score = (credit_score / 850.0) * 100
    
    df["risk_score"] = risk_score.astype(float)
    
    return df
