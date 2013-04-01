'''
Created on 2010-11-9

@author: jeffrey
'''

from model.models import MoneyIO, MoneyIOUserType, MoneyIOSysType, MoneyIOTemplate, MoneyTransfer, MoneyBL
from account.service import AccountService

import datetime

BASE_MONEY_INCOME_TYPE = 'INCOME'
BASE_MONEY_EXPENSE_TYPE = 'EXPENSE'
        
class MoneyStat:
    total_income = 0
    total_expense = 0
    currency = None
    income_dict = {}
    expense_dict = {}
        
    def __init__(self, total_income=0, total_expense=0, currency=None, income_dict={}, expense_dict={}):
        self.total_income = total_income
        self.total_expense = total_expense
        self.currency = currency        
        '''
        dict={'moneyiotype_name': totalmoney}
        '''
        self.income_dict = income_dict
        self.expense_dict = expense_dict
    
    def addMoneyIO(self, moneyio):
        try:
            if moneyio.moneyiotype.isio == 1:
                if self.income_dict.has_key(moneyio.moneyiotype.name):
                    self.income_dict[moneyio.moneyiotype.name] = self.income_dict[moneyio.moneyiotype.name] + moneyio.money
                else:
                    self.income_dict[moneyio.moneyiotype.name] = moneyio.money
            if moneyio.moneyiotype.isio == -1:
                if self.expense_dict.has_key(moneyio.moneyiotype.name):
                    self.expense_dict[moneyio.moneyiotype.name] = self.expense_dict[moneyio.moneyiotype.name] + moneyio.money
                else:
                    self.expense_dict[moneyio.moneyiotype.name] = moneyio.money
        except:
            a=1

