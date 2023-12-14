from kite_trade import *
import pandas as pd
import time
import threading
import multiprocessing
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed



# account_details = [
# {"enctoken" :"TmtaGGHsf4Pz/iJftsqJrBPPpAWvdn/Wyc0SpafMXddz2YBD5dFHtt3Zww7wWKhFbE33Zz5KJZ6kFc+IsgoaFz6zjP/YWdQqqad1FEkIEe3anKcgHqCz9w=="},
# {"enctoken":"z/UmjT3Cw9ZwyZHCmwzT5G8OqBdVtlCvZfnGRvsx02Kra/QrFgN6EeYItcIBXa3VKJUr15OdJ0OiZ8ZvLH0+1TmvNTuYocSiZmXyBhyn08il8X9vMS2fYw=="}
# ]

# # Create a list to store KiteConnect instances
# kite_accounts = []

# # Initialize KiteConnect instances for each account
# for details in account_details:
#     kite = KiteApp(enctoken=details['enctoken'])
#     kite_accounts.append(kite)


# staratagy_2_qty=120

##############################################################################################################

class TradingStrategy:
        

        def __init__(self, account, qty, riskpercent):
            self.account = account
            self.qty = qty
            self.percentage = riskpercent
            print("User Given Percentage",self.percentage)



        def fetch_spot_symbols_bn(self,spot_price):
            # ... (unchanged)
            import datetime
            # Get the current date
            current_date = datetime.date.today()

            # Get the current month in text format (e.g., "NOV" for November)
            current_month_text = current_date.strftime('%b')
            current_month = current_date.month

            # Get the current week within the month
            current_week = (current_date.day - 1) // 7 + 1

            file_path = 'output_banknifty_symbols.csv'
            number_to_match = current_week
            string_to_match = current_month_text

            # List to store extracted strings
            matched_strings = []

            # Open the text file and extract lines based on the criteria
            with open(file_path, 'r') as file:
                for line in file:
                    if str(current_month) in line and str(spot_price) in line:
                        # matched_strings.append(line.strip().split(',')[0])
                        matched_strings.append(line.strip())


            sorted_data = sorted(matched_strings, key=lambda s: s.split(',')[1])
            return sorted_data, current_week
        def modify_spotprice(self,input_list, delta):
            # ... (unchanged)
                # Use regular expression to find the last five digits in each string
            modified_list = [re.sub(r'\d{5}(?=[^\d]*$)', lambda x: str(int(x.group()) + delta).zfill(5), string) for string in input_list]
            return modified_list


        def Momentum_CE(self):


            import datetime
            target_time = datetime.time(4, 16,1)
            current_time = datetime.datetime.now().time()


            while datetime.datetime.now().time() < target_time:
                time.sleep(1)
                print("Time:",datetime.datetime.now())
                print("start")

            while True:
                spot=self.account.ltp("NSE:NIFTY BANK")
                spot_price = spot['NSE:NIFTY BANK']['last_price']
                spot_price = round(spot_price/100)*100


                spot_symbols_bn_1=[]
                spot_symbols_bn_1,current_week= self.fetch_spot_symbols_bn(spot_price)
                spot_symbols_bn_1 = [element.split(',')[0] for element in spot_symbols_bn_1]
                spot_symbols = spot_symbols_bn_1[current_week*3-2:current_week*3]
                trading_symbol_ce= [string for string in spot_symbols if 'CE' in string] # convert list to string
                trading_symbol_pe= [string for string in spot_symbols if 'PE' in string]
                st2_trade_symbol_pe = self.modify_spotprice(trading_symbol_pe,200)
                st2_trade_symbol_ce = self.modify_spotprice(trading_symbol_ce,-200)


                print(st2_trade_symbol_pe,st2_trade_symbol_ce)
                
                # previous_price_ce=current_price_ce
                print("In CE Momentum #####")

                previous_price_ce = self.account.ltp("NFO:" + st2_trade_symbol_ce[0])
                previous_price_ce = previous_price_ce["NFO:" + st2_trade_symbol_ce[0]]['last_price']

                print("time :",datetime.datetime.now().time(), "Previous_CE_Price :",previous_price_ce)
                time.sleep(40)
                current_price_ce = self.account.ltp("NFO:" + st2_trade_symbol_ce[0])
                current_price_ce = current_price_ce["NFO:" + st2_trade_symbol_ce[0]]['last_price']

                percentage_change= ((current_price_ce-previous_price_ce)/current_price_ce) *100
                print("time :",datetime.datetime.now().time(), "Current_CE_Price :",current_price_ce,"Percentage change in CE :",percentage_change)
                print("User given percentage:", self.percentage)
                if (percentage_change>=self.percentage):
                    percentage = self.percentage/100


                    order = self.account.place_order(variety=self.account.VARIETY_REGULAR,
                                            exchange=self.account.EXCHANGE_NFO,
                                            tradingsymbol=st2_trade_symbol_ce[0],
                                            transaction_type=self.account.TRANSACTION_TYPE_BUY,
                                            quantity=self.qty,
                                            product=self.account.PRODUCT_MIS,
                                            order_type=self.account.ORDER_TYPE_MARKET)
                    comparision_price = self.account.ltp("NFO:" + st2_trade_symbol_ce[0])
                    comparision_price = comparision_price["NFO:" + st2_trade_symbol_ce[0]]['last_price']
                    while True:
                        comparision_price = self.account.ltp("NFO:" + st2_trade_symbol_ce[0])
                        comparision_price = comparision_price["NFO:" + st2_trade_symbol_ce[0]]['last_price']
                        time.sleep(1)

                        print("waiting for CE target/sl & CE Traded Price: ",comparision_price,"current_CE_price :" ,current_price_ce, "stoploss_CE :",(current_price_ce-(0.1*comparision_price)),"Target_CE :",(current_price_ce+(0.1*current_price_ce)))
                        time.sleep(1)
                        if current_price_ce-(percentage*current_price_ce) > comparision_price or  current_price_ce+(percentage*current_price_ce) < comparision_price:

                            order = self.account.place_order(variety=self.account.VARIETY_REGULAR,
                                                exchange=self.account.EXCHANGE_NFO,
                                                tradingsymbol=st2_trade_symbol_ce[0],
                                                transaction_type=self.account.TRANSACTION_TYPE_SELL,
                                                quantity=self.qty,
                                                product=self.account.PRODUCT_MIS,
                                                order_type=self.account.ORDER_TYPE_MARKET)
                            break


        def Momentum_PE(self):


            import datetime
            target_time = datetime.time(4, 16,1)
            current_time = datetime.datetime.now().time()


            while datetime.datetime.now().time() < target_time:
                time.sleep(1)
                print("Time:",datetime.datetime.now())
                print("start")

            while True:
                spot=self.account.ltp("NSE:NIFTY BANK")
                print(self.account.positions())
                spot_price = spot['NSE:NIFTY BANK']['last_price']
                spot_price = round(spot_price/100)*100

                spot_symbols_bn_1=[]
                spot_symbols_bn_1,current_week= self.fetch_spot_symbols_bn(spot_price)
                spot_symbols_bn_1 = [element.split(',')[0] for element in spot_symbols_bn_1]
                spot_symbols = spot_symbols_bn_1[current_week*3-2:current_week*3]
                trading_symbol_ce= [string for string in spot_symbols if 'CE' in string] # convert list to string
                trading_symbol_pe= [string for string in spot_symbols if 'PE' in string]
                st2_trade_symbol_pe = self.modify_spotprice(trading_symbol_pe,200)
                st2_trade_symbol_ce = self.modify_spotprice(trading_symbol_ce,-200)



                print("In PE Momentum #####")
                previous_price_pe = self.account.ltp("NFO:" + st2_trade_symbol_pe[0])
                previous_price_pe = previous_price_pe["NFO:" + st2_trade_symbol_pe[0]]['last_price']
                print("time :",datetime.datetime.now().time(), "Previous_PE_Price :",previous_price_pe)
                time.sleep(40)
                current_price_pe = self.account.ltp("NFO:" + st2_trade_symbol_pe[0])
                current_price_pe = current_price_pe["NFO:" + st2_trade_symbol_pe[0]]['last_price']

                percentage_change= ((current_price_pe-previous_price_pe)/current_price_pe) *100
                print("time :",datetime.datetime.now().time(), "Current_PE_Price :",current_price_pe,"Percentage change in PE :",percentage_change)
                print("User given percentage:", self.percentage)

                if (percentage_change>=self.percentage):
                    percentage= self.percentage/100


                    order = self.account.place_order(variety=self.account.VARIETY_REGULAR,
                                            exchange=self.account.EXCHANGE_NFO,
                                            tradingsymbol=st2_trade_symbol_pe[0],
                                            transaction_type=self.account.TRANSACTION_TYPE_BUY,
                                            quantity=self.qty,
                                            product=self.account.PRODUCT_MIS,
                                            order_type=self.account.ORDER_TYPE_MARKET)
                    comparision_price = self.account.ltp("NFO:" + st2_trade_symbol_pe[0])
                    comparision_price = comparision_price["NFO:" + st2_trade_symbol_pe[0]]['last_price']
                    while True:
                        comparision_price = self.account.ltp("NFO:" + st2_trade_symbol_pe[0])
                        comparision_price = comparision_price["NFO:" + st2_trade_symbol_pe[0]]['last_price']
                        time.sleep(1)

                        print("waiting for PE target/sl & PE Traded Price: ",comparision_price,"current_pe_price :" ,current_price_pe, "stoploss PE :",(current_price_pe-(0.01*comparision_price)),"Target PE :",(current_price_pe+(0.1*current_price_pe)))

                        if current_price_pe-(percentage*current_price_pe) > comparision_price or  current_price_pe+(percentage*current_price_pe) < comparision_price:

                            order = self.account.place_order(variety=self.account.VARIETY_REGULAR,
                                                exchange=self.account.EXCHANGE_NFO,
                                                tradingsymbol=st2_trade_symbol_pe,
                                                transaction_type=self.account.TRANSACTION_TYPE_SELL,
                                                quantity=self.qty,
                                                product=self.account.PRODUCT_MIS,
                                                order_type=self.account.ORDER_TYPE_MARKET)
                            break                   

        def ninetwenty_stratefy(self,):
            import datetime
            target_time = datetime.time(9, 20,2)
            current_time = datetime.datetime.now().time()


            while datetime.datetime.now().time() < target_time:
                time.sleep(1)
                print("Time:",datetime.datetime.now())
               
            print("Nine-Twenty Strategy started")
            while True:
                spot=self.account.ltp("NSE:NIFTY BANK")
                print(self.account.positions())
                spot_price = spot['NSE:NIFTY BANK']['last_price']
                spot_price = round(spot_price/100)*100

                spot_symbols_bn_1=[]
                spot_symbols_bn_1,current_week= self.fetch_spot_symbols_bn(spot_price)
                spot_symbols_bn_1 = [element.split(',')[0] for element in spot_symbols_bn_1]
                spot_symbols = spot_symbols_bn_1[current_week*2-2:current_week*2]
                trading_symbol_ce= [string for string in spot_symbols if 'CE' in string] # convert list to string
                trading_symbol_pe= [string for string in spot_symbols if 'PE' in string]
                # st2_trade_symbol_pe = self.modify_spotprice(trading_symbol_pe,100)
                # st2_trade_symbol_ce = self.modify_spotprice(trading_symbol_ce,-100)

                order_ce = self.account.place_order(variety=self.account.VARIETY_REGULAR,
                                            exchange=self.account.EXCHANGE_NFO,
                                            tradingsymbol=trading_symbol_ce[0],
                                            transaction_type=self.account.TRANSACTION_TYPE_SELL,
                                            quantity=15,
                                            product=self.account.PRODUCT_MIS,
                                            order_type=self.account.ORDER_TYPE_MARKET)
                
                bought_price_ce = self.account.ltp("NFO:" + trading_symbol_ce[0])
                order_pe = self.account.place_order(variety=self.account.VARIETY_REGULAR,
                            exchange=self.account.EXCHANGE_NFO,
                            tradingsymbol=trading_symbol_pe[0],
                            transaction_type=self.account.TRANSACTION_TYPE_SELL,
                            quantity=15,
                            product=self.account.PRODUCT_MIS,
                            order_type=self.account.ORDER_TYPE_MARKET)
                bought_price_pe = self.account.ltp("NFO:" + trading_symbol_pe[0])


                pe_flag=True
                ce_flag=True 
                while True:
                    current_price_ce = self.account.ltp("NFO:" + trading_symbol_ce[0])
                    current_price_ce = current_price_ce["NFO:" + trading_symbol_ce[0]]['last_price']
                    time.sleep(1)

                    if bought_price_ce+(0.4*bought_price_ce) > current_price_ce and ce_flag:
                        order = self.account.place_order(variety=self.account.VARIETY_REGULAR,
                                            exchange=self.account.EXCHANGE_NFO,
                                            tradingsymbol=trading_symbol_ce[0],
                                            transaction_type=self.account.TRANSACTION_TYPE_SELL,
                                            quantity=15,
                                            product=self.account.PRODUCT_MIS,
                                            order_type=self.account.ORDER_TYPE_MARKET)
                        ce_flag=False    

                    current_price_pe = self.account.ltp("NFO:" + trading_symbol_pe[0])
                    current_price_pe = current_price_pe["NFO:" + trading_symbol_pe[0]]['last_price']
                    time.sleep(1)

                    if bought_price_pe+(0.4*bought_price_pe) > current_price_pe:
                        order = self.account.place_order(variety=self.account.VARIETY_REGULAR,
                                            exchange=self.account.EXCHANGE_NFO,
                                            tradingsymbol=trading_symbol_pe[0],
                                            transaction_type=self.account.TRANSACTION_TYPE_SELL,
                                            quantity=15,
                                            product=self.account.PRODUCT_MIS,
                                            order_type=self.account.ORDER_TYPE_MARKET)
                        pe_flag=False                


   
