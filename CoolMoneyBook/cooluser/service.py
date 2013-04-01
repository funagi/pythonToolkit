'''
Created on 2010-11-9

@author: jeffrey
'''
from django.utils.translation import ugettext

from model.models import CoolUser, UserMessage
from money.service import MoneyService

class UserService:
    '''
    Get the recom user liset
    '''
    def getRecomUserList(self, user):
        user_list = CoolUser.gql('WHERE __key__ != :1 order by __key__ desc', user.key())
        user_list = user_list.fetch(12, 0)
        return user_list
    
    def updateCoolUser(self, user):
        if user:
            user.put()

    def updateUserMessageRead(self, message):
        if message:
            message.isread = True
            message.put()
        
    def deleteMessage(self, id, user):
        message = self.getUserMessage(id, user)
        if message:
            message.delete()

    def getUserMessage(self, id, user):
        message = None
        try:
            message = UserMessage.get_by_id(int(id))
            if message.user.id <> user.id:
                message = None
        except:
            message = None
        return message
    
    def createMessageByAlarm(self, alarm):
        if alarm:
            title = ugettext('Alarm') + ' : ' + alarm.name
            content = ugettext('You have an alarm ') + '<a href="/alarm/' + alarm.id + '">' + alarm.name + '</a>'
            '''str(alarm.content)'''
            user = alarm.user
            self.createMessage(title, content, user)
    
    def createMessage(self, title, content, user):
        message = UserMessage(title=title, content=content, user=user)
        message.put()
    
    def getMessageCount(self, filter_dict, user):
        message_list = UserMessage.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                message_list = message_list.filter(filter_key, filter_dict[filter_key])
        
        if user:
            message_list = message_list.filter('user', user)
           
        return message_list.count()
    
    def getMessageList(self, filter_dict, orderby, pagesize, pagecount, user):
        message_list = UserMessage.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                message_list = message_list.filter(filter_key, filter_dict[filter_key])
        
        if user:
            message_list = message_list.filter('user', user)
        
        total_records = message_list.count()
        
        if orderby:
            message_list = message_list.order(orderby)
        
        if pagesize > 0:
            message_list = message_list.fetch(pagesize, pagesize * (pagecount-1))
           
        return message_list, total_records
    
    def checkUserNameExist(self, name, id):
        user_list = CoolUser.all().filter('name', name)
        if user_list.count() == 0:
            return False
        elif user_list.count() == 1:
            if id and user_list[0].id == id:
                return False
            else:
                return True
        else:
            return True
    
    def checkUserEmailExist(self, email, id):
        user_list = CoolUser.all().filter('email', email)
        if user_list.count() == 0:
            return False
        elif user_list.count() == 1:
            if id and user_list[0].id == id:
                return False
            else:
                return True
        else:
            return True
    
    def removeUserSinaID(self, user):
        if user:
            user.sinaid = None
            user.put()
    
    def getUser(self, user):
        if user:
            newuser = CoolUser.get_by_id(int(user.id))
            return newuser
        else:
            return None
    
    def getUserCount(self, filter_dict):
        user_list = CoolUser.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                user_list = user_list.filter(filter_key, filter_dict[filter_key])
           
        return user_list.count()
    
    def getCoolUserList(self, filter_dict, orderby, pagesize, pagecount):
        user_list = CoolUser.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                user_list = user_list.filter(filter_key, filter_dict[filter_key])
        
        totalRecords = user_list.count()
        
        if orderby:
            user_list = user_list.order(orderby)
        
        if pagesize > 0:
            user_list = user_list.fetch(pagesize, pagesize * (pagecount-1))
           
        return user_list, totalRecords
    
    def getCoolUser(self, id):
        return CoolUser.get_by_id(int(id))
    
    '''
    create the user data
    '''
    def initCoolUserData(self, user):        
        moneyiousertype_list = MoneyService().getMoneyIOUserTypeList(user)
        if moneyiousertype_list == None or moneyiousertype_list.count() == 0:
            MoneyService().initMoneyIOUserTypeFromSystem(user)
    
    def getorCreateCoolUserByGoogleUser(self, google_user):
        cooluserlist = CoolUser.all().filter('googleid', google_user.user_id())
        count = cooluserlist.count()
        isnewuser=False
        if count == 0:
            if self.checkUserNameExist(google_user.nickname(), '0'):
                name = google_user.user_id()
            else:
                name = google_user.nickname()
            
            if self.checkUserEmailExist(google_user.email(), '0'):
                email = None
            else:
                email = google_user.email()
            cooluser = CoolUser(googleid=google_user.user_id(), name=name, email=email)
            cooluser.put()
            UserService().initCoolUserData(cooluser)
            isnewuser=True
        else:
            cooluser = cooluserlist[0]
            isnewuser=False
        return cooluser, isnewuser
    
    def getorCreateCoolUserBySinaUser(self, sina_user):
        cooluserlist = CoolUser.all().filter('sinaid', sina_user.id)
        count = cooluserlist.count()
        isnewuser=False
        if count == 0:
            gender = 0
            if sina_user.gender == 'm':
                gender = 0
            else:
                gender = 1
            if self.checkUserNameExist(sina_user.name, '0'):
                name = sina_user.id
            else:
                name = sina_user.name
            cooluser = CoolUser(sinaid=sina_user.id, 
                                name=name, 
                                gender=gender,
                                logo=sina_user.profile_image_url)
            cooluser.put()
            UserService().initCoolUserData(cooluser)
            isnewuser=True
        else:
            cooluser = cooluserlist[0] 
            isnewuser=False 
        return cooluser, isnewuser
    
    def updateSinaID(self, user, sina_user):        
        errormessage = None
        if user:
            user_count = CoolUser.all().filter('sinaid', sina_user.id).count()
            if user_count == 0:            
                user.sinaid = sina_user.id
                if user.logo == None:
                    user.logo = sina_user.profile_image_url
                user.put()
            else:
                errormessage = ugettext('Your sina twitter account has been bind to another account, please login with your sina twitter account directly')
        else:
            errormessage = ugettext('Your did not login')
        
        return errormessage

        
    def updateGoogleID(self, user, google_user):        
        errormessage = None
        if user:
            user_count = CoolUser.all().filter('googleid', google_user.user_id()).count()
            if user_count == 0:            
                user.googleid = google_user.user_id()
                user.put()
            else:
                errormessage = ugettext('Your google account has been bind to another account, please login with your google account directly')
        else:
            errormessage = ugettext('Your did not login')
        return errormessage
        
    def editCoolUser(self, id, name, gender, email, logo, isreceivemail, pagecount):
        user = CoolUser.get_by_id(int(id))
        if user:
            user.name = name
            user.gender = gender
            user.email = email
            user.logo = logo
            user.isreceivemail = isreceivemail
            user.pagecount = pagecount            
            user.put()