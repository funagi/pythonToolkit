'''
Created on 2010-11-17

@author: jeffrey
'''
from google.appengine.ext import db
from django.utils.translation import ugettext
import datetime

class MyBaseModel(db.Model):
    @property
    def id(self):
        return str(self.key().id())
    
    def to_head(self, attrnamelist):
        if attrnamelist == None or len(attrnamelist) == 0:
            return self.to_dict_head_all()
        
        result = []
        for attrname in attrnamelist:            
            result.append(ugettext(attrname))
        
        return result
    
    def to_dict(self, attrnamelist):
        if attrnamelist == None or len(attrnamelist) == 0:
            return self.to_dict_all()
        
        result = []
        for attrname in attrnamelist:
            attrvalue = self.__getattribute__(attrname)
            if isinstance(attrvalue,datetime.datetime):
                attrvalue = datetime.datetime.strftime(attrvalue, '%Y-%m-%d %H:%M:%S')
            elif isinstance(attrvalue, datetime.date):
                attrvalue = datetime.date.strftime(attrvalue, '%Y-%m-%d')
            elif isinstance(attrvalue, float):
                attrvalue = '%10.2f' % attrvalue
            elif isinstance(attrvalue, db.Key):
                attrvalue = attrvalue.__unicode__()
            elif isinstance(attrvalue, bool):
                if attrvalue:
                    attrvalue = ugettext('Yes')
                else:
                    attrvalue = ugettext('No')
            
            result.append(attrvalue)
        
        return result
    
    def to_dict_head_all(self):        
        attrnamelist = self.__dict__.keys()
        
        result = []
        for attrname in attrnamelist:            
            result.append(ugettext(attrname))
        
        return result
    
    def to_dict_all(self):
        attrnamelist = self.properties().keys()
        
        result = []
        for attrname in attrnamelist:
            attrvalue = self.__getattribute__(attrname)
            if isinstance(attrvalue,datetime.datetime):
                attrvalue = datetime.datetime.strftime(self.createtime, '%Y-%m-%d %H:%M:%S')
            elif isinstance(attrvalue, datetime.date):
                attrvalue = datetime.date.strftime(self.createtime, '%Y-%m-%d')
            elif isinstance(attrvalue, float):
                attrvalue = '%10.2f' % attrvalue
            elif isinstance(attrvalue, db.Key):
                attrvalue = attrvalue.__unicode__()
            elif isinstance(attrvalue, bool):
                if attrvalue:
                    attrvalue = ugettext('Yes')
                else:
                    attrvalue = ugettext('No')
            
            result.append(attrvalue)
        
        return result

class HelpText(MyBaseModel):
    title = db.StringProperty(multiline=False,required=True)    
    category = db.StringProperty(required=True)
    abstract = db.StringProperty(default='')   
    content = db.TextProperty(default='')
    createtime = db.DateTimeProperty(auto_now_add=True)

class CoolUser(MyBaseModel):
    userid = db.StringProperty()
    name = db.StringProperty(required=True)
    gender = db.IntegerProperty(choices=[0,1], default=0)
    logo = db.LinkProperty()
    email = db.EmailProperty()
    isreceivemail = db.BooleanProperty(default=False)
    pagecount = db.IntegerProperty(default=10)
    usertype = db.StringProperty()
    createtime = db.DateTimeProperty(auto_now_add=True)
    lastlogtime = db.DateTimeProperty(auto_now=True)
    newmessagecount = db.IntegerProperty(default=0)
    googleid = db.StringProperty()
    sinaid = db.IntegerProperty()
    
    def __unicode__(self):
        return self.name
    
    @property
    def totalmoney(self):
        return 0.0
    
    @property
    def totalmoneyiocount(self):
        return 0

class UserMessage(MyBaseModel):
    user = db.ReferenceProperty(CoolUser)
    title = db.StringProperty(required=True)
    content = db.TextProperty()
    isread = db.BooleanProperty(default=False)
    createtime = db.DateTimeProperty(auto_now_add=True)
    
    def __unicode__(self):
        return self.title
    
    def to_dict(self):
        result = []
        result.append(self.title)
        result.append(self.content)
        if self.isread:
            result.append(ugettext('Yes'))
        else:
            result.append(ugettext('No'))
        result.append(datetime.datetime.strftime(self.createtime, '%Y-%m-%d %H:%M:%S'))
        result.append('<a href="/message/%s/">%s</a> <span> |</span><a href="/message/delete/%s/">%s</a>' 
                      % (self.id, ugettext('View'), self.id, ugettext('Delete')))
        return result
    
