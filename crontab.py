from crontab import CronTab
import os
import getpass

cron = CronTab(user=getpass.getuser())

job = cron.new(command='python3 ' + os.getcwd() +"/test.py")

job.minute.every(1)
cron.write()
