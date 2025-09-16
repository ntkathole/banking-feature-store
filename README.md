# Banking Feature Store Demo

This project demonstrates a comprehensive Feast feature store implementation for banking use cases with three different teams:

## Teams Structure
- **Customer Experience Team**: Customer Charter Model, Customer Behavior Prediction
- **Risk & Fraud Team**: Transaction Type Prediction, Fraud Detection
- **Operations Team**: Call Prediction, Branch Optimization

## Use Cases
1. **Customer Charter Model**: Predict customer satisfaction and loyalty
2. **Customer Behavior Prediction**: Predict spending patterns and financial needs
3. **Call Prediction Model**: Predict likelihood of customer service calls
4. **Transaction Type Prediction**: Classify transactions and detect fraud

## Project Structure
```
banking-feature-store/
├── feature_repo/                 # Feast feature repository
│   ├── data/                     # Sample parquet files
│   │   ├── customers.parquet
│   │   ├── transactions.parquet
│   │   ├── atm_usage.parquet
│   │   ├── branch_visits.parquet
│   │   └── call_center.parquet
│   ├── features/                 # Feature definitions
│   │   ├── customer_features.py
│   │   ├── transaction_features.py
│   │   ├── atm_features.py
│   │   ├── branch_features.py
│   │   └── call_center_features.py
│   ├── entities.py               # Entity definitions
│   ├── feature_services.py      # Feature service definitions
│   └── feature_store.yaml       # Feast configuration
├── generate_sample_data.py       # Data generation script
├── demo_notebook.ipynb          # Demo notebook
└── README.md                    # This file
```

## Getting Started
1. Install dependencies: `pip install feast pandas pyarrow`
2. Generate sample data: `python generate_sample_data.py`
3. Initialize Feast: `cd feature_repo && feast apply`
4. Run demo: `jupyter notebook demo_notebook.ipynb`
