# Create your views here.

from django.shortcuts import render_to_response
from django import forms
from django.forms.widgets import Textarea
from django.http import HttpResponseRedirect

from django.utils.translation import ugettext

import datetime

from common.service import *

from service import AlarmService
from cooluser.views import login, check_user_login
from account.service import AccountService
from money.service import MoneyService
from admin.service import AdminService

class AlarmForm(forms.Form):
    id = None
    user = None
    name = forms.CharField(max_length=100, label=ugettext('Alarm Name'), required=True)
    account = forms.ChoiceField(choices=[], label=ugettext('Account'), required=True)
    begindate = forms.DateField(initial=datetime.date.today, label=ugettext('Begin Date'), required=True)
    enddate = forms.DateField(label=ugettext('End Date'), required=False)
    cycletype = forms.ChoiceField(choices=[('Year',ugettext('Year')), ('Month',ugettext('Month')),('Week',ugettext('Week')), ('Day', ugettext('Day')) ], label=ugettext('Cycle Type'), required=True)
    cyclevalue = forms.IntegerField(label=ugettext('Cycle Value'), initial=1, required=True)
    isautogenmoneyio = forms.BooleanField(label=ugettext('Auto Generate Money Income and Expense'), required=False)
    moneyiousertype = forms.ChoiceField(choices=[], label=ugettext('Money Income and Expense Type'), required=False)
    money = forms.FloatField(initial=0.0, label=ugettext('Alarm Amount'), required=False)
    currency = forms.ChoiceField(choices=[], label=ugettext('Currency'), required=False)
    description = forms.CharField(max_length=500, widget=Textarea(), label=ugettext('Description'), required=False)
    
    def __init__(self, id, user, *args, **kwargs ):        
        super(AlarmForm, self).__init__(*args, **kwargs)
        self.id = id
        self.user = user
        self.fields['account'].choices=AccountService().getAccountChoices(self.user)
        self.fields['moneyiousertype'].choices=MoneyService().getMoneyIOUserTypeChoices(self.user)  
        self.fields['currency'].choices=AccountService().getCurrencyChoices()
        if 'data' in kwargs:
            self.data = kwargs['data']
    
    def clean_name(self):
        cleaned_data = self.cleaned_data
        
        name = cleaned_data.get('name')
        if AlarmService().checkAlarmNameExist(name, self.id, self.user):
            raise forms.ValidationError(ugettext('The alarm name already exists'))
        
        return name
    
    def clean(self):
        cleaned_data = self.cleaned_data
        
        begindate = cleaned_data.get('begindate')
        enddate = cleaned_data.get('enddate')

        if begindate and enddate and begindate >= enddate:
            raise forms.ValidationError(ugettext('The begin data should be earlier than end date'))
        
        isautogenmoneyio = cleaned_data.get('isautogenmoneyio')
        money = cleaned_data.get('money')
        if isautogenmoneyio and money <= 0:
            raise forms.ValidationError(ugettext('The amount should be more than zero'))
        
        account_id = cleaned_data.get('account')
        account = AccountService().getAccount(account_id, self.user)
        moneyiousertype_id = cleaned_data.get('moneyiousertype')
        moneyiousertype = MoneyService().getMoneyIOUserType(moneyiousertype_id, self.user)
        
        if (isautogenmoneyio 
            and account
            and moneyiousertype
            and moneyiousertype.isio == -1
            and money > 0
            and account.totalmoney < money):
            totalmoney = account.totalmoney
            raise forms.ValidationError(ugettext('The account total amount (%(totalmoney)10.2f) is not enough to expense') 
                                        % {'totalmoney': totalmoney}) 
        return cleaned_data

def index(request):      
    if not check_user_login(request):
        return login(request)  
    
    user = request.session.get('user')
    pageinfo = PageInfo(page_menu_name='Alarm', user=user)
    helptext_list = AdminService().getCategoryHelpTextList('Alarm')
    return render_to_response('alarm.html',                               
                              {'user':user,
                               'pageinfo': pageinfo,
                               'helptext_list': helptext_list                               
                               })

