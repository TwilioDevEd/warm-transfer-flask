from xml.etree import ElementTree

from .base import BaseTestCase
from warm_transfer_flask import twiml_generator


class RootTest(BaseTestCase):
    def test_wait_conference_contains_verb_say_with_message(self):
        response = twiml_generator.generate_wait()

        xml = ElementTree.fromstring(response)
        wait_message = (
            'Thank you for calling. Please wait in line for a few seconds.'
            ' An agent will be with you shortly.'
        )
        self.assertEquals(wait_message, xml.find('./Say').text)

    def test_wait_conference_plays_music(self):
        response = twiml_generator.generate_wait()

        xml = ElementTree.fromstring(response)
        wait_music = 'http://com.twilio.music.classical.s3.amazonaws.com/BusyStrings.mp3'
        self.assertEquals(wait_music, xml.find('./Play').text)

    def test_generate_connect_conference_xml_conference_nested_on_dial(self):
        response = twiml_generator.generate_connect_conference('', '', True, False)

        xml = ElementTree.fromstring(response)
        self.assertEquals(xml.tag, 'Response')
        self.assertIsNotNone(xml.find('./Dial/Conference'))

    def test_generate_connect_conference_uses_parameters_for_attribs(self):
        call_sid = 'CallSID'
        url = 'http://www.example.com'

        response = twiml_generator.generate_connect_conference(call_sid, url, True, False)

        xml = ElementTree.fromstring(response)
        conference = xml.find('./Dial/Conference')
        self.assertEquals('true', conference.attrib['startConferenceOnEnter'])
        self.assertEquals('false', conference.attrib['endConferenceOnExit'])
        self.assertEquals(url, conference.attrib['waitUrl'])
