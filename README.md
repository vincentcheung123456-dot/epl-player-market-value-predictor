# Premier League Player Market Value Prediction Engine

Uses 55 different football stats to train this model and provide an accurate evaluation of a player's market value

## Data sourcing
* **Performance Stats:** Scraped across 5 seasons (2021/22-2025/26) from FBref
* **Market Value:** Extracted from historical **transfermarkt-datasets** by *davidcaribou*

## Machine Learning & UI
* **Algorithm Standard:** Hyperparameter-tuned **XGBoost Regressor**
* **Optimization:** Mitigated overfitting by 5 fold cross validation
* **Validation Performance:** Achieved an R^2 Score of 66% evaulated against 2025/26 Season dataset layer
* **Front-End Development:** Built a **Streamlit web dashboard** with interactive sliders

## Core Data Insight
1. **Attacking output(G+A):** Accounts for at least 27% of the model's value calculation engine
2. **Big Club Premium(Club_tier):** Financial weighting difference between the top clubs vs mid table and relegation clubs
3. **Age & Playtime:** Accounted for how player's age impacts their market value over time, while using playing time to filter out one-time wonder performances

## Execution & Installation
### To run the database.ipynb, the following libaries are required(run the following command in cmd):
   pip install pandas soccerdata thefuzz numpy matplotlib seaborn scipy scikit-learn xgboost pickle
### To run the interactive web dashboard on your local system, you will need to install and run the following from command prompt:
1. pip install streamlit pandas
2. cd "path/to/your/downloaded/'your-project-folder'"
3. python -m streamlit run app.py

   

