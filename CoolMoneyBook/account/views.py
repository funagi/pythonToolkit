# Create your views here.

from django.shortcuts import render_to_response
from django import forms
from django.forms.widgets import Textarea
from django.http import HttpResponseRedirect

from django.utils.translation import ugettext

from service import AccountService
from cooluser.views import login, check_user_login
from admin.service import AdminService

from common.service import PageInfo

'''
The Form is used to add/edit Account
'''
class AccountForm(forms.Form):
    id = None
    user = None
    name = forms.CharField(max_length=100, label=ugettext('Account Name'), required=True)
    type = forms.ChoiceField(choices=[], label=ugettext('Account Type'), required=True)
    currency = forms.ChoiceField(choices=[], label=ugettext('Currency'), required=True)
    initmoney = forms.FloatField(initial=0.0, label=ugettext('Initial Amount'), required=True)
    description = forms.CharField(max_length=500, widget=Textarea(), label=ugettext('Description'), required=False)
    
    def __init__(self, id, user, *args, **kwargs ):        
        super(AccountForm, self).__init__(*args, **kwargs)
        self.id = id
        self.user = user
        self.fields['type'].choices=AccountService().getAccountTypeChoices()
        self.fields['currency'].choices=AccountService().getCurrencyChoices()
        if 'data' in kwargs:
            self.data = kwargs['data'] 
    
    '''
    Check the account name has already exists
    '''
    def clean_name(self):
        cleaned_data = self.cleaned_data
        name = cleaned_data.get('name', '')
        if AccountService().checkAccountNameExist(name, self.id, self.user):
            raise forms.ValidationError(ugettext('The account name already exists'))
        return name       

'''
Account index page view
'''
def index(request):      
    if not check_user_login(request):
        return login(request)  
    
    user = request.session.get('user')
    pageinfo = PageInfo(page_menu_name='Account', user=user)
    helptext_list = AdminService().getCategoryHelpTextList('Account')
    return render_to_response('account.html',                               
                              {'user':user,
                               'pageinfo': pageinfo,
                               'helptext_list': helptext_list                               
                               })

def detail(request, id):
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')    
    pageinfo = PageInfo(page_menu_name='Account', user=user)    
    account = AccountService().getAccount(id, user)    
    helptext_list = AdminService().getCategoryHelpTextList('Account')
    return render_to_response('account_detail.html', {'account': account, 
                                                      'user':user,
                                                      'pageinfo': pageinfo,
                                                      'helptext_list':helptext_list
                                                      })

def add(request):  
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = AccountForm(data = request.POST, user = user, id=None)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            type = AccountService().getAccountType(form.cleaned_data['type'])
            currency = AccountService().getCurrency(form.cleaned_data['currency'])
            initmoney = float(form.cleaned_data['initmoney'])
            description = form.cleaned_data['description']
            AccountService().addAccount(name, type, currency, initmoney, description, user)
            return HttpResponseRedirect('/account/')
    else:
        form = AccountForm(user=user, id=None)

    page_title=ugettext('Add Account')
    pageinfo = PageInfo(page_menu_name='Account', user=user, page_title=page_title)
    helptext_list = AdminService().getCategoryHelpTextList('Account')
    form_action_url='/account/add/'    
    return render_to_response('common_add_edit.html', {'pageinfo':pageinfo, 
                                                       'helptext_list':helptext_list,
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user
                                                       })

def edit(request, id): 
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    account = AccountService().getAccount(id, user)
    if account:
        if account.isclosed:
            return HttpResponseRedirect('/account/')
        
    if request.method == 'POST':
        form = AccountForm(data=request.POST, id=id, user=user)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            type = AccountService().getAccountType(form.cleaned_data['type'])
            currency = AccountService().getCurrency(form.cleaned_data['currency'])
            initmoney = float(form.cleaned_data['initmoney'])
            description = form.cleaned_data['description']
            AccountService().editAccount(id, name, type, currency, initmoney, description, user)
            return HttpResponseRedirect('/account/')
    else: 
        if account:
            account_type_id = None            
            if account.type:
                account_type_id = account.type.id
            account_currency_id = None
            if account.currency:
                account_currency_id = account.currency.id
            form = AccountForm(initial=
                               {'name': account.name, 
                                'type':account_type_id, 
                                'currency':account_currency_id, 
                                'initmoney':account.initmoney, 
                                'description':account.description}, id=id, user=user)
        else:
            return HttpResponseRedirect('/account/')

    page_title=ugettext('Edit Account')
    helptext_list = AdminService().getCategoryHelpTextList('Account')
    form_action_url='/account/edit/' + id
    page_module='Account'
    return render_to_response('common_add_edit.html', {'page_title':page_title, 
                                                       'helptext_list':helptext_list,
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user,
                                                       'page_module' : page_module
                                                       })

def delete(request, id): 
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    
    account = AccountService().getAccount(id, user)
    if account:
        if account.isclosed:
            return HttpResponseRedirect('/account/')
    
    AccountService().deleteAccount(id, user)
    
    return HttpResponseRedirect('/account/')

def open(request, id): 
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    AccountService().openAccount(id, user)
    
    return HttpResponseRedirect('/account/')