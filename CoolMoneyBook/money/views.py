# Create your views here.

from django.shortcuts import render_to_response
from django import forms
from django.forms.widgets import Textarea
from django.http import HttpResponseRedirect

from django.utils.translation import ugettext

from service import MoneyService
from cooluser.views import login, check_user_login
from account.service import AccountService
from admin.service import AdminService
from common.service import PageInfo

import common.datetimeutil

import datetime

class MoneyTransferForm(forms.Form):
    user = None
    happentime = forms.DateField(initial=datetime.date.today, label=ugettext('Happen Date'), required=True)
    fromaccount = forms.ChoiceField(choices=[], label=ugettext('From Account'), required=True)
    toaccount = forms.ChoiceField(choices=[], label=ugettext('To Account'), required=True)
    money = forms.FloatField(initial=0.0, label=ugettext('Amount'), required=True)
    currency = forms.ChoiceField(choices=[], label=ugettext('Currency'), required=True)
    description = forms.CharField(max_length=500, widget=Textarea(), label=ugettext('Description'), required=False) 
    
    def __init__(self, user, *args, **kwargs ):        
        super(MoneyTransferForm, self).__init__(*args, **kwargs)
        self.user = user        
        self.fields['fromaccount'].choices=AccountService().getAccountChoices(self.user)
        self.fields['toaccount'].choices=AccountService().getAccountChoices(self.user)
        self.fields['currency'].choices=AccountService().getCurrencyChoices()
        if 'data' in kwargs:
            self.data = kwargs['data']
    
    def clean(self):        
        cleaned_data = self.cleaned_data
        
        fromaccount_id = cleaned_data.get('fromaccount')
        toaccount_id = cleaned_data.get('toaccount')
        if fromaccount_id == toaccount_id:
            raise forms.ValidationError(ugettext('The from account should not be same as to account'))
        
        cleaned_data = self.cleaned_data
        fromaccount_id = cleaned_data.get('fromaccount')
        money = cleaned_data.get('money')
        fromaccount = AccountService().getAccount(fromaccount_id, self.user)
        if fromaccount and fromaccount.type.canadvance==False and money > 0 and fromaccount.totalmoney < money:
            totalmoney = fromaccount.totalmoney
            raise forms.ValidationError(ugettext('The from account total amount (%(totalmoney)10.2f) is not enough to transfer') 
                                        % {'totalmoney': totalmoney})

        return cleaned_data
    
    def clean_money(self):
        cleaned_data = self.cleaned_data
        
        money = cleaned_data.get('money')
        if money <= 0:
            raise forms.ValidationError(ugettext('The amount should be more than zero'))
        
        return money

class MoneyBLForm(forms.Form):
    user = None
    happentime = forms.DateField(initial=datetime.date.today, label=ugettext('Happen Date'), required=True)
    account = forms.ChoiceField(choices=[], label=ugettext('From Account'), required=True)
    isio = forms.ChoiceField(choices=((1, ugettext('Borrow')),(-1, ugettext('Lend'))), label='Borrow or Lend', required = True)
    money = forms.FloatField(initial=0.0, label=ugettext('Amount'), required=True)
    currency = forms.ChoiceField(choices=[], label=ugettext('Currency'), required=True)
    description = forms.CharField(max_length=500, widget=Textarea(), label=ugettext('Description'), required=False) 
    
    def __init__(self, user, *args, **kwargs ):        
        super(MoneyBLForm, self).__init__(*args, **kwargs)
        self.user = user        
        self.fields['account'].choices=AccountService().getAccountChoices(self.user)
        self.fields['currency'].choices=AccountService().getCurrencyChoices()
        if 'data' in kwargs:
            self.data = kwargs['data']
    
    def clean_money(self):
        cleaned_data = self.cleaned_data
        
        money = cleaned_data.get('money')
        if money <= 0:
            raise forms.ValidationError(ugettext('The amount should be more than zero'))
        
        return money
    
    def clean(self):
        cleaned_data = self.cleaned_data
        
        money = cleaned_data.get('money')
        isio = int(cleaned_data.get('isio'))
        account_id = cleaned_data.get('account')
        account = AccountService().getAccount(account_id, self.user)
        if account and account.type.canadvance==False and money > 0 and isio == -1 and account.totalmoney < money:
            totalmoney = account.totalmoney
            raise forms.ValidationError(ugettext('The account total amount (%(totalmoney)10.2f) is not enough to borrow') 
                                        % {'totalmoney': totalmoney})
        return cleaned_data

