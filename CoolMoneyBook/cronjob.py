#coding:utf-8

# Standard Python imports.
import os
import sys
import logging

from appengine_django import InstallAppengineHelperForDjango
InstallAppengineHelperForDjango()

from appengine_django import have_django_zip
from appengine_django import django_zip_path

# Google App Engine imports.
from google.appengine.ext.webapp import util

from google.appengine.ext import webapp
from model.models import Alarm
from alarm.service import AlarmService

class Alarm(webapp.RequestHandler):
    def get(self):
        '''Get all alarms'''
        alarm_list = AlarmService().getAlarmList(None, None, 0, 0, None)[0]
        for alarm in alarm_list:
            AlarmService().executeAlarm(alarm)

def main():
    # Ensure the Django zipfile is in the path if required.
    if have_django_zip and django_zip_path not in sys.path:
        sys.path.insert(1, django_zip_path)
    
    application = webapp.WSGIApplication([('/cronjob/alarm', Alarm)
                                        ],
                                       debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__': 
    main()
