from requests import get

from app.exceptions import AuthException


class GoogleService:
    @staticmethod
    def get_token_info(id_token):
        resp = get(f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}")
        print("GoogleService.get_token_info", resp)
        if resp.status_code != 200:
            raise AuthException("Google couldn't verify idToken")
        return resp.json()
