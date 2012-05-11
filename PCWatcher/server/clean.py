from google.appengine.ext import db
from basetypes import *
import logging

def pc_key(pc_name=None):
    if pc_name:
        return db.Key.from_path('Imageviewer', pc_name)
    else:
        return db.Key.from_path('Imageviewer', 'default')
    
pclist = PCList().all().get()
pc_list = pclist.names.split('\n')
for pc in pc_list:
    query = db.GqlQuery('SELECT __key__ FROM imgitem'
                        'WHERE ANCESTER IS :1'
                        'ORDER BY time DESC',
                        pc_key(pc))
    count = query.count()
    logging.info(pc+':'+str(count))
    if count >= 100:
        query = db.GqlQuery('SELECT __key__ FROM imgitem'
                            'WHERE ANCESTER IS :1'
                            'ORDER BY time ASC',
                            pc_key(pc))
