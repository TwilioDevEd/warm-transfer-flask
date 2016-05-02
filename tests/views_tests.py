from .base import BaseTest
from mock import Mock
import json
from flask import url_for
from warm_transfer_flask import views
from warm_transfer_flask.models import ActiveCall


class RootTest(BaseTest):

    def test_renders_all_questions(self):
        response = self.client.get('/')

        self.assertEquals(200, response.status_code)

    def test_generate_token(self):
        views.token = token_mock = Mock()
        token_mock.generate.return_value = 'token123'

        response = self.client.post('/user1/token')
        response_as_dict = json.loads(response.data.decode('utf8'))
        expected_dict = {'token': 'token123', 'agentId': 'user1'}

        self.assertEquals(200, response.status_code)
        self.assertEquals(expected_dict, response_as_dict)
        token_mock.generate.assert_called_with('user1')

    def test_call_agent(self):
        ActiveCall.create('agent1', 'conference123')
        views.call = call_mock = Mock()
        call_mock.call_agent.return_value = 'CallSid'
        connect_agent_url = url_for('connect_agent', agent_id='agent2',
                                    conference_id='conference123')

        response = self.client.post('/conference/agent2/call')

        self.assertEquals(200, response.status_code)
        self.assertEquals('CallSid', response.data.decode('utf8'))
        call_mock.call_agent.assert_called_with('agent2', connect_agent_url)

    def test_wait_conference(self):
        views.twiml_generator = twiml_mock = Mock()
        twiml_mock.generate_wait.return_value = 'Twiml for waiting'

        response = self.client.post('conference/wait')

        self.assertEquals(200, response.status_code)
        self.assertEquals('Twiml for waiting', response.data.decode('utf8'))
        twiml_mock.generate_wait.assert_called()

    def test_connect_agent1(self):
        views.twiml_generator = twiml_mock = Mock()
        twiml_mock.generate_connect_conference.return_value = 'Twiml'

        response = self.client.post('conference/ConferenceId/connect/agent1')

        self.assertEquals(200, response.status_code)
        self.assertEquals('Twiml', response.data.decode('utf8'))
        twiml_mock.generate_connect_conference.assert_called_with('ConferenceId', views.AGENT_WAIT_URL, True, False)

    def test_connect_agent2(self):
        views.twiml_generator = twiml_mock = Mock()
        twiml_mock.generate_connect_conference.return_value = 'Twiml'

        response = self.client.post('conference/ConferenceId/connect/agent2')

        self.assertEquals(200, response.status_code)
        self.assertEquals('Twiml', response.data.decode('utf8'))
        twiml_mock.generate_connect_conference.assert_called_with('ConferenceId', views.AGENT_WAIT_URL, True, True)

    def test_connect_client(self):
        views.twiml_generator = twiml_mock = Mock()
        views.call = call_mock = Mock()
        call_mock.call_agent.return_value = 'CallSid'
        twiml_mock.generate_connect_conference.return_value = 'Twiml'
        connect_agent_url = url_for('connect_agent', agent_id='agent1',
                                    conference_id='call123')

        response = self.client.post('/conference/connect/client',
                                    data={'CallSid': 'call123'})

        self.assertEquals(200, response.status_code, response.data)
        self.assertEquals('Twiml', response.data.decode('utf8'))
        twiml_mock.generate_connect_conference.assert_called_with('call123', url_for('wait'), False, True)
        call_mock.call_agent.assert_called_with('agent1', connect_agent_url)

    def test_connect_client_sets_active_call(self):
        views.twiml_generator = twiml_mock = Mock()
        views.call = call_mock = Mock()
        call_mock.call_agent.return_value = 'CallSid'
        twiml_mock.generate_connect_conference.return_value = 'Twiml'

        self.client.post('/conference/connect/client',
                         data={'CallSid': 'call123'})

        self.assertEquals(1, ActiveCall.query.count())
        self.assertEquals('agent1', ActiveCall.query.first().agent_id)
        self.assertEquals('call123', ActiveCall.query.first().conference_id)
