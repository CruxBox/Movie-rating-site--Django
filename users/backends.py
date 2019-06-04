from users.models import Person
import logging

class AuthBackend:
    def authenticate(self,username,password):
        try:
            user = Person.objects.get(username = username)
            if user.check_password(password):
                return user
            else:
                return None
        except Person.DoesNotExist:
            logging.getLogger("error_logger").error("user with login %s does not exists " % login)
            return None
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None
    def get_user(self,user_id):
        try:
            user = Person.objects.get(pk = user_id)
            if user.active:
                return user
            return None
        except Person.DoesNotExist:
            logging.getLogger("error_logger").error("user eith %(user_id)d not found")