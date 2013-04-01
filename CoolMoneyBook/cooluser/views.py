# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import forms
from google.appengine.api import users 

from django.utils.translation import ugettext

from admin.service import AdminService
from money.service import MoneyService
from account.service import AccountService
from object.service import ObjectService
from budget.service import BudgetService
from service import UserService
from common.service import PageInfo

from weibopy import OAuthHandler, API, WeibopError

import datetime
import common.datetimeutil

consumer_key = '2431073663' # App Key
consumer_secret = 'd9848a58a1cb745b3ffce8efcad4eaa5' # App Secret

class UserForm(forms.Form):
    id = None
    name = forms.CharField(max_length=100, label=ugettext('User Name'), required=True)
    gender = forms.ChoiceField(choices=(('0', ugettext('Male')),('1', ugettext('Female')),), label=ugettext('Gender'), required=True)
    email = forms.EmailField(required=True)
    logo = forms.URLField(label=ugettext('User Logo'),required=False)
    isreceivemail = forms.BooleanField(initial=False, label=ugettext('Is receive mail'), required=False)
    pagecount = forms.IntegerField(initial=10, label=ugettext('How many count in a page(1-50)'))

    def __init__(self, id, *args, **kwargs ):  
        super(UserForm, self).__init__(*args, **kwargs)
        self.id = id  
        if 'data' in kwargs:
            self.data = kwargs['data'] 
    
    def clean_name(self):
        cleaned_data = self.cleaned_data
        
        name = cleaned_data.get('name')
        if UserService().checkUserNameExist(name, self.id):
            raise forms.ValidationError(ugettext('User name already exists'))
        
        return name
    
    def clean_email(self):
        cleaned_data = self.cleaned_data
        
        email = cleaned_data.get('email')
        if UserService().checkUserEmailExist(email, self.id):
            raise forms.ValidationError(ugettext('User email already exists'))
        
        return email
    
    def clean_pagecount(self):
        cleaned_data = self.cleaned_data
        
        pagecount = cleaned_data.get('pagecount')
        if pagecount < 1 or pagecount > 50:
            raise forms.ValidationError(ugettext('The page count should be in 1 to 50'))
        
        return pagecount

def _get_referer_url(request):
    referer_url = request.META.get('HTTP_REFERER', '/')
    host = request.META['HTTP_HOST']
    if referer_url.startswith('http') and host not in referer_url:
        referer_url = '/'
    return referer_url

def index(request):
    if not check_user_login(request):
        return login(request)
    
    helptext_list = AdminService().getCategoryHelpTextList('Home')
    user = request.session.get('user', None)
    pageinfo = PageInfo(page_menu_name='Home', user=user)
    
    begindate = datetime.datetime.strptime(common.datetimeutil.get_firstday_month(), '%Y-%m-%d')
    enddate = datetime.date.today()
      
    moneyio_list = MoneyService().getMoneyIOList(None, '-createtime', 5, 1, user)[0]
    
    account_list = AccountService().getAccountList(None, '-createtime', 5, 1, user)[0]
    
    object_list = ObjectService().getObjectList(None, '-createtime', 5, 1, user)[0]
    
    budget_filter_dict = {'begindate >=': begindate, 'begindate <=': enddate} 
    budget_list = BudgetService().getBudgetList(budget_filter_dict, '-begindate', 5, 1, user)[0]
    
    errormessage = request.session.get('errormessage', None)
    request.session['errormessage'] = None
   
    return render_to_response('index.html', {'user': user,
                                             'helptext_list': helptext_list,
                                             'pageinfo':pageinfo,
                                             'moneyio_list': moneyio_list,
                                             'account_list': account_list,
                                             'object_list':object_list,
                                             'budget_list':budget_list,
                                             'errormessage': errormessage
                                             })

def _createGoogleLoginUrl(request):
    google_login_url = users.create_login_url(request.build_absolute_uri('/check_user_login_google'))
    return google_login_url

def login(request):
    if check_user_login(request):
        user = UserService().getUser(request.session.get('user', None))            
        request.session['user'] = user
        return HttpResponseRedirect('/')
    
    if request.path == '/login/' or request.path == '/logout/':    
        login_back_to_url = '/'
    else:
        login_back_to_url = request.path
            
    request.session['login_back_to_url'] = login_back_to_url
    
    google_login_url = _createGoogleLoginUrl(request)
    #sina_login_url = _createSinaLoginUrl(request)
    errormessage = request.session.get('errormessage', None)
    request.session['errormessage'] = None
    
    return render_to_response('user_login.html', 
                              {'google_login_url':google_login_url, 
                               #'sina_login_url':sina_login_url, 
                               'errormessage': errormessage
                               })

def check_user_login(request):
    user = request.session.get('user', None)
    if user:
        return True
    else:
        return False

def login_with_sinaid(request):
    callback = request.build_absolute_uri('/check_user_login_sina')    
    auth = OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret , callback=callback)
    try:
        authorization_url = auth.get_authorization_url()
    except WeibopError:
        request.session['errormessage'] = ugettext('Connect sina twitter fail, please retry')
        return login(request)
        
    request_token = auth.request_token
    request.session['oauth_request_token'] = request_token
    return HttpResponseRedirect(authorization_url)

