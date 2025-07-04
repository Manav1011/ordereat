from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    # uses email authentication instead of username

    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('Email field not found')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        return self.create_user(email,password,**extra_fields)    

    def get_or_create(self, email, password=None, **extra_fields):
        try:
            user = self.get(email=email)
            created = False
        except self.model.DoesNotExist:
            user = self.create_user(email, password, **extra_fields)
            created = True
        return user, created
    
    def get_or_create_by_name(self, name=None,role=None, **extra_fields):
        try:
            user = self.get(name=name,role=role)
            created = False
        except self.model.DoesNotExist:
            user = self.create(name=name, role=role, is_active=False,**extra_fields)
            created = True
        return user, created