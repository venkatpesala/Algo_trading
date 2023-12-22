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
            target_time = datetime.time(9,20,0)
            target_time2 = datetime.time(11,59,0)
            current_time = datetime.datetime.now().time()


            while True:
                 time.sleep(1)
#                print("Time:",datetime.datetime.now())
#                 print("start CE")
#                 while True:
                 while datetime.datetime.now().time() > target_time:
                    
                    spot=self.account.ltp("NSE:NIFTY BANK")
                    spot_price = spot['NSE:NIFTY BANK']['last_price']
                    spot_price = round(spot_price/100)*100


                    spot_symbols_bn_1=[]
                    spot_symbols_bn_1,current_week= self.fetch_spot_symbols_bn(spot_price)
                    spot_symbols_bn_1 = [element.split(',')[0] for element in spot_symbols_bn_1]
                    spot_symbols = spot_symbols_bn_1[current_week*2-2:current_week*2]
                    trading_symbol_ce= [string for string in spot_symbols if 'CE' in string] # convert list to string
                    trading_symbol_pe= [string for string in spot_symbols if 'PE' in string]
                    st2_trade_symbol_pe = self.modify_spotprice(trading_symbol_pe,0)
                    st2_trade_symbol_ce = self.modify_spotprice(trading_symbol_ce,-0)


    #                print(st2_trade_symbol_pe,st2_trade_symbol_ce)
                    
                    # previous_price_ce=current_price_ce
    #                print("In CE Momentum #####")

                    previous_price_ce = self.account.ltp("NFO:" + st2_trade_symbol_ce[0])
                    previous_price_ce = previous_price_ce["NFO:" + st2_trade_symbol_ce[0]]['last_price']

    #                print("time :",datetime.datetime.now().time(), "Previous_CE_Price :",previous_price_ce)
                    time.sleep(57)
                    current_price_ce = self.account.ltp("NFO:" + st2_trade_symbol_ce[0])
                    current_price_ce = current_price_ce["NFO:" + st2_trade_symbol_ce[0]]['last_price']

                    percentage_change= ((current_price_ce-previous_price_ce)/current_price_ce) *100
                    print("CE :",datetime.datetime.now().time(), "Strike Price:", st2_trade_symbol_ce[0], "Current_CE_Price :",current_price_ce,"Percentage change in CE :",percentage_change)
    #                print("User given percentage:", self.percentage)
                    if (percentage_change>=self.percentage):
                        percentage = self.percentage/100
                        if(datetime.datetime.now().time() > target_time2 ):
                            qty2 = self.qty*2
                        else:
                            qty2=self.qty

                        print("qty", self.qty)
                        order = self.account.place_order(variety=self.account.VARIETY_REGULAR,
                                                exchange=self.account.EXCHANGE_NFO,
                                                tradingsymbol=st2_trade_symbol_ce[0],
                                                transaction_type=self.account.TRANSACTION_TYPE_BUY,
                                                quantity=qty2,
                                                product=self.account.PRODUCT_MIS,
                                                order_type=self.account.ORDER_TYPE_MARKET)                    
                        comparision_price = self.account.ltp("NFO:" + st2_trade_symbol_ce[0])
                        comparision_price = comparision_price["NFO:" + st2_trade_symbol_ce[0]]['last_price']

                        print("CE:",datetime.datetime.now().time(),"Traded Price: ",comparision_price, "Buy price :" ,current_price_ce, "stoploss_CE :",(current_price_ce-(percentage*current_price_ce)),"Target_CE :",(current_price_ce+(percentage*current_price_ce)))
                        while True:
#                            print("time :",datetime.datetime.now().time(),"Traded Price: ",comparision_price)
                            comparision_price = self.account.ltp("NFO:" + st2_trade_symbol_ce[0])
                            comparision_price = comparision_price["NFO:" + st2_trade_symbol_ce[0]]['last_price']
                            time.sleep(1)
    #                        if current_price_ce-(percentage*current_price_ce) > comparision_price or  current_price_ce+(percentage*current_price_ce) < comparision_price:
                            if ((current_price_ce-30 > comparision_price or  current_price_ce+30 < comparision_price) and datetime.datetime.now().time() > target_time2 ) or ((current_price_ce-(percentage*current_price_ce) > comparision_price or  current_price_ce+30 < comparision_price) and datetime.datetime.now().time() < target_time2 ) :

                                order = self.account.place_order(variety=self.account.VARIETY_REGULAR,
                                                    exchange=self.account.EXCHANGE_NFO,
                                                    tradingsymbol=st2_trade_symbol_ce[0],
                                                    transaction_type=self.account.TRANSACTION_TYPE_SELL,
                                                    quantity=qty2,
                                                    product=self.account.PRODUCT_MIS,
                                                    order_type=self.account.ORDER_TYPE_MARKET)
                                
                                print("CE:",datetime.datetime.now().time(),"Traded Price: ",comparision_price, "Buy price :" ,current_price_ce, "stoploss_CE :",(current_price_ce-(percentage*current_price_ce)),"Target_CE :",(current_price_ce+(percentage*current_price_ce)))
                                
                                break

        def Momentum_PE(self):


            import datetime
            target_time = datetime.time(9,20,0)
            target_time2 = datetime.time(11,59,0)
            current_time = datetime.datetime.now().time()


            while True:
                 time.sleep(1)
#                print("Time:",datetime.datetime.now())

#                 while True:
                 while datetime.datetime.now().time() > target_time:
