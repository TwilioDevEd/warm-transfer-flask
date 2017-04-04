from twilio.twiml.voice_response import VoiceResponse, Dial


def generate_wait():
    twiml_response = VoiceResponse()
    wait_message = 'Thank you for calling. Please wait in line for a few seconds. An agent will be with you shortly.'
    wait_music = 'http://com.twilio.music.classical.s3.amazonaws.com/BusyStrings.mp3'
    twiml_response.say(wait_message)
    twiml_response.play(wait_music)
    return str(twiml_response)


def generate_connect_conference(call_sid, wait_url, start_on_enter, end_on_exit):
    twiml_response = VoiceResponse()
    dial = Dial()
    dial.conference(call_sid,
                    start_conference_on_enter=start_on_enter,
                    end_conference_on_exit=end_on_exit,
                    wait_url=wait_url)
    return str(twiml_response.append(dial))
