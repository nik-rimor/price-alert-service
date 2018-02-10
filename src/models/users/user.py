import uuid

from src.models.alerts.alert import Alert
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
import  src.models.users.constants as UserConstants




class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id


    def __repr__(self):
        return "<User {}>".format(self.email)


    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that the email.password combo (as sent by the site form) is valid.
        Checks that the email exists and that the password associated with it is correct.
        :param email: the users email
        :param password:  a SHA512 hashed password
        :return: true if valid combo, false otherwise
        """
        user_data = Database.find_one(collection=UserConstants.COLLECTION, query={'email': email}) # password in sha512 -> pbkdf2_sha512
        if user_data == None:
            # tell the user their email doesn't exist
            raise  UserErrors.UserNotExistsError("The user is not registered.")
        if not Utils.check_hashed_password(password, user_data['password']):
            # Tell them that their password is wrong
            raise UserErrors.IncorrectPasswordError("The password is not correct")

        return True


    @staticmethod
    def register_user(email, password):
        """
        This method registers a user using email and password.
        The password already comes hashed as sha-512.
        :param email: user's email (may be invalid)
        :param password: sha-512 hashed password
        :return: True if registered successfully or False otherwise (exceptions can alse be raised)
        """
        user_data = Database.find_one(collection= UserConstants.COLLECTION, query= {"email": email})

        if user_data is not None:
            # Tell user they are already registered
            raise UserErrors.UserNotExistsError("This email is already registered")
        if not Utils.email_is_valid(email):
            # Tell the user their email is not constructed properly
            raise UserErrors.InvalidEmailError("The email format is not valid")

        User(email, Utils.hash_password(password)).save_to_db()

        return True


    def save_to_db(self):
        Database.insert(collection= UserConstants.COLLECTION, data=self.json())

    def json(self):
        return {
            "_id": self ._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls,email):
        return cls(**Database.find_one(collection=UserConstants.COLLECTION, query={"email": email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)