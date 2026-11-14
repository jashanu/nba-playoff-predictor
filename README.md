\# NBA Playoff Predictor



An end-to-end machine learning application that predicts NBA playoff game outcomes and simulates a complete playoff bracket.



\## Project Overview



This project uses historical NBA statistics from ten seasons of playoff data to train a Random Forest classification model. The model estimates the probability of one team winning against another based on differences in their statistical performance.



Those predictions are used to simulate best-of-seven playoff series and generate a complete playoff bracket through the NBA Finals.



\## Features



\- Historical NBA data collection using the NBA API

\- Data processing and feature engineering with Pandas

\- Random Forest classification model

\- Game outcome probability predictions

\- Best-of-seven playoff series simulations

\- Eastern and Western Conference playoff brackets

\- NBA Finals and predicted champion

\- Interactive Streamlit interface with team logos



\## Machine Learning



The model uses ten team-statistic difference features:



\- Win percentage

\- Points

\- Rebounds

\- Assists

\- Field goal percentage

\- Three-point percentage

\- Free throw percentage

\- Steals

\- Blocks

\- Plus/minus



Each feature represents the difference between Team A and Team B.



The target variable indicates whether Team A won the historical game.



A Random Forest classifier with 300 decision trees is trained using an 80/20 train-test split.



\## Technologies Used



\- Python

\- Pandas

\- NumPy

\- Scikit-learn

\- NBA API

\- Joblib

\- Streamlit

\- Matplotlib

\- Seaborn



\## Project Structure



```text

nba\_playoff\_predictor/

├── pages/

│   ├── app.py

│   └── playoff\_simulator.py

├── logos/

├── build\_real\_dataset.py

├── train\_real\_model.py

├── current\_stats.py

├── playoff\_dataset.csv

├── current\_teams.csv

├── playoff\_model.pkl

├── requirements.txt

└── README.md

```



\## Installation



1\. Clone the repository:



```bash

git clone https://github.com/YOUR\_USERNAME/nba-playoff-predictor.git

cd nba-playoff-predictor

```



2\. Create and activate a virtual environment:



```powershell

python -m venv venv

venv\\Scripts\\Activate.ps1

```



3\. Install dependencies:



```bash

pip install -r requirements.txt

```



\## Running the Application



Start the Streamlit application from the project root:



```bash

streamlit run pages/app.py

```



The application will open in your browser.



\## Model Training



To rebuild the historical dataset and train the model:



```bash

python build\_real\_dataset.py

python train\_real\_model.py

```



The included team statistics are configured for the 2025-26 season. To regenerate them, run:



```bash

python current\_stats.py

```



\## Future Improvements



\- Evaluate model performance using season-based train-test splits

\- Incorporate additional team statistics and advanced metrics

\- Improve home-court advantage modelling

\- Run multiple simulations to estimate championship probabilities

\- Update team data and playoff matchups automatically for each season



\## Disclaimer



This project is for educational purposes. Predictions and simulated outcomes are estimates based on historical statistics and simplified assumptions. They do not guarantee actual game results.

