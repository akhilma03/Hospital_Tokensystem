from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, hospital_name, district, city,phone, email, password=None):
        if not email:
            raise ValueError("You must have email address")

        user = self.model(
            email=self.normalize_email(email),
            hospital_name=hospital_name,
            district_id=district,
            city_id=city,
            phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, hospital_name,email, password,district,city,phone):
        user = self.create_user(
            email=self.normalize_email(email),
            hospital_name=hospital_name,
            password=password,
            district=district,
            city=city,
            phone=phone
          
        
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class District(models.Model):
    district = models.CharField(max_length=100)

    def __str__(self):
        return self.district


class City(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.city


class Hospital(AbstractBaseUser):
    hospital_name = models.CharField(max_length=50,blank=True,null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE,blank=True,null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE,blank=True,null=True)
    email = models.EmailField(max_length=30, unique=True,blank=True,null=True)
    phone = models.CharField(max_length=10, blank=True,null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['hospital_name','city','district','phone']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    
class Doctor(models.Model):
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=50,unique=True)
    specialization = models.CharField(max_length=200)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    password = models.CharField(max_length=100)


    def __str__(self):
        return self.name
    
    
    
