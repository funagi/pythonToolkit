'''
Created on 2010-11-9

@author: jeffrey
'''

from model.models import Object

class ObjectService:
    def checkObjectNameExist(self, name, id, user):
        object_list = Object.all().filter('name', name).filter('user', user)
        if object_list.count() == 0:
            return False
        elif object_list.count() == 1:
            if id and object_list[0].id == id:
                return False
            else:
                return True
        else:
            return True  
    
    def getObjectCount(self, filter_dict, user):
        object_list = Object.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                object_list = object_list.filter(filter_key, filter_dict[filter_key])
        
        if user:
            object_list = object_list.filter('user', user)
           
        return object_list.count()
    
    def getObjectList(self, filter_dict, orderby, pagesize, pagecount, user):
        object_list = Object.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                object_list = object_list.filter(filter_key, filter_dict[filter_key])
        
        if user:
            object_list = object_list.filter('user', user)
        
        total_records = object_list.count()
        
        if orderby:
            object_list = object_list.order(orderby)
        
        if pagesize > 0:
            object_list = object_list.fetch(pagesize, pagesize * (pagecount-1))
           
        return object_list, total_records
    
    def getObject(self, id, user):
        object = None
        try:
            object = Object.get_by_id(int(id))
            if object.user.id <> user.id:
                object = None
        except:
            object = None
        return object
    
    def deleteObject(self, id, user):
        object = self.getObject(id, user)
        if object:
            object.delete()
    
    def addObject(self, name, finishdate, money, currency, accountlist, description, user):
        object = Object(name=name, finishdate=finishdate, money=money, currency=currency,accountlist=accountlist,description=description, user=user)        
        object.put()
        #AccountService().updateObjectStatus(object) 
        
    def editObject(self, id, name, finishdate, money, currency, accountlist, description, user):
        object = self.getObject(id, user)
        if object:
            object.name = name
            object.finishdate = finishdate
            object.money = money
            object.currency = currency
            object.accountlist = accountlist
            object.description = description 
            if user:
                object.user = user       
            object.put()
            
            #AccountService().updateObjectStatus(object)