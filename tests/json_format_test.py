from unittest import TestCase
import json
from request import Request
from unittest import mock

def mocked_requests_get():
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.text = json.dumps(json_data)

        def json(self):
            return self.json_data

    return MockResponse({"exemplo_chave": "exemplo_valor"}, 200)


class RequestTest(TestCase):

    @classmethod
    def setUpClass(self):
        self.request = Request('hotTechCompanies')

    #Testa se a funcao call_api retorna um json do request
    @mock.patch('requests.post')
    def test_call_api(self, mocked_request_get):
        self.assertEquals(self.request.call_api(), mocked_request_get().json())

    #Testa se a funcao de validate_response retorna um dict
    def test_validate_response(self):
        self.assertTrue(isinstance(
            self.request.validate_response(mocked_requests_get()), dict
        ))