class MoneyIOForm(forms.Form):
    user = None
    account = forms.ChoiceField(choices=[], label=ugettext('Account'), required=True)
    happentime = forms.DateField(initial=datetime.date.today, label=ugettext('Happen Date'), required=True)
    moneyiotype = forms.ChoiceField(choices=[], label=ugettext('Money Income and Expense Type'), required=True)
    money = forms.FloatField(initial=0.0, label=ugettext('Amount'), required=True)    
    currency = forms.ChoiceField(choices=[], label=ugettext('Currency'), required=True)
    isshare = forms.BooleanField(initial=False, label=ugettext('Is Share'), required=False)
    description = forms.CharField(max_length=500, widget=Textarea(), label=ugettext('Description'), required=False) 
    
    '''The user'''
    def __init__(self, user, *args, **kwargs ):        
        super(MoneyIOForm, self).__init__(*args, **kwargs)
        self.user = user        
        self.fields['account'].choices=AccountService().getAccountChoices(self.user)
        self.fields['moneyiotype'].choices=MoneyService().getMoneyIOUserTypeChoices(self.user)  
        self.fields['currency'].choices=AccountService().getCurrencyChoices()
        if 'data' in kwargs:
            self.data = kwargs['data']  
    
    def clean_money(self):
        cleaned_data = self.cleaned_data
        
        money = cleaned_data.get('money')
        if money <= 0:
            raise forms.ValidationError(ugettext('The amount should be more than zero'))
        
        return money
    
    def clean(self):
        cleaned_data = self.cleaned_data

        money = cleaned_data.get('money')
        moneyiotype_id = cleaned_data.get('moneyiotype')
        moneyiotype = MoneyService().getMoneyIOUserType(moneyiotype_id, self.user)
        isio = moneyiotype.isio
        account_id = cleaned_data.get('account')
        account = AccountService().getAccount(account_id, self.user)
        if account and account.type.canadvance==False and money > 0 and isio == -1 and account.totalmoney < money:
            totalmoney = account.totalmoney
            raise forms.ValidationError(ugettext('The account total amount (%(totalmoney)10.2f) is not enough to expense') 
                                        % {'totalmoney': totalmoney}) 
        
        return cleaned_data

class MoneyIOSearchForm(forms.Form):
    user = None
    begindate = forms.DateField(initial=common.datetimeutil.get_firstday_month(), label=ugettext('Begin Date'), required=False)
    enddate = forms.DateField(initial=datetime.date.today, label=ugettext('End Date'), required=False)
    account = forms.ChoiceField(choices=[], label=ugettext('Account'), required=False)
    moneyiotype = forms.ChoiceField(choices=[], label=ugettext('Money Income and Expense Type'), required=False)
    '''
    minmoney = forms.FloatField(initial=0.0, label=ugettext('Min Amount'), required=False)
    maxmoney = forms.FloatField(initial=0.0, label=ugettext('Max Amount'), required=False)
    '''
    currency = forms.ChoiceField(choices=[], label=ugettext('Currency'), required=False)
    
    '''The user'''
    def __init__(self, user, *args, **kwargs ):        
        super(MoneyIOSearchForm, self).__init__(*args, **kwargs)
        self.user = user        
        self.fields['account'].choices=[(-1, 'All')] + AccountService().getAccountChoices(self.user)
        self.fields['moneyiotype'].choices=[(-1, 'All')] + MoneyService().getMoneyIOUserTypeChoices(self.user)  
        self.fields['currency'].choices=[(-1, 'All')] + AccountService().getCurrencyChoices()
        if 'data' in kwargs:
            self.data = kwargs['data']

