# Financial Data ETL and Forecasting

This project demonstrates an ETL pipeline for financial stock data, including data validation, exploratory data analysis (EDA), and forecasting using SARIMAX and XGBoost.

## Problem Statement
Financial data comes from multiple sources and can be noisy, incomplete, or inconsistent. Analysts face challenges in cleaning, storing, and deriving insights from such data.

## Proposed solution

- Download stock data via API or other viable and legal means
- Clean and validate data using Pandas
- Store processed data in SQL database
- Perform EDA and feature engineering
- Train forecasting models (SARIMAX, XGBoost) and evaluate performance

## Features
- Download financial stock data via API or other viable and legal means
- ETL pipeline using Pandas
- Data cleaning and validation
- Exploratory Data Analysis (EDA)
- SQL database as structured storage
- Feature engineering
- Model training and forecasting (SARIMAX, XGBoost)

## Installation & Usage
### Requirements:
- Python >= 3.11
- supported db: SQLite
### Installation
```bash
pip install -r .\requirements.txt
```
### Usage
- Sample usage available in analysis.ipynb
- Sample data etl into sqlite db:
```bash
python transform.py
```

## Resources


## Contributing

Contributions available after previous contact.

## License

CC0 1.0 Universal