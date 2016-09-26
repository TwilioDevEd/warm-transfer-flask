from twilio.rest import Client
from os import environ as ENV


def call_agent(agent_id, callback_url):
    account_sid = ENV['TWILIO_ACCOUNT_SID']
    auth_token = ENV['TWILIO_AUTH_TOKEN']
    my_number = ENV['TWILIO_NUMBER']
    client = Client(account_sid, auth_token)
    call = client.calls.create(to='client:' + agent_id, from_=my_number,
                               url=callback_url)
    return call.sid
