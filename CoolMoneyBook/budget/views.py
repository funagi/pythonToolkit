# Create your views here.

from django.shortcuts import render_to_response
from django import forms
from django.forms.formsets import formset_factory
from django.forms.widgets import Textarea, HiddenInput
from django.http import HttpResponseRedirect, HttpResponse

from django.utils.translation import ugettext

from account.service import AccountService
from cooluser.views import login, check_user_login
from money.service import MoneyService
from admin.service import AdminService
import common.datetimeutil

from common.service import *

from django.utils.simplejson import JSONEncoder

from service import BudgetService

class BudgetForm(forms.Form):
    name = forms.CharField(max_length=100, label=ugettext('Budget Name'), required=True)
    begindate = forms.DateField(initial=common.datetimeutil.get_firstday_month(), label=ugettext('Begin Date'), required=True)
    enddate = forms.DateField(initial=common.datetimeutil.get_lastday_month(), label=ugettext('End Date'), required=True)
    currency = forms.ChoiceField(choices=[], label=ugettext('Currency'), required=True)
    description = forms.CharField(max_length=500, widget=Textarea(), label=ugettext('Description'), required=False)
    
    def __init__(self, *args, **kwargs ):        
        super(BudgetForm, self).__init__(*args, **kwargs)        
        self.fields['currency'].choices=AccountService().getCurrencyChoices()
        if 'data' in kwargs:
            self.data = kwargs['data']
    
    def clean(self):
        cleaned_data = self.cleaned_data
        begindate = cleaned_data.get('begindate')
        enddate = cleaned_data.get('enddate')

        if begindate and enddate and begindate >= enddate:
            raise forms.ValidationError(ugettext('The begin data should be earlier than end date'))
        return cleaned_data

class BudgetDetailForm(forms.Form):
    moneyiousertypeid = forms.CharField(widget=HiddenInput())
    moneyiousertypename = forms.CharField(required=True, label=ugettext('Money Income and Expense Type'))
    money = forms.FloatField(initial=0.0, label=ugettext('Amount'), required=True)

    def __init__(self, *args, **kwargs):
        super(BudgetDetailForm, self).__init__(*args, **kwargs)
        self.fields['moneyiousertypename'].widget.attrs['readonly'] = True
        if 'data' in kwargs:
            self.data = kwargs['data']

    def clean_money(self):
        cleaned_data = self.cleaned_data
        money = cleaned_data.get('money')
        if money < 0:
            raise forms.ValidationError(ugettext('Amount can not be negative'))
        return money

def index(request):      
    if not check_user_login(request):
        return login(request)  
    
    user = request.session.get('user')
    pageinfo = PageInfo(page_menu_name='Budget', user=user)
    helptext_list = AdminService().getCategoryHelpTextList('Budget')
    return render_to_response('budget.html',                               
                              {'user':user,
                               'pageinfo': pageinfo,
                               'helptext_list': helptext_list                               
                               })

def add(request):  
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    
    moneyiousertype_list = MoneyService().getMoneyIOUserTypeList(user)
    moneyiousertype_count = MoneyService().getMoneyIOUserTypeCount(user)
    BudgetDetailFormSet = formset_factory(BudgetDetailForm, max_num=moneyiousertype_count)
    if request.method == 'POST':         
        budgetform = BudgetForm(request.POST)
        budgetdetailformset = BudgetDetailFormSet(request.POST)
        if budgetform.is_valid() and budgetdetailformset.is_valid():
            name = budgetform.cleaned_data['name']
            begindate = budgetform.cleaned_data['begindate']
            enddate = budgetform.cleaned_data['enddate']
            currency = AccountService().getCurrency(budgetform.cleaned_data['currency'])
            description = budgetform.cleaned_data['description']
            budget = BudgetService().addBudget(name, begindate, enddate, currency, description, user)
            
            for budgetdetailform in budgetdetailformset.forms:
                moneyiousertypeid = budgetdetailform.cleaned_data['moneyiousertypeid']
                moneyiousertype = MoneyService().getMoneyIOUserType(moneyiousertypeid, user)
                money = budgetdetailform.cleaned_data['money']
                if money > 0.0 :
                    BudgetService().addBudgetDetail(budget, moneyiousertype, money)
            return HttpResponseRedirect('/budget/')
            
    else:
        budgetform = BudgetForm()
        
        formsetinitdata=[{'moneyiousertypeid': moneyiousertype.id, 'moneyiousertypename': moneyiousertype.name, 'money': 0.0} 
                         for moneyiousertype in moneyiousertype_list]
        budgetdetailformset = BudgetDetailFormSet(initial=formsetinitdata)

        

    page_title=ugettext('Add Budget')
    pageinfo = PageInfo(page_menu_name='Budget', user=user, page_title=page_title)
    helptext_list = AdminService().getCategoryHelpTextList('Budget')
    form_action_url='/budget/add/'
    return render_to_response('budget_add_edit.html', {'helptext_list': helptext_list,
                                                       'form_action_url': form_action_url, 
                                                       'budgetform': budgetform, 
                                                       'budgetdetailformset': budgetdetailformset,
                                                       'user':user,
                                                       'pageinfo' : pageinfo
                                                       })

