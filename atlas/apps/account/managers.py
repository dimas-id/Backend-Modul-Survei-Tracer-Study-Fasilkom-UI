from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, password: str, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if self.model.USERNAME_FIELD == 'email':
            if not extra_fields['email']:
                raise ValueError(_("The given email must be set"))
            extra_fields['email'] = self.normalize_email(extra_fields['email'])
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password: str = None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(password, **extra_fields)

    def create_superuser(self, password: str, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self._create_user(password, **extra_fields)
