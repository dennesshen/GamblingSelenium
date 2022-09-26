import logging
import time

import requests
from selenium import webdriver
from  DataStorage import DataStorage

def getData(driver:webdriver, dataStorage:DataStorage):

    dataStorage.period = ""
    dataStorage.compareDataList = [[], [], [], [], [], [], [], [], [], []]
    dataStorage.countList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dataStorage.countOfRequest = 0 #計數 統計總共已經發出多少次資料請求
    dataStorage.indexOfBet = [] #用來放要下哪幾名的注

    while dataStorage.ifDetect:
        time.sleep(5)

        session_id = dict(driver.get_cookie("ASP.NET_SessionId")).get("value")

        headers = {"cookie" : "ASP.NET_SessionId=" + str(session_id) +"; CrNewsFlag=0"}
        body    = {"gType":"171", "dataType":"analytics"}

        # 連網取得資料
        oringinData = requests.post("https://ts777.nsb777.net/game/ajax/OutputIOContext.aspx", headers=headers, data=body )

        # 分析原始資料
        dataJson  = oringinData.json()
        keys      = dict(dataJson).keys()
        targetKey = list(keys)[-1]

        targetDictionary = dict(dict(dataJson).get(targetKey))


        if dataStorage.period == targetKey: continue   #如果還沒更新下一期，後面就不用做了
        logging.getLogger("觀察開獎").info("期數："+ targetKey)
        print("期數："+ targetKey)

        dataStorage.period = targetKey
        resultLists = []
        observeRange = dataStorage.coolNumber
        for i in range(1,11) :
            goalList = dict(targetDictionary.get(str(i)))
            dealList = sorted(goalList.items(), key= lambda x:x[1])
            resultList = []
            for j in range(observeRange):
                resultList.append(dealList[-(j+1)][0])

            # print("第"+str(i)+"名")
            # print(dealList)
            # print("test datastorage", dataStorage.compareDataList[i-1])
            # print("test resultlist", resultList)
            # print("test countOfRequest", dataStorage.countOfRequest)
            print("第" + str(i) + "名前" + str(observeRange) + "冷門號碼：" + str(resultList))
            logging.getLogger("觀察開獎").info("第"+str(i)+"名前"+str(observeRange)+"冷門號碼：" + str(resultList))

        # 比較跟上一期冷門號碼是否有變化，有變化代表本期開出了冷門號碼
            if resultList != dataStorage.compareDataList[i-1] and dataStorage.countOfRequest!=0 :
                dataStorage.countList[i-1] = dataStorage.countList[i-1]+1
            else:
                dataStorage.countList[i-1] = 0

            resultLists.append(resultList)

        dataStorage.compareDataList = resultLists
        # print(dataStorage.period, dataStorage.compareDataList, dataStorage.countList)
        dataStorage.countOfRequest += 1

        countString = ""
        for i in range(1, 11):
            countString = countString + "第" + str(i) + "名累積開冷門次數:" + str(dataStorage.countList[i-1]) + "次\n"

        logging.getLogger("觀察開獎").info(dataStorage.period + "期各名次連續開中冷門獎號次數：\n"+ countString)
        print(dataStorage.period + "期各名次連續開中冷門獎號次數：\n"+ countString)

        observeTime = dataStorage.observeTime
        message = ""
        ifBetHere = False
        indexOfBetHere = []
        for i in range(10):
            if dataStorage.countList[i] == observeTime:
                message = message + "第"+str(i+1)+"名已開冷門達"+ str(observeTime) +"次 \n"
                ifBetHere = True
                indexOfBetHere.append(i)

        if ifBetHere == True :
            if not (dataStorage.betTime > dataStorage.betTimeCount > 0):
                print(message)
                logging.getLogger("觀察開獎").info(message)
                dataStorage.ifBetMiddle = True
                dataStorage.indexOfBet = indexOfBetHere
            dataStorage.countList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def getBetSymbol(driver:webdriver, dataStorage: DataStorage):

    session_id = dict(driver.get_cookie("ASP.NET_SessionId")).get("value")

    headers = {"cookie" : "ASP.NET_SessionId=" + str(session_id) +"; CrNewsFlag=0"}
    body    = {"gType":"171", "dataType":"analytics"}

    # 連網取得資料
    oringinData = requests.post("https://ts777.nsb777.net/game/ajax/OutputIOContext.aspx", headers=headers, data=body )

    # 分析原始資料
    dataJson  = oringinData.json()
    keys      = dict(dataJson).keys()
    targetKey = list(keys)[-1]

    targetDictionary = dict(dict(dataJson).get(targetKey))

    dataStorage.betPeriod = targetKey

    observeRange = dataStorage.coolNumber
    resultList = []

    for i in dataStorage.indexOfBet:
        goalList = dict(targetDictionary.get(str(i+1)))
        dealList = sorted(goalList.items(), key= lambda x:x[1])
        for j in range(10-observeRange):
            resultList.append("aK1RankS_" + str(i+1) + "_" + str(dealList[j][0]))

    logging.getLogger("下注紀錄").info(str(targetKey)+"期最終下注號碼：" + str(resultList))
    dataStorage.BetSymbolList = resultList
    return resultList


def getPriceNumber(driver:webdriver, dataStorage: DataStorage):

    while True :
        time.sleep(5)
        session_id = dict(driver.get_cookie("ASP.NET_SessionId")).get("value")

        headers = {"cookie" : "ASP.NET_SessionId=" + str(session_id) +"; CrNewsFlag=0"}
        body    = {"gType":"171", "dataType":"analytics"}

        # 連網取得資料
        oringinData = requests.post("https://ts777.nsb777.net/game/ajax/OutputIOContext.aspx", headers=headers, data=body )

        # 分析原始資料
        dataJson  = oringinData.json()
        keys      = dict(dataJson).keys()
        targetKey = list(keys)[-1]

        targetDictionary = dict(dict(dataJson).get(targetKey))

        if dataStorage.betPeriod == targetKey: continue

        compareList = []
        for i in range(10) :
            goalList = dict(targetDictionary.get(str(i+1)))
            dealList = sorted(goalList.items(), key= lambda x:x[1])
            compareList.append("aK1RankS_" + str(i+1) + "_" + str(dealList[0][0]))

        print("本輪開獎號碼："+str(compareList))
        print("本輪中獎號碼："+str( list(set(compareList).intersection(dataStorage.BetSymbolList) ) ) )
        logging.getLogger("下注紀錄").info("本輪開獎號碼："+str(compareList))
        logging.getLogger("下注紀錄").info("本輪中獎號碼："+str( list(set(compareList).intersection(dataStorage.BetSymbolList) ) ) )

        priceCount = len(list(set(compareList).intersection(dataStorage.BetSymbolList)))
        betAmount = dataStorage.betAmountList[dataStorage.betTimeCount]
        dataStorage.betMoneyTotal += priceCount * betAmount * 9.9

        print("本輪下注中獎"+ str(priceCount * betAmount * 9.9) + "元")
        logging.getLogger("下注紀錄").info("本輪下注中獎"+ str(priceCount * betAmount * 9.9) + "元")
        logging.getLogger("下注紀錄").info("目前餘額 ： " + str(dataStorage.betMoneyTotal) + "元")
        return



