import logging
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from DataStorage import DataStorage
from GetData import getPriceNumber


class GambleScript:

   
    def __init__(self,mainDriver:WebDriver, dataStorage: DataStorage):
        
        self.mainDriver = mainDriver
        self.dataStorage = dataStorage



    def firstPageScript(self):
        inputUsername = self.mainDriver.find_element(By.ID, "txtUser" )
        inputPassword = self.mainDriver.find_element(By.ID, "txtPassword" )

        # "832452"
        # "rood8879"
        inputUsername.send_keys(self.dataStorage.username)
        inputPassword.send_keys(self.dataStorage.password)
        time.sleep(5)
        self.mainDriver.find_element(By.CLASS_NAME, "btn_signIn").click()
        
        time.sleep(5)

    def secondPageScript(self):
        newWindow = 'window.open("https://iju888.net/Game/CBAPI.aspx?cbUrl=https://TS777.NSB777.NET/")'
        self.mainDriver.execute_script(newWindow)
        
        self.mainDriver.switch_to.window(self.mainDriver.window_handles[1])
        WebDriverWait(self.mainDriver, 20).until(
            EC.presence_of_element_located((By.ID, "divMenu_2" ))
        )
        self.mainDriver.implicitly_wait(30)
        time.sleep(5)
        print("頁面準備成功")

    def secondPageScript2(self):
        self.mainDriver.find_element(By.ID, "divMenu_2").click()
        time.sleep(5)
        leftNames = self.mainDriver.find_elements(By.CSS_SELECTOR, "span[class='leftName']")

        for leftName in leftNames:
            if leftName.text == "BET 賽馬":
                print( "目標：" + leftName.text )
                leftName.click()

        print("找到賽馬")
        time.sleep(20)
        self.mainDriver.implicitly_wait(30)

    def secondPageScript3_pre(self):
        time.sleep(5)
        iframe = self.mainDriver.find_element(By.ID, "ifrKType")
        self.mainDriver.switch_to.frame(iframe)

    def secondPageScript3(self):
        time.sleep(20)

        for i in self.dataStorage.BetSymbolList:
            time.sleep(0.5)
            self.mainDriver.find_element(By.ID, i).click()

        self.mainDriver.find_element(By.ID, "txbBetAmt")\
                       .send_keys(self.dataStorage.betAmountList[self.dataStorage.betTimeCount])

        needMoney = self.mainDriver.find_element(By.ID, "spnetTotal").get_property("innerText")

        print( self.dataStorage.betPeriod + "下注號碼："+str(self.dataStorage.BetSymbolList))
        logging.getLogger("下注紀錄").info( self.dataStorage.betPeriod + "下注號碼："+str(self.dataStorage.BetSymbolList))
        print("本次下注所需總金額 : " + needMoney)
        logging.getLogger("下注紀錄").info(("本次下注所需總金額 : " + needMoney))


        if int(needMoney) > self.dataStorage.betMoneyTotal:
            self.dataStorage.isMoneyEnough = False
            print("餘額剩" + str(self.dataStorage.betMoneyTotal) +"元, 不夠下注，本程式自動關閉")
            logging.getLogger("下注紀錄").warning("餘額剩" + str(self.dataStorage.betMoneyTotal) +"元, 不夠下注，本程式自動關閉")
            return

        self.dataStorage.betMoneyTotal -= int(needMoney)

        if self.dataStorage.model == "F":
            pass
        else:
            pass

        getPriceNumber(self.mainDriver, self.dataStorage)
        print("目前餘額 ： "+ str(self.dataStorage.betMoneyTotal) +"元")