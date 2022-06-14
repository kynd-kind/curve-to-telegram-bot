# -*- coding: utf-8 -*-
"""
@author: kynd_kind
"""

import requests
import json
import sched, time

BOT_CHAT_ID = 'The chat ID of you and your bot'
BOT_API_KEY = 'The API key of your bot'

# For information on Telegram bots: https://core.telegram.org/bots

s = sched.scheduler(time.time, time.sleep)

def ping():
    
    # Sends GET request to API and loads it into readable workable text
    
    response = requests.get("https://api.curve.fi/api/getPools/fantom/factory/62/")
    jsondata = json.loads(response.text)
    
    # Locating specific data sets
    
    for i in jsondata['data']['poolData']:
        if i['id'] == 'factory-v2-62':
            factory = i
            break    
    for i in factory['coins']:
        if i['symbol'] == 'DAI+USDC':
            dai_usdc = i
            break
    for i in factory['coins']:
        if i['symbol'] == 'TOR':
            tor = i
            break
        
    # Loading specific data points
    
    tor_PB = tor['poolBalance']
    daiusdc_PB = dai_usdc['poolBalance']
    daiusdcDec = -abs(int(dai_usdc['decimals']))
    torDec = -abs(int(tor['decimals']))
    
    # Formating data points
    
    daiusdcClear = int(round((int(daiusdc_PB[:daiusdcDec]) / 2), 0))
    torClear = int(tor_PB[:torDec])
    fullPool = daiusdcClear + torClear    
    
    # Extrapolating information from data
    
    perc_dai = round((daiusdcClear / fullPool) * 100, 2)
    perc_tor = round((torClear / fullPool) * 100, 2)
    discrepency = abs(daiusdcClear - torClear) 
    
    # Formating the information into a readable string and passing it
    
    resultStr = "TOR: {}% DAI/USDC: {}%. {}$ Discrepency".format(perc_tor, perc_dai, discrepency)
    botSendMsg(resultStr)
    print(resultStr)

def botSendMsg(msg):

    send_txt = f"https://api.telegram.org/bot{BOT_API_KEY}/sendMessage?chat_id={BOT_CHAT_ID}&text={msg}"
    res = requests.get(send_txt)

def main():
    ping()

def do_something(sc): 
    print("Doing stuff...")
    main()
    sc.enter(60, 1, do_something, (sc,))
    
s.enter(60, 1, do_something, (s,))
s.run()
     




    

    
    