class MoneyIOStatSearchForm(forms.Form):
    user = None
    begindate = forms.DateField(initial=common.datetimeutil.get_firstday_month(), label=ugettext('Begin Date'), required=False)
    enddate = forms.DateField(initial=datetime.date.today, label=ugettext('End Date'), required=False)
    account = forms.ChoiceField(choices=[], label=ugettext('Account'), required=False)
    currency = forms.ChoiceField(choices=[], label=ugettext('Currency'), required=False)
    
    '''The user'''
    def __init__(self, user, *args, **kwargs ):        
        super(MoneyIOStatSearchForm, self).__init__(*args, **kwargs)
        self.user = user        
        self.fields['account'].choices=[(-1, 'All')] + AccountService().getAccountChoices(self.user)
        self.fields['currency'].choices=[(-1, 'All')] + AccountService().getCurrencyChoices()
        if 'data' in kwargs:
            self.data = kwargs['data']    
    
class MoneyIOUserTypeForm(forms.Form):
    user = None
    id   = None
    isio = forms.ChoiceField(choices=((1, ugettext('Income')),(-1, ugettext('Expense'))), label='Money Income and Expense Type', required = True)
    name = forms.CharField(label='Money Income and Expense Name', required = True)  
    
    def __init__(self, id, user, *args, **kwargs ):        
        super(MoneyIOUserTypeForm, self).__init__(*args, **kwargs)
        self.user = user    
        self.id = id    
        if 'data' in kwargs:
            self.data = kwargs['data']
    
    def clean_name(self):
        cleaned_data = self.cleaned_data
        
        name = cleaned_data.get('name')
        if MoneyService().checkMoneyIOUserTypeNameExist(name, self.id, self.user):
            raise forms.ValidationError(ugettext('The Money Income and Expense name already exists'))
               
        return name

def moneyio_analyze_index(request):
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    page_title=ugettext('Money Income and Expense Analyze')
    pageinfo = PageInfo(page_menu_name='Money', user=user, page_title=page_title)
    helptext_list = AdminService().getCategoryHelpTextList('Money Income and Expense')
    
    year = common.datetimeutil.year
    month = int(common.datetimeutil.month)
    yearmonthlist = [(year + '/' + str(i)) for i in range(1, month)] + [year + '/' +str(month)]
    if request.method == 'POST':
        form = MoneyIOStatSearchForm(data=request.POST, user=user)
        if form.is_valid():
            filter_dict = {}
            begindate = form.cleaned_data['begindate']
            if begindate:
                filter_dict.update({'happentime >=': begindate})
                
            enddate = form.cleaned_data['enddate']
            if enddate:
                enddate = common.datetimeutil.getdayofday(enddate, 1)
                filter_dict.update({'happentime <': enddate})
                
            account = AccountService().getAccount(form.cleaned_data['account'], user)
            if account:
                filter_dict.update({'account': account})
            
            currency = AccountService().getCurrency(form.cleaned_data['currency'])
            if currency:
                filter_dict.update({'currency': currency})
    else:
        form = MoneyIOStatSearchForm(user=user)        
            
        try:
            yearmonth=request.GET['yearmonth']
        except:
            yearmonth=''
        if not yearmonth or yearmonth == '':
            yearmonth = year + '/' + str(month)
        begindate = datetime.datetime.strptime(yearmonth, '%Y/%m')
        enddate = common.datetimeutil.datetime_offset_by_month(begindate, 1)
        filter_dict = {'happentime >=': begindate, 'happentime <': enddate}
    
    begindatestr = datetime.datetime.strftime(begindate, '%Y-%m-%d')
    enddatestr = datetime.datetime.strftime(enddate, '%Y-%m-%d')
    
    moneystat_list = MoneyService().getMoneyStatList(filter_dict, user)
    
    return render_to_response('moneyioanalyze.html', 
                              {'yearmonthlist': yearmonthlist,
                               'form': form,
                               'moneystat_list': moneystat_list,
                               'begindate': begindatestr,
                               'enddate': enddatestr,
                               'user':user,
                               'pageinfo': pageinfo,
                               'helptext_list': helptext_list
                               })

