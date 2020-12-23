from sqlalchemy.orm import class_mapper

from app.entities.user import User


class TestUserController:
    def test_that_application_handles_user_request(self, testapp):
        response = testapp.get("/api/v1/users", status="*")
        assert response is not None
        assert response.status_code == 200

        response = testapp.get("/api/v1/users/1", status="*")
        assert response is not None
        assert response.status_code == 200

    def test_that_invalid_data_is_not_allowed_in_creation(self, testapp):
        # Invalid name: number instead of string
        response = testapp.post_json("/api/v1/users", {"name": 1231, "email": "abc@mail.com"}, status="*")
        assert response.status_code == 400

        # Too long name
        response = testapp.post_json("/api/v1/users", {"name": "1234567891011", "email": "abc@mail.com"}, status="*")
        assert response.status_code == 400

        # Invalid email
        response = testapp.post_json("/api/v1/users", {"name": "1234", "email": "invalid_mail"}, status="*")
        assert response.status_code == 400

    def test_that_we_can_create_new_user(self, testapp, db):
        response = testapp.post_json("/api/v1/users", {"name": "ivhas", "email": "abc@mail.com"}, status="*")
        assert response.status_code == 200
        assert response.json["name"] == "ivhas"

    def test_that_user_is_saved_to_database_after_creation(self, testapp, db):
        response = testapp.post_json("/api/v1/users", {"name": "ivhas", "email": "abc@mail.com"}, status="*")
        assert len(db.session.query(User).all()) == 1