def check_user_login_sina(request):
    try:
        oauth_verifier = request.GET.get('oauth_verifier', None)
        request_token = request.session.get('oauth_request_token', None)
        request.session['oauth_request_token'] = None
        
        auth=OAuthHandler(consumer_key, consumer_secret)
        
        auth.request_token=request_token
        access_token=auth.get_access_token(oauth_verifier)
    
        request.session['oauth_access_token'] = access_token
        
        api = API(auth)
        sina_user = api.me()
        
        user_in_session = request.session.get('user', None)
        isnewuser = False
        if user_in_session == None:
            user, isnewuser = UserService().getorCreateCoolUserBySinaUser(sina_user)
            user = UserService().getUser(user)
        else:
            errormessage = UserService().updateSinaID(user_in_session, sina_user)      
            if errormessage:
                request.session['errormessage'] = errormessage      
            user = UserService().getUser(user_in_session)
            
        request.session['user'] = user
        newmessagecount = UserService().getMessageCount({'isread':False}, user)
        user.newmessagecount = newmessagecount
        UserService().updateCoolUser(user)
        
        if isnewuser:
            back_to_url = '/setting'
        else:
            back_to_url = request.session.get('login_back_to_url', '/')
        
        return HttpResponseRedirect(back_to_url)
    except WeibopError:
        errormessage = ugettext('Auth sina twitter account failed, please retry.')
        request.session['errormessage'] = errormessage
        return login(request)

def check_user_login_google(request):
    google_user = users.get_current_user()
    
    user_in_session = request.session.get('user', None)
    isnewuser = False
    if user_in_session == None:
        user, isnewuser = UserService().getorCreateCoolUserByGoogleUser(google_user)    
        user = UserService().getUser(user)
    else:
        errormessage = UserService().updateGoogleID(user_in_session, google_user)  
        if errormessage:
            request.session['errormessage'] = errormessage           
        user = UserService().getUser(user_in_session)
                    
    request.session['user'] = user
    newmessagecount = UserService().getMessageCount({'isread':False}, user)
    user.newmessagecount = newmessagecount
    UserService().updateCoolUser(user)
    
    if isnewuser:
        back_to_url='/setting'
    else:
        back_to_url = request.session.get('login_back_to_url', '/')
    return HttpResponseRedirect(back_to_url)

def logout(request):
    #google_logout_url = users.create_logout_url('/login/')
    
    request.session['user'] = None
    request.session['oauth_request_token'] = None
    request.session['oauth_access_token'] = None
    request.session['login_back_to_url'] = None
    request.session.clear()
    return HttpResponseRedirect('/')

def message(request):
    if not check_user_login(request):
        return login(request)  
    
    user = request.session.get('user')
    pageinfo = PageInfo(page_menu_name='Setting', user=user)
    helptext_list = AdminService().getCategoryHelpTextList('Setting')
    return render_to_response('message.html',                               
                              {'user':user,
                               'pageinfo': pageinfo,
                               'helptext_list': helptext_list                               
                               })

def message_detail(request, id):
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')    
    message = UserService().getUserMessage(id, user)
    if message:
        UserService().updateUserMessageRead(message)
    
    page_title = ugettext('Message Detail')
    pageinfo = PageInfo(page_menu_name='Setting', user=user, page_title=page_title)
    helptext_list = AdminService().getCategoryHelpTextList('Setting')
    
    return render_to_response('message_detail.html', {'message': message, 
                                                      'user':user,
                                                      'helptext_list':helptext_list,
                                                      'pageinfo' : pageinfo
                                                      })

def message_delete(request, id): 
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    UserService().deleteMessage(id, user)
    
    return HttpResponseRedirect('/message/')

def setting(request):
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    if request.method == 'POST':
        form = UserForm(data=request.POST, id=user.id)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            gender = int(form.cleaned_data['gender'])
            email = form.cleaned_data['email']
            logo = form.cleaned_data['logo']
            isreceivemail = form.cleaned_data['isreceivemail']
            pagecount = form.cleaned_data['pagecount']
            if logo == '':
                logo = None
            UserService().editCoolUser(user.id, name, gender, email, logo, isreceivemail, pagecount)
    else:
        form = UserForm(initial={'name': user.name, 
                              'gender':user.gender, 
                              'logo':user.logo,
                              'email':user.email,
                              'isreceivemail':user.isreceivemail,
                              'pagecount':user.pagecount
                              }, id=user.id)
    
    '''
    sina_login_url = None
    if not user.sinaid:
        sina_login_url = _createSinaLoginUrl(request)
    '''
    google_login_url = None
    if not user.googleid:
        google_login_url = _createGoogleLoginUrl(request)
    user = UserService().getUser(user)
    request.session['user'] = user
    page_title=ugettext('Setting')
    pageinfo = PageInfo(page_menu_name='Setting', user=user, page_title=page_title)
    helptext_list = AdminService().getCategoryHelpTextList('Setting')
    form_action_url='/setting/'
    return render_to_response('user_setting.html', {'pageinfo':pageinfo, 
                                                       'form_action_url': form_action_url, 
                                                       'form': form, 
                                                       'user':user,
                                                       'helptext_list':helptext_list,
                                                       #'sina_login_url': sina_login_url,
                                                       'google_login_url': google_login_url
                                                       })