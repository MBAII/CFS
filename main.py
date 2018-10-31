import pandas as pd
import matplotlib.pyplot as plt
from Black_Scholes import BS_model
import numpy
import copy
import collections


sp_price_global = []
libor_global = []
vix_global = []
sixty_day_ave_price = []
hundrend_twenty_ave_price = []


##Assume we are able to short
def Portfolio1_cumulative():
    length = len(sp_price_global)
    index_holding = 0
    daily_return_list =[0]
    daily_return_cumulative = [0]
    total_return = 0

    if sixty_day_ave_price[0] > hundrend_twenty_ave_price[0]:
        index_holding += 1
    else:
        index_holding -= 1

    for i in range(1,length):
        daily_return = (sp_price_global[i] - sp_price_global[i-1]) * index_holding
        total_return += daily_return
        daily_return_cumulative.append(total_return)
        daily_return_list.append(daily_return)
        if sixty_day_ave_price[i] > hundrend_twenty_ave_price[i]:
            index_holding += 1
        else:
            index_holding -= 1
    return total_return, daily_return_list,daily_return_cumulative

def Portfolio2_cumulative():
    length = len(sp_price_global)

    call_put_list = [] #[[call_price1,put_price1],[call_price2,put_price2]...]
    daily_return_list = [0]
    daily_return_cumulative = [0]
    total_return = 0
    #store all call and put in a list
    for i in range(length):
        call,put = BS_model(sp_price_global[i],sp_price_global[i],90.0/365.0,libor_global[i]/100.0,vix_global[i]/100.0)
        call_put_list.append([call,put])
    #calculate the daily return
    holding_option = collections.deque(maxlen=90)
    if sixty_day_ave_price[0] > hundrend_twenty_ave_price[0]:
        holding_option.append("Call")
    else:
        holding_option.append("Put")
    for i in range(1, length):
        daily_return = (call_put_list[i][0] - call_put_list[i-1][0]) * holding_option.count("Call") + \
                       (call_put_list[i][1] - call_put_list[i - 1][1]) * holding_option.count("Put")
        # print holding_option.count("Call") + holding_option.count("Put")
        # print daily_return
        total_return += daily_return
        daily_return_cumulative.append(total_return)
        daily_return_list.append(daily_return)
        if sixty_day_ave_price[i] > hundrend_twenty_ave_price[i]:
            holding_option.append("Call")
        else:
            holding_option.append("Put")
    return total_return, daily_return_list, daily_return_cumulative


#only hold each stock one day and sell it on the next day
def Portfolio1():
    length = len(sp_price_global)
    daily_return_list =[0]
    daily_return_cumulative = [0]
    total_return = 0

    if sixty_day_ave_price[0] > hundrend_twenty_ave_price[0]:
        index_holding = 1
    else:
        index_holding = -1

    for i in range(1,length):
        daily_return = (sp_price_global[i] - sp_price_global[i-1]) * index_holding
        total_return += daily_return
        daily_return_cumulative.append(total_return)
        daily_return_list.append(daily_return)
        if sixty_day_ave_price[i] > hundrend_twenty_ave_price[i]:
            index_holding = 1
        else:
            index_holding = -1
    return total_return, daily_return_list,daily_return_cumulative


def Portfolio2():
    length = len(sp_price_global)

    call_put_list = [] #[[call_price1,put_price1],[call_price2,put_price2]...]
    daily_return_list = [0]
    daily_return_cumulative = [0]
    total_return = 0
    #store all call and put in a list
    for i in range(length):
        call,put = BS_model(sp_price_global[i],sp_price_global[i],90.0/365.0,libor_global[i]/100.0,vix_global[i]/100.0)
        call_put_list.append([call,put])
    #calculate the daily return
    holding_option = collections.deque(maxlen=1)
    if sixty_day_ave_price[0] > hundrend_twenty_ave_price[0]:
        holding_option.append("Call")
    else:
        holding_option.append("Put")
    for i in range(1, length):
        daily_return = (call_put_list[i][0] - call_put_list[i-1][0]) * holding_option.count("Call") + \
                       (call_put_list[i][1] - call_put_list[i - 1][1]) * holding_option.count("Put")

        # print holding_option.count("Call") + holding_option.count("Put")
        # print daily_return
        total_return += daily_return
        daily_return_cumulative.append(total_return)
        daily_return_list.append(daily_return)
        if sixty_day_ave_price[i] > hundrend_twenty_ave_price[i]:
            holding_option.append("Call")
        else:
            holding_option.append("Put")
    return total_return, daily_return_list, daily_return_cumulative

