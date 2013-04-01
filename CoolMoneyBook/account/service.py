'''
Created on 2010-11-9

@author: jeffrey
'''

from model.models import *

class AccountService:
    
    def accountEncode(self, account_list, sEcho, total_records):
        result = {"sEcho": sEcho, "iTotalRecords": total_records, "iTotalDisplayRecords": total_records}
        item = []
        for account in account_list:
            item.append(account.to_dict())
        result.update({"aaData": item})
        return result
    
    '''
    def updateObjectStatus(self, object):
        if object:
            totalmoney = 0.0
            for account_id in object.accountlist:
                account = self.getAccount(account_id, object.user)
                if account:
                    totalmoney = totalmoney + account.totalmoney
            status = 0
            if object.money > 0:
                if totalmoney > object.money:
                    status = 1 * 100
                else:
                    status = totalmoney/object.money * 100
            object.status = int(status)
            object.put()
    '''

    def getObjectListByAccount(self, account_id, user):
        object_list = Object.all() 
        
        if user:
            object_list = object_list.filter('user', user)
        
        object_list.filter('accountlist', account_id)
           
        return object_list
    
    def checkAccountNameExist(self, name, id, user):
        account_list = Account.all().filter('name', name).filter('user', user)
        if account_list.count() == 0:
            return False
        elif account_list.count() == 1:
            if id and account_list[0].id == id:
                return False
            else:
                return True
        else:
            return True            
        
    def getAccountChoices(self, user):
        account_list = Account.all().filter('isclosed', False)
        if user:
            account_list = account_list.filter('user', user)
        
        choices=[(account.id,account.name) for account in account_list]            
        return choices
    
    def getAccountCount(self, filter_dict, user):
        account_list = Account.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                account_list = account_list.filter(filter_key, filter_dict[filter_key])
        
        if user:
            account_list = account_list.filter('user', user)
           
        return account_list.count()
    
    def getAccountListByIDList(self, id_list, user):
        account_list = []
        for id in id_list:
            account = self.getAccount(id, user)
            if account:
                account_list.append(account)
        if len(account_list) == 0:
            account_list = None
        return account_list
    
    def getAccountList(self, filter_dict, orderby, pagesize, pagecount, user):
        account_list = Account.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                account_list = account_list.filter(filter_key, filter_dict[filter_key])
        
        if user:
            account_list = account_list.filter('user', user)
        
        total_records = account_list.count()
        
        if orderby:
            account_list = account_list.order(orderby)
        
        if pagesize > 0:
            account_list = account_list.fetch(pagesize, pagesize * (pagecount-1))
           
        return account_list, total_records
    
    def deleteAccount(self, id, user):
        account = self.getAccount(id, user)
        if account:
            if self.checkAccountCanDelete(account):
                account.delete()
            else:
                account.isclosed = True
                account.put()
    
    def openAccount(self, id, user):
        account = self.getAccount(id, user)
        if account and account.isclosed == True:
            account.isclosed = False
            account.put()            
    
    def checkAccountCanDelete(self, account):
        result = True
        if Alarm.all().filter('account', account).count() > 0:
            return False
        if MoneyTransfer.all().filter('fromaccount', account).count() > 0:
            return False
        if MoneyTransfer.all().filter('toaccount', account).count() > 0:
            return False
        if MoneyIO.all().filter('account', account).count() > 0:
            return False
        if MoneyIOTemplate.all().filter('account', account).count() > 0:
            return False
        if MoneyTransfer.all().filter('fromaccount', account).count() > 0:
            return False
        if MoneyTransfer.all().filter('toaccount', account).count() > 0:
            return False
        if MoneyBL.all().filter('account', account).count() > 0:
            return False
        if Object.all().filter('accountlist', account.id).count() > 0:
            return False
        return result
    
    def getAccount(self, id, user):
        account = None
        try:
            account = Account.get_by_id(int(id))
            if account.user.id <> user.id:
                account = None
        except:
            account = None
        return account
    
    def addAccount(self, name, type, currency, initmoney, description, user):
        account = Account(name=name)
        account.type = type
        account.currency = currency
        account.initmoney = initmoney
        account.totalmoney = account.totalmoney + initmoney
        account.description = description
        if user:
            account.user = user        
        account.put()
        
    def editAccount(self, id, name, type, currency, initmoney, description, user):
        account = self.getAccount(id, user)
        if account:            
            account.name = name
            account.type = type
            account.currency = currency             
            old_initmoney = account.initmoney 
            account.initmoney = initmoney          
            account.totalmoney = account.totalmoney - old_initmoney + initmoney
            account.description = description 
            if user:
                account.user = user       
            account.put()
    
    def getAccountTypeChoices(self):
        choices=[(accounttype.id, accounttype.name) for accounttype in AccountType.all()]
        return choices
    
    def getCurrencyList(self):
        return Currency.all()
    
    def getCurrencyChoices(self):
        choices=[(currency.id,currency.symbol) for currency in Currency.all()]
        return choices
    
    def getAccountType(self, id):
        try:
            accounttype = AccountType.get_by_id(int(id))
        except ValueError:
            accounttype = None
        return accounttype
        
            
    def getCurrency(self, id):
        try:
            currenncy = Currency.get_by_id(int(id))
        except ValueError:
            currenncy =None
        return currenncy
    
    def updateAccountMoney(self, account, money, isio):
        try:
            account.totalmoney = account.totalmoney + money * isio
            account.put()
        except:
            '''Do Nothing'''