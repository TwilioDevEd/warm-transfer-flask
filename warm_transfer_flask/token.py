from twilio.util import TwilioCapability
from os import environ as ENV


def generate(agent_id):
    account_sid = ENV['TWILIO_ACCOUNT_SID']
    auth_token = ENV['TWILIO_AUTH_TOKEN']
    capability = TwilioCapability(account_sid, auth_token)
    capability.allow_client_incoming(agent_id)
    return capability.generate()
