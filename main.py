import streamlit as st
from trading_stratagy import run_trading_startagies
from Trading_PE_CE import run_trading_startagies_PE_CE
import os

# Use the Heroku-assigned port or default to 5000
port = int(os.environ.get("PORT", 5000))

# Use st.set_page_config to set the port
# st.set_page_config(port=port)

def main():
    st.title("AI Algo Bot")

    # Input for user tokens
    user_tokens = st.text_area("Enter User's Kite encToken")

        # Main Content
    # st.header("Trading Parameters")

    # Radio Button for Momentum Trading
    # momentum_trading_enabled = st.checkbox("Enable Momentum Trading", value=True)
    # nine_twenty_trading_enabled = st.checkbox("9:20 AM Starategy", value=True)

    # # Risk and Quantity Inputs
    # st.subheader("Risk and Quantity Configuration")


    # Input for % Risk and Quantity
    # risk_percentage = st.number_input("Enter % Risk", min_value=0.1, max_value=100.0, step=0.1, value=1.0)
    quantity = st.number_input("Enter Quantity ( Multiples of 30 Only like 30,60,90,120,...)", min_value=30, step=30, value=30)

    # Button to trigger trading
    if st.button("Start Trading"):
        # Convert user_tokens to a list
        user_tokens_list = [token.strip() for token in user_tokens.split(',')]

        # Call your trading function with the inputs
        st_instance = st
        message_container = st.empty()
        run_trading_startagies_PE_CE(user_tokens_list, 7, quantity, True, st_instance, message_container)


if __name__ == "__main__":
    main()











