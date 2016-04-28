from .base import BaseTest
from mock import Mock
from warm_transfer_flask import token


class TokenTest(BaseTest):

    def test_get_token(self):
        # given
        capability_mock = Mock()
        token.TwilioCapability = Mock(return_value=capability_mock)
        token.ENV = {'TWILIO_ACCOUNT_SID': 'sid321',
                     'TWILIO_AUTH_TOKEN': 'auth123'}
        capability_mock.generate.return_value = 'token123'

        # when
        generated_token = token.generate('agent10')
        self.assertEquals('token123', generated_token)

        # then
        token.TwilioCapability.assert_called_with('sid321', 'auth123')
        capability_mock.allow_client_incoming.assert_called_with('agent10')
