from django.http import HttpResponse

from common.service import CommonService, model_column_dict
from cooluser.views import check_user_login
from account.service import AccountService
from alarm.service import AlarmService


def get_json_data(request, filter_dict=None):    
    if not check_user_login(request):
        return ''
    
    model_name = request.GET['model_name']
    if model_name == None or model_name == '':
        return ''

    model_column = model_column_dict.get(model_name)
    if model_column == None or len(model_column) == 0:
        return ''
    
    user = request.session.get('user')
    
    sEcho = request.GET['sEcho']
        
    sort = int(request.GET['iSortCol_0'])
    try:
        orderby = model_column[sort]
    except:
        orderby = model_column[0]    
        
    sorttype = request.GET['sSortDir_0']
    if sorttype == 'desc':
        orderby = '-' + orderby
    
    if orderby == '':
        orderby = '-createtime'
    
    pagesize = int(request.GET['iDisplayLength'])    
    pagebegin = int(request.GET['iDisplayStart'])
    pagecount = pagebegin / pagesize + 1
    
    if model_name == 'moneyio':
        filter_dict = request.session['moneyio_filter_dict']
        
    model_list, total_records = CommonService().getModelList(model_name, filter_dict, orderby, pagesize, pagecount, user)
    jsondata = CommonService().getJSONData(model_list, sEcho, total_records)
    return HttpResponse(jsondata)

def moneyio_account_data(request, account_id):
    if not check_user_login(request):
        return ''
    
    user = request.session.get('user')
    
    account = AccountService().getAccount(account_id, user)
    if account == None:
        return ''
    
    filter_dict = {'account': account}
    return get_json_data(request, filter_dict)

def moneybl_account_data(request, account_id):
    if not check_user_login(request):
        return ''
    
    user = request.session.get('user')
    
    account = AccountService().getAccount(account_id, user)
    if account == None:
        return ''
    
    filter_dict = {'account': account}
    return get_json_data(request, filter_dict)

def moneytransfer_account_from_data(request, account_id):
    if not check_user_login(request):
        return ''
    
    user = request.session.get('user')
    
    account = AccountService().getAccount(account_id, user)
    if account == None:
        return ''
    
    filter_dict = {'fromaccount': account}
    return get_json_data(request, filter_dict)

def moneytransfer_account_to_data(request, account_id):
    if not check_user_login(request):
        return ''
    
    user = request.session.get('user')
    
    account = AccountService().getAccount(account_id, user)
    if account == None:
        return ''
    
    filter_dict = {'toaccount': account}
    return get_json_data(request, filter_dict)

def moneyio_alarm_data(request, alarm_id):
    if not check_user_login(request):
        return ''
    
    user = request.session.get('user')
    
    alarm = AlarmService().getAlarm(alarm_id, user)
    if alarm == None:
        return ''
    
    filter_dict = {'alarm': alarm}
    return get_json_data(request, filter_dict)