
from authentication.schemas import UserRequestSchema, UserResponseSchema


class TestUserRequestSchema():
    def test_request_schema(self):
        check = UserRequestSchema(email='pavel@mail.ru', password='1234')
        expect = {'email' : 'pavel@mail.ru', 'password' : '1234'}

        assert check.dict() == expect, 'Not valid request schema!'


class TestUserResponseSchema():
    def test_response_shema(self):
        check = UserResponseSchema(describtion='Good answer', status_code=200, token='Your token')
        expect = {'describtion' : 'Good answer', 'status_code' : 200, 'token' : 'Your token'}
        
        assert check.dict() == expect, 'Not valid response schema!'
