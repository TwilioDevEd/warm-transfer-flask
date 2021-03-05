from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant

from warm_transfer_flask import app


def generate(agent_id):
    # Create access token with credentials
    access_token = AccessToken(
        app.config['TWILIO_ACCOUNT_SID'],
        app.config['TWILIO_API_KEY'],
        app.config['TWILIO_API_SECRET'],
        identity=agent_id,
    )

    # Create a Voice grant and add to token
    voice_grant = VoiceGrant(
        incoming_allow=True,  # add to allow incoming calls
    )
    access_token.add_grant(voice_grant)

    return access_token.to_jwt().decode()
