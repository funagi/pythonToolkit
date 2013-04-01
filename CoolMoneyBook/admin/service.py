'''
Created on 2010-11-17

@author: Jeffrey
'''
from model.models import Currency, AccountType, MoneyIOSysType, HelpText
from account.service import AccountService
from money.service import MoneyService

class AdminService:
    
    def encode(self, budgetdetail_list):
        result = {"iTotalRecords": budgetdetail_list.count(), "iTotalDisplayRecords": budgetdetail_list.count()}
        item = []
        for budgetdetail in budgetdetail_list:
            item.append(budgetdetail.to_dict([]))
        result.update({"aaData": item})
        return result
    
    def getHelpTextList(self):
        helptext_list = HelpText.all().order('category').order('-createtime')
        if helptext_list.count() == 0:
            return None
        return helptext_list
    
    def getCategoryHelpTextList(self, category):
        helptext_list = HelpText.all().filter('category', category).order('createtime')
        if helptext_list.count() == 0:
            return None
        return helptext_list
    
    def getHelpText(self, id):
        try:
            helptext = HelpText.get_by_id(int(id))
        except:
            helptext = None
        return helptext
    
    def editHelpText(self, id, title, category, abstract, content):
        helptext = AdminService().getHelpText(id)
        if helptext:
            helptext.title = title
            helptext.category = category
            helptext.abstract = abstract
            helptext.content = content
            helptext.put()
    
    def deleteHelpText(self, id):
        helptext = AdminService().getHelpText(id)
        if helptext:
            helptext.delete()
    
    def addHelpText(self, title, category, abstract, content):
        helptext = HelpText(title=title, category=category, abstract=abstract, content=content)
        helptext.put()
        
    def getCurrencyList(self):
        currency_list = Currency.all().order('name')
        if currency_list.count() == 0:
            return None
        return currency_list
    
    def addCurrency(self, name, symbol):
        currency = Currency(name=name, symbol=symbol)
        currency.put()
        
    def editCurrency(self, id, name, symbol):
        currency = AccountService().getCurrency(id)
        if currency:
            currency.name = name
            currency.symbol = symbol
            currency.put()
    
    def deleteCurrency(self, id):
        currency = AccountService().getCurrency(id)
        if currency:
            currency.delete()
    
    def getAccountTypeList(self):
        accounttype_list = AccountType.all().order('name')
        if accounttype_list.count() == 0:
            return None
        return accounttype_list
    
    def addAccountType(self, name, canadvance):
        accounttype = AccountType(name=name, canadvance=canadvance)
        accounttype.put()
        
    def editAccountType(self, id, name, canadvance):
        accounttype = AccountService().getAccountType(id)
        if accounttype:
            accounttype.name = name
            accounttype.canadvance= canadvance
            accounttype.put()
    
    def deleteAccountType(self, id):
        accounttype = AccountService().getAccountType(id)
        if accounttype:
            accounttype.delete()
    
    def getMoneyIOSysTypeList(self):
        moneyiosystype_list = MoneyIOSysType.all().order('name')
        if moneyiosystype_list.count() == 0:
            return None        
        return moneyiosystype_list
    
    def addMoneyIOSysType(self, name, isio):
        moneyiosystype = MoneyIOSysType(name=name, isio=isio)
        moneyiosystype.put()
        
    def editMoneyIOSysType(self, id, name, isio):
        moneyiosystype = MoneyService().getMoneyIOSysType(id)
        if moneyiosystype:
            moneyiosystype.name = name
            moneyiosystype.isio = isio
            moneyiosystype.put()
    
    def deleteMoneyIOSysType(self, id):
        moneyiosystype = MoneyService().getMoneyIOSysType(id)
        if moneyiosystype:
            moneyiosystype.delete()