def moneyio_stat_index(request):
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    page_title=ugettext('Money Income and Expense Statistics')
    pageinfo = PageInfo(page_menu_name='Money', user=user, page_title=page_title)
    helptext_list = AdminService().getCategoryHelpTextList('Money Income and Expense')
    
    year = common.datetimeutil.year
    month = int(common.datetimeutil.month)
    yearmonthlist = [(year + '/' + str(i)) for i in range(1, month)] + [year + '/' +str(month)]
    account_id = '-1'
    currency_id = '-1'   
    
    if request.method == 'POST':
        form = MoneyIOStatSearchForm(data=request.POST, user=user)
        if form.is_valid():
            filter_dict = {}
            begindate = form.cleaned_data['begindate']
            if begindate:
                filter_dict.update({'happentime >=': begindate})
                
            enddate = form.cleaned_data['enddate']
            if enddate:
                enddate = common.datetimeutil.getdayofday(enddate, 1)
                filter_dict.update({'happentime <': enddate})
                
            account = AccountService().getAccount(form.cleaned_data['account'], user)
            if account:
                filter_dict.update({'account': account})
                account_id = account.id
            
            currency = AccountService().getCurrency(form.cleaned_data['currency'])
            if currency:
                filter_dict.update({'currency': currency})
                currency_id = currency.id
    else:
        form = MoneyIOStatSearchForm(user=user)        
            
        try:
            yearmonth=request.GET['yearmonth']
        except:
            yearmonth=''
        if not yearmonth or yearmonth == '':
            yearmonth = year + '/' + str(month)
        begindate = datetime.datetime.strptime(yearmonth, '%Y/%m')
        enddate = common.datetimeutil.datetime_offset_by_month(begindate, 1)
        filter_dict = {'happentime >=': begindate, 'happentime <': enddate}
    
    begindatestr = datetime.datetime.strftime(begindate, '%Y-%m-%d')
    enddatestr = datetime.datetime.strftime(enddate, '%Y-%m-%d')
    
    '''getMoneyStatList will return a money stat list, every currency has one'''
    moneystat_list = MoneyService().getMoneyStatList(filter_dict, user)
    
    return render_to_response('moneyiostat.html', 
                              {'yearmonthlist': yearmonthlist,
                               'form': form,
                               'moneystat_list': moneystat_list,
                               'begindate': begindatestr,
                               'enddate': enddatestr,
                               'account_id': account_id,
                               'currency_id': currency_id,
                               'user':user,
                               'pageinfo': pageinfo,
                               'helptext_list': helptext_list
                               })

def moneybl_index(request):
    if not check_user_login(request):
        return login(request)  
    
    user = request.session.get('user')
    pageinfo = PageInfo(page_menu_name='Money', user=user, page_title=ugettext('Money Borrow and Lend'))
    helptext_list = AdminService().getCategoryHelpTextList('Money Income and Expense')
    return render_to_response('moneybl.html',                               
                              {'user':user,
                               'pageinfo': pageinfo,
                               'helptext_list': helptext_list                               
                               })

