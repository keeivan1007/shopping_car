"""  ===執行程式碼區===

流程： 程式實體化 → 輸入商品類別 → 開始跑購物車(題目一) Case_A、Case_B

有待開發：1.(程式碼) 因經驗不夠純熟，時間等因素，故Input無設，正規表達式(re)、規定格式等限制。

         2.(測試)對CI跟單元測試有概念，但程式碼沒做到這塊。

"""


all_class = {}

all_class['電子'] = ['ipad','iphone','螢幕','筆記型電腦','鍵盤']
all_class['食品'] = ['麵包','餅乾','蛋糕','牛肉','魚','蔬菜']
all_class['日用品'] = ['餐巾紙','收納箱','咖啡杯','雨傘']
all_class['酒類'] = ['啤酒','白酒','伏特加']

#===== Case A =====

Case_A = pos_machine() # 初始化
Case_A.insert_modify_produce_class_dict(all_class) # 匯入所有商品的類別
Case_A.added_discount_days('2015-11-11','電子',0.7) # 輸入促銷資訊

Case_A.purchase(1,'ipad',2399)
Case_A.purchase(1,'螢幕',1799)
Case_A.purchase(12,'啤酒',25)
Case_A.purchase(5,'麵包',9)

Case_A.use_discount(1000,200,'2015-11-11','2016-3-2') #使用優惠券　2017-9-7　使用　，期限：2017-12-12　滿一千抵五百

print('Case A total cost : ' + str(Case_A.checkout_with_day('2015-11-11')))

#===== Case B =====

Case_B = pos_machine() # 初始化
Case_B.insert_modify_produce_class_dict(all_class) # 匯入所有商品的類別

Case_B.purchase(3,'蔬菜',5.98)
Case_B.purchase(8,'餐巾紙',3.20)

print('Case B total cost : ' + str(Case_B.checkout_with_day('2015-1-1')))


"""

purpose:進行商品購物車結帳

進行每次支付(購物車結帳)就建立個實體　ex: Mr_Wang_checkout = pos_machine

added_discount_days：新增折扣資訊　ex: Mr_Wang_checkout.added_discount_days('2017-9-8','攝影器材',0.7)
input：added_discount_days(時間，商品類型，折扣％數)　

insert_modify_produce_class：整理商品的類別  ex:Mr_Wang_checkout.insert_modify_produce_class('牙刷','清潔用品')
input： insert_modify_produce_class(商品名稱，商品類型)

check_discount_days：查該日期有哪些商品優惠　ex:Mr_Wang_checkout.check_discount_days('2017-9-8')
input：check_discount_daye(日期)　output：該天商品優惠資訊

purchase：消費購買，僅限同種商品但不限數量　ex:Mr_Wang_checkout.purchase(2,'牙籤',1000)
input：purchase(商品數量，商品名稱，商品單價)

__purchase_cost：查看該商品的消費總金額　ex:Mr_Wang_checkout.__purchase_cost['牙膏']
input：__purchase_cost(商品名稱)　output：該商品總消費金額

use_discount：使用優惠券　ex:Mr_Wang_checkout.use_discount(1000,500,'2017-09-07','2017-12-12') 
input：use_discount(限制金額，消費抵用額，使用時間，限制時間) output：成功或失敗的訊息

checkout_with_day：結帳，根據使用日期幫有做有做優惠的商品打折，結算總金額 ex:Mr_Wang_checkout.checkout_with_day('2017-9-8')
input：checkout_with_day(結帳日期)  output：總消費金額

print(Mr_Wang_checkout) 打印出購物車整體狀況，購買的商品細目，總金額，與是否用過購物券

"""