def Portfolio3():
    length = len(sp_price_global)

    call_put_list = [] #[[call_price1,put_price1],[call_price2,put_price2]...]
    daily_return_list = [0]
    daily_return_cumulative = [0]
    total_return = 0
    #store all call and put in a list
    for i in range(length):
        call,put = BS_model(sp_price_global[i],sp_price_global[i],90.0/365.0,libor_global[i]/100.0,vix_global[i]/100.0)
        call_put_list.append([call,put])
    #calculate the daily return
    position = ""
    if sixty_day_ave_price[0] > hundrend_twenty_ave_price[0]:
        position = "long"
    else:
        position = "short"
    for i in range(1, length):
        if position == "long":
            daily_return = (call_put_list[i][0] - call_put_list[i-1][0]) * 1 + \
                           (call_put_list[i][1] - call_put_list[i - 1][1]) * 1
        else:
            daily_return = (call_put_list[i][0] - call_put_list[i - 1][0]) * -1 + \
                           (call_put_list[i][1] - call_put_list[i - 1][1]) * -1

        # print holding_option.count("Call") + holding_option.count("Put")
        # print daily_return
        total_return += daily_return
        daily_return_cumulative.append(total_return)
        daily_return_list.append(daily_return)
        if sixty_day_ave_price[i] > hundrend_twenty_ave_price[i]:
            position = "long"
        else:
            position = "short"
    return total_return, daily_return_list, daily_return_cumulative

def main():
    # read file
    df = pd.read_csv("data_modified.csv")
    sp_price = df["SP500Price"]
    sp_price_global.extend(sp_price[120:])
    libor = df["LIBOR"]
    libor_global.extend(libor[120:])
    vix = df["VIX"]
    vix_global.extend(vix[120:])



    # date = df["Date"][:-120]
    for i in range(120,len(sp_price)):
        ave_60 = sum(sp_price[i-60:i])/60
        ave_120 = sum(sp_price[i-120:i])/120
        sixty_day_ave_price.append(ave_60)
        hundrend_twenty_ave_price.append(ave_120)

    ##Plot the average lines
    # plt.plot(sixty_day_ave_price,c = "r",linewidth=1,label='60 average')
    # plt.plot(hundrend_twenty_ave_price, c = 'b',linewidth=1,label='120 average')
    # plt.legend()
    # plt.show()



    #Portfolio 1 cumulative
    # rc1 = Portfolio1_cumulative()
    # plt.plot(rc1[2],linewidth=1,label='Cumulative Return')
    # plt.legend()
    # plt.show()



    #Portfolio 2 cumulative
    # rc2 = Portfolio2_cumulative()
    # plt.plot(rc2[2],linewidth=1,label='Cumulative Return')
    # plt.legend()
    # plt.show()


    ##Portfolio 1
    # r1 = Portfolio1()
    # plt.plot(r1[2],linewidth=1,label='Cumulative Return')
    # plt.legend()
    # plt.show()

    ##Portfolio 2
    # r2 = Portfolio2()
    # plt.plot(r2[2],linewidth=1,label='Cumulative Return')
    # plt.legend()
    # plt.show()


    ##Portfolio 3
    # r3 = Portfolio3()
    # plt.plot(r3[2],linewidth=1,label='Cumulative Return')
    # plt.legend()
    # plt.show()



if __name__ == '__main__':
    main()