def moneybl_add(request):  
    if not check_user_login(request):
        return login(request)    
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = MoneyBLForm(data=request.POST, user=user)
        if form.is_valid(): 
            account = AccountService().getAccount(form.cleaned_data['account'], user)
            isio = int(form.cleaned_data['isio'])
            happentime = form.cleaned_data['happentime']          
            money = form.cleaned_data['money']
            currency = AccountService().getCurrency(form.cleaned_data['currency'])
            description = form.cleaned_data['description']
            MoneyService().addMoneyBL(account, isio, happentime, money, currency, description, user)
            return HttpResponseRedirect('/moneybl/')            
    else:
        form = MoneyBLForm(user=user)
    pageinfo = PageInfo(page_menu_name='Money', user=user, page_title=ugettext('Add Money Borrow and Lend'))
    helptext_list = AdminService().getCategoryHelpTextList('Money Income and Expense')
    form_action_url='/moneybl/add'
    return render_to_response('common_add_edit.html', {'pageinfo':pageinfo, 
                                                       'helptext_list': helptext_list,
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user
                                                       })

def moneybl_edit(request, id): 
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = MoneyBLForm(data=request.POST, user=user)
        if form.is_valid(): 
            account = AccountService().getAccount(form.cleaned_data['account'], user)
            isio = int(form.cleaned_data['isio'])
            happentime = form.cleaned_data['happentime']         
            money = form.cleaned_data['money']
            currency = AccountService().getCurrency(form.cleaned_data['currency'])
            description = form.cleaned_data['description']
            MoneyService().editMoneyBL(id, account, isio, happentime, money, currency, description, user)
            return HttpResponseRedirect('/moneybl/')
    else:                
        moneybl = MoneyService().getMoneyBL(id, user)
        if moneybl:
            moneybl_currency_id = None
            if moneybl.currency:
                moneybl_currency_id = moneybl.currency.id
            moneybl_account_id = None
            if moneybl.account:
                moneybl_account_id = moneybl.account.id
            form = MoneyBLForm(initial=
                               {'account': moneybl_account_id, 
                                'isio': moneybl.isio, 
                                'happentime':moneybl.happentime, 
                                'money':moneybl.money, 
                                'currency':moneybl_currency_id, 
                                'description':moneybl.description}, user=user)
        else:
            return HttpResponseRedirect('/moneybl/')

    pageinfo = PageInfo(page_menu_name='Money', user=user, page_title=ugettext('Edit Money Borrow and Lend'))
    helptext_list = AdminService().getCategoryHelpTextList('Money Income and Expense')
    form_action_url='/moneybl/edit/' + id
    return render_to_response('common_add_edit.html', {'pageinfo':pageinfo, 
                                                       'helptext_list': helptext_list,
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user
                                                       })

def moneybl_delete(request, id): 
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    MoneyService().deleteMoneyBL(id, user)
    
    return HttpResponseRedirect('/moneybl/')

def moneytransfer_index(request):      
    if not check_user_login(request):
        return login(request)  
    
    user = request.session.get('user')
    pageinfo = PageInfo(page_menu_name='Money', user=user, page_title=ugettext('Money Transfer'))
    helptext_list = AdminService().getCategoryHelpTextList('Money Income and Expense')
    return render_to_response('moneytransfer.html',                               
                              {'user':user,
                               'pageinfo': pageinfo,
                               'helptext_list': helptext_list                               
                               })

def moneytransfer_add(request):  
    if not check_user_login(request):
        return login(request)    
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = MoneyTransferForm(data=request.POST, user=user)
        if form.is_valid(): 
            fromaccount = AccountService().getAccount(form.cleaned_data['fromaccount'], user)
            toaccount = AccountService().getAccount(form.cleaned_data['toaccount'], user)  
            happentime = form.cleaned_data['happentime']         
            money = form.cleaned_data['money']
            currency = AccountService().getCurrency(form.cleaned_data['currency'])
            description = form.cleaned_data['description']
            MoneyService().addMoneyTransfer(fromaccount, toaccount, happentime, money, currency, description, user)
            return HttpResponseRedirect('/moneytransfer/')            
    else:
        form = MoneyTransferForm(user=user)
    pageinfo = PageInfo(page_menu_name='Money', user=user, page_title=ugettext('Add Money Transfer'))
    helptext_list = AdminService().getCategoryHelpTextList('Money Income and Expense')
    form_action_url='/moneytransfer/add'
    return render_to_response('common_add_edit.html', {'pageinfo':pageinfo, 
                                                       'helptext_list': helptext_list,
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user
                                                       })

