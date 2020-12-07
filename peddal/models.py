from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Brand(models.Model):
    brand_name= models.CharField(max_length=40)
    def __str__(self):
        return self.brand_name
class Cycle(models.Model):
    CHOICES = {
        ('Brand New','Brand New'),
        ('Used','Used')
    }
    name = models.CharField(max_length=40)
    brand = models.ForeignKey(Brand,on_delete=models.RESTRICT,null=True)
    color = models.CharField(max_length=40)
    cycle_description = models.CharField(max_length=800,null=True)
    hire_description= models.CharField(max_length=800,null=True)
    selling_rate = models.IntegerField(default=0, null=True)
    hire_rate = models.IntegerField(default=0,null=True)
    main_image = models.ImageField(null=True, upload_to='cycle_photo')
    rental_status = models.BooleanField(null=True,default=True)
    sold_status = models.BooleanField(null=True , default=False)
    condition = models.CharField(choices=CHOICES,max_length=30,null=True)
    published_date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name


class CycleImage(models.Model):
    cycle = models.ForeignKey(Cycle,on_delete=models.CASCADE)
    side_image = models.ImageField(upload_to='cycle_photo',null=True,blank=True)

    def __str__(self):
        return self.cycle.name + "media"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=20,null=True)
    address= models.CharField(max_length=20)
    contact = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='customer_images',default='default.jpg',null=True)

    def __str__(self):
        return self.name



class Rental(models.Model):

    customer = models.ForeignKey(Customer,on_delete=models.RESTRICT)
    cycle = models.ForeignKey(Cycle,on_delete=models.RESTRICT)
    rental_date = models.DateField(auto_now_add=False,auto_now=False)
    rental_time = models.TimeField(auto_now_add=False,null=True)
    return_date = models.DateField(auto_now_add=False,auto_now=False)
    rental_status = models.BooleanField(default=True)

    def __str__(self):
        return self.cycle



