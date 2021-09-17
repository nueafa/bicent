from binance.client import Client
import time
import math
import requests
import os

firsttime = time.localtime()[3]*60+time.localtime()[4]

url = 'https://notify-api.line.me/api/notify'
token = 'vFKNzn2QtVxtnBXs7ks7KHtbh21XQknE1BXIbyw5KgL'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
def msgsend(text):
    msg = (text)
    r = requests.post(url, headers=headers, data = {'message':msg})
    print (r.text)

print("#"*50)
print(" "*15,"This is Bicent")
print("#"*50)

api_key = 'g8bsSQqGYIZs9GHRlg7HRIkztUVYd6c1VsybpEsEySWkRLGYqczKKmFIeTQxlpdw'
api_secret = 'RZmj3wwJxEri7alasQSjm0etB8H2bFQMbPthMJ822stDPRLK6Pi943vS1O3dSLA5'
subpair = 'USDT'
client = Client(api_key, api_secret)

listenlist = ['SOL','XRP'] #what you want to listen + from your port
listenprice = []

def cleanlisten():
    listenlist.sort()
    for i in range(len(listenlist)):
        if i < len(listenlist)-1:
            if listenlist[i] == listenlist[i+1] or listenlist[i+1] == subpair :
                listenlist[i+1] = 'none'
                listenlist.remove('none')

def get_all_account():
    status1 = client.get_account()['balances']
    status2 = client.get_margin_account()['userAssets']
    status3 = client.get_isolated_margin_account()['assets']
    for i in range(len(status1)):
        if float((status1[i]['free'])) != 0:
            print(status1[i])
            listenlist.append(status1[i]['asset'])

    for i in range(len(status2)):
        if float((status2[i]['netAsset'])) != 0:
            print(status2[i])
            listenlist.append(status2[i]['asset'])

    for i in range(len(status3)):
        if float((status3[i]["baseAsset"]['netAsset'])) > 1:
            print(status3[i]["baseAsset"])
            listenlist.append(status3[i]["baseAsset"]['asset'])

def bicent():
    for j in listenlist :
        if j == subpair:
            continue
        kline = []
        kline = list(client.get_historical_klines_generator(j+subpair, Client.KLINE_INTERVAL_1MINUTE, "2 Hour ago UTC+7"))
        for i in range(len(kline)):
            if i == 0:
                fprice = float(kline[i][4])
            lprice = float(kline[i][4])

        if ((lprice-fprice)*100/fprice) > 5 or ((lprice-fprice)*100/fprice) < -5:
            text = j+'\nFirst : '+str(fprice)+'\nLast : '+str(lprice)+'\nChange : '+str(int(((lprice-fprice)*100/fprice)))
            msgsend(text)
            listenlist.remove(j)
        listenprice.append([j,fprice,lprice,((lprice-fprice)*100/fprice)])
        
    return listenprice 



def main ():
    global firsttime
    global listenprice
    get_all_account()
    while True:
        cleanlisten()
        log = bicent()
        listenprice = []
        clear = os.system('cls')

        for i in log :
            for j in range(len(i)):
                print(i[j],'   ',end = '')
            print('')
        print('')
        time.sleep(5)
        lasttime = time.localtime()[3]*60+time.localtime()[4]
        if abs(lasttime-firsttime) > 30:
            print("Refesh after 30 minute")
            firsttime = lasttime
            get_all_account()

main()