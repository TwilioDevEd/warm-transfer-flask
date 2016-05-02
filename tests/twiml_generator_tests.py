from .base import BaseTest
from warm_transfer_flask import twiml_generator


class RootTest(BaseTest):

    def test_wait_conference(self):
        response = twiml_generator.generate_wait()

        root = self.assertXmlDocument(bytes(bytearray(response, encoding='utf-8')))
        wait_message = 'Thank you for calling. Please wait in line for a few seconds. An agent will be with you shortly.'
        self.assertEquals([wait_message], root.xpath('./Say/text()'))
        wait_music = 'http://com.twilio.music.classical.s3.amazonaws.com/BusyStrings.mp3'
        self.assertEquals([wait_music], root.xpath('./Play/text()'))