class Currency(MyBaseModel):
    name = db.StringProperty(required=True)
    symbol = db.StringProperty(required=True)
    
    def __unicode__(self):
        return self.symbol 

class AccountType(MyBaseModel):
    name = db.StringProperty(required=True)
    canadvance = db.BooleanProperty(default=False)
    
    def __unicode__(self):
        return self.name
    
class Account(MyBaseModel):
    user = db.ReferenceProperty(CoolUser)
    name = db.StringProperty(required=True)
    type = db.ReferenceProperty(AccountType)
    currency = db.ReferenceProperty(Currency)
    description = db.StringProperty(multiline=True)
    isclosed = db.BooleanProperty(default=False)
    initmoney = db.FloatProperty(default=0.0)
    totalmoney = db.FloatProperty(default=0.0)
    createtime = db.DateTimeProperty(auto_now_add=True)

    def __unicode__(self):
        if self.isclosed:
            return self.name + '(' + 'closed' + ')'
        else:
            return self.name
    
    def to_dict(self):
        result = []
        result.append(self.name)
        result.append(self.type.name);
        result.append('%10.2f %s' % (self.totalmoney, self.currency.symbol))
        result.append(datetime.date.strftime(self.createtime, '%Y-%m-%d'))
        if self.isclosed:
            result.append('<a href="/account/open/%s/">%s</a> <span> |</span><a href="/account/%s/">%s</a>'  % (self.id, ugettext('Open Account'), self.id, ugettext('View')))
        else:
            result.append('<a href="/account/%s/">%s</a> <span> |</span><a href="/account/edit/%s/">%s</a> <span> |</span><a href="/account/delete/%s/">%s</a>' 
                      % (self.id, ugettext('View'), self.id, ugettext('Edit'), self.id, ugettext('Delete')))
        
        return result
        

class MoneyIOSysType(MyBaseModel):
    name = db.StringProperty(required=True)
    '''uppertype = db.SelfReferenceProperty()'''
    '''1=input, -1=output'''
    isio = db.IntegerProperty(default=1)
    createtime = db.DateTimeProperty(auto_now_add=True) 
    
    def __unicode__(self):
        if self.isio == 1:
            isiotype = 'Income'
        elif self.isio == -1:
            isiotype = 'Expense'  
        
        result = ''
        result = result.join(isiotype)
        result = result.join(' | ')
        result = result.join(self.name)        
        return result


class MoneyIOUserType(MyBaseModel):
    name = db.StringProperty(required=True)
    '''uppertype = db.SelfReferenceProperty()'''
    '''1=input, -1=output'''
    isio = db.IntegerProperty(default=1)
    user = db.ReferenceProperty(CoolUser)
    createtime = db.DateTimeProperty(auto_now_add=True)
    
    @property
    def display_name(self):
        if self.isio == 1:
            isiotype = ugettext('Income')
        elif self.isio == -1:
            isiotype = ugettext('Expense')  
        
        result = isiotype + ' | ' + self.name    
        return result
    
    def __unicode__(self):
        if self.isio == 1:
            isiotype = ugettext('Income')
        elif self.isio == -1:
            isiotype = ugettext('Expense')  
        
        result = isiotype + ' | ' + self.name    
        return result

class Alarm(MyBaseModel):
    user = db.ReferenceProperty(CoolUser)
    name = db.StringProperty(required=True)
    account = db.ReferenceProperty(Account)    
    begindate = db.DateProperty()
    enddate = db.DateProperty()
    cycletype = db.StringProperty(choices=set(['Year', 'Month', 'Week', 'Day']))
    cyclevalue = db.IntegerProperty(default=1)
    isautogenmoneyio = db.BooleanProperty(default=False)    
    moneyiousertype = db.ReferenceProperty(MoneyIOUserType)
    money = db.FloatProperty(default = 0.0)
    currency = db.ReferenceProperty(Currency)
    latestalarmtime = db.DateTimeProperty(auto_now_add=True)
    description = db.StringProperty(multiline=True)
    createtime = db.DateTimeProperty(auto_now_add=True)
    
    def __unicode__(self):
        return self.name
    
    def to_dict(self):
        result = []
        
        result.append(self.name)
        result.append(self.account.name)
        if self.begindate:
            result.append(datetime.date.strftime(self.begindate, '%Y-%m-%d'))
        else:
            result.append('')
        if self.enddate:
            result.append(datetime.date.strftime(self.enddate, '%Y-%m-%d'))
        else:
            result.append('')
        result.append(ugettext(self.cycletype))
        result.append(self.cyclevalue)
        result.append('<a href="/alarm/%s/">%s</a> <span> |</span><a href="/alarm/edit/%s/">%s</a> <span> |</span><a href="/alarm/delete/%s/">%s</a>' 
                      % (self.id, ugettext('View'), self.id, ugettext('Edit'), self.id, ugettext('Delete')))        
        
        return result

