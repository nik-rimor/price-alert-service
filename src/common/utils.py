
from passlib.hash import pbkdf2_sha512
import re

class Utils(object):

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The SHA512 password from the login/register form
        :return: A sha512 -> pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)


    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password the user sent matches the one hashed in the database
        :param password: SHA512 hashed password from front end
        :param hashed_password: the PBKDF2 encrypted password in the database for the user
        :return: True if password match, false otherwise
        """

        return pbkdf2_sha512.verify(password, hashed_password)


    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile("^[\w.-]+@([\w-]+\.)+[\w]+$")
        return True if email_address_matcher.match(email) else False
