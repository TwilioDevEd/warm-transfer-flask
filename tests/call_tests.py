from .base import BaseTest
from mock import Mock
from warm_transfer_flask import call


class CallTest(BaseTest):

    def test_call_agent(self):
        # given
        rest_client_mock = Mock()
        call.TwilioRestClient = Mock(return_value=rest_client_mock)
        call.ENV = {'TWILIO_ACCOUNT_SID': 'sid321',
                    'TWILIO_AUTH_TOKEN': 'auth123',
                    'TWILIO_NUMBER': '+55'}
        mocked_call = Mock()
        rest_client_mock.calls.create.return_value = mocked_call
        mocked_call.sid = 'CallSid'

        # when
        sid = call.call_agent('agent1', 'callback')

        # then
        call.TwilioRestClient.assert_called_with('sid321', 'auth123')
        rest_client_mock.calls.create.assert_called_with(to='client:agent1',
                                                         from_='+55',
                                                         url='callback')
        self.assertEquals(sid, mocked_call.sid)