#                    print("start PE")
                    spot=self.account.ltp("NSE:NIFTY BANK")
    #                print(self.account.positions())
                    spot_price = spot['NSE:NIFTY BANK']['last_price']
                    spot_price = round(spot_price/100)*100

                    spot_symbols_bn_1=[]
                    spot_symbols_bn_1,current_week= self.fetch_spot_symbols_bn(spot_price)
                    spot_symbols_bn_1 = [element.split(',')[0] for element in spot_symbols_bn_1]
                    spot_symbols = spot_symbols_bn_1[current_week*2-2:current_week*2]
                    trading_symbol_ce= [string for string in spot_symbols if 'CE' in string] # convert list to string
                    trading_symbol_pe= [string for string in spot_symbols if 'PE' in string]
                    st2_trade_symbol_pe = self.modify_spotprice(trading_symbol_pe,0)
                    st2_trade_symbol_ce = self.modify_spotprice(trading_symbol_ce,-0)



    #                print("In PE Momentum #####")
                    previous_price_pe = self.account.ltp("NFO:" + st2_trade_symbol_pe[0])
                    previous_price_pe = previous_price_pe["NFO:" + st2_trade_symbol_pe[0]]['last_price']
    #                print("time :",datetime.datetime.now().time(), "Previous_PE_Price :",previous_price_pe)
                    time.sleep(57)
                    current_price_pe = self.account.ltp("NFO:" + st2_trade_symbol_pe[0])
                    current_price_pe = current_price_pe["NFO:" + st2_trade_symbol_pe[0]]['last_price']

                    percentage_change= ((current_price_pe-previous_price_pe)/current_price_pe)*100
                    print("PE :",datetime.datetime.now().time(),"Strike Price:", st2_trade_symbol_pe[0], "Current_PE_Price :",current_price_pe,"Percentage change in PE :",percentage_change)
    #                print("User given percentage:", self.percentage)

                    if (percentage_change>=self.percentage):
                        percentage= self.percentage/100
                        if(datetime.datetime.now().time() > target_time2 ):
                            qty2 = self.qty*2
                        else:
                            qty2= self.qty
                            
                        print("qty", self.qty)    
                        order = self.account.place_order(variety=self.account.VARIETY_REGULAR,
                                                exchange=self.account.EXCHANGE_NFO,
                                                tradingsymbol=st2_trade_symbol_pe[0],
                                                transaction_type=self.account.TRANSACTION_TYPE_BUY,
                                                quantity=qty2,
                                                product=self.account.PRODUCT_MIS,
                                                order_type=self.account.ORDER_TYPE_MARKET)
                        comparision_price = self.account.ltp("NFO:" + st2_trade_symbol_pe[0])
                        comparision_price = comparision_price["NFO:" + st2_trade_symbol_pe[0]]['last_price']
                        print("PE:",datetime.datetime.now().time(),"Traded Price: ",comparision_price, "Buy Price :" ,current_price_pe, "stoploss PE :",(current_price_pe-(percentage*current_price_pe)),"Target PE :",(current_price_pe+(percentage*current_price_pe)))
                        while True:
#                            print("time :",datetime.datetime.now().time(),"Traded Price: ",comparision_price)
                            comparision_price = self.account.ltp("NFO:" + st2_trade_symbol_pe[0])
                            comparision_price = comparision_price["NFO:" + st2_trade_symbol_pe[0]]['last_price']
                            time.sleep(1)

    #                        if current_price_pe-(percentage*current_price_pe) > comparision_price or  current_price_pe+(percentage*current_price_pe) < comparision_price:
                            if ((current_price_pe-30 > comparision_price or  current_price_pe+30 < comparision_price) and datetime.datetime.now().time() > target_time2 ) or ((current_price_pe-(percentage*current_price_pe) > comparision_price or  current_price_pe+30 < comparision_price) and datetime.datetime.now().time() < target_time2):

                                order = self.account.place_order(variety=self.account.VARIETY_REGULAR,
                                                    exchange=self.account.EXCHANGE_NFO,
                                                    tradingsymbol=st2_trade_symbol_pe,
                                                    transaction_type=self.account.TRANSACTION_TYPE_SELL,
                                                    quantity=qty2,
                                                    product=self.account.PRODUCT_MIS,
                                                    order_type=self.account.ORDER_TYPE_MARKET)
                                
                                print("PE :",datetime.datetime.now().time(),"Traded Price: ",comparision_price, "Buy Price :" ,current_price_pe, "stoploss PE :",(current_price_pe-(percentage*current_price_pe)),"Target PE :",(current_price_pe+(percentage*current_price_pe)))
                                break                   
     


   
def run_trading_startagies(account_details,quantity,riskpercentage,momentum_trading_enabled):
    kite_accounts = []

    # Initialize KiteConnect instances for each account
    for details in account_details:
        kite = KiteApp(enctoken=details)
        kite_accounts.append(kite)

        starategy_instances = [TradingStrategy(account,riskpercentage,quantity) for account in kite_accounts]

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=len(account_details) * 2) as executor:
        # Submit tasks to the executor for each account
        if momentum_trading_enabled:
            futures = [executor.submit(strategy.Momentum_CE) for strategy in starategy_instances] + \
                    [executor.submit(strategy.Momentum_PE) for strategy in starategy_instances] 
                   
            

            # Wait for tasks to complete
            for future in as_completed(futures):
                result = future.result()
#                print(result)

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
    




