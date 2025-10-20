# 📈 Stock Market Predictor

A complete, end-to-end MLOps project that automatically retrains a model to predict the next day's stock market movement and provides an interactive dashboard for analysis.

## Key Features

- **End-to-End MLOps Pipeline**: An automated workflow for data ingestion, feature engineering, model training, and evaluation.
- **Market Regime Detection**: Uses a K-Means clustering model to identify market states (e.g., high volatility, bullish trend) and uses this as a feature for the main prediction model.
- **Experiment Tracking**: Integrated with **MLflow** to log model parameters, performance metrics, and artifacts for every training run, enabling scientific model improvement.
- **Interactive Dashboard**: A user-friendly front-end built with **Streamlit** that allows users to get predictions for any stock, view price charts with Bollinger Bands, and run historical backtests.
- **Historical Backtesting**: Simulates the model's trading strategy on historical data to evaluate its hypothetical profitability against a simple buy-and-hold strategy.
- **Automated Retraining & Alerting**: A **GitHub Actions** CI/CD pipeline automatically retrains the model on a weekly schedule and sends email alerts for "UP" predictions on a predefined watchlist.
- **Containerized Application**: The entire project is containerized using **Docker**, making it reproducible, portable, and ready for cloud deployment.

## Tech Stack

- **Languages & Frameworks**: Python, Streamlit
- **Data & ML Libraries**: Pandas, yfinance, Scikit-learn, XGBoost, TA (Technical Analysis)
- **MLOps Tools**: MLflow, Docker, GitHub Actions

## Modeling Approach

The project uses two traditional machine learning models working in tandem:

1.  **K-Means Clustering**: An unsupervised model that analyzes market momentum (RSI) and volatility (Bollinger Band Width) to categorize each trading day into one of several distinct "market regimes."
2.  **XGBoost Classifier**: A powerful gradient boosting model that takes in technical indicators and the identified market regime to perform a binary classification, predicting whether the next day's stock price will go "Up" or "Down."

## Project Workflow

The project is architected as a multi-stage, automated pipeline:

`[Data Ingestion]` -> `[Data Transformation]` -> `[Model Training]` -> `[Model Evaluation]` -> `[Alerting]`

1.  **Data Ingestion**: Downloads the latest historical stock data from Yahoo Finance.
2.  **Data Transformation**: Cleans data, calculates technical indicators (SMA, RSI, Bollinger Bands), and uses the K-Means model to generate the `market_regime` feature.
3.  **Model Training**: Trains the XGBoost classifier on the feature-rich historical data.
4.  **Model Evaluation**: Evaluates the model's performance using F1-score and logs the results to MLflow.
5.  **Alerting**: An automated script runs predictions on a watchlist and sends proactive email alerts.

## Project Structure

├── .github
│   └── workflows
│       └── main.yaml              
├── artifacts/                     
├── research/
│   └── .gitkeep                    
├── src
│   └── stock_market_predictor
│       ├── __init__.py
│       ├── components             
│       │   ├── __init__.py
│       │   ├── alerting.py
│       │   ├── data_ingestion.py
│       │   ├── data_transformation.py
│       │   ├── model_evaluation.py
│       │   └── model_trainer.py
│       ├── config                 
│       │   ├── __init__.py
│       │   └── configuration.py
│       ├── entity                 
│       │   ├── __init__.py
│       │   └── config_entity.py
│       ├── pipeline               
│       │   ├── __init__.py
│       │   ├── backtesting_pipeline.py
│       │   └── training_pipeline.py
│       └── utils                  
│           ├── __init__.py
│           └── common.py
├── .env                           
├── .gitignore                     
├── app.py                          
├── config.yaml                     
├── Dockerfile                     
├── params.yaml                   
├── README.md                     
├── requirements.txt                
├── run_alerts.py                
├── run_pipeline.py                
└── setup.py                       

## Setup and Usage Instructions

### Prerequisites
- Python 3.9+
- Git
- A virtual environment tool (`venv`)

### 1. Clone the Repository
'''bash
git clone [https://github.com/pragyan2905/stock-market-predictor.git](https://github.com/pragyan2905/stock-market-predictor.git)
cd stock-market-predictor

### 2. Create and Activate Virtual Environment
'''bash
python -m venv venv
source venv/bin/activate

### 3. Install Dependencies
'''bash
pip install -r requirements.txt

### 4. Set Up Email Credentials (for Alerting)
Create a .env file in the root directory.

Add your credentials:

EMAIL_ADDRESS="your_email@gmail.com"
EMAIL_PASSWORD="your_16_character_google_app_password"
Important: Make sure .env is listed in your .gitignore file.

### 6. Run the Training Pipeline
To manually run the entire training process from start to finish:
python run_pipeline.py

### 7. View Experiments

To see your logged experiments in the MLflow UI:

'''bash
mlflow ui

Then, navigate to http://127.0.0.1:5000 in your browser.


