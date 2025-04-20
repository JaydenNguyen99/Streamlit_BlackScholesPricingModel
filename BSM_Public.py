import numpy as np
import pandas as pd
import streamlit as st
from scipy.stats import norm
import math
import matplotlib.pyplot as plt
import seaborn as sns
import time


# Setting the page layouts and stuff
st.set_page_config(
    page_title="Black-Scholes Pricing Model",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

# Setting the general color scheme
call_bg = "#d4edda"  # light green
put_bg = "#f8d7da"    # light red
normal_bg = '#F4EFE7' # beige
font_color = "#000000"
font_size = "24px"


# Introduction to the website
st.title("Black-Scholes Pricing Model")

st.markdown("## Introduction")
st.markdown("##### 📌 Hi, I am Khoa (Jay), and welcome to my mini Python project!: The Black-Scholes Pricing Model")
st.markdown("##### 📌 The main purposes of the Python project are as follows:")
st.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🚀 Given the paramaters input, what is the Call and Put options value")
st.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🚀 To observe how will the Option Values fluctuate given different Spot prices and Volatility while maintaining other parameters")
st.markdown("##### 📌 Without further ado, let's get started! Please follow the below instruction:")
st.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🚀 Step 1: Please fill in the necessary parameters on the left to calculate the Call and Put options value")
st.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🚀 Step 2: Please fill in the desired range for the Spot prices on the left")
st.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🚀 Step 3: Wait for the computer to calculate the option values")
st.write("⭐ Thank you for your time of interest. Have a nice day!")

progress_calculating_bar = st.progress(0, text='The computer is calculating options prices. Please wait...')
for percent_complete in range(100):
    time.sleep(0.025)
    progress_calculating_bar.progress(percent_complete + 1, text='The computer is calculating options prices. Please wait...')
time.sleep(1)
progress_calculating_bar.empty()
st.divider()

# Creating the sidebar for user to input prices

Black_Scholes_parameters ={
    'Current Asset Price': None,
    'Strike Price': None,
    'Time to Maturity (Years)': None,
    'Volatility' : None,
    'Risk-free Rate': None}

User_current_position = {
    'Current Call Price': None,
    'Current Call Quantity': None,
    'Current Put Price': None,
    'Current Put Quantity': None}

PnL_heatmap = {
    'Min Spot Price': None,
    'Max Spot Price': None,
    'Min Volatility': None,
    'Max Volatility': None}

# Step 1: Basic information
side_bar_user_input = st.sidebar.write("Created by: ")
st.sidebar.link_button("![LinkedIn](https://cdn-icons-png.flaticon.com/512/174/174857.png)  Khoa Nguyen (Jay)", "https://www.linkedin.com/in/khoadnguyen21/")
st.sidebar.write("---")

# Creating a section for user to input the basic paramters input
with st.sidebar:
    # Setting the Black-Scholes parameter inputs
    st.sidebar.write("🚀 Step 1: Black-Scholes Paramaters Input")
    Black_Scholes_parameters['Current Asset Price'] = st.number_input("Current Asset Price (USD)")
    Black_Scholes_parameters['Strike Price'] = st.number_input("Strike Price (USD)")
    Black_Scholes_parameters['Time to Maturity (Years)'] = st.number_input("Time to Maturity (Years)")
    Black_Scholes_parameters['Volatility'] = st.number_input("Volatility (Annually)")
    Black_Scholes_parameters['Risk-free Rate'] = st.number_input("Risk-free Rate (Annually)")
    st.sidebar.write("---")
    
    # Setting the profit and loss heatmap
    st.sidebar.write("🚀 Step 2: Options Price Heatmap")
    PnL_heatmap['Min Spot Price'] = st.number_input("Min Spot Price (USD)")
    PnL_heatmap['Max Spot Price'] = st.number_input("Max Spot Price (USD)")
    PnL_heatmap['Min Volatility'] = st.slider("Min Volatility", min_value = 0.01, max_value = 1.00)
    PnL_heatmap['Max Volatility'] = st.slider("Max Volatility", min_value = 0.01, max_value = 1.00)


# Calculating the Call and Put
S = Black_Scholes_parameters['Current Asset Price']
K = Black_Scholes_parameters['Strike Price']
t = Black_Scholes_parameters['Time to Maturity (Years)']
vol = Black_Scholes_parameters['Volatility']
r = Black_Scholes_parameters['Risk-free Rate']

d1 = (math.log(S / K) + (r + (vol**2)/2) * t) / (vol * math.sqrt(t))
d2 = d1 - (vol * math.sqrt(t))
call_option_price = S * norm.cdf(d1) - K * norm.cdf(d2)*(math.exp(-r*t))
put_option_price = K * math.exp(-r * t) * norm.cdf(-d2) - S * norm.cdf(-d1)

st.markdown("## ⌨️ Your paramaters data input")
data_to_display = pd.DataFrame([
    [Black_Scholes_parameters['Current Asset Price'],
    Black_Scholes_parameters['Strike Price'],
    Black_Scholes_parameters['Time to Maturity (Years)'],
    Black_Scholes_parameters['Volatility'],
    Black_Scholes_parameters['Risk-free Rate']]], 
    columns = ['Current Asset Price (USB)', 'Strike Price (USD)', 'Time to Maturity (Years)', 'Volatility (Annually)', 'Risk-free Rate (Annually)'],
    index = ['Values'])    

st.table(data_to_display)

# Create 2 columns to display the values of calculated option prices
Call_price, Put_price = st.columns(2, vertical_alignment="bottom", gap = 'small')

with Call_price:
    st.markdown(
        f"""
        <div style='background-color: {call_bg}; 
                    padding: 10px; 
                    border-radius: 10px; 
                    text-align: center;
                    color: {font_color}; 
                    font-size: {font_size};'>
            <strong>Call option value:</strong><br>$<strong>{round(call_option_price, 2)}</strong>
        </div>
        """,
        unsafe_allow_html=True)


with Put_price:
    st.markdown(
        f"""
        <div style='background-color: {put_bg}; 
                    padding: 10px; 
                    border-radius: 10px; 
                    text-align: center;
                    color: {font_color}; 
                    font-size: {font_size};'>
            <strong>Put option value:</strong><br>$<strong>{round(put_option_price, 2)}</strong>
        </div>
        """,
        unsafe_allow_html=True)

st.divider()

# Create Call Heat map
spot_result = np.linspace(PnL_heatmap['Min Spot Price'], PnL_heatmap['Max Spot Price'], num = 10)
spot_result_round = np.round(spot_result, 2)
spot_result_df = pd.Series(spot_result_round, name = 'Spot price')
vol_result = np.linspace(PnL_heatmap['Min Volatility'], PnL_heatmap['Max Volatility'], num = 10)
vol_result_round = np.round(vol_result, 2)
vol_result_df = pd.Series(vol_result_round, name = 'Volatility')

call_option_price_recal_list = []
put_option_price_recal_list = []

# Create a dictionary to store the recalculation values
    # For Call recalculation
call_option_price_recalculation_dict = {
    'Run_0': [], # Min Spot Price
    'Run_1': [],
    'Run_2': [],
    'Run_3': [],
    'Run_4': [],
    'Run_5': [],
    'Run_6': [],
    'Run_7': [],
    'Run_8': [],
    'Run_9': [], # Max Spot Price
}

    # For Put recalculation
put_option_price_recalculation_dict = {
    'Run_0': [], # Min Spot Price
    'Run_1': [],
    'Run_2': [],
    'Run_3': [],
    'Run_4': [],
    'Run_5': [],
    'Run_6': [],
    'Run_7': [],
    'Run_8': [],
    'Run_9': [], # Max Spot Price
}

for a in range(10):
    for b in range(10):
        S_recal = spot_result_round[a]
        vol_recal = vol_result[b]
        d1_recal = (math.log(S_recal / K) + (r + (vol_recal**2)/2) * t) / (vol_recal * math.sqrt(t))
        d2_recal = d1_recal - (vol_recal * math.sqrt(t))
        call_option_price_recal = S_recal * norm.cdf(d1_recal) - K * norm.cdf(d2_recal)*(math.exp(-r*t))
        put_option_price_recal = K * math.exp(-r * t) * norm.cdf(-d2_recal) - S_recal * norm.cdf(-d1_recal)
        call_option_price_recalculation_dict['Run_'+str(a)].append(call_option_price_recal)
        put_option_price_recalculation_dict['Run_'+str(a)].append(put_option_price_recal)

call_option_price_recal_df = pd.DataFrame(call_option_price_recalculation_dict)
put_option_price_recal_df = pd.DataFrame(put_option_price_recalculation_dict)

call_option_price_recal_df.columns = spot_result_df
call_option_price_recal_df.index = vol_result_df
put_option_price_recal_df.columns = spot_result_df
put_option_price_recal_df.index = vol_result_df

# Displaying the heatmap
st.markdown("## 🔥 Options Price Heatmap")
st.markdown(
        f"""
        <div style='background-color: {normal_bg}; 
                    padding: 10px; 
                    border-radius: 10px; 
                    text-align: left;
                    color: {font_color}; 
                    font-size: 12pt;'>
            Let explore how the option values flucuate with different "Spot prices and Volatility" while maintaining the parameters
        </div>
        """,
        unsafe_allow_html=True
    )

Call_price_heatmap, Put_price_heatmap = st.columns(2)

with Call_price_heatmap:
    st.markdown('### Call option value heatmap')
    fig = plt.figure(figsize = (8, 6))
    sns.heatmap(call_option_price_recal_df, annot = True, fmt = ".2f")
    plt.title('Call')
    st.pyplot(fig)

with Put_price_heatmap:
    st.markdown('### Put option value heatmap')
    fig = plt.figure(figsize = (8, 6))
    sns.heatmap(put_option_price_recal_df, annot = True, fmt = ".2f")
    plt.title('Put')
    st.pyplot(fig)