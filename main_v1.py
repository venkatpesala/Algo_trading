import streamlit as st
from trading_stratagy import run_trading_startagies
from Trading_PE_CE import run_trading_startagies_PE_CE
import os
import pytz

# Set the time zone for the entire script
IST = pytz.timezone('Asia/Kolkata')


# Use the Heroku-assigned port or default to 5000
port = int(os.environ.get("PORT", 5000))

# Use st.set_page_config to set the port
# st.set_page_config(port=port)

# Read list of users from a text file
def read_user_list(file_path):
    with open(file_path, 'r') as file:
        users = [tuple(line.strip().split(',')) for line in file]
    return users


def main():
    
    st.title("Trading Automation UI")

    # Define the file path for the user list
    user_file_path = 'user_list.txt'

    # Read the list of valid users from the text file
    valid_users = read_user_list(user_file_path)

    # Add a form to collect username and password
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    # Check if the submitted credentials are valid
    if st.button("Login"):
        if (username, password) in valid_users:
            st.success("Logged In as {}".format(username))

            # Input for user tokens
            user_tokens = st.text_area("Enter User Tokens (comma-separated)", help="Example: token1, token2")
        
                # Main Content
            # st.header("Trading Parameters")
        
            # Radio Button for Momentum Trading
            # momentum_trading_enabled = st.checkbox("Enable Momentum Trading", value=True)
            # nine_twenty_trading_enabled = st.checkbox("9:20 AM Starategy", value=True)
        
            # Risk and Quantity Inputs
            # st.subheader("Risk and Quantity Configuration")
        
        
        
            # Input for % Risk and Quantity
            # risk_percentage = st.number_input("Enter % Risk", min_value=0.1, max_value=100.0, step=0.1, value=1.0)
            # quantity = st.number_input("Enter Quantity", min_value=15, step=15, value=15)
        
            # Button to trigger trading
            if st.button("Start Trading"):
                # Convert user_tokens to a list
                user_tokens_list = [token.strip() for token in user_tokens.split(',')]
        
                # Call your trading function with the inputs
                st_instance = st
        
                
                message_container = st.empty()
                # run_trading_startagies(user_tokens_list, risk_percentage, quantity,momentum_trading_enabled,st_instance)
                # run_trading_startagies_PE_CE(user_tokens_list, risk_percentage, quantity,momentum_trading_enabled,st_instance,message_container)
                run_trading_startagies_PE_CE(user_tokens_list, 7, 30,True,st_instance,message_container)


if __name__ == "__main__":
    main()
