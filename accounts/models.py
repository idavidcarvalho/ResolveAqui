from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
	def create_user(self, email, firstName, lastName, password=None, **extra_fields):
		if not email:
			raise ValueError('O email deve ser informado')
		email = self.normalize_email(email)
		user = self.model(email=email, firstName=firstName, lastName=lastName, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, firstName, lastName, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)
		return self.create_user(email, firstName, lastName, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	firstName = models.CharField(max_length=150)
	lastName = models.CharField(max_length=150)
	email = models.EmailField(unique=True)
	profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
	TYPE_CHOICES = (
		('Comum', 'Comum'),
		('Gestor', 'Gestor'),
	)
	typeUser = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Comum')

	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	date_joined = models.DateTimeField(default=timezone.now)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['firstName', 'lastName']

	def __str__(self):
		return self.email