class MoneyService: 
    
    def getMoneyIOShareList(self, filter_dict, orderby, pagesize, pagecount):
        return self.getMoneyIOList(filter_dict, orderby, pagesize, pagecount, None)        
    
    def moneyTransferEncode(self, moneytransfer_list, sEcho, totalcount):
        result = {"sEcho": sEcho, "iTotalRecords": totalcount, "iTotalDisplayRecords": totalcount}
        item = []
        for moneytransfer in moneytransfer_list:
            item.append(moneytransfer.to_dict())
        result.update({"aaData": item})
        return result
    
    def moneyIOEncode(self, moneyio_list, sEcho, totalcount):
        result = {"sEcho": sEcho, "iTotalRecords": totalcount, "iTotalDisplayRecords": totalcount}
        item = []
        for moneyio in moneyio_list:
            item.append(moneyio.to_dict())
        result.update({"aaData": item})
        return result
    
    def moneyblEncode(self, moneybl_list, sEcho, totalcount):
        result = {"sEcho": sEcho, "iTotalRecords": totalcount, "iTotalDisplayRecords": totalcount}
        item = []
        for moneybl in moneybl_list:
            item.append(moneybl.to_dict())
        result.update({"aaData": item})
        return result
    
    def checkMoneyIOUserTypeNameExist(self, name, id, user):
        moneyiousertype_list = MoneyIOUserType.all().filter('name', name).filter('user', user)
        if moneyiousertype_list.count() == 0:
            return False
        elif moneyiousertype_list.count() == 1:
            if id and moneyiousertype_list[0].id == id:
                return False
            else:
                return True
        else:
            return True 
    
    def getMoneyStatList(self, filter_dict, user):
        currency_list = AccountService().getCurrencyList()
        moneystat_list = []
        for currency in currency_list:
            moneystat = self.getMoneyStat(filter_dict, currency, user)
            if moneystat:
                moneystat_list.append(moneystat)
        
        return moneystat_list
    
    def getMoneyStat(self, filter_dict, currency, user):
        moneyio_list = MoneyIO.all()
        if filter_dict:
            for filter_key in filter_dict.keys():
                moneyio_list = moneyio_list.filter(filter_key, filter_dict[filter_key])
        
        moneyio_list.filter('currency', currency)
        
        if user:
            moneyio_list = moneyio_list.filter('user', user)
        
        moneystat = None
        if moneyio_list.count() > 0:           
            moneystat = MoneyStat(total_income=0, total_expense=0, currency=currency, income_dict={}, expense_dict={})    
            for moneyio in moneyio_list:
                moneystat.addMoneyIO(moneyio)
            
            for income_key in moneystat.income_dict.keys():
                moneystat.total_income = moneystat.total_income + moneystat.income_dict[income_key]
            for expense_key in moneystat.expense_dict.keys():
                moneystat.total_expense = moneystat.total_expense + moneystat.expense_dict[expense_key]

        return moneystat
    
    def getMoneyIOCount(self, filter_dict, user):
        moneyio_list = MoneyIO.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                moneyio_list = moneyio_list.filter(filter_key, filter_dict[filter_key])
        
        if user:
            moneyio_list = moneyio_list.filter('user', user)
           
        return moneyio_list.count()
    
    def getMoneyBLList(self, filter_dict, orderby, pagesize, pagecount, user):
        moneybl_list = MoneyBL.all()
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                moneybl_list = moneybl_list.filter(filter_key, filter_dict[filter_key])
        
        if user:
            moneybl_list = moneybl_list.filter('user', user)
        
        total_records = moneybl_list.count()
        
        if orderby:
            moneybl_list = moneybl_list.order(orderby)
        
        if pagesize > 0:
            moneybl_list = moneybl_list.fetch(pagesize, pagesize * (pagecount-1))
           
        return moneybl_list, total_records
    
    def getMoneyBLCount(self, filter_dict, user):
        moneybl_list = MoneyBL.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                moneybl_list = moneybl_list.filter(filter_key, filter_dict[filter_key])
        
        if user:
            moneybl_list = moneybl_list.filter('user', user)
           
        return moneybl_list.count()
    
    def addMoneyBL(self, account, isio, happentime, money, currency, description, user):
        moneybl = MoneyBL(account = account,
                                      isio = isio,
                                      happentime = happentime,
                                      money = money,
                                      currency = currency,
                                      description = description,
                                      user = user)
        
        moneybl.put()
        AccountService().updateAccountMoney(account, money, isio)

    def editMoneyBL(self, id, account, isio, happentime, money, currency, description, user):
        moneybl = self.getMoneyBL(id, user)
        if moneybl:
            initmoney = moneybl.money
            initaccount = moneybl.account
            initisio = moneybl.isio
            moneybl.account = account
            moneybl.isio = isio
            moneybl.happentime = happentime
            moneybl.money = money
            moneybl.currency = currency
            moneybl.description = description
            if user:
                moneybl.user = user       
            moneybl.put()
            AccountService().updateAccountMoney(initaccount, initmoney, initisio * -1)       
            AccountService().updateAccountMoney(AccountService().getAccount(account.id, user), money, isio)
    
    def deleteMoneyBL(self, id, user):
        moneybl = self.getMoneyBL(id, user)
        if moneybl:
            AccountService().updateAccountMoney(moneybl.account, moneybl.money, moneybl.isio * -1)
            moneybl.delete()
    
    def getMoneyBL(self, id, user):
        moneybl = None
        try:
            moneybl = MoneyBL.get_by_id(int(id))
            if moneybl.user.id <> user.id:
                moneybl = None
        except:
            moneybl = None
        return moneybl
    
    def getMoneyTransferList(self, filter_dict, orderby, pagesize, pagecount, user):
        moneytransfer_list = MoneyTransfer.all()
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                moneytransfer_list = moneytransfer_list.filter(filter_key, filter_dict[filter_key])
        
        if user:
            moneytransfer_list = moneytransfer_list.filter('user', user)
        
        total_records = moneytransfer_list.count()
        
        if orderby:
            moneytransfer_list = moneytransfer_list.order(orderby)
        
        if pagesize > 0:
            moneytransfer_list = moneytransfer_list.fetch(pagesize, pagesize * (pagecount-1))
           
        return moneytransfer_list, total_records
    
    def getMoneyTransferCount(self, filter_dict, user):
        moneytransfer_list = MoneyTransfer.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                moneytransfer_list = moneytransfer_list.filter(filter_key, filter_dict[filter_key])
        
        if user:
            moneytransfer_list = moneytransfer_list.filter('user', user)
           
        return moneytransfer_list.count()
    
    def addMoneyTransfer(self, fromaccount, toaccount, happentime, money, currency, description, user):
        moneytransfer = MoneyTransfer(fromaccount = fromaccount,
                                      toaccount = toaccount,
                                      happentime = happentime,
                                      money = money,
                                      currency = currency,
                                      description = description,
                                      user = user)
        
        moneytransfer.put()
        AccountService().updateAccountMoney(fromaccount, money, -1)
        AccountService().updateAccountMoney(toaccount, money, 1)
    
    def editMoneyTransfer(self, id, fromaccount, toaccount, happentime, money, currency, description, user):
        moneytransfer = MoneyService().getMoneyTransfer(id, user)
        if moneytransfer:
            initmoney = moneytransfer.money
            initfromaccount = moneytransfer.fromaccount
            inittoaccount = moneytransfer.toaccount
            moneytransfer.fromaccount = fromaccount
            moneytransfer.toaccount = toaccount
            moneytransfer.happentime = happentime
            moneytransfer.money = money
            moneytransfer.currency = currency
            moneytransfer.description = description
            if user:
                moneytransfer.user = user       
            moneytransfer.put()
            AccountService().updateAccountMoney(initfromaccount, initmoney, 1)
            AccountService().updateAccountMoney(inittoaccount, initmoney, -1)
            
            AccountService().updateAccountMoney(AccountService().getAccount(fromaccount.id, user), money, -1)            
            AccountService().updateAccountMoney(AccountService().getAccount(toaccount.id, user), money, 1)
    
    def deleteMoneyTransfer(self, id, user):
        moneytransfer = self.getMoneyTransfer(id, user)
        if moneytransfer:
            AccountService().updateAccountMoney(moneytransfer.fromaccount, moneytransfer.money, 1)
            AccountService().updateAccountMoney(moneytransfer.toaccount, moneytransfer.money, -1)
            moneytransfer.delete()
    
    def getMoneyTransfer(self, id, user):
        moneytransfer = None
        try:
            moneytransfer = MoneyTransfer.get_by_id(int(id))
            if moneytransfer.user.id <> user.id:
                moneytransfer = None
        except:
            moneytransfer = None
        return moneytransfer
            
    def getMoneyIOList(self, filter_dict, orderby, pagesize, pagecount, user):
        moneyio_list = MoneyIO.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                moneyio_list = moneyio_list.filter(filter_key, filter_dict[filter_key])

        if user:
            moneyio_list = moneyio_list.filter('user', user)
            
        total_records = moneyio_list.count()
        
        moneyio_list = moneyio_list.order('-happentime')
        if orderby:
            moneyio_list = moneyio_list.order(orderby)
                
        if pagesize > 0:
            moneyio_list = moneyio_list.fetch(pagesize, pagesize * (pagecount-1))
           
        return moneyio_list, total_records
    
    def getMoneyIOListForData(self, filter_dict, orderby, pagesize, pagecount, user):
        moneyio_list = MoneyIO.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                moneyio_list = moneyio_list.filter(filter_key, filter_dict[filter_key])

        if user:
            moneyio_list = moneyio_list.filter('user', user)
        
        if orderby:
            moneyio_list = moneyio_list.order(orderby)
                
        if pagesize > 0:
            moneyio_list = moneyio_list.fetch(pagesize, pagesize * (pagecount-1))
           
        return moneyio_list
    
    def deleteMoneyIO(self, id, user):
        moneyio = self.getMoneyIO(id, user)
        if moneyio:
            AccountService().updateAccountMoney(moneyio.account, moneyio.money, moneyio.moneyiotype.isio * -1)
            moneyio.delete()
    
    def getMoneyIO(self, id, user):
        moneyio = None
        try:
            moneyio = MoneyIO.get_by_id(int(id))
            if moneyio.user.id <> user.id:
                moneyio = None
        except:
            moneyio = None
        return moneyio    
    
    def addMoneyIO(self, account, happentime, moneyiotype, money, currency, isshare, description, user, alarm=None):
        moneyio = MoneyIO()        
        
        moneyio.account = account
        moneyio.happentime = happentime
        moneyio.moneyiotype = moneyiotype
        moneyio.money = money
        moneyio.currency = currency
        moneyio.isshare = isshare
        moneyio.description = description
        if user:
            moneyio.user = user
        if alarm:
            moneyio.alarm = alarm

        moneyio.put()
        
        AccountService().updateAccountMoney(account, money, moneyiotype.isio)
    
    def editMoneyIO(self, id, account, happentime, moneyiotype, money, currency, isshare, description, user, alarm=None):
        moneyio = self.getMoneyIO(id, user)
        if moneyio:
            initaccount = moneyio.account
            initmoney = moneyio.money
            initmoneyiotype = moneyio.moneyiotype
            moneyio.account = account
            moneyio.happentime = happentime
            moneyio.moneyiotype = moneyiotype
            moneyio.money = money
            moneyio.currency = currency
            moneyio.isshare = isshare
            moneyio.description = description
            if user:
                moneyio.user = user
            if alarm:
                moneyio.alarm = alarm   
            moneyio.put()
            AccountService().updateAccountMoney(initaccount, initmoney, initmoneyiotype.isio * -1)
            AccountService().updateAccountMoney(AccountService().getAccount(account.id, user), money, moneyiotype.isio)        
    
    def deleteMoneyIOUserType(self, id, user):
        moneyiousertype = self.getMoneyIOUserType(id, user)
        if moneyiousertype:
            #Create a new base money io type if it does not exist
            basemoneytype = self.getBaseMoneyIOUserType(moneyiousertype)
                    
            moneyio_list = MoneyIO.all().filter('moneyiotype', moneyiousertype)
            for moneyio in moneyio_list:
                moneyio.moneyiotype = basemoneytype
                moneyio.put()
            moneyiousertype.delete()
    
    def getBaseMoneyIOUserType(self, moneyiousertype):
        isio = moneyiousertype.isio
        user = moneyiousertype.user
        if isio == 1:
            moneytypename = BASE_MONEY_INCOME_TYPE
        else:
            moneytypename = BASE_MONEY_EXPENSE_TYPE
        
        basemoneyiotype_list = MoneyIOUserType.all().filter('name', moneytypename).filter('user', user)
        if basemoneyiotype_list.count() == 0:
            basemoneyiotype = MoneyIOUserType(name=moneytypename, isio=isio, user=user)
            basemoneyiotype.put()
        else:
            basemoneyiotype = basemoneyiotype_list[0]
        
        return basemoneyiotype        
    
    def getMoneyIOUserType(self, id, user):
        moneyiousertype = None
        try:
            moneyiousertype = MoneyIOUserType.get_by_id(int(id))
            if moneyiousertype.user.id <> user.id:
                moneyiousertype = None
        except:
            moneyiousertype = None
        return moneyiousertype
    
    def getMoneyIOSysType(self, id):
        try:
            moneyiosystype = MoneyIOSysType.get_by_id(int(id))
        except ValueError:
            moneyiosystype = None
        return moneyiosystype
    
    def getMoneyIOUserTypeChoices(self, user):
        moneyiotype_list = MoneyIOUserType.all()
        if user:
            moneyiotype_list = moneyiotype_list.filter('user', user)
            
        choices=[(moneytype.id, moneytype.display_name) for moneytype in moneyiotype_list]
        return choices
    
    def getMoneyIOUserTypeList(self, user):
        moneyiousertype_list = MoneyIOUserType.all().filter('name !=', BASE_MONEY_INCOME_TYPE).filter('name !=', BASE_MONEY_EXPENSE_TYPE)
        if user:
            moneyiousertype_list = moneyiousertype_list.filter('user', user)
        
        #moneyiousertype_list = moneyiousertype_list.order('-isio')
        if moneyiousertype_list.count() == 0:
            moneyiousertype_list = None
        
        return moneyiousertype_list
    
    def getMoneyIOUserTypeCount(self, user):
        moneyiousertype_list = MoneyIOUserType.all()
        if user:
            moneyiousertype_list = moneyiousertype_list.filter('user', user)
            
        if moneyiousertype_list:
            count = moneyiousertype_list.count()
        else:
            count = 0
        return count
    
    def addMoneyIOUserType(self, name, isio, user):
        moneyiousertype = MoneyIOUserType(name=name, isio=isio, user=user)
        moneyiousertype.put()
    
    def editMoneyIOUserType(self, id, name, isio, user):
        moneyiousertype = MoneyService().getMoneyIOUserType(id, user)
        if moneyiousertype:
            moneyiousertype.name = name
            moneyiousertype.isio = isio
            moneyiousertype.user = user
            moneyiousertype.put()
    
    def initMoneyIOUserTypeFromSystem(self, user):        
        moneyiousertype_list = MoneyIOUserType.all().filter('user', user)
        for moneyiousertype in moneyiousertype_list:
            moneyiousertype.delete()
        
        moneyiosystype_list = MoneyIOSysType.all()
        for moneyiosystype in moneyiosystype_list:
            moneyiousertype = MoneyIOUserType(name=moneyiosystype.name)
            moneyiousertype.isio = moneyiosystype.isio
            moneyiousertype.user = user
            moneyiousertype.put()

    def createMoneyIOTemplate(self, alarm):
        if alarm.isautogenmoneyio:
            moneyiotemplate_list = MoneyIOTemplate.all().filter('alarm', alarm)
            for moneyiotemplate in moneyiotemplate_list:
                moneyiotemplate.delete()
            
            description='Auto generate this template by ' + alarm.name + ' on ' + str(datetime.datetime.now())
            moneyiotemplate = MoneyIOTemplate(moneyiotype=alarm.moneyiousertype,
                                              money=alarm.money,
                                              currency=alarm.currency,
                                              account=alarm.account,
                                              user=alarm.user,
                                              alarm = alarm,
                                              description=description
                                              )
            moneyiotemplate.put()