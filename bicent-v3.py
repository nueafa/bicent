while True:
    try:
        import math
        import os
        import time
        import requests
        from binance.client import Client

        def msgsend(text):
            url = 'https://notify-api.line.me/api/notify'
            token = 'vFKNzn2QtVxtnBXs7ks7KHtbh21XQknE1BXIbyw5KgL'
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
            msg = (text)
            r = requests.post(url, headers=headers, data = {'message':msg})
            print (r.text)
        print ("Bicent-v3.py")
        msgsend("init time"+str(time.localtime()))
        api_key = 'g8bsSQqGYIZs9GHRlg7HRIkztUVYd6c1VsybpEsEySWkRLGYqczKKmFIeTQxlpdw'
        api_secret = 'RZmj3wwJxEri7alasQSjm0etB8H2bFQMbPthMJ822stDPRLK6Pi943vS1O3dSLA5'
        client = Client(api_key, api_secret)
        subpair = 'USDT'
        cooldown = False
        rtcd = 1

        coinlist = ["GTC","BTC","ETH","BNB","ICP","SOL","ADA","ALGO","VET","SAND","GALA","NBS","NEAR","SHIB"]
        coincd = {}
        for i in coinlist:
            firsttime = time.localtime()[3]*60+time.localtime()[4]
            thistime = firsttime
            coincd[i] = [False,firsttime,thistime]
        listenprice = []
        coindata  = {}
        def bicent():
            global firsttime
            global coincd
            client = Client(api_key, api_secret)
            for coin in coinlist :
                kline = list(client.get_historical_klines_generator(coin+subpair, Client.KLINE_INTERVAL_1MINUTE, "2 Hour ago UTC+7"))
                fprice = float(kline[0][4])
                lprice = float(kline[-1][4])
                cprice = round(((lprice-fprice)*100/fprice),3)
                coindata[coin] = [fprice,lprice,cprice]
                if ((cprice >= 5 or cprice <= -5) and coincd[coin][0] == False):
                    msgsend("%s/%s/%s/%s"%(coin,fprice,lprice,cprice))
                    coincd[coin][0] = True
                    coincd[coin][2] = time.localtime()[3]*60+time.localtime()[4]
                if abs(coincd[coin][2]-coincd[coin][1])  > 30:
                    coincd[coin][0] = False
                    coincd[coin][1] = coincd[coin][2]
                    if rtcd > 1:
                        rtcd = rtcd - 1
            r = os.system("cls") 
            for i in coindata:
                    print(i," "*(10-len(i)),coindata[i][0]," "*(10-len(str(coindata[i][0]))),coindata[i][1]," "*(10-len(str(coindata[i][1]))),coindata[i][2]," "*(10-len(str(coindata[i][2]))),coincd[i][0])
            return coindata 
        while True:
                bicent()
                time.sleep(6)
    except:
        rtcd += 1
        msgsend("Error now restarting in %s seconds"%rtcd**2)
        time.sleep(rtcd**2)
        continue