import streamlit as st
import pandas as pd
from fredapi import Fred
from statsmodels.tsa.api import VAR
import plotly.express as px

import os

fred_api_key = os.environ.get("FRED_API_KEY")

# Function to fetch data from FRED
def fetch_data(series_id):
    fred = Fred(api_key=fred_api_key)
    data = fred.get_series(series_id)
    return data

# Function to run VAR model and forecast
def var_forecast(data, steps=5):
    model = VAR(data)
    model_fit = model.fit()
    # Use .endog to get the endogenous variables
    forecast = model_fit.forecast(model_fit.endog, steps=steps)
    return forecast


# Streamlit app
def main():
    st.title("Forecasting Using VAR Model")

    # User inputs for selecting indicators
#    use_gdp = st.checkbox("Include Quarterly GDP", value=True)
    use_industrial = st.checkbox("Include Monthly Industrial Production", value=True)
    use_retail = st.checkbox("Include Advance Monthly Retail Sales", value=True)
    use_ism = st.checkbox("Include Total Monthly Nonfarm Payrolls", value=True)

    # Fetch data based on user selection
    data = {}
#    if use_gdp:
#        data["GDP"] = fetch_data("GDP_SERIES_ID")
    if use_industrial:
        data["Industrial Production"] = fetch_data("INDPRO")
    if use_retail:
        data["Retail Sales"] = fetch_data("RSXFS")
    if use_ism:
        data["Payrolls"] = fetch_data("PAYEMS")

    # Create DataFrame
    df = pd.DataFrame(data)

    for column in df.columns:
        df[column] = df[column].pct_change(12)
    
    df = df.dropna()

    # Forecast GDP using VAR
    if df.empty:
        st.write("Please select at least one indicator")
    else:
        forecast = var_forecast(df)
        forecast_df = pd.DataFrame(forecast, columns=df.columns)

        # Plot the forecast
        fig = px.line(forecast_df, y=forecast_df.columns)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
