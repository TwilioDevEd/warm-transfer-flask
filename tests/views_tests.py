from .base import BaseTest


class RootTest(BaseTest):

    def test_renders_all_questions(self):
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)
