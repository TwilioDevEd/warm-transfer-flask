from twilio import twiml


def generate_wait():
    twiml_response = twiml.Response()
    wait_message = 'Thank you for calling. Please wait in line for a few seconds. An agent will be with you shortly.'
    wait_music = 'http://com.twilio.music.classical.s3.amazonaws.com/BusyStrings.mp3'
    twiml_response.say(wait_message)
    twiml_response.play(wait_music)
    return str(twiml_response)
