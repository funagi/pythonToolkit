# Create your views here.

from django.shortcuts import render_to_response
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.forms.widgets import Textarea
from django.utils.translation import ugettext
from django.conf import settings

from google.appengine.api import users

from service import AdminService
from cooluser.service import UserService
from account.service import AccountService
from money.service import MoneyService

from django.utils.simplejson import JSONEncoder

class HelpTextForm(forms.Form):
    title = forms.CharField(max_length=100, label=ugettext('Help Title'), required=True)
    category = forms.ChoiceField(choices=(('Home', ugettext('Home')),
                                          ('Money Income and Expense', ugettext('Money Income and Expense')),
                                          ('Account', ugettext('Account')),
                                          ('Object', ugettext('Object')),
                                          ('Alarm', ugettext('Alarm')),
                                          ('Budget', ugettext('Budget')),
                                          ('Setting', ugettext('Setting')),
                                          ), 
                                 label=ugettext('Page Title'), 
                                 required=True)
    abstract = forms.CharField(max_length=200, widget=Textarea(), label=ugettext('Abstract'), required=False)
    content = forms.CharField(max_length=500, widget=Textarea(), label=ugettext('Description'), required=False)

    def __init__(self, *args, **kwargs ):  
        super(HelpTextForm, self).__init__(*args, **kwargs)      
        if 'data' in kwargs:
            self.data = kwargs['data'] 
    
class CurrencyForm(forms.Form):
    name = forms.CharField(max_length=100, label=ugettext('Currency Name'), required=True)
    symbol = forms.CharField(label=ugettext('Currency Symbol'), required=True)

class AccountTypeForm(forms.Form):
    name = forms.CharField(max_length=100, label='Account Type Name', required=True)
    canadvance = forms.BooleanField(label='Can Advance', required=False)

class MoneyIOSysTypeForm(forms.Form):
    isio = forms.ChoiceField(choices=((1, 'Income'),(-1, 'Expense')), label=ugettext('Money Income and Expense Type'), required = True)
    name = forms.CharField(label=ugettext('Money Income and Expense Name'), required = True)  

def check_user_is_admin(request):
    user = request.session.get('user')
    result = False
    if user:
        email = user.email
        if email == settings.ADMIN_EMAIL:
            result = True
    return result        

def notadmin(request):
    return HttpResponse('You are not admin!')

def index(request):
    if not check_user_is_admin(request):
        return HttpResponseRedirect('/notadmin/')    
    
    page_title = ugettext('Admin')
    user = request.session.get('user')
    page_module='Admin'
    currency_list = AdminService().getCurrencyList()
    accounttype_list = AdminService().getAccountTypeList()
    moneyiosystype_list = AdminService().getMoneyIOSysTypeList()
    helptext_list = AdminService().getHelpTextList()
    '''helptext_list_json = JSONEncoder().encode(AdminService().encode(helptext_list))'''
    return render_to_response('admin.html', 
                              {'currency_list': currency_list, 
                               'accounttype_list': accounttype_list,
                               'moneyiosystype_list': moneyiosystype_list,
                               'helptext_list': helptext_list,
                               'user':user,
                               'page_title': page_title,
                               'page_module': page_module,                               
                               
                               })
    
def currency_delete(request, id):
    if not check_user_is_admin(request):
        return HttpResponseRedirect('/notadmin/') 
    AdminService().deleteCurrency(id)
    return HttpResponseRedirect('/admin/')

def currency_add(request): 
    if not check_user_is_admin(request):
        return HttpResponseRedirect('/notadmin/')
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = CurrencyForm(data=request.POST)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            symbol = form.cleaned_data['symbol']
            AdminService().addCurrency(name, symbol)
            return HttpResponseRedirect('/admin/')
    else:
        form = CurrencyForm()

    page_title=ugettext('Add Currency')
    form_action_url='/admin/currency/add'
    page_module='Admin'
    return render_to_response('common_add_edit.html', {'page_title':page_title, 
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user,
                                                       'page_module' : page_module
                                                       })

def currency_edit(request, id): 
    if not check_user_is_admin(request):
        return HttpResponseRedirect('/notadmin/')
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = CurrencyForm(data=request.POST)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            symbol = form.cleaned_data['symbol']
            AdminService().editCurrency(id, name, symbol)
            return HttpResponseRedirect('/admin/')
    else:                
        currency = AccountService().getCurrency(id)
        if currency:
            form = CurrencyForm(initial=
                               {'name': currency.name, 
                                'symbol':currency.symbol
                                })
        else:
            form = CurrencyForm()

    page_title=ugettext('Edit Currency')
    form_action_url='/admin/currency/edit/' + id
    page_module='Admin'
    return render_to_response('common_add_edit.html', {'page_title':page_title, 
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user,
                                                       'page_module' : page_module
                                                       })

def accounttype_delete(request, id):  
    if not check_user_is_admin(request):
        return HttpResponseRedirect('/notadmin/') 
    AdminService().deleteAccountType(id)
    return HttpResponseRedirect('/admin/')

