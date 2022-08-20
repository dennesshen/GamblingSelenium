import datetime
import random
import time
import logging

from datetime import date

import DataStorage
import GetData
from ManipulateScript import GambleScript
from chromeDriver import GambleDriver

def startAutoGamble(parmList : list ):

    gambleDriver = GambleDriver("./chromedriver/chromedriver")
    gambleDriver.runPageByURL("https://iju888.net/index.aspx")

    dataStorage = DataStorage.DataStorage(parmList)
    gamblesScript = GambleScript(gambleDriver.driver, dataStorage)

    gambleDriver.execute_with_errorLimit(3, gamblesScript.firstPageScript)

    gambleDriver.execute_with_errorLimit(3, gamblesScript.secondPageScript)

    gambleDriver.execute_with_errorLimit(3, gamblesScript.secondPageScript2)

    gambleDriver.execute_with_errorLimit(3, gamblesScript.secondPageScript3_pre)

    try:
        while True:
            print("開始偵測")
            logging.info("開始偵測")

            # 偵測冷門號碼開獎次數
            GetData.getData(gambleDriver.driver, dataStorage)


            logging.info("開始下注:")
            print("開始下注:")

            dataStorage.indexOfBet = random.sample(dataStorage.indexOfBet, 1)
            betIndexString = ""
            for i in dataStorage.indexOfBet:
                betIndexString = betIndexString + "第" +str(i+1) + "名  "
            logging.info("下注名次:  " + betIndexString)
            print("下注名次:  " + betIndexString)

            betTime = 0
            dataStorage.betTimeCount = 0
            while True:
                gainMoneyUplimit = dataStorage.betMoneyTotal
                betTime += 1
                # 準備下注所需的按鍵id 的list
                GetData.getBetSymbol(gambleDriver.driver, dataStorage)

                # 開始執行下注
                gambleDriver.execute_with_errorLimit(1, gamblesScript.secondPageScript3)
                dataStorage.betTimeCount += 1
                if dataStorage.betTime == betTime or (not dataStorage.isMoneyEnough) or dataStorage.betMoneyTotal >= gainMoneyUplimit:
                    dataStorage.ifBet = False
                    break

            if ( (not dataStorage.isMoneyEnough) or dataStorage.betMoneyTotal >= dataStorage.gainMoneyUplimit) : break

        print("本輪自動化下注結束，目前餘額：" + str(dataStorage.betMoneyTotal))
        logging.info("本輪自動化下注結束，目前餘額：" + str(dataStorage.betMoneyTotal))
    except Exception as e:
        logging.warning(str(e.args))



def startLogging():
    FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    FileName = date.today().strftime("%Y年%m月%d日") + ' 運行日誌.log'
    logging.basicConfig(level=logging.INFO, filename=FileName, filemode='a', format=FORMAT)


if __name__ == "__main__":


    model = input("請輸入使用模式，模擬模式輸入F, 真實模式輸入T : ")
    coolNumber = input("請輸入要觀察幾門冷門號碼 : ")
    observeTime = input("請輸入連續開冷門號幾次後才要開始下注 : ")
    betTime = input("請輸入開始下注後，要連續下注幾次 : ") or 3

    betMoneyTotal = input("請輸入本輪自動化下注所準備金額 ： ")
    gainMoneyLimit = input("請輸入本輪自動化下注獲利了結金額 ： ")
    username = input("請輸入博弈網站帳號 ： ")
    password = input("請輸入博弈網站密碼 ： ")

    betAmountList = []
    for i in range(int(betTime)):
       betAmount = input("第"+ str(i+1) + "次下注每一注金額：" ) or 10
       betAmountList.append(int(betAmount))

    parmList = [model, int(coolNumber), int(observeTime), int(betTime), betAmountList,
                int(betMoneyTotal), username, password, int(gainMoneyLimit)]
    print(parmList)
    startLogging()
    logging.info("設定參數："+str(parmList))
    print("設定參數："+str(parmList))

    print("開始自動化下注程式，開始時間 -> " + datetime.datetime.now().strftime("%H:%M:%S") )
    logging.info("開始自動化下注程式，開始時間 -> " + datetime.datetime.now().strftime("%H:%M:%S") )

    startAutoGamble(parmList)