class MoneyTransfer(MyBaseModel):
    user = db.ReferenceProperty(CoolUser)
    happentime = db.DateProperty()    
    fromaccount = db.ReferenceProperty(Account, collection_name="MoneyTransfer_fromaccount_set")
    toaccount = db.ReferenceProperty(Account, collection_name="MoneyTransfer_toaccount_set")
    money = db.FloatProperty(default=0.0)
    currency = db.ReferenceProperty(Currency)
    description = db.StringProperty(multiline=True)
    createtime = db.DateTimeProperty(auto_now_add=True)
    
    def to_dict(self):
        result = []
        if self.happentime:
            result.append(datetime.datetime.strftime(self.happentime, '%Y-%m-%d'))
        else:
            result.append('')
        result.append('<a href="/account/%s">%s</a>' % (self.fromaccount.id, self.fromaccount.name))
        result.append('<a href="/account/%s">%s</a>' % (self.toaccount.id, self.toaccount.name))
        result.append("%10.2f %s" %(self.money, self.currency.symbol))
        result.append('<a href="/moneytransfer/edit/%s/">%s</a> <span> |</span><a href="/moneytransfer/delete/%s/">%s</a>' 
                      % (self.id, ugettext('Edit'), self.id, ugettext('Delete')))
        return result

class MoneyBL(MyBaseModel):
    user = db.ReferenceProperty(CoolUser)
    happentime = db.DateProperty()    
    account = db.ReferenceProperty(Account)
    '''1=borrow, -1=lend'''
    isio = db.IntegerProperty(default=1)
    money = db.FloatProperty(default=0.0)
    currency = db.ReferenceProperty(Currency)
    description = db.StringProperty(multiline=True)
    createtime = db.DateTimeProperty(auto_now_add=True)
    
    def to_dict(self):
        result = []
        if self.happentime:
            result.append(datetime.datetime.strftime(self.happentime, '%Y-%m-%d'))
        else:
            result.append('')
        result.append('<a href="/account/%s">%s</a>' % (self.account.id, self.account.name))
        if self.isio == 1:
            result.append(ugettext('Borrow'))
        else:
            result.append(ugettext('Lend'))
        result.append("%10.2f %s" %(self.money, self.currency.symbol))
        result.append('<a href="/moneybl/edit/%s/">%s</a> <span> |</span><a href="/moneybl/delete/%s/">%s</a>' 
                      % (self.id, ugettext('Edit'), self.id, ugettext('Delete')))
        return result

"""
This model is for money Input & Output
"""
class MoneyIO(MyBaseModel):
    moneyiotype = db.ReferenceProperty(MoneyIOUserType)
    happentime = db.DateProperty()
    money = db.FloatProperty(default=0.0)
    currency = db.ReferenceProperty(Currency)
    description = db.StringProperty(multiline=True)
    account = db.ReferenceProperty(Account) 
    user = db.ReferenceProperty(CoolUser) 
    alarm = db.ReferenceProperty(Alarm)
    createtime = db.DateTimeProperty(auto_now_add=True) 
    isshare = db.BooleanProperty(default=False)
    
    @property
    def id(self):
        return str(self.key().id())
    
    def to_dict(self):
        result = []
        result.append(datetime.datetime.strftime(self.happentime, '%Y-%m-%d'))
        result.append(self.moneyiotype.name)
        result.append(self.description.replace('\n',' '))
        result.append("%10.2f %s" %(self.money, self.currency.symbol))
        result.append('<a href="/account/%s">%s</a>' % (self.account.id, self.account.name))
        result.append('<a href="/moneyio/edit/%s/">%s</a> <span> |</span><a href="/moneyio/delete/%s/">%s</a>' 
                      % (self.id, ugettext('Edit'), self.id, ugettext('Delete')))
        return result

