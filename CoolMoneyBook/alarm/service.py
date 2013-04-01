'''
Created on 2010-11-9

@author: jeffrey
'''

from model.models import Alarm, MoneyIOTemplate, MoneyIO
from money.service import MoneyService
from cooluser.service import UserService
import datetime
import common.datetimeutil

class AlarmService:
    def executeAlarm(self, alarm):
        today = datetime.date.today()
        if (alarm 
            and (alarm.begindate  == None or alarm.begindate <= today) 
            and (alarm.enddate  == None or alarm.enddate >= today)):
            
            currenttime = datetime.datetime.now()
            nextalarmtime = currenttime
            if alarm.latestalarmtime:
                latestalarmtime = alarm.latestalarmtime
            else:
                latestalarmtime = alarm.createtime
            
            cycletype = alarm.cycletype
            cyclevalue = alarm.cyclevalue
        
            if cycletype == 'Year':
                nextalarmtime = common.datetimeutil.datetime_offset_by_month(latestalarmtime, cyclevalue * 12)
            elif cycletype == 'Month':
                nextalarmtime = common.datetimeutil.datetime_offset_by_month(latestalarmtime, cyclevalue)                
            elif cycletype == 'Week':
                nextalarmtime = latestalarmtime + datetime.timedelta(days=7 * cyclevalue)
            elif cycletype == 'Day':
                nextalarmtime = latestalarmtime + datetime.timedelta(days=1 * cyclevalue)
            
            if nextalarmtime <= currenttime:
                UserService().createMessageByAlarm(alarm)
                alarm.latestalarmtime = currenttime
                alarm.put()
                
                if alarm.isautogenmoneyio:
                    moneyiotemplate_list = MoneyIOTemplate.all().filter('alarm', alarm)
                    if moneyiotemplate_list:
                        moneyiotemplate = moneyiotemplate_list[0]
                        if (moneyiotemplate 
                            and 
                            (moneyiotemplate.moneyiotype.isio == 1 
                             or (moneyiotemplate.moneyiotype.isio == -1 
                                 and moneyiotemplate.account.totalmoney >= moneyiotemplate.money)
                             )
                            ):
                            MoneyService().addMoneyIO(account=moneyiotemplate.account,
                                            happentime=datetime.date.today(),
                                            moneyiotype=moneyiotemplate.moneyiotype, 
                                            money=moneyiotemplate.money, 
                                            currency=moneyiotemplate.currency, 
                                            description='Created by alarm ' + alarm.name, 
                                            user=moneyiotemplate.user, 
                                            alarm = alarm)
                        
    
    def checkAlarmNameExist(self, name, id, user):
        alarm_list = Alarm.all().filter('name', name).filter('user', user)
        if alarm_list.count() == 0:
            return False
        elif alarm_list.count() == 1:
            if id and alarm_list[0].id == id:
                return False
            else:
                return True
        else:
            return True    
    
    def getAlarmCount(self, filter_dict, user):
        alarm_list = Alarm.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                alarm_list = alarm_list.filter(filter_key, filter_dict[filter_key])
        
        if user:
            alarm_list = alarm_list.filter('user', user)
           
        return alarm_list.count()
    
    def getAlarmList(self, filter_dict, orderby, pagesize, pagecount, user):
        alarm_list = Alarm.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                alarm_list = alarm_list.filter(filter_key, filter_dict[filter_key])
        
        if user:
            alarm_list = alarm_list.filter('user', user)
            
        total_records = alarm_list.count()
        
        if orderby:
            alarm_list = alarm_list.order(orderby)
        
        '''pagesize = 0 mean all records'''
        if pagesize > 0:
            alarm_list = alarm_list.fetch(pagesize, pagesize * (pagecount-1))
           
        return alarm_list, total_records
    
    def getAlarm(self, id, user):
        alarm = None
        try:
            alarm = Alarm.get_by_id(int(id))
            if alarm.user.id <> user.id:
                alarm = None
        except:
            alarm = None
        return alarm
    
    def deleteAlarm(self, id, user):
        alarm = self.getAlarm(id, user)
        if alarm:
            moneyiotemplate_list = MoneyIOTemplate.all().filter('alarm', alarm)
            for moneyiotemplate in moneyiotemplate_list:
                moneyiotemplate.delete()
            moneyio_list = MoneyIO.all().filter('alarm', alarm)
            for moneyio in moneyio_list:
                moneyio.alarm = None
                moneyio.put()
            alarm.delete()
    
    def addAlarm(self, name, account, begindate, enddate, cycletype, cyclevalue, isautogenmoneyio, moneyiousertype, money, currency, description, user):
        alarm = Alarm(name=name)
        alarm.account = account
        alarm.begindate = begindate
        alarm.enddate = enddate
        alarm.cycletype = cycletype
        alarm.cyclevalue = cyclevalue
        alarm.isautogenmoneyio = isautogenmoneyio
        alarm.moneyiousertype = moneyiousertype
        alarm.money = money
        alarm.currency = currency
        alarm.description = description
        if user:
            alarm.user = user        
        alarm.put()
        
        MoneyService().createMoneyIOTemplate(alarm)
        
    def editAlarm(self, id, name, account, begindate, enddate, cycletype, cyclevalue, isautogenmoneyio, moneyiousertype, money, currency, description, user):
        alarm = self.getAlarm(id, user)
        if alarm:
            alarm.name = name
            alarm.account = account
            alarm.begindate = begindate
            alarm.enddate = enddate
            alarm.cycletype = cycletype
            alarm.cyclevalue = cyclevalue
            alarm.isautogenmoneyio = isautogenmoneyio
            alarm.moneyiousertype = moneyiousertype
            alarm.money = money
            alarm.currency = currency
            alarm.description = description
            if user:
                alarm.user = user        
            alarm.put()
            
            MoneyService().createMoneyIOTemplate(alarm)