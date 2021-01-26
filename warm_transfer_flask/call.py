from twilio.rest import Client

from warm_transfer_flask import app


def call_agent(agent_id, callback_url):
    account_sid = app.config.get('TWILIO_ACCOUNT_SID')
    api_key = app.config.get('TWILIO_API_KEY')
    api_secret = app.config.get('TWILIO_API_SECRET')
    twilio_number = app.config.get('TWILIO_NUMBER')
    client = Client(api_key, api_secret, account_sid)

    to = 'client:' + agent_id
    from_ = twilio_number
    call = client.calls.create(to, from_, url=callback_url)

    return call.sid