class pos_machine:
    
    # 類別變數，改變後所有實體皆可使用
    __discount_days = {} # 折扣資訊  {日期}:{{類別{:{折扣數量}
    __produce_class = {} # {'商品名稱':'商品類別'} 
     
    
    def __init__(self):
    
        self.__purchase_details = {} # 消費細目_商品.數量
        self.__purchase_cost = {} #消費細目_商品.總消費
        self.__sum_cost = 0 # 消費總金額
        self.__shoping_date = ''
        self.__not_had_discount = True
        self.__total_offset = 0
        # self.offset_discount_cost = 0 # 抵用折扣後總金額
        
    def __str__(self):
        
        #迴圈把商品組合跟數量加入進字串
        
        if self.__purchase_details:
            purchase_items_str = ''
            for i,k in self.__purchase_details.items():
                purchase_items_str = purchase_items_str + i + ":" + str(k) + '個;'
            
        #判斷有無使用過值價券
            __not_had_discount_str = 'had not use discound record' if self.__not_had_discount else 'had ues discound record'
            
            return 'the shopping basket have ' + purchase_items_str + 'total:'+ str(self.__sum_cost) +' NT,'+__not_had_discount_str
        else: 
            return 'had no buy everything'
            
    
    # 產品購買
    def purchase(self,num,produce,price): #購買- 數量/商品名稱/價格
        
        import copy
        
        SPD = copy.copy(self.__purchase_details)
        SPC = copy.copy(self.__purchase_cost)
            
        try: # 控制交易
            
            if produce in SPD:
                SPD[produce] = SPD[produce] + num 
            else:
                SPD[produce] = num

            if produce in SPC:
                SPC[produce] = SPC[produce] + num * price
            else:
                SPC[produce] = num * price
                
        except Axception as e: # 如果中間出現問題，物件本身屬性沒改
            print('we have problem in purchase(),detail:transaction control,log:{}'.format(e))
        
        self.__purchase_details = SPD # 到這裡交易中沒問題，才真正改資訊
        self.__purchase_cost = SPC
        
        self.__sum_cost = sum(SPC.values()) # 把每個商品賺到的錢取出來總結算
    
    
    #　新增折扣優惠資訊
    def added_discount_days(self,datetime,produce_class,discount): # 輸入折購優惠日期/產品類別/折扣趴數
        
        if datetime in self.__discount_days: #如果該日已經有儲存過商品優惠資訊，則新增
            self.__discount_days[datetime][produce_class] = discount
        
        else: #　如果該天都無任何商品優惠資訊，則建立　；　並在該天建立該商品優惠資訊
            self.__discount_days[datetime] = {produce_class:discount}
        
        
    #　刪除折扣優惠資訊
    def delete_discount_days(self,datetime,produce_class=None): # 刪除折扣項目 
        
        if produce_class == None:                           # 只輸入日期就刪除當天所有商品優惠
            del self.__discount_days[time]
        else:                                               # 日期加上商品則刪除當天該類型商品的優惠
            del self.__discount_days[time][produce_class]
            
    def check_discount_days(self,datetime):
        
        return_text = ''
        if datetime in self.__discount_days:
            for i,a in self.__discount_days[datetime].items():
                return_text = return_text + i + ':' + str(a) + '；'
            return return_text
        else:
            return_text = 'have no discount in ' + datetime
            return return_text
            
    #　新增 and 修改商品類別
    def insert_modify_produce_class(self,produce_name,produce_class):
        self.__produce_class[produce_name] = produce_class
        
    #　新增 and 修改商品類別_dict
    def insert_modify_produce_class_dict(self,produce_class_dict):
        
        for i,o in produce_class_dict.items(): # 把類別跟商品組合的list拆開來
            
            for a in o: # 讓list跑迴圈，登記是甚麼類別
                
                self.__produce_class[a] = i
            
    #　查看該商品的類別
    def check_produce_class(self,produce_name):
        return self.__produce_class[produce_name]
    
    
    @property
    def sum_cost(self):
        return self.__sum_cost
    
    #　使用折扣優惠券
    def use_discount(self,limit_cash,offset,use_date,effective_date):
        
        from datetime import datetime as Dd #匯入timedelta格式讓時間可以比大小
        format_str = "%Y-%m-%d" #時間的格式
        
        # 條件判斷時間、限制金額、有否使用過折價券
        if Dd.strptime(use_date,format_str)<Dd.strptime(effective_date,format_str) and self.__sum_cost > limit_cash and self.__not_had_discount:
            
            self.__not_had_discount = False # 表示該客人已使用過一次抵用券
            self.__sum_cost = self.__sum_cost - offset # 條件通過則總金額扣除抵用金額
            self.__total_offset = self.__total_offset + offset # 紀錄折扣累積總金額
            return 'you success offset ' + str(offset) + 'NT, Think you!'
        else:
            error_str = 'Sorry!'
            if Dd.strptime(use_date,format_str)>Dd.strptime(effective_date,format_str) : error_str = error_str+ 'effective time is overd;'
            if self.__sum_cost < limit_cash : error_str = error_str + 'the limit limit cash more sum cost;'
            if self.__not_had_discount == False : error_str = error_str + 'you had use discount-cost once time'
            return error_str  # 回傳錯誤訊息
    
    #  結算，與sum_cost不同，會根據
    def checkout_with_day(self,checkout_time):
        
        if checkout_time in self.__discount_days:
            this_date_discounts = self.__discount_days[checkout_time] # 取出當天優惠資訊，參考變數

            for i,o in self.__purchase_cost.items(): # 讓每個商品去對照，使用迴圈查找
                this_produce_class = self.__produce_class[i] # 該商品的商品類別

                if this_produce_class in this_date_discounts: # 該商品類別對照，當天有無優惠類別
                    self.__purchase_cost[i] = o * this_date_discounts[this_produce_class] #　有的話則讓該商品總消費進行折扣
        
        return round(sum(self.__purchase_cost.values()) - self.__total_offset,2)