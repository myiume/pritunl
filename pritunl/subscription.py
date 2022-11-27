from pritunl.constants import *
from pritunl.helpers import *
from pritunl.exceptions import *
from pritunl import settings
from pritunl import utils
from pritunl import messenger



def update():

    if not settings.app.id:
        settings.app.id = utils.random_name()
        settings.commit()

    settings.local.sub_active = True
    settings.local.sub_status = 'active'
    settings.local.sub_plan = 'enterprise'
    settings.local.sub_quantity = 6
    settings.local.sub_amount = 30000
    settings.local.sub_period_end = 1653834479
    settings.local.sub_trial_end = 0
    settings.local.sub_cancel_at_period_end = False
    settings.local.sub_balance = '4905000'
    settings.local.sub_url_key = 'demo'
    settings.commit()
    return True

def dict():
    if settings.app.demo_mode:
        url_key = 'demo'
    else:
        url_key = settings.local.sub_url_key

    return {
        'active': settings.local.sub_active,
        'status': settings.local.sub_status,
        'plan': settings.local.sub_plan,
        'quantity': settings.local.sub_quantity,
        'amount': settings.local.sub_amount,
        'period_end': settings.local.sub_period_end,
        'trial_end': settings.local.sub_trial_end,
        'cancel_at_period_end': settings.local.sub_cancel_at_period_end,
        'balance': settings.local.sub_balance,
        'url_key': url_key,
    }

def update_license(license):
    settings.app.license = license
    settings.app.license_plan = None
    settings.commit()
    valid = update()
    messenger.publish('subscription', 'updated')