class MoneyIOTemplate(MyBaseModel):
    moneyiotype = db.ReferenceProperty(MoneyIOUserType)
    money = db.FloatProperty(default=0.0)
    currency = db.ReferenceProperty(Currency)
    description = db.StringProperty(multiline=True)
    account = db.ReferenceProperty(Account) 
    user = db.ReferenceProperty(CoolUser) 
    alarm = db.ReferenceProperty(Alarm)   
    createtime = db.DateTimeProperty(auto_now_add=True) 

class Budget(MyBaseModel):
    name = db.StringProperty(required=True)
    begindate = db.DateProperty(required=True)
    enddate = db.DateProperty(required=True) 
    currency = db.ReferenceProperty(Currency)   
    user = db.ReferenceProperty(CoolUser)
    description = db.StringProperty(multiline=True)
    createtime = db.DateTimeProperty(auto_now_add=True)
    
    @property
    def id(self):
        return str(self.key().id())
    
    @property
    def income(self):
        totalamount = 0.0
        budgetdetail_list = BudgetDetail.all().filter('budget', self)        
        for budgetdetail in budgetdetail_list:
            if budgetdetail.moneyiousertype.isio == 1:
                totalamount = totalamount + budgetdetail.money
        return totalamount
    
    @property   
    def expense(self):
        totalamount = 0.0
        budgetdetail_list = BudgetDetail.all().filter('budget', self)        
        for budgetdetail in budgetdetail_list:
            if budgetdetail.moneyiousertype.isio == -1:
                totalamount = totalamount + budgetdetail.money
        return totalamount
    
    def to_dict(self):
        result = []
        result.append(self.name)
        result.append(datetime.date.strftime(self.begindate, '%Y-%m-%d'))
        result.append(datetime.date.strftime(self.enddate, '%Y-%m-%d'))
        result.append('%10.2f %s' % (self.income, self.currency.symbol))
        result.append('%10.2f %s' % (self.expense, self.currency.symbol))
        result.append('<a href="/budget/%s/">%s</a> <span> |</span><a href="/budget/edit/%s/">%s</a> <span> |</span><a href="/budget/delete/%s/">%s</a>' 
                      % (self.id, ugettext('View'), self.id, ugettext('Edit'), self.id, ugettext('Delete')))
        
        return result

class BudgetDetail(MyBaseModel):
    budget = db.ReferenceProperty(Budget)
    moneyiousertype = db.ReferenceProperty(MoneyIOUserType)
    money=db.FloatProperty(default=0.0)
    actualmoney=db.FloatProperty(default=0.0)
    createtime = db.DateTimeProperty(auto_now_add=True)
    
    def difference(self):
        return self.money - self.actualmoney
    
    def to_dict(self):
        result = []
        result.append(self.moneyiousertype.name)
        result.append('%10.2f %s' % (self.money, self.budget.currency.symbol))
        result.append('%10.2f %s' % (self.actualmoney, self.budget.currency.symbol))
        result.append('%10.2f %s' % (self.difference(), self.budget.currency.symbol))
        return result
    
class Object(MyBaseModel):    
    name = db.StringProperty(required=True)
    finishdate = db.DateProperty()
    money = db.FloatProperty(default=0.0)
    currency = db.ReferenceProperty(Currency)
    description = db.StringProperty(multiline=True)
    user = db.ReferenceProperty(CoolUser)
    accountlist = db.StringListProperty()
    createtime = db.DateTimeProperty(auto_now_add=True)
    
    def __unicode__(self):
        return self.name    
    
    @property
    def status(self):
        totalmoney = 0.0
        for account_id in self.accountlist:
            account = Account.get_by_id(int(account_id))
            if account:
                totalmoney = totalmoney + account.totalmoney
        status = 0
        if self.money > 0:
            if totalmoney > self.money:
                status = 1 * 100
            else:
                status = totalmoney/self.money * 100
        return status
    
    def to_dict(self):
        result = []
        result.append(self.name)
        if self.finishdate:
            result.append(datetime.date.strftime(self.finishdate, '%Y-%m-%d'))
        else:
            result.append('')
        result.append('%10.2f %s' % (self.money, self.currency.symbol))
        result.append('%i %s' % (self.status, '%'))
        result.append('<a href="/object/%s/">%s</a> <span> |</span><a href="/object/edit/%s/">%s</a> <span> |</span><a href="/object/delete/%s/">%s</a>' 
                      % (self.id, ugettext('View'), self.id, ugettext('Edit'), self.id, ugettext('Delete')))
        return result