
from sqlalchemy import inspect

from main.settings import engine, engine_test


class TestUserDbModel():
    def test_exists_user_db_model(self):
        check = inspect(subject=engine).get_table_names()
        expect = 'users'

        assert expect in check, 'Table "users" do not exists!'

    def test_chek_columns_user_db_model(self):
        check = [col['name'] for col in inspect(subject=engine).get_columns('users')]
        expect = ['id', 'email', 'password']

        assert expect == check 


class TestUserDbTestModel():
    def test_exists_user_db_test_model(self):
        check = inspect(subject=engine_test).get_table_names()
        expect = 'users'

        assert expect in check, 'Table "users" do not exists!'

    def test_chek_columns_user_db_test_model(self):
        check = [col['name'] for col in inspect(subject=engine_test).get_columns('users')]
        expect = ['id', 'email', 'password']

        assert expect == check