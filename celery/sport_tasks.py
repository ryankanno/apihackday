from datetime import timedelta
from celery.task.schedules import crontab
from celery.task import task, periodic_task

@periodic_task(run_every=timedelta(seconds=30))
def poll_sub():
    print ("Execute every 10 seconds per task deco")    
    
from twilio.rest import TwilioRestClient
import settings_local
client = TwilioRestClient(settings_local.TWILIO_ACCOUNT_SID,
                          settings_local.TWILIO_AUTH_TOKEN)

# create a task to notify somebody of an interesting game
@task(countdown=60)
def notify_to_sms(time, message, phone_num):
    print "notify to watch called, time [%s], to number [%s], with message [%s]" % (time, message, phone_num)

    return client.sms.messages.create(to=phone_num, from_=settings_local.TWILIO_NUMBER, body=message)
