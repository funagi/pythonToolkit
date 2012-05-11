import xmlrpclib
        
conn = xmlrpclib.ServerProxy('http://www.pythonchallenge.com/pc/phonebook.php')
print conn.system.listMethods()
print conn.phone('Bert')