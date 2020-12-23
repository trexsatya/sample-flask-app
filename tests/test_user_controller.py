

class TestUserController:
    def test_that_application_handles_user_request(self, testapp):
        response = testapp.get("/api/v1/users", status="*")
        assert response is not None
        assert response.status_code == 200

        response = testapp.get("/api/v1/users/1", status="*")
        assert response is not None
        assert response.status_code == 200
