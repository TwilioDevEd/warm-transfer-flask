from .base import BaseTest
from mock import Mock
import json
from warm_transfer_flask import views


class RootTest(BaseTest):

    def test_renders_all_questions(self):
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)

    def test_generate_token(self):
        views.token = token_mock = Mock()
        token_mock.generate.return_value = 'token123'
        response = self.client.post('/user1/token')

        self.assertEquals(200, response.status_code)
        response_as_dict = json.loads(response.data.decode('utf8'))
        expected_dict = {'token': 'token123', 'agentId': 'user1'}
        self.assertEquals(expected_dict, response_as_dict)

        token_mock.generate.assert_called_with('user1')

    def test_call_agent(self):
        views.call = call_mock = Mock()
        call_mock.call_agent.return_value = 'CallSid'
        response = self.client.post('/conference/user1/call')

        self.assertEquals(200, response.status_code)
        self.assertEquals('CallSid', response.data.decode('utf8'))

        call_mock.call_agent.assert_called_with('user1')

    def test_wait_conference(self):
        response = self.client.post('conference/wait')
        self.assertEquals(200, response.status_code)

        root = self.assertXmlDocument(response.data)
        wait_message = 'Thank you for calling. Please wait in line for a few seconds. An agent will be with you shortly.'
        self.assertEquals([wait_message], root.xpath('./Say/text()'))
        wait_music = 'http://com.twilio.music.classical.s3.amazonaws.com/BusyStrings.mp3'
        self.assertEquals([wait_music], root.xpath('./Play/text()'))
