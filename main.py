import streamlit as st
from trading_stratagy import run_trading_startagies

def main():
    st.title("Trading Automation UI")

    # Input for user tokens
    user_tokens = st.text_area("Enter User Tokens (comma-separated)", help="Example: token1, token2")

        # Main Content
    st.header("Trading Parameters")

    # Radio Button for Momentum Trading
    momentum_trading_enabled = st.checkbox("Enable Momentum Trading", value=True)
    nine_twenty_trading_enabled = st.checkbox("9:20 AM Starategy", value=True)

    # Risk and Quantity Inputs
    st.subheader("Risk and Quantity Configuration")


    # Input for % Risk and Quantity
    risk_percentage = st.number_input("Enter % Risk", min_value=0.1, max_value=100.0, step=0.1, value=1.0)
    quantity = st.number_input("Enter Quantity", min_value=15, step=15, value=15)

    # Button to trigger trading
    if st.button("Start Trading"):
        # Convert user_tokens to a list
        user_tokens_list = [token.strip() for token in user_tokens.split(',')]

        # Call your trading function with the inputs
        run_trading_startagies(user_tokens_list, risk_percentage, quantity,momentum_trading_enabled)
        # run_ninetwnety_strategy(user_tokens_list,nine_twenty_trading_enabled)


if __name__ == "__main__":
    main()




