from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, mobile_number, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not mobile_number:
            raise ValueError('Users must have a mobile_number')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            mobile_number=mobile_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, mobile_number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            mobile_number=mobile_number,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    like_choices = [[0 ,'email'],[1 ,'facebook'],[2 ,'google']]
    user_id         = models.AutoField(primary_key=True)
    email           = models.EmailField(verbose_name="email", max_length=60,unique=True, null=True, blank=True,default=None)
    profile_photo   = models.ImageField(default="default.png", upload_to="profile_pics")
    username        = models.CharField(max_length=50, blank=True)
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    mobile_number   = PhoneNumberField(unique=True, null=True, blank=True,default=None)
    mobile_code     = models.CharField(max_length=50,default="",null=True,blank=True)
    user_status     = models.BooleanField(default=True)
    facebook_token  = models.CharField(max_length=200,blank=True)
    google_token    = models.CharField(max_length=200,blank=True)
    login_type      = models.IntegerField(default=0,choices=like_choices)
    date_joined     = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)

    notification_token = models.CharField(max_length=256, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'mobile_number']

    objects = MyAccountManager()

    # def __str__(self):
    #     return self.email
    def save(self, *args, **kwargs):
        if not self.email:
            self.email = None
        super(Account, self).save(*args, **kwargs)
    
    def getAbsolutePhoneNumber(self):
        return str(self.mobile_number)[3:]

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True