def detail(request, id):
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')    
    pageinfo = PageInfo(page_menu_name='Alarm', user=user)    
    alarm = AlarmService().getAlarm(id, user)
    helptext_list = AdminService().getCategoryHelpTextList('Alarm')
    return render_to_response('alarm_detail.html', {'alarm': alarm, 
                                                      'user':user,
                                                      'pageinfo': pageinfo,
                                                      'helptext_list':helptext_list
                                                      })

def add(request):  
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = AlarmForm(data=request.POST, user=user, id=None)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            account = AccountService().getAccount(form.cleaned_data['account'], user)
            begindate = form.cleaned_data['begindate']
            enddate = form.cleaned_data['enddate']
            cycletype = form.cleaned_data['cycletype']
            cyclevalue = form.cleaned_data['cyclevalue']
            isautogenmoneyio = form.cleaned_data['isautogenmoneyio']
            moneyiousertype = MoneyService().getMoneyIOUserType(form.cleaned_data['moneyiousertype'], user)
            money = form.cleaned_data['money']
            currency = AccountService().getCurrency(form.cleaned_data['currency'])
            description = form.cleaned_data['description']
            AlarmService().addAlarm(name, account, begindate, enddate, cycletype, cyclevalue, isautogenmoneyio, moneyiousertype, money, currency, description, user)
            return HttpResponseRedirect('/alarm/')
    else:
        form = AlarmForm(user=user, id=None)

    pageinfo = PageInfo(page_menu_name='Alarm', user=user, page_title=ugettext('Add Alarm'))
    helptext_list = AdminService().getCategoryHelpTextList('Alarm')
    form_action_url='/alarm/add/'    
    return render_to_response('common_add_edit.html', {'pageinfo':pageinfo, 
                                                       'helptext_list': helptext_list,
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user
                                                       })

def edit(request, id): 
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = AlarmForm(data=request.POST, user=user, id=id)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            account = AccountService().getAccount(form.cleaned_data['account'], user)
            begindate = form.cleaned_data['begindate']
            enddate = form.cleaned_data['enddate']
            cycletype = form.cleaned_data['cycletype']
            cyclevalue = form.cleaned_data['cyclevalue']
            isautogenmoneyio = form.cleaned_data['isautogenmoneyio']
            moneyiousertype = MoneyService().getMoneyIOUserType(form.cleaned_data['moneyiousertype'], user)
            money = form.cleaned_data['money']
            currency = AccountService().getCurrency(form.cleaned_data['currency'])
            description = form.cleaned_data['description']
            AlarmService().editAlarm(id, name, account, begindate, enddate, cycletype, cyclevalue, isautogenmoneyio, moneyiousertype, money, currency, description, user)
            return HttpResponseRedirect('/alarm/')
    else:                
        alarm = AlarmService().getAlarm(id, user)
        if alarm:
            alarm_account_id = None
            if alarm.account:
                alarm_account_id = alarm.account.id
            alarm_moneyiousertype_id = None
            if alarm.moneyiousertype:
                alarm_moneyiousertype_id = alarm.moneyiousertype.id
            form = AlarmForm(initial=
                               {'name': alarm.name, 
                                'account':alarm_account_id, 
                                'begindate':alarm.begindate, 
                                'enddate':alarm.enddate, 
                                'cycletype':alarm.cycletype,
                                'cyclevalue':alarm.cyclevalue,
                                'isautogenmoneyio':alarm.isautogenmoneyio,
                                'moneyiousertype':alarm_moneyiousertype_id,
                                'money':alarm.money,
                                'currency':alarm.currency.id,
                                'description':alarm.description,
                                }, user=user, id =id)
        else:
            return HttpResponseRedirect('/alarm/')

    page_title=ugettext('Edit Alarm')
    helptext_list = AdminService().getCategoryHelpTextList('Alarm')
    form_action_url='/alarm/edit/' + id
    page_module='Alarm'
    return render_to_response('common_add_edit.html', {'page_title':page_title, 
                                                       'helptext_list': helptext_list,
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user,
                                                       'page_module' : page_module
                                                       })

def delete(request, id): 
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    
    AlarmService().deleteAlarm(id, user)
    
    return HttpResponseRedirect('/alarm/')