def accounttype_add(request):  
    if not check_user_is_admin(request):
        return HttpResponseRedirect('/notadmin/')
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = AccountTypeForm(data=request.POST)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            canadvance = form.cleaned_data['canadvance']
            AdminService().addAccountType(name, canadvance)
            return HttpResponseRedirect('/admin/')
    else:
        form = AccountTypeForm()

    page_title=ugettext('Add Account Type')
    form_action_url='/admin/accounttype/add'
    page_module='Admin'
    return render_to_response('common_add_edit.html', {'page_title':page_title, 
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user,
                                                       'page_module' : page_module
                                                       })

def accounttype_edit(request, id): 
    if not check_user_is_admin(request):
        return HttpResponseRedirect('/notadmin/')
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = AccountTypeForm(data=request.POST)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            canadvance = form.cleaned_data['canadvance']
            AdminService().editAccountType(id, name, canadvance)
            return HttpResponseRedirect('/admin/')
    else:                
        accounttype = AccountService().getAccountType(id)
        if accounttype:
            form = AccountTypeForm(initial=
                               {'name': accounttype.name,
                                'canadvance':accounttype.canadvance
                                })
        else:
            form = AccountTypeForm()

    page_title=ugettext('Edit Account Type')
    form_action_url='/admin/accounttype/edit/' + id
    page_module='Admin'
    return render_to_response('common_add_edit.html', {'page_title':page_title, 
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user,
                                                       'page_module' : page_module
                                                       })

def moneyiosystype_delete(request, id): 
    if not check_user_is_admin(request):
        return HttpResponseRedirect('/notadmin/')
    
    moneyiosystype_list = AdminService().getMoneyIOSysTypeList()
    return HttpResponseRedirect('/admin/')

def moneyiosystype_add(request):
    if not check_user_is_admin(request):
        return HttpResponseRedirect('/notadmin/')
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = MoneyIOSysTypeForm(data=request.POST)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            isio = int(form.cleaned_data['isio'])
            AdminService().addMoneyIOSysType(name, isio)
            return HttpResponseRedirect('/admin/')
    else:
        form = MoneyIOSysTypeForm()

    page_title=ugettext('Add Money Income and Expense System Type')
    form_action_url='/admin/moneyiosystype/add'
    page_module='Admin'
    return render_to_response('common_add_edit.html', {'page_title':page_title, 
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user,
                                                       'page_module' : page_module
                                                       })

def moneyiosystype_edit(request, id):
    if not check_user_is_admin(request):
        return HttpResponseRedirect('/notadmin/')
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = MoneyIOSysTypeForm(data=request.POST)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            isio = int(form.cleaned_data['isio'])
            AdminService().editMoneyIOSysType(id, name, isio)
            return HttpResponseRedirect('/admin/')
    else:                
        moneyiosystype = MoneyService().getMoneyIOSysType(id)
        if moneyiosystype:
            form = MoneyIOSysTypeForm(initial=
                               {'name': moneyiosystype.name, 
                                'isio':moneyiosystype.isio
                                })
        else:
            form = MoneyIOSysTypeForm()

    page_title=ugettext('Edit Money Income and Expense System Type')
    form_action_url='/admin/moneyiosystype/edit/' + id
    page_module='Admin'
    return render_to_response('common_add_edit.html', {'page_title':page_title, 
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user,
                                                       'page_module' : page_module
                                                       })

def helptext_delete(request, id):
    if not check_user_is_admin(request):
        return HttpResponseRedirect('/notadmin/')    
    
    AdminService().deleteHelpText(id)
    return HttpResponseRedirect('/admin/')

def helptext_add(request):
    if not check_user_is_admin(request):
        return HttpResponseRedirect('/notadmin/')
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = HelpTextForm(data=request.POST)
        if form.is_valid(): 
            title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            abstract = form.cleaned_data['abstract']
            content = form.cleaned_data['content']
            AdminService().addHelpText(title, category, abstract, content)
            return HttpResponseRedirect('/admin/')
    else:
        form = HelpTextForm()

    page_title=ugettext('Add Help Text')
    form_action_url='/admin/helptext/add'
    page_module='Admin'
    return render_to_response('common_add_edit.html', {'page_title':page_title, 
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user,
                                                       'page_module' : page_module
                                                       })

def helptext_edit(request, id):
    if not check_user_is_admin(request):
        return HttpResponseRedirect('/notadmin/')
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = HelpTextForm(data=request.POST)
        if form.is_valid(): 
            title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            abstract = form.cleaned_data['abstract']
            content = form.cleaned_data['content']
            AdminService().editHelpText(id, title, category, abstract, content)
            return HttpResponseRedirect('/admin/')
    else:                
        helptext = AdminService().getHelpText(id)
        if helptext:
            form = HelpTextForm(initial=
                               {'title': helptext.title, 
                                'category':helptext.category,
                                'abstract':helptext.abstract,
                                'content':helptext.content
                                })
        else:
            form = HelpTextForm()

    page_title=ugettext('Edit Help Text')
    form_action_url='/admin/helptext/edit/' + id
    page_module='Admin'
    return render_to_response('common_add_edit.html', {'page_title':page_title, 
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user,
                                                       'page_module' : page_module
                                                       })
