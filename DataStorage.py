
class DataStorage:
    def __init__(self, parmList : list):
        self.period = ""
        self.compareDataList = [[], [], [], [], [], [], [], [], [], []]
        self.countList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.countOfRequest = 0 #計數 統計總共已經發出多少次資料請求
        self.ifBet = False   #用來判斷是否開始下注
        self.ifBetMiddle = False
        self.indexOfBet = [] #用來放要下哪幾名的注
        self.BetSymbolList = [] # 用來放下注號碼的 id
        self.model = parmList[0] # 預設使用模擬模式
        self.betAmountList = parmList[4] # 預設下注金額為最低十元
        self.betMoneyTotal = parmList[5] # 預設最高資金準備為500元
        self.betPeriod = ""
        self.betTime = parmList[3]
        self.betTimeCount = 0
        self.isMoneyEnough = True
        self.gainMoneyUplimit = parmList[8]
        self.coolNumber = parmList[1]
        self.observeTime = parmList[2]
        self.username = parmList[6]
        self.password = parmList[7]
        self.ifDetect = True


