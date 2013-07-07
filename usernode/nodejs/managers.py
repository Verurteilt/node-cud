from django.contrib.auth.models import BaseUserManager


class NodeUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, twitter, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a First Name')
        if not last_name:
            raise ValueError('Users must have a Last Name')
        user = self.model(first_name=first_name, last_name=last_name, email=self.normalize_email(email), twitter=twitter)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, twitter, password):
        user = self.create_user(first_name, last_name, email, twitter, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
