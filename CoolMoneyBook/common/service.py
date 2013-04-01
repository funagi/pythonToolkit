'''
Created on 2010-12-1

@author: jeffrey
'''
from django.utils.translation import ugettext
from django.utils.simplejson import JSONEncoder

from account.service import AccountService
from budget.service import BudgetService
from alarm.service import AlarmService
from object.service import ObjectService
from money.service import MoneyService
from cooluser.service import UserService

model_column_dict = {'account':['name', 'type', 'totalmoney', 'createtime'],
                     'alarm':['name', 'begindate', 'enddate', 'cycletype', 'cyclevalue'],
                     'object':['name', 'finishdate', 'money'],
                     'budget':['name', 'begindate', 'enddate'],
                     'moneyio':['happentime', 'moneyiotype', 'money', 'account'],
                     'moneybl':['happentime', 'account', 'isio', 'money'],
                     'moneytransfer':['happentime', 'fromaccount', 'toaccount', 'money'],
                     'usermessage':['title', 'content', 'isread', 'createtime']
                     }

class PageInfo:
    user = None
    page_menu_name = ''
    page_title = ''    
    page_size = 0

    
    def __init__(self, page_menu_name=None, user=None, page_title=None):
        self.page_menu_name = page_menu_name
        if page_title:
            self.page_title = page_title
        else:
            self.page_title = ugettext(page_menu_name)
        self.user = user        
        self.page_size = self.user.pagecount
        if self.page_size < 1 or self.page_size > 50:
            self.page_size = 10

class CommonService:
    
    def getModelList(self, model_name, filter_dict, orderby, pagesize, pagecount, user):
        if model_name == 'account':
            return AccountService().getAccountList(filter_dict, orderby, pagesize, pagecount, user)
        elif model_name == 'budget':
            return BudgetService().getBudgetList(filter_dict, orderby, pagesize, pagecount, user)
        elif model_name == 'alarm':
            return AlarmService().getAlarmList(filter_dict, orderby, pagesize, pagecount, user)
        elif model_name == 'object':
            return ObjectService().getObjectList(filter_dict, orderby, pagesize, pagecount, user)
        elif model_name == 'moneyio':
            return MoneyService().getMoneyIOList(filter_dict, orderby, pagesize, pagecount, user)
        elif model_name == 'moneybl':
            return MoneyService().getMoneyBLList(filter_dict, orderby, pagesize, pagecount, user)
        elif model_name == 'moneytransfer':
            return MoneyService().getMoneyTransferList(filter_dict, orderby, pagesize, pagecount, user)
        elif model_name == 'usermessage':
            return UserService().getMessageList(filter_dict, orderby, pagesize, pagecount, user)
        
    def getModelCount(self, model_name, filter_dict, user):
        if model_name == 'account':
            return AccountService().getAccountCount(filter_dict, user)
    
    def getJSONData(self, model_list, sEcho, total_records):
        data = {"sEcho": sEcho, "iTotalRecords": total_records, "iTotalDisplayRecords": total_records}
        item = []
        for model in model_list:
            item.append(model.to_dict())
        data.update({"aaData": item})
        jsonstr = JSONEncoder().encode(data)
        return jsonstr
        