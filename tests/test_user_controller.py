from _pytest import monkeypatch
from flask_httpauth import HTTPAuth, HTTPTokenAuth
from sqlalchemy.orm import class_mapper
import app.services.auth_service as auth
from app.entities.user import User
from app.services.auth_service import AuthService
from app.services.user_service import ExternalService
from tests.conftest import as_admin, as_user


class TestUserController:
    def setup_method(self, method):
        print("starting execution of tc: {}".format(method.__name__))

    def teardown_method(self, method):
        print("Ending execution of tc: {}".format(method.__name__))

    def test_that_application_handles_user_request(self, testapp, db):
        response = testapp.get("/api/v1/users", status="*", **as_admin())
        assert response is not None
        assert response.status_code == 404

        response = testapp.get("/api/v1/users/1", status="*", **as_admin())
        assert response is not None
        assert response.status_code == 404

    def test_that_invalid_data_is_not_allowed_in_creation(self, testapp):
        # Invalid name: number instead of string
        response = testapp.post_json("/api/v1/users", {"name": 1231, "email": "abc@mail.com"}, status="*", **as_admin())
        assert response.status_code == 400

        # Too long name
        response = testapp.post_json("/api/v1/users", {"name": "1234567891011", "email": "abc@mail.com"}, status="*",
                                     **as_admin())
        assert response.status_code == 400

        # Invalid email
        response = testapp.post_json("/api/v1/users", {"name": "1234", "email": "invalid_mail"}, status="*",
                                     **as_admin())
        assert response.status_code == 400

    def test_that_we_can_create_new_user(self, testapp, db):
        response = testapp.post_json("/api/v1/users", {"name": "ivhas", "email": "abc@mail.com"}, status="*",
                                     **as_admin())
        assert response.status_code == 200
        assert response.json["name"] == "ivhas"

    def test_that_user_is_saved_to_database_after_creation(self, testapp, db):
        response = testapp.post_json("/api/v1/users", {"name": "ivhas", "email": "abc@mail.com"}, status="*",
                                     **as_admin())
        assert len(User.find_all()) == 1

    def test_that_user_is_not_saved_to_database_if_transaction_fails(self, testapp, db, monkeypatch):
        def mock_call():
            raise Exception("Unknown")
        monkeypatch.setattr(ExternalService, "call", mock_call)
        response = testapp.post_json("/api/v1/users", {"name": "ivhas", "email": "abc@mail.com"}, status="*",
                                     **as_admin())
        assert len(User.find_all()) == 0, "Shouldn't have been saved!"

    def test_that_we_can_retrieve_the_user_created(self, testapp, db):
        response = testapp.post_json("/api/v1/users", {"name": "ivhas", "email": "abc@mail.com"}, status="*",
                                     **as_admin())
        response = testapp.get("/api/v1/users", status="*", **as_user())
        assert response.status_code == 200

        # Id=1 is automatically assigned while creating user in database; this autoincrement feature
        # is not available in all databases
        response = testapp.get(f"/api/v1/users/{1}", status="*", **as_user())
        assert response.status_code == 200

        response = testapp.post_json("/api/v1/users", {"name": "another", "email": "xyz@mail.com"}, status="*",
                                     **as_admin())
        response = testapp.get(f"/api/v1/users/{2}", status="*", **as_user())
        assert response.status_code == 200
