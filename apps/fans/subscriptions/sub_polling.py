import datetime

from celery.task import task, periodic_task
from twilio.rest import TwilioRestClient

import settings

from fans.models import Subscription
from fans.subscriptions import sub_rules

@periodic_task(run_every=datetime.timedelta(seconds=settings.SUB_EVAL_INTERVAL_SEC))
def poll_subcriptions():
    '''
    Poll according to defined interval and determine if subscription's "interesting or not"
    '''
    print "Polling all subscriptions..."

    for sub in Subscription.objects.all():
        print "Processing subscription..."
        process_subscription.delay(sub)

@task
def process_subscription(sub):
    print "Processing subscription..."

    if sub_rules.alert_on_game(sub):
        print "Alerting for subscription..."
        notify_to_sms("alert TODO ...", sub.phone_num)

def notify_to_sms(message, phone_num):
    print "notify to watch called, to number [%s], with message [%s]" % (message, phone_num)
#    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#    return client.sms.messages.create(to=phone_num, from_=settings.TWILIO_NUMBER, body=message)

