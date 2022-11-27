from pritunl.constants import *
from pritunl.exceptions import *
from pritunl import utils
from pritunl import app
from pritunl import subscription
from pritunl import settings
from pritunl import auth

@app.app.route('/subscription', methods=['GET'])
@auth.session_auth
def subscription_get():
    if settings.app.demo_mode:
        resp = utils.demo_get_cache()
        if resp:
            return utils.jsonify(resp)

    subscription.update()
    resp = subscription.dict()
    if settings.app.demo_mode:
        utils.demo_set_cache(resp)
    return utils.jsonify(resp)

@app.app.route('/subscription/styles/<plan>/<ver>.css', methods=['GET'])
@auth.session_light_auth
def subscription_styles_get(plan, ver):
    try:
        styles = settings.local.sub_styles[plan]
    except KeyError:
        subscription.update()
        try:
                styles = settings.local.sub_styles[plan]
        except KeyError:
                styles = {'etag' : 0, 'last_modified' : 0, 'data' : ''}

    return utils.styles_response(
        styles['etag'],
        styles['last_modified'],
        styles['data'],
    )

@app.app.route('/subscription', methods=['POST'])
@auth.session_auth
def subscription_post():
    return utils.jsonify(subscription.dict())

@app.app.route('/subscription', methods=['PUT'])
@auth.session_auth
def subscription_put():
    return utils.jsonify(subscription.dict())

@app.app.route('/subscription', methods=['DELETE'])
@auth.session_auth
def subscription_delete():
    if settings.app.demo_mode:
        return utils.demo_blocked()

    subscription.update_license(None)
    return utils.jsonify({})
