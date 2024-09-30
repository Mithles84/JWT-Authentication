from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, name, country, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, country=country)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'country']

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        permissions = [
             
        ]

    # Override these properties to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='Groups this user belongs to.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

class LoginLogData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login = models.DateTimeField(null=True, blank=True)
    logout = models.DateTimeField(null=True, blank=True)
    token = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.email
