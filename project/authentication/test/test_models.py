
from sqlalchemy import inspect

from main.settings import test_engine


class TestUserDbModel():
    def test_exists_user_db_model(self):
        check = inspect(subject=test_engine).get_table_names()
        expect = 'users'

        assert expect in check, 'Table "users" do not exists!'

    def test_chek_columns_user_db_model(self):
        check = [col['name'] for col in inspect(subject=test_engine).get_columns('users')]
        expect = ['id', 'email', 'password']

        assert expect == check