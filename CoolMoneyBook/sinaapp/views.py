'''
Created on 2010-12-8

@author: jeffrey
'''
from django.shortcuts import render_to_response

from common.service import PageInfo
from cooluser.views import login, check_user_login
from cooluser.service import UserService
from money.service import MoneyService
from django.http import HttpResponseRedirect

def index(request):
    return index_page(request, 1)

def index_page(request, id):
    if not check_user_login(request):
        return login(request)  
    
    user = request.session.get('user')
    pageinfo = PageInfo(page_menu_name='Sinaapp', user=user)
    
    filter_dict={'isshare': True}
    orderby = '-createtime'
    current_page = int(id)
    
    moneyiosharelist, total_records = MoneyService().getMoneyIOShareList(filter_dict, orderby, pageinfo.page_size, current_page)
    total_page = (total_records + pageinfo.page_size - 1) / pageinfo.page_size
    page_begin_num = 1 + (current_page - 1) * pageinfo.page_size
    if page_begin_num > total_records:
        page_begin_num = total_records    
    if total_page > current_page:        
        page_end_num = current_page * pageinfo.page_size
    else:
        page_end_num = total_records
    recomuserlist = UserService().getRecomUserList(user)
    
    return render_to_response('sinaapp_index.html',                               
                              {'user':user,
                               'pageinfo': pageinfo,
                               'total_records': total_records,
                               'current_page': current_page,
                               'total_page': total_page,
                               'page_begin_num': page_begin_num,
                               'page_end_num': page_end_num,
                               'moneyiosharelist': moneyiosharelist,
                               'recomuserlist': recomuserlist
                               })

def user_index(request):
    return user_index_page(request, 1)

def user_index_page(request, id):
    if not check_user_login(request):
        return login(request)  
    
    user = request.session.get('user')
    pageinfo = PageInfo(page_menu_name='Sinaapp', user=user)

    current_page = int(id)
    orderby = '-createtime'
    sinauserlist, total_records = UserService().getCoolUserList(None, orderby, pageinfo.page_size, current_page)
    total_page = (total_records + pageinfo.page_size - 1) / pageinfo.page_size
    page_begin_num = 1 + (current_page - 1) * pageinfo.page_size
    if page_begin_num > total_records:
        page_begin_num = total_records    
    if total_page > current_page:        
        page_end_num = current_page * pageinfo.page_size
    else:
        page_end_num = total_records
    recomuserlist = UserService().getRecomUserList(user)
    
    return render_to_response('sinaapp_user_index.html',                               
                              {'user':user,
                               'pageinfo': pageinfo,
                               'total_records': total_records,
                               'current_page': current_page,
                               'total_page': total_page,
                               'page_begin_num': page_begin_num,
                               'page_end_num': page_end_num,
                               'sinauserlist': sinauserlist,
                               'recomuserlist': recomuserlist
                               })

def user_view(request, id):
    return user_view_page(request, id, 1)

def user_view_page(request, id, pagenum):
    if not check_user_login(request):
        return login(request)
    
    user = request.session.get('user')
    pageinfo = PageInfo(page_menu_name='Sinaapp', user=user)
    sinauser = UserService().getCoolUser(id)    
    if sinauser:
        current_page = int(id)
        filter_dict={'isshare': True}
        orderby = '-createtime'
        moneyiosharelist, total_records = MoneyService().getMoneyIOList(filter_dict, orderby, pageinfo.page_size, current_page, sinauser)
        total_page = (total_records + pageinfo.page_size - 1) / pageinfo.page_size
        page_begin_num = 1 + (current_page - 1) * pageinfo.page_size
        if page_begin_num > total_records:
            page_begin_num = total_records    
        if total_page > current_page:        
            page_end_num = current_page * pageinfo.page_size
        else:
            page_end_num = total_records
        recomuserlist = UserService().getRecomUserList(user)
        return render_to_response('sinaapp_user_view.html',
                              {'user':user,
                               'sinauser':sinauser,
                               'pageinfo': pageinfo,
                               'total_records': total_records,
                               'current_page': current_page,
                               'total_page': total_page,
                               'page_begin_num': page_begin_num,
                               'page_end_num': page_end_num,
                               'moneyiosharelist': moneyiosharelist,
                               'recomuserlist': recomuserlist
                               })
    else:
        return HttpResponseRedirect('/sinaapp/')
    