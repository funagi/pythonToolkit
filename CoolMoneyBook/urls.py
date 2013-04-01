# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'cooluser.views.index'),
             
    (r'^login/$', 'cooluser.views.login'),
    (r'^logout/$', 'cooluser.views.logout'),
    (r'^login_with_sinaid/$', 'cooluser.views.login_with_sinaid'),
    (r'^check_user_login_sina/$', 'cooluser.views.check_user_login_sina'),
    (r'^check_user_login_google/$', 'cooluser.views.check_user_login_google'),
    
    (r'^account/$', 'account.views.index'),    
    (r'^account/(?P<id>\d+)/$', 'account.views.detail'),
    (r'^account/add', 'account.views.add'),
    (r'^account/edit/(?P<id>\d+)', 'account.views.edit'),
    (r'^account/delete/(?P<id>\d+)', 'account.views.delete'),
    (r'^account/open/(?P<id>\d+)', 'account.views.open'),
    
    (r'^moneyio/$', 'money.views.moneyio_index'),
    (r'^moneyio/add', 'money.views.moneyio_add'),
    (r'^moneyio/edit/(?P<id>\d+)', 'money.views.moneyio_edit'),
    (r'^moneyio/delete/(?P<id>\d+)', 'money.views.moneyio_delete'),
    (r'^moneyio/account/(?P<account_id>\d+)/$', 'common.views.moneyio_account_data'),
    (r'^moneyio/alarm/(?P<alarm_id>\d+)/$', 'common.views.moneyio_alarm_data'),
    
    (r'^moneytransfer/$', 'money.views.moneytransfer_index'),
    (r'^moneytransfer/add', 'money.views.moneytransfer_add'),
    (r'^moneytransfer/edit/(?P<id>\d+)', 'money.views.moneytransfer_edit'),
    (r'^moneytransfer/delete/(?P<id>\d+)', 'money.views.moneytransfer_delete'),
    (r'^moneytransfer/account/from/(?P<account_id>\d+)/$', 'common.views.moneytransfer_account_from_data'),
    (r'^moneytransfer/account/to/(?P<account_id>\d+)/$', 'common.views.moneytransfer_account_to_data'),
        
    (r'^moneybl/$', 'money.views.moneybl_index'),
    (r'^moneybl/add', 'money.views.moneybl_add'),
    (r'^moneybl/edit/(?P<id>\d+)', 'money.views.moneybl_edit'),
    (r'^moneybl/delete/(?P<id>\d+)', 'money.views.moneybl_delete'),
    (r'^moneybl/account/(?P<account_id>\d+)/$', 'common.views.moneybl_account_data'),
    
    (r'^moneyio/stat/$', 'money.views.moneyio_stat_index'),
    (r'^moneyio/analyze/$', 'money.views.moneyio_analyze_index'),
    
    (r'^moneyiousertype/$', 'money.views.moneyiousertype_index'),
    (r'^moneyiousertype/add', 'money.views.moneyiousertype_add'),
    (r'^moneyiousertype/edit/(?P<id>\d+)', 'money.views.moneyiousertype_edit'),
    (r'^moneyiousertype/delete/(?P<id>\d+)', 'money.views.moneyiousertype_delete'),
    
    (r'^budget/$', 'budget.views.index'),
    (r'^budget/(?P<id>\d+)/$', 'budget.views.detail'),
    (r'^budget/data/(?P<id>\d+)/$', 'budget.views.detail_data'),
    (r'^budget/add', 'budget.views.add'),
    (r'^budget/edit/(?P<id>\d+)', 'budget.views.edit'),
    (r'^budget/delete/(?P<id>\d+)', 'budget.views.delete'),
    
    (r'^object/$', 'object.views.index'),
    (r'^object/(?P<id>\d+)/$', 'object.views.detail'),
    (r'^object/add', 'object.views.add'),
    (r'^object/edit/(?P<id>\d+)', 'object.views.edit'),
    (r'^object/delete/(?P<id>\d+)', 'object.views.delete'),
    
    (r'^alarm/$', 'alarm.views.index'),
    (r'^alarm/add', 'alarm.views.add'),
    (r'^alarm/edit/(?P<id>\d+)', 'alarm.views.edit'),
    (r'^alarm/delete/(?P<id>\d+)', 'alarm.views.delete'),
    (r'^alarm/(?P<id>\d+)/$', 'alarm.views.detail'),
    (r'^alarm/(?P<id>\d+)/page/(?P<pageid>\d+)/$', 'alarm.views.detail_page'),
    
    (r'^notadmin/$', 'admin.views.notadmin'),
    
    (r'^admin/$', 'admin.views.index'),
    (r'^admin/currency/add', 'admin.views.currency_add'),
    (r'^admin/currency/edit/(?P<id>\d+)', 'admin.views.currency_edit'),
    (r'^admin/currency/delete/(?P<id>\d+)', 'admin.views.currency_delete'),
    (r'^admin/accounttype/add', 'admin.views.accounttype_add'),
    (r'^admin/accounttype/edit/(?P<id>\d+)', 'admin.views.accounttype_edit'),
    (r'^admin/accounttype/delete/(?P<id>\d+)', 'admin.views.accounttype_delete'),
    (r'^admin/moneyiosystype/add', 'admin.views.moneyiosystype_add'),
    (r'^admin/moneyiosystype/edit/(?P<id>\d+)', 'admin.views.moneyiosystype_edit'),
    (r'^admin/moneyiosystype/delete/(?P<id>\d+)', 'admin.views.moneyiosystype_delete'),
    (r'^admin/helptext/add', 'admin.views.helptext_add'),
    (r'^admin/helptext/edit/(?P<id>\d+)', 'admin.views.helptext_edit'),
    (r'^admin/helptext/delete/(?P<id>\d+)', 'admin.views.helptext_delete'),
    
    (r'^setting/$', 'cooluser.views.setting'),
    (r'^setting/removeusersinaid/$', 'cooluser.views.remove_user_sina_id'),
    (r'^message/$', 'cooluser.views.message'),
    (r'^message/page/(?P<id>\d+)/$', 'cooluser.views.message_page'),
    (r'^message/(?P<id>\d+)/$', 'cooluser.views.message_detail'),
    (r'^message/delete/(?P<id>\d+)', 'cooluser.views.message_delete'),
    
    (r'^get_json_data/$', 'common.views.get_json_data'),
    
    (r'^sinaapp/$', 'sinaapp.views.index'),
    (r'^sinaapp/page/(?P<id>\d+)/$', 'sinaapp.views.index_page'),
    (r'^sinaapp/users/$', 'sinaapp.views.user_index'),
    (r'^sinaapp/users/page/(?P<id>\d+)/$', 'sinaapp.views.user_index_page'),
    (r'^sinaapp/user/(?P<id>\d+)/$', 'sinaapp.views.user_view'),
    (r'^sinaapp/user/(?P<id>\d+)/page/(?P<pagenum>\d+)/$', 'sinaapp.views.user_view_page'),


    # Example:
    # (r'^foo/', include('foo.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
