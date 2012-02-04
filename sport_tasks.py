from datetime import timedelta
from celery.task import task

# check which events are about to end and are "interesting"
# TODO - hardcoded 10 minutes, parameterize
from celery.task import PeriodicTask
from datetime import timedelta
class poll_subscriptions(PeriodicTask):
    run_every = timedelta(seconds=10*60)
    
    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)
        print ("Execute every 10 seconds")

    
from twilio.rest import TwilioRestClient
import settings_local
client = TwilioRestClient(settings_local.TWILIO_ACCOUNT_SID,
                          settings_local.TWILIO_AUTH_TOKEN)



# create a task to notify somebody of an interesting game
# TODO - how is time specified
@task(countdown=60)
def notify_to_sms(time, message, phone_num):
    print "notify to watch called, time [%s], to number [%s], with message [%s]" % (time, message, phone_num)

    message = client.sms.messages.create(to=phone_num, from_=settings_local.TWILIO_NUMBER, body=message)

    return
