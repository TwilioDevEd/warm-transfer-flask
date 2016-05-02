from .base import BaseTest
from warm_transfer_flask import twiml_generator


class RootTest(BaseTest):

    def test_wait_conference_contains_verb_say_with_message(self):
        response = twiml_generator.generate_wait()

        root = self.assertXmlDocument(bytes(bytearray(response, encoding='utf-8')))
        wait_message = 'Thank you for calling. Please wait in line for a few seconds. An agent will be with you shortly.'
        self.assertEquals([wait_message], root.xpath('./Say/text()'))

    def test_wait_conference_plays_music(self):
        response = twiml_generator.generate_wait()

        root = self.assertXmlDocument(bytes(bytearray(response, encoding='utf-8')))
        wait_music = 'http://com.twilio.music.classical.s3.amazonaws.com/BusyStrings.mp3'
        self.assertEquals([wait_music], root.xpath('./Play/text()'))

    def test_generate_connect_conference_xml_conference_nested_on_dial(self):
        response = twiml_generator.generate_connect_conference('', '', True, False)

        root = self.assertXmlDocument(bytes(bytearray(response, encoding='utf-8')))
        self.assertTrue(root.xpath('/Response/Dial/Conference'), response)

    def test_generate_connect_conference_uses_parameters_for_attribs(self):
        call_sid = 'CallSID'
        url = 'http://www.example.com'

        response = twiml_generator.generate_connect_conference(call_sid, url, True, False)

        root = self.assertXmlDocument(bytes(bytearray(response, encoding='utf-8')))
        conference = root.xpath('//Conference')[0]
        self.assertEquals('true', conference.attrib['startConferenceOnEnter'])
        self.assertEquals('false', conference.attrib['endConferenceOnExit'])
        self.assertEquals(url, conference.attrib['waitUrl'])
