from django.db import models
from django.conf import settings
from django.urls import reverse



class Slider_Images(models.Model):
    image = models.ImageField(upload_to='slider_images/')
    def __str__(self):
        return self.image.name

class Main_Slider(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    images = models.ManyToManyField(Slider_Images, blank=True)
    def __str__(self):
        return self.title
    

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('onlinecourse:course_details', args=[str(self.id)])
    

class Partners(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partner_images/')
    def __str__(self):
        return self.name


class Customers(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='customer_images/')
    def __str__(self):
        return self.name
    

class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    def __str__(self):
        return self.name
   
    