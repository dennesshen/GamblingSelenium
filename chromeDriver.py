import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from exception_gamble import ExecuteOverErrorLimitException


class GambleDriver:

    def __init__(self, driverPath: str):
        self.driverPath = driverPath
        self.driver: WebDriver = webdriver.Chrome(self.driverPath)

    def runPageByURL(self, url: str):
        self.driver.get(url)
        self.driver.implicitly_wait(10)

    def execute_with_errorLimit(self, errorLimit: int, function):
        errorTime = 0
        while errorTime < errorLimit:
            try:
                time.sleep(1)
                function()
                return

            except Exception as e:
                print(str(function.__name__) + "錯誤" + str(errorTime))
                logging.error(str(function.__name__) + "錯誤" + str(errorTime))
                print(e)
                logging.error(str(e.args))
                errorTime += 1

        raise ExecuteOverErrorLimitException(str(function.__name__) + "執行多次持續錯誤")
