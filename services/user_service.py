from collections.user import User
import time as ts

class UserService(object):
    @staticmethod
    def create_user(keywords,email,city):
        """
        Create a new user
        """

        user = User(keywords=keywords,email=email,city=city,timestamp=ts.time()).save()
        return user

    @staticmethod
    def modify_user(User):
       ##ee
       return "NULL"

    @staticmethod
    def list_users():
        """
        Get created users
        :return:
        :rtype:
        """
        return User.objects()
    

    @staticmethod
    def get_user(email):
        """
        Get created user
        :return:
        :rtype:
        """
        return User.objects.get(email=email)

    @staticmethod
    def delete_user(email):
        """
        Delete the study
        """
        User.objects(email=email).delete()