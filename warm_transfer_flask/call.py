from twilio.rest import TwilioRestClient
from os import environ as ENV


def call_agent(agent_id, callback_url):
    account_sid = ENV['TWILIO_ACCOUNT_SID']
    auth_token = ENV['TWILIO_AUTH_TOKEN']
    my_number = ENV['TWILIO_NUMBER']
    client = TwilioRestClient(account_sid, auth_token)
    call = client.calls.create(to=agent_id, from_=my_number,
                               url=callback_url)
    return call.sid