def moneytransfer_edit(request, id): 
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = MoneyTransferForm(data=request.POST, user=user)
        if form.is_valid(): 
            fromaccount = AccountService().getAccount(form.cleaned_data['fromaccount'], user)
            toaccount = AccountService().getAccount(form.cleaned_data['toaccount'], user)  
            happentime = form.cleaned_data['happentime']         
            money = form.cleaned_data['money']
            currency = AccountService().getCurrency(form.cleaned_data['currency'])
            description = form.cleaned_data['description']
            MoneyService().editMoneyTransfer(id, fromaccount, toaccount, happentime, money, currency, description, user)
            return HttpResponseRedirect('/moneytransfer/')
    else:                
        moneytransfer = MoneyService().getMoneyTransfer(id, user)
        if moneytransfer:
            moneytransfer_currency_id = None
            if moneytransfer.currency:
                moneytransfer_currency_id = moneytransfer.currency.id
            moneytransfer_fromaccount_id = None
            if moneytransfer.fromaccount:
                moneytransfer_fromaccount_id = moneytransfer.fromaccount.id
            moneytransfer_toaccount_id = None
            if moneytransfer.toaccount:
                moneytransfer_toaccount_id = moneytransfer.toaccount.id
            form = MoneyTransferForm(initial=
                               {'fromaccount': moneytransfer_fromaccount_id, 
                                'toaccount': moneytransfer_toaccount_id, 
                                'happentime':moneytransfer.happentime, 
                                'money':moneytransfer.money, 
                                'currency':moneytransfer_currency_id, 
                                'description':moneytransfer.description}, user=user)
        else:
            return HttpResponseRedirect('/moneytransfer/')

    pageinfo = PageInfo(page_menu_name='Money', user=user, page_title=ugettext('Edit Money Transfer'))
    helptext_list = AdminService().getCategoryHelpTextList('Money Income and Expense')
    form_action_url='/moneytransfer/edit/' + id
    return render_to_response('common_add_edit.html', {'pageinfo':pageinfo, 
                                                       'helptext_list': helptext_list,
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user
                                                       })

def moneytransfer_delete(request, id): 
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    MoneyService().deleteMoneyTransfer(id, user)
    
    return HttpResponseRedirect('/moneytransfer/')

