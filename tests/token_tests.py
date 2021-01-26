from .base import BaseTestCase
from unittest.mock import Mock
from warm_transfer_flask import token


class TokenTest(BaseTestCase):
    def test_get_token(self):
        # given
        access_token = Mock()
        token.AccessToken = Mock(return_value=access_token)
        access_token.to_jwt.return_value = b'token123'

        # when
        generated_token = token.generate('agent10')
        self.assertEquals('token123', generated_token)

        # then
        token.AccessToken.assert_called_with(
            'ACxxx', 'SKxxx', 'xxxxx', identity='agent10'
        )
        access_token.add_grant.assert_called_once()
