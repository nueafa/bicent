import math
import os
import time
import requests
from binance.client import Client

checktime = time.localtime()

def timecheck(dif):
    global checktime
    
#send msg to line

def msgsend(text):
    url = 'https://notify-api.line.me/api/notify'
    token = 'vFKNzn2QtVxtnBXs7ks7KHtbh21XQknE1BXIbyw5KgL'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    msg = (text)
    r = requests.post(url, headers=headers, data = {'message':msg})
    print (r.text)

print("#"*50)
print(" "*15,"This is Bicent")
print("#"*50)

#all config?

api_key = 'g8bsSQqGYIZs9GHRlg7HRIkztUVYd6c1VsybpEsEySWkRLGYqczKKmFIeTQxlpdw'
api_secret = 'RZmj3wwJxEri7alasQSjm0etB8H2bFQMbPthMJ822stDPRLK6Pi943vS1O3dSLA5'
client = Client(api_key, api_secret)
pricelist = []
valuelist = []
coinlist = []
amountlist = []
subpair = 'USDT'

#get all infomation in account

def get_all_account():
    global coinlist,amountlist
    coinlist = []
    amountlist = []
    status1 = client.get_account()['balances']
    status2 = client.get_margin_account()['userAssets']
    status3 = client.get_isolated_margin_account()['assets']

    for i in range(len(status1)):
        if float((status1[i]['free'])) != 0:
            #print(status1[i])
            coinlist.append(status1[i]['asset'])
            amountlist.append(status1[i]['free'])

    for i in range(len(status2)):
        if float((status2[i]['netAsset'])) != 0:
            #print(status2[i])
            coinlist.append(status2[i]['asset'])
            amountlist.append(status2[i]['free'])

    for i in range(len(status3)):
        if float((status3[i]["baseAsset"]['netAsset'])) > 1:
            #print(status3[i]["baseAsset"])
            coinlist.append(status3[i]["baseAsset"]['asset'])
            amountlist.append(status3[i]["baseAsset"]['free'])

#get value and print it            

def getvalue (symbollist,amountlist) :
    global pricelist,valuelist
    pricelist = []
    valuelist = []

    for i in range(len(symbollist)):
        if symbollist[i] != subpair:
            pricelist.append((client.get_avg_price(symbol=symbollist[i]+subpair)['price']))
            valuelist.append(float(amountlist[i])*float(pricelist[i]))
        elif symbollist[i] == subpair:
            pricelist.append('1')
            valuelist.append(float(amountlist[i])*float(pricelist[i]))
    for i in range(len(symbollist)):
        print(symbollist[i],' '*(10-len(symbollist[i])),amountlist[i],' '*(15-len(amountlist[i])),pricelist[i],' '*(15-len(pricelist[i])),valuelist[i])
def main ():
    get_all_account()

    while True:
        time.sleep(2)
        clear = os.system("cls")
        getvalue(coinlist,amountlist)
        client = Client(api_key, api_secret)
main()