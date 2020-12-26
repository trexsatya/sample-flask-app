from app.entities.user import User
from app.exceptions import AuthException
from app.services.auth_service import AuthService
from app.services.google_service import GoogleService
from tests.conftest import raise_exception


class TestAuthController:

    def test_that_we_get_access_token_if_google_verifies_given_token(self, testapp, monkeypatch, db):
        google_token_resp = {"email": "test@mail.com"}
        user = User(email=google_token_resp["email"], name="Name")
        # Given
        monkeypatch.setattr(GoogleService, "get_token_info", lambda x: google_token_resp)
        # And
        monkeypatch.setattr(User, "find_first", lambda **x: user)
        monkeypatch.setattr(AuthService, "create_token", lambda u: "fake_token")

        # When
        response = testapp.post_json("/api/v1/auth/login", {"idToken": 1231, "social": "google"}, status="*")

        # Then
        assert response.status_code == 200
        assert response.json["access_token"] == "fake_token"

    def test_that_we_dont_get_access_token_if_google_verification_fails(self, testapp, monkeypatch, db):
        # Given
        monkeypatch.setattr(GoogleService, "get_token_info", lambda x: raise_exception(AuthException("ada")))

        # When
        response = testapp.post_json("/api/v1/auth/login", {"idToken": 1231, "social": "google"}, status="*")

        # Then
        assert response.status_code == 401

    def test_that_we_user_is_saved_to_db_on_registration_via_google(self, testapp, monkeypatch, db):
        google_token_resp = {"email": "test@mail.com", "given_name": "fnam", "family_name": "snm",
                             "email_verified": "false"}
        # Given
        monkeypatch.setattr(GoogleService, "get_token_info", lambda x: google_token_resp)

        # When
        response = testapp.post_json("/api/v1/auth/register", {"idToken": 1231, "social": "google"}, status="*")

        # Then
        assert response.status_code == 200
        assert User.find_first(email=google_token_resp["email"]) is not None