def run_trading_startagies(account_details,quantity,riskpercentage,momentum_trading_enabled):
    kite_accounts = []

    # Initialize KiteConnect instances for each account
    for details in account_details:
        kite = KiteApp(enctoken=details)
        kite_accounts.append(kite)

        starategy_instances = [TradingStrategy(account,riskpercentage,quantity) for account in kite_accounts]

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=len(account_details) * 4) as executor:
        # Submit tasks to the executor for each account
        if momentum_trading_enabled:
            futures = [executor.submit(strategy.Momentum_CE) for strategy in starategy_instances] + \
                    [executor.submit(strategy.Momentum_PE) for strategy in starategy_instances] 
                   
            

            # Wait for tasks to complete
            for future in as_completed(futures):
                result = future.result()
                print(result)

# def run_ninetwnety_strategy(account_details,nine_twenty_trading_enabled):
#     if nine_twenty_trading_enabled:
#             # Initialize KiteConnect instances for each account
#         for details in account_details:
#             kite = KiteApp(enctoken=details)
#             kite_accounts.append(kite)
#         with ThreadPoolExecutor(max_workers=len(account_details) * 2) as executor:
#             # Submit tasks to the executor for each account
#             futures = [executor.submit(ninetwenty_stratefy, account) for account in kite_accounts] 
                    

#             # Wait for tasks to complete
#             for future in as_completed(futures):
#                 result = future.result()
#                 print(result)
    