'''
def moneyio_index(request):      
    if not check_user_login(request):
        return login(request) 
    
    user = request.session.get('user')
    pageinfo = PageInfo(page_menu_name='Money', user=user)
    helptext_list = AdminService().getCategoryHelpTextList('Money Income and Expense') 
    
    return render_to_response('moneyio.html',                               
                              {'user':user,
                               'pageinfo': pageinfo,
                               'helptext_list': helptext_list
                               })
'''
def moneyio_index(request):      
    if not check_user_login(request):
        return login(request)  
    
    user = request.session.get('user')
    pageinfo = PageInfo(page_menu_name='Money', user=user)
    helptext_list = AdminService().getCategoryHelpTextList('Money Income and Expense')
    year = common.datetimeutil.year
    month = int(common.datetimeutil.month)
    yearmonthlist = [(year + '/' + str(i)) for i in range(1, month)] + [year + '/' +str(month)]
    
    if request.method == 'POST':
        form = MoneyIOSearchForm(data=request.POST, user=user)
        if form.is_valid():
            filter_dict = {}
            begindate = form.cleaned_data['begindate']            
            if begindate:
                filter_dict.update({'happentime >=': begindate})
                
            enddate = form.cleaned_data['enddate']
            if enddate:
                enddate = common.datetimeutil.getdayofday(enddate, 1)
                filter_dict.update({'happentime <': enddate})
                
            account = AccountService().getAccount(form.cleaned_data['account'], user)
            if account:
                filter_dict.update({'account': account})
            
            moneyiotype = MoneyService().getMoneyIOUserType(form.cleaned_data['moneyiotype'], user)
            if moneyiotype:
                filter_dict.update({'moneyiotype': moneyiotype})
            
            currency = AccountService().getCurrency(form.cleaned_data['currency'])
            if currency:
                filter_dict.update({'currency': currency})
    else:
        form = MoneyIOSearchForm(user=user)    
            
        try:
            yearmonth=request.GET['yearmonth']
        except:
            yearmonth=''
        if not yearmonth or yearmonth == '':
            yearmonth = year + '/' + str(month)
        begindate = datetime.datetime.strptime(yearmonth, '%Y/%m')
        enddate = common.datetimeutil.datetime_offset_by_month(begindate, 1)
        filter_dict = {'happentime >=': begindate, 'happentime <': enddate} 
    
    request.session['moneyio_filter_dict'] = filter_dict
    
    return render_to_response('moneyio.html',                               
                              {'user':user,
                               'pageinfo': pageinfo,
                               'helptext_list': helptext_list,
                               'yearmonthlist': yearmonthlist,
                               'form': form
                               })

def moneyio_add(request):  
    if not check_user_login(request):
        return login(request)    
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = MoneyIOForm(data=request.POST, user=user)
        if form.is_valid(): 
            account = AccountService().getAccount(form.cleaned_data['account'], user)  
            happentime = form.cleaned_data['happentime']
            moneyiotype = MoneyService().getMoneyIOUserType(form.cleaned_data['moneyiotype'], user)
            money = form.cleaned_data['money']
            currency = AccountService().getCurrency(form.cleaned_data['currency'])
            isshare = form.cleaned_data['isshare']
            description = form.cleaned_data['description']
            MoneyService().addMoneyIO(account, happentime, moneyiotype, money, currency, isshare, description, user)
            return HttpResponseRedirect('/moneyio/')            
    else:
        form = MoneyIOForm(user=user)
    page_title=ugettext('Add Money Income and Expense')
    pageinfo = PageInfo(page_menu_name='Money', user=user, page_title=page_title)
    helptext_list = AdminService().getCategoryHelpTextList('Money Income and Expense')
    form_action_url='/moneyio/add'
    return render_to_response('common_add_edit.html', {'pageinfo':pageinfo, 
                                                       'helptext_list': helptext_list,
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user,
                                                       })

def moneyio_edit(request, id): 
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = MoneyIOForm(data=request.POST, user=user)
        if form.is_valid(): 
            account = AccountService().getAccount(form.cleaned_data['account'], user)  
            happentime = form.cleaned_data['happentime']
            moneyiotype = MoneyService().getMoneyIOUserType(form.cleaned_data['moneyiotype'], user)
            money = form.cleaned_data['money']
            currency = AccountService().getCurrency(form.cleaned_data['currency'])
            isshare = form.cleaned_data['isshare']
            description = form.cleaned_data['description']
            MoneyService().editMoneyIO(id, account, happentime, moneyiotype, money, currency, isshare, description, user)
            return HttpResponseRedirect('/moneyio/')
    else:                
        moneyio = MoneyService().getMoneyIO(id, user)
        if moneyio:
            moneyio_account_id =None
            if moneyio.account:
                moneyio_account_id = moneyio.account.id
            moneyio_moneyiotype_id = None
            if moneyio.moneyiotype:
                moneyio_moneyiotype_id = moneyio.moneyiotype.id
            moneyio_currency_id = None
            if moneyio.currency:
                moneyio_currency_id = moneyio.currency.id
            form = MoneyIOForm(initial=
                               {'account': moneyio_account_id, 
                                'happentime':moneyio.happentime, 
                                'moneyiotype':moneyio_moneyiotype_id, 
                                'money':moneyio.money, 
                                'currency':moneyio_currency_id, 
                                'isshare':moneyio.isshare,
                                'description':moneyio.description}, user=user)
        else:
            return HttpResponseRedirect('/moneyio/')

    page_title=ugettext('Edit Money Income and Expense')
    pageinfo = PageInfo(page_menu_name='Money', user=user, page_title=page_title)
    helptext_list = AdminService().getCategoryHelpTextList('Money Income and Expense')
    form_action_url='/moneyio/edit/' + id
    return render_to_response('common_add_edit.html', {'pageinfo':pageinfo, 
                                                       'helptext_list': helptext_list,
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user
                                                       })

