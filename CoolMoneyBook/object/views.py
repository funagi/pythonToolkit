# Create your views here.

from django.shortcuts import render_to_response
from django import forms
from django.forms.widgets import Textarea
from django.http import HttpResponseRedirect

from django.utils.translation import ugettext

import datetime

from service import ObjectService
from cooluser.views import login, check_user_login
from account.service import AccountService
from admin.service import AdminService
from common.service import *

class ObjectForm(forms.Form):
    id = None
    user = None
    name = forms.CharField(max_length=100, label=ugettext('Object Name'), required=True)
    finishdate = forms.DateField(initial=datetime.date.today, label=ugettext('Finish Date'), required=True)
    accountlist = forms.MultipleChoiceField(choices=[], label=ugettext('Account'), required=True)
    money = forms.FloatField(initial=0.0, label=ugettext('Object Amount'), required=True)
    currency = forms.ChoiceField(choices=[], label=ugettext('Currency'), required=True)
    description = forms.CharField(max_length=500, widget=Textarea(), label=ugettext('Description'), required=False)    
    
    def __init__(self, id, user, *args, **kwargs ):  
        super(ObjectForm, self).__init__(*args, **kwargs)
        self.id = id
        self.user = user        
        self.fields['accountlist'].choices=AccountService().getAccountChoices(self.user) 
        self.fields['currency'].choices=AccountService().getCurrencyChoices()
        if 'data' in kwargs:
            self.data = kwargs['data']

    def clean_name(self):
        cleaned_data = self.cleaned_data
        
        name = cleaned_data.get('name')
        if ObjectService().checkObjectNameExist(name, self.id, self.user):
            raise forms.ValidationError(ugettext('The object name already exists'))
        
        return name
    
    def clean_money(self):
        cleaned_data = self.cleaned_data
        
        money = cleaned_data.get('money')
        if money <= 0:
            raise forms.ValidationError(ugettext('The amount should be more than zero'))
        
        return money

def index(request):      
    if not check_user_login(request):
        return login(request)  
    
    user = request.session.get('user')
    pageinfo = PageInfo(page_menu_name='Object', user=user)
    helptext_list = AdminService().getCategoryHelpTextList('Object')
    return render_to_response('object.html',                               
                              {'user':user,
                               'pageinfo': pageinfo,
                               'helptext_list': helptext_list                               
                               })

def detail(request, id):
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')    
    object = ObjectService().getObject(id, user)
    object_list = []    
    if object:
        object_list.append(object)
        page_title = ugettext('Object Detail')
        pageinfo = PageInfo(page_menu_name='Object', user=user, page_title=page_title)
        helptext_list = AdminService().getCategoryHelpTextList('Object')
        
        account_list = AccountService().getAccountListByIDList(object.accountlist, user)
        
        return render_to_response('object_detail.html', {'object': object, 
                                                         'object_list': object_list,
                                                         'user':user,
                                                         'pageinfo': pageinfo,
                                                         'helptext_list':helptext_list, 
                                                         'account_list' : account_list
                                                         })
    else:
        return render_to_response('object_detail.html', {'object': None})
    
def add(request):  
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = ObjectForm(data=request.POST, user=user, id = None)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            finishdate = form.cleaned_data['finishdate']
            money = float(form.cleaned_data['money'])
            currency = AccountService().getCurrency(form.cleaned_data['currency'])
            accountlist = form.cleaned_data['accountlist']
            description = form.cleaned_data['description']
            ObjectService().addObject(name, finishdate, money, currency, accountlist, description, user)
            return HttpResponseRedirect('/object/')
    else:
        form = ObjectForm(user=user, id = None)

    page_title=ugettext('Add Object')
    pageinfo = PageInfo(page_menu_name='Object', user=user, page_title=page_title)
    helptext_list = AdminService().getCategoryHelpTextList('Object')
    form_action_url='/object/add/'
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
        form = ObjectForm(data=request.POST, user=user, id=id)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            finishdate = form.cleaned_data['finishdate']
            money = float(form.cleaned_data['money'])
            currency = AccountService().getCurrency(form.cleaned_data['currency'])
            accountlist = form.cleaned_data['accountlist'] 
            description = form.cleaned_data['description']
            ObjectService().editObject(id, name, finishdate, money, currency, accountlist, description, user)
            return HttpResponseRedirect('/object/')
    else:                
        object = ObjectService().getObject(id, user)
        if object:
            object_currency_id = None
            if object.currency:
                object_currency_id = object.currency.id            
            form = ObjectForm(initial=
                               {'name': object.name, 
                                'finishdate':object.finishdate,
                                'money':object.money, 
                                'currency':object_currency_id, 
                                'accountlist':object.accountlist, 
                                'description':object.description}, user=user, id=id)
        else:
            return HttpResponseRedirect('/object/')

    page_title=ugettext('Edit Object')
    pageinfo = PageInfo(page_menu_name='Object', user=user, page_title=page_title)
    helptext_list = AdminService().getCategoryHelpTextList('Object')
    form_action_url='/object/edit/' + id
    return render_to_response('common_add_edit.html', {'pageinfo':pageinfo, 
                                                       'helptext_list': helptext_list,
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user
                                                       })
    
def delete(request, id):  
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    ObjectService().deleteObject(id, user)
    
    return HttpResponseRedirect('/object/')
