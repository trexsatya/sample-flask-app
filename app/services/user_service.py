import transaction
from injector import inject

from app.dto.user import UserData
from app.entities.user import User
from app.extensions import database


class ExternalService:
    def call(self):
        # TODO: Add call to some actual service
        pass


class UserService:
    @inject
    def __init__(self, external_service: ExternalService):
        self.external_service = external_service

    def create_user(self, user_data: UserData):
        transaction.begin()
        user = User(name=user_data.name, email=user_data.email,
                    email_verified=user_data.email_verified).save(commit=False)
        self.external_service.call()
        transaction.commit()

        return user
