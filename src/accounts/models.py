from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('You forgot username')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
        	username = username,
            email=self.normalize_email(email),

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
        	username=username,
        	email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(
        max_length=255,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    phone_regex = RegexValidator(
    	regex=r'^\+?1?\d{9,15}$',
    	message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(
    validators=[phone_regex],
    blank=True,
    max_length=15,
    ) # validators should be a list

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number','first_name']

    def get_full_name(self):
        # The user is identified by their email address
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __unicode__ (self):          
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin