import pickle
import streamlit as st
import pandas as pd
import plotly.express as px
#Setting the layout on streamlit
st.set_page_config(layout = "wide")
#loading the model
model_file = "EPL_value_prediction.pkl"
with open(model_file, "rb") as f:
    model = pickle.load(f)

feature_file = "feature_importance.xlsx"
feature_df = pd.read_excel(feature_file)
st.sidebar.header("Input player features")

default_values = {
    "age": 25.0, "Playing Time_MP": 20.0, "Playing Time_Starts": 15.0, 
    "Playing Time_Min": 1800.0, "Playing Time_90s": 20.0, "Performance_Gls": 2.0, 
    "Performance_Ast": 1.0, "Performance_G+A": 3.0, "Performance_G-PK": 2.0, 
    "Performance_PK": 0.0, "Performance_PKatt": 0.0, "Performance_CrdY": 2.0, 
    "Performance_CrdR": 0.0, "Per 90 Minutes_Gls": 0.1, "Per 90 Minutes_Ast": 0.05, 
    "Per 90 Minutes_G+A": 0.15, "Per 90 Minutes_G-PK": 0.1, "Per 90 Minutes_G+A-PK": 0.15, 
    "Standard_Gls": 2.0, "Standard_Sh": 20.0, "Standard_SoT": 8.0, "Standard_SoT%": 40.0, 
    "Standard_Sh/90": 1.0, "Standard_SoT/90": 0.4, "Standard_G/Sh": 0.1, 
    "Standard_G/SoT": 0.25, "Performance_2CrdY": 0.0, "Performance_Fls": 15.0, 
    "Performance_Fld": 15.0, "Performance_Off": 2.0, "Performance_Crs": 25.0, 
    "Performance_Int": 10.0, "Performance_TklW": 12.0, "Performance_OG": 0.0, 
    "Performance_GA": 0.0, "Performance_GA90": 0.0, "Performance_SoTA": 0.0, 
    "Performance_Saves": 0.0, "Performance_Save%": 0.0, "Performance_W": 8.0, 
    "Performance_D": 5.0, "Performance_L": 7.0, "Performance_CS": 5.0, 
    "Performance_CS%": 25.0, "Penalty Kicks_PKatt": 0.0, "Penalty Kicks_PKA": 0.0, 
    "Penalty Kicks_PKsv": 0.0, "Penalty Kicks_PKm": 0.0, "Penalty Kicks_Save%": 0.0, 
    "Per 90 Performance_Int": 0.5, "Per 90 Performance_TklW": 0.6, "Club_tier": 2.0, 
    "Main_Position_FW": 0.0, "Main_Position_GK": 0.0, "Main_Position_MF": 1.0
}

core_display_features = ["age", "Playing Time_Min", "Performance_Gls", "Performance_Ast", "Performance_TklW", "Performance_Int", "Club_tier", "Standard_Sh"]
player_input = {}

#input fields with default values
for col, default in default_values.items():
    if col in core_display_features:
        if col == "Club_tier":
            player_input[col] = st.sidebar.selectbox(f"{col}", [1.0, 2.0, 3.0], index = int(default -1))
        elif col == "age":
            player_input[col] = st.sidebar.slider(f"{col}", 16, 40, int(default))
        elif col == "Performance_Gls":
            player_input[col] = st.sidebar.slider("Goals in one season",0, 100, int(default))
        elif col =="Performance_Ast":
            player_input[col] = st.sidebar.slider("Assists in on season",0, 100, int(default))
        elif col == "Playing Time_Min":
            player_input[col] = st.sidebar.number_input("Playing minutes in one season", 450, 3420)
        elif col == "Performance_TklW":
            player_input[col] = st.sidebar.slider("Tackles won", 0, 200, int(default))
        elif col == "Standard_Sh":
            player_input[col] = st.sidebar.slider("Shots made", 0, 200, int(default))
        else:
            player_input[col] = st.sidebar.slider("Interception", 0, 200, int(default))

    elif col == "Main_Position":
        player_input[col] = st.sidebar.selectbox(f"{col}", [0.0, 1.0], index = int(default))
    else:
        if col == "Performance_G+A":
            player_input[col] = float(player_input.get("Performance_Gls", 2.0) + player_input.get("Performance_Ast", 1.0))
        else:
            player_input[col] = float(default)

input_df = pd.DataFrame([player_input])

#Extract our feature score list
exp_features = model.get_booster().feature_names

input_df = input_df[exp_features]
#Main page and display
st.title("Premier League Player Market Value Predictor")
st.markdown("A little personal experiment and learning curve for machine learning")
st.markdown("--")

col_pre, col_insight = st.columns([2,2.15])

with col_pre:
    st.subheader("Algorithmic Price predictor")
    if st.button("Predict market value"):
        prediction =  float(model.predict(input_df)[0])
        st.success(f"Predicted market value:€{prediction: ,.0f} ")
    else:
        st.info("Enter inputs on the and click 'Predict market value' ")
    st.markdown('--')
    with st.sidebar.expander("Club tier reference"):
        st.markdown("""Tier 3: 'Manchester City', 'Arsenal', 'Liverpool', 'Chelsea', 'Manchester Utd', 'Tottenham'
                    Tier 2: 'Newcastle', 'Brighton', 'Everton', 'Crystal Palace',
                    Tier 1: Lower Mid-Table teams""")
with col_insight:
    st.subheader("Feature importance score")
    display_df = feature_df.copy()
    if len(display_df.columns) > 2:
        display_df.columns = ['Feature Name', 'Feature importance score']
    st.dataframe(display_df.head(5), use_container_width= True)