def moneyio_delete(request, id): 
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    MoneyService().deleteMoneyIO(id, user)
    
    return HttpResponseRedirect('/moneyio/')

def moneyiousertype_index(request):
    if not check_user_login(request):
        return login(request)  
       
    user = request.session.get('user')
    page_title=ugettext('Money Income and Expense Type')
    pageinfo = PageInfo(page_menu_name='Money', user=user, page_title=page_title)
    helptext_list = AdminService().getCategoryHelpTextList('Money Income and Expense')
    moneyiousertype_list = MoneyService().getMoneyIOUserTypeList(user)
    return render_to_response('moneyiousertype.html', 
                              {'moneyiousertype_list': moneyiousertype_list, 
                               'user':user,
                               'pageinfo': pageinfo,
                               'helptext_list': helptext_list,
                               })

def moneyiousertype_add(request):  
    if not check_user_login(request):
        return login(request)    
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = MoneyIOUserTypeForm(data=request.POST, user=user, id=None)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            isio = int(form.cleaned_data['isio'])
            MoneyService().addMoneyIOUserType(name, isio, user)
            return HttpResponseRedirect('/moneyiousertype/')            
    else:
        form = MoneyIOUserTypeForm(user=user, id=None)

    page_title=ugettext('Add Money Income and Expense Type')
    pageinfo = PageInfo(page_menu_name='Money', user=user, page_title=page_title)
    helptext_list = AdminService().getCategoryHelpTextList('Money Income and Expense')
    form_action_url='/moneyiousertype/add'
    return render_to_response('common_add_edit.html', {'pageinfo':pageinfo, 
                                                       'helptext_list': helptext_list,
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user
                                                       })

def moneyiousertype_edit(request, id): 
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = MoneyIOUserTypeForm(data=request.POST, user=user, id=id)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            isio = int(form.cleaned_data['isio'])          
            MoneyService().editMoneyIOUserType(id, name, isio, user)
            return HttpResponseRedirect('/moneyiousertype/')      
    else:                
        moneyiousertype = MoneyService().getMoneyIOUserType(id, user)
        if moneyiousertype:
            form = MoneyIOUserTypeForm(initial=
                               {'name': moneyiousertype.name, 
                                'isio':moneyiousertype.isio}, user=user, id=id)
        else:
            return HttpResponseRedirect('/moneyiousertype/')

    page_title=ugettext('Edit Money Income and Expense Type')
    pageinfo = PageInfo(page_menu_name='Money', user=user, page_title=page_title)
    helptext_list = AdminService().getCategoryHelpTextList('Money Income and Expense')
    form_action_url='/moneyiousertype/edit/' + id
    return render_to_response('common_add_edit.html', {'pageinfo':pageinfo, 
                                                       'helptext_list': helptext_list,
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user
                                                       })

def moneyiousertype_delete(request, id): 
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    MoneyService().deleteMoneyIOUserType(id, user)
    
    return HttpResponseRedirect('/moneyiousertype/')