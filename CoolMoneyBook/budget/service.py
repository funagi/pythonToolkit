'''
Created on 2010-11-16

@author: jeffrey
'''

from model.models import Budget, BudgetDetail

class BudgetService:
    def encode(self, budgetdetail_list):
        result = {"iTotalRecords": budgetdetail_list.count(), "iTotalDisplayRecords": budgetdetail_list.count()}
        item = []
        for budgetdetail in budgetdetail_list:
            item.append(budgetdetail.to_dict())
        result.update({"aaData": item})
        return result
    
    def updateBudgetDetailActualMoney(self, budgetdetail, moneystat):
        if moneystat:
            if moneystat.income_dict.has_key(budgetdetail.moneyiousertype.name):
                budgetdetail.actualmoney = moneystat.income_dict[budgetdetail.moneyiousertype.name]
            elif moneystat.expense_dict.has_key(budgetdetail.moneyiousertype.name):
                budgetdetail.actualmoney = moneystat.expense_dict[budgetdetail.moneyiousertype.name]
            budgetdetail.put()
            
    def getBudgetList(self, filter_dict, orderby, page_size, current_page, user):
        budget_list = Budget.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                budget_list = budget_list.filter(filter_key, filter_dict[filter_key])
        
        if user:
            budget_list = budget_list.filter('user', user)
        
        total_records = budget_list.count()
        
        if orderby:
            budget_list = budget_list.order(orderby)
        
        if page_size > 0:
            budget_list = budget_list.fetch(page_size, page_size * (current_page-1))
           
        return budget_list, total_records
    
    def getBudgetCount(self, filter_dict, user):
        budget_list = Budget.all()        
        
        if filter_dict:
            for filter_key in filter_dict.keys():
                budget_list = budget_list.filter(filter_key, filter_dict[filter_key])
        
        if user:
            budget_list = budget_list.filter('user', user)
           
        return budget_list.count()
    
    def addBudget(self, name, begindate, enddate, currency, description, user):
        budget = Budget(name = name, 
                        begindate = begindate, 
                        enddate = enddate, 
                        currency = currency,
                        description = description, user = user)
        budget.put()
        return budget
    
    def editBudget(self, id, name, begindate, enddate, currency, description, user):
        budget = BudgetService().getBudget(id, user)
        if budget:
            budget.name = name
            budget.begindate = begindate
            budget.enddate = enddate
            budget.currency = currency
            budget.description = description
            budget.user = user
            budget.put()
        return budget
    
    def addBudgetDetail(self, budget, moneyiousertype, money):
        budgetdetail = BudgetDetail(budget = budget, moneyiousertype = moneyiousertype, money = money)
        budgetdetail.put()
    
    def deleteBudgetDetail(self, budget):
        budgetdetail_list = BudgetDetail.all().filter('budget', budget)
        for budgetdetail in budgetdetail_list:
            budgetdetail.delete()
    
    def editBudgetDetail(self, id, budget, moneyiousertype, money):
        budgetdetail = BudgetDetail(budget = budget, moneyiousertype = moneyiousertype, money = money)
        budgetdetail.put()
    
    def deleteBudget(self, id, user):
        budget = self.getBudget(id, user)
        if budget:
            budgetdetail_list = BudgetDetail.all().filter('budget', budget)
            for budgetdetail in budgetdetail_list:
                budgetdetail.delete()
            budget.delete()
            
    def getBudget(self, id, user):
        budget = None
        try:
            budget = Budget.get_by_id(int(id))
            if budget.user.id <> user.id:
                budget = None
        except:
            budget = None
        return budget
    
    def getBudgetDetailList(self, budget):
        return BudgetDetail.all().filter('budget', budget)
    
    
        