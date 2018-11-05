import pandas as pd
import matplotlib.pyplot as plt
from Black_Scholes import BS_model
import numpy as np
import copy
import collections
import math

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

    daily_return_list = [0]
    daily_return_cumulative = [0]
    total_return = 0

    #calculate the option price for the first day
    holding_option_list = collections.deque(maxlen=89)
    call,put = BS_model(sp_price_global[0],sp_price_global[0],90.0/252.0,libor_global[0]/100.0,vix_global[0]/100.0)
    if sixty_day_ave_price[0] > hundrend_twenty_ave_price[0]:
        holding_option_list.append(["Call",call,0])
    else:
        holding_option_list.append(["Put",put,0])


    #calculate the daily return
    for i in range(1, length):
        daily_return = 0
        for j in range(len(holding_option_list)):
            holding_option_item = holding_option_list[j]
            call, put = BS_model(sp_price_global[i], sp_price_global[holding_option_item[2]], (90.0 - (i - holding_option_item[2])) / 252.0, libor_global[i] / 100.0,
                                 vix_global[i] / 100.0)
            if holding_option_item[0] == "Call":
                daily_return += call - holding_option_item[1]
                holding_option_list[j][1] = call
            else:
                daily_return += put - holding_option_item[1]
                holding_option_list[j][1] = put

        total_return += daily_return
        daily_return_cumulative.append(total_return)
        daily_return_list.append(daily_return)

        call, put = BS_model(sp_price_global[i], sp_price_global[i], 90.0 / 252.0, libor_global[i] / 100.0,
                             vix_global[i] / 100.0)
        if sixty_day_ave_price[i] > hundrend_twenty_ave_price[i]:
            holding_option_list.append(["Call", call, i])
        else:
            holding_option_list.append(["Put", put, i])
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

    daily_return_list = [0]
    daily_return_cumulative = [0]
    total_return = 0

    #calculate the option price for the first day
    holding_option_list = collections.deque(maxlen=1)
    call,put = BS_model(sp_price_global[0],sp_price_global[0],90.0/252.0,libor_global[0]/100.0,vix_global[0]/100.0)
    if sixty_day_ave_price[0] > hundrend_twenty_ave_price[0]:
        holding_option_list.append(["Call",call,0])
    else:
        holding_option_list.append(["Put",put,0])


    #calculate the daily return
    for i in range(1, length):
        daily_return = 0
        for j in range(len(holding_option_list)):
            holding_option_item = holding_option_list[j]
            call, put = BS_model(sp_price_global[i], sp_price_global[holding_option_item[2]], (90.0 - (i - holding_option_item[2])) / 252.0, libor_global[i] / 100.0,
                                 vix_global[i] / 100.0)
            if holding_option_item[0] == "Call":
                daily_return += call - holding_option_item[1]
                holding_option_list[j][1] = call
            else:
                daily_return += put - holding_option_item[1]
                holding_option_list[j][1] = put

        total_return += daily_return
        daily_return_cumulative.append(total_return)
        daily_return_list.append(daily_return)

        call, put = BS_model(sp_price_global[i], sp_price_global[i], 90.0 / 252.0, libor_global[i] / 100.0,
                             vix_global[i] / 100.0)
        if sixty_day_ave_price[i] > hundrend_twenty_ave_price[i]:
            holding_option_list.append(["Call", call, i])
        else:
            holding_option_list.append(["Put", put, i])
    return total_return, daily_return_list, daily_return_cumulative

def Portfolio3():
    length = len(sp_price_global)

    daily_return_list = [0]
    daily_return_cumulative = [0]
    total_return = 0

    #calculate the option price for the first day
    holding_option_list = collections.deque(maxlen=2)
    call,put = BS_model(sp_price_global[0],sp_price_global[0],90.0/252.0,libor_global[0]/100.0,vix_global[0]/100.0)
    holding_option_list.append(["Call",call,0])
    holding_option_list.append(["Put",put,0])


    #calculate the daily return
    for i in range(1, length):
        daily_return = 0
        for j in range(len(holding_option_list)):
            holding_option_item = holding_option_list[j]
            call, put = BS_model(sp_price_global[i], sp_price_global[holding_option_item[2]], (90.0 - (i - holding_option_item[2])) / 252.0, libor_global[i] / 100.0,
                                 vix_global[i] / 100.0)
            if holding_option_item[0] == "Call":
                daily_return += call - holding_option_item[1]
                holding_option_list[j][1] = call
            else:
                daily_return += put - holding_option_item[1]
                holding_option_list[j][1] = put

        total_return += daily_return
        daily_return_cumulative.append(total_return)
        daily_return_list.append(daily_return)

        call, put = BS_model(sp_price_global[i], sp_price_global[i], 90.0 / 252.0, libor_global[i] / 100.0,
                             vix_global[i] / 100.0)
        holding_option_list.append(["Call", call, i])
        holding_option_list.append(["Put", put, i])
    return total_return, daily_return_list, daily_return_cumulative


def Var_function():
    var_lines = [0]
    Cvar_lines = [0]
    position = 1
    if sixty_day_ave_price[0] > hundrend_twenty_ave_price[0]:
        position = 1
    else:
        position = -1
    length = len(sp_price_global)
    for j in range(1,length):
        mu, sigma = (libor_global[j]-(vix_global[j]**2) / 2) * 1/252, (vix_global[j]**2) * 1/252
        s = np.random.normal(mu, sigma, 10000)
        loss_list = []
        for i in range(len(s)):
            loss = position * libor_global[j] * (1 - math.exp(s[i]))
            loss_list.append(loss)
        loss_list.sort()
        index_95 = int(math.ceil(0.95 * len(loss_list)))
        var = loss_list[index_95]
        Cvar = sum(loss_list[index_95:]) / len(loss_list[index_95:])
        if sixty_day_ave_price[j] > hundrend_twenty_ave_price[j]:
            position = 1
        else:
            position = -1
        var_lines.append(var)
        Cvar_lines.append(Cvar)
    print var_lines
    print Cvar_lines
    # plt.plot(var_lines,linewidth=1,label='Var')
    plt.plot(range(len(var_lines)),Cvar_lines, linewidth=1, label='Cvar')
    plt.legend()
    plt.show()

    # print loss_list
    # print var
    # print Cvar








def main():
    # read file
    df = pd.read_csv("data_modified.csv")
    sp_price = df["SP500Price"]
    sp_price_global.extend(sp_price[119:])
    libor = df["LIBOR"]
    libor_global.extend(libor[119:])
    vix = df["VIX"]
    vix_global.extend(vix[119:])



    for i in range(119,len(sp_price)):
        ave_60 = sum(sp_price[i-59:i+1])/60.0
        ave_120 = sum(sp_price[i-119:i+1])/120.0
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

    ##Var
    Var_function()


if __name__ == '__main__':
    main()