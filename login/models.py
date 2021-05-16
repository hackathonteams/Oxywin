from django.db import models

# Create your models here.
class Hospital(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    state=models.CharField(max_length=50)
    pincode=models.IntegerField()
    email=models.CharField(max_length=200)
    storage=models.IntegerField()
    rate=models.IntegerField()
    available=models.IntegerField()
    hours=models.IntegerField()

class Producer(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    state=models.CharField(max_length=50)
    pincode=models.IntegerField()
    email=models.CharField(max_length=200)
    storage=models.IntegerField()
    rate=models.IntegerField()
    available=models.IntegerField()

class Transporter(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    state=models.CharField(max_length=50)
    pincode=models.IntegerField()
    email=models.CharField(max_length=200)
    avail_tanker=models.IntegerField()
    capacity=models.IntegerField()
    total_tanker=models.IntegerField()

class Order(models.Model):
    hospital_ID=models.IntegerField()
    vendor_ID=models.IntegerField()
    transporter_ID=models.IntegerField()
    quantity=models.IntegerField()
    hours=models.IntegerField()
    status=models.IntegerField()
    SOS=models.IntegerField()