def edit(request, id):  
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')    
    
    moneyiousertype_count = MoneyService().getMoneyIOUserTypeCount(user)
    BudgetDetailFormSet = formset_factory(BudgetDetailForm, max_num=moneyiousertype_count)
    if request.method == 'POST':         
        budgetform = BudgetForm(request.POST)
        budgetdetailformset = BudgetDetailFormSet(request.POST)
        if budgetform.is_valid() and budgetdetailformset.is_valid():
            name = budgetform.cleaned_data['name']
            begindate = budgetform.cleaned_data['begindate']
            enddate = budgetform.cleaned_data['enddate']
            currency = AccountService().getCurrency(budgetform.cleaned_data['currency'])
            description = budgetform.cleaned_data['description']
            budget = BudgetService().editBudget(id, name, begindate, enddate, currency, description, user)
            
            if budget:
                BudgetService().deleteBudgetDetail(budget)
                for budgetdetailform in budgetdetailformset.forms:
                    moneyiousertypeid = budgetdetailform.cleaned_data['moneyiousertypeid']
                    moneyiousertype = MoneyService().getMoneyIOUserType(moneyiousertypeid, user)
                    money = budgetdetailform.cleaned_data['money']
                    if money > 0.0 :
                        BudgetService().addBudgetDetail(budget, moneyiousertype, money)
            return HttpResponseRedirect('/budget/')
            
    else:        
        budget = BudgetService().getBudget(id, user)
        if budget:
            budget_currency_id = None
            if budget.currency:
                budget_currency_id = budget.currency.id         
            budgetform = BudgetForm(initial=
                               {'name': budget.name, 
                                'begindate':budget.begindate, 
                                'enddate':budget.enddate,
                                'currency': budget_currency_id,
                                'description':budget.description})
            moneyiousertype_list = MoneyService().getMoneyIOUserTypeList(user)
            formsetinitdata=[{'moneyiousertypeid': moneyiousertype.id, 'moneyiousertypename': moneyiousertype.name, 'money': 0.0} 
                         for moneyiousertype in moneyiousertype_list]
            budgetdetail_list = BudgetService().getBudgetDetailList(budget)
            for budgetdetail in budgetdetail_list:
                for budgetdetailinitdata in formsetinitdata:
                    moneyiousertypeid = budgetdetailinitdata.get('moneyiousertypeid')
                    if moneyiousertypeid == budgetdetail.moneyiousertype.id:
                        budgetdetailinitdata['money'] = budgetdetail.money                        
            
            budgetdetailformset = BudgetDetailFormSet(initial=formsetinitdata)
        else:
            return HttpResponseRedirect('/budget/')

    page_title = ugettext('Edit Budget')
    pageinfo = PageInfo(page_menu_name='Budget', user=user, page_title=page_title)
    helptext_list = AdminService().getCategoryHelpTextList('Budget')
    form_action_url='/budget/edit/' + id
    return render_to_response('budget_add_edit.html', {'helptext_list': helptext_list,
                                                       'form_action_url': form_action_url, 
                                                       'budgetform': budgetform, 
                                                       'budgetdetailformset': budgetdetailformset,
                                                       'user':user,
                                                       'pageinfo' : pageinfo
                                                       })

def delete(request, id):  
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    BudgetService().deleteBudget(id, user)
    
    return HttpResponseRedirect('/budget/')

def detail(request, id):
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')    
    budget = BudgetService().getBudget(id, user)
    if budget:            
        page_title = ugettext('Budget Detail')
        pageinfo = PageInfo(page_menu_name='Budget', user=user, page_title=page_title)
        helptext_list = AdminService().getCategoryHelpTextList('Budget')
        
        return render_to_response('budget_detail.html', {'budget': budget,                                                          
                                                         'user':user,
                                                         'helptext_list':helptext_list,
                                                         'pageinfo' : pageinfo
                                                         })
    else:
        return render_to_response('budget_detail.html', {'budget': None})

def detail_data(request, id):
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')    
    budget = BudgetService().getBudget(id, user)
    if budget:
        budgetdetail_list = BudgetService().getBudgetDetailList(budget)
        filter_dict = {'happentime >=': budget.begindate, 'happentime <=': budget.enddate}
        moneystat = MoneyService().getMoneyStat(filter_dict, budget.currency, user)
        for budgetdetail in budgetdetail_list:
            BudgetService().updateBudgetDetailActualMoney(budgetdetail, moneystat)
        jsondata = BudgetService().encode(budgetdetail_list)
        return HttpResponse(JSONEncoder().encode(jsondata))
    else:
        return HttpResponse('')

