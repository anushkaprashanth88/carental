from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class login(models.Model):
    login_id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=225)
    password=models.CharField(max_length=225)
    usertype=models.CharField(max_length=225)
    
class users(models.Model):
    user_id=models.AutoField(primary_key=True)
    login=models.ForeignKey(login,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=225)
    second_name=models.CharField(max_length=225)
    house_name=models.CharField(max_length=225)
    place=models.CharField(max_length=225)
    pincode=models.CharField(max_length=225)
    phone=models.CharField(max_length=225)
    email=models.CharField(max_length=225)
    adhar_card=models.CharField(max_length=225)
    driving_license_back=models.FileField()
    driving_license_front=models.FileField()
    picture=models.FileField()
    latitude=models.CharField(max_length=225)
    logitu=models.CharField(max_length=225)
    
class owners(models.Model):
    owner_id=models.AutoField(primary_key=True)
    login=models.ForeignKey(login,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=225)
    second_name=models.CharField(max_length=225)
    place=models.CharField(max_length=225)
    phone=models.CharField(max_length=225)
    email=models.CharField(max_length=225)
    image=models.FileField()
    
class vehicles(models.Model):
    vehicle_id=models.AutoField(primary_key=True)
    owner=models.ForeignKey(owners,on_delete=models.CASCADE)
    brand=models.CharField(max_length=225)
    model=models.CharField(max_length=225)
    colour=models.CharField(max_length=225)
    no_seat=models.CharField(max_length=225)
    description=models.CharField(max_length=225)
    per_day_rent=models.CharField(max_length=225)
    car_status=models.CharField(max_length=225)
    vehicle_image=models.FileField()
    
class rent(models.Model):
    rent_id=models.AutoField(primary_key=True)
    total_km=models.CharField(max_length=225)
    rate=models.CharField(max_length=225)
    duration=models.CharField(max_length=225)
    extra_km_rate=models.CharField(max_length=225)
    date_time=models.CharField(max_length=225)

class booking(models.Model):
    booking_id=models.AutoField(primary_key=True)
    book_for_id=models.IntegerField()
    book_for_type=models.CharField(max_length=225)
    user=models.ForeignKey(users,on_delete=models.CASCADE)
    from_date=models.CharField(max_length=225)
    from_time=models.CharField(max_length=225)
    to_date=models.CharField(max_length=225)
    to_time=models.CharField(max_length=225)
    b_quantity=models.CharField(max_length=225)
    returned_date=models.CharField(max_length=225)
    booking_status=models.CharField(max_length=225)
    booked_datetime=models.CharField(max_length=225)
    balance_amount=models.CharField(max_length=225)
    driver=models.CharField(max_length=225)


class payment(models.Model):
    payment_id=models.AutoField(primary_key=True)
    booking=models.ForeignKey(booking,on_delete=models.CASCADE)
    payment_type=models.CharField(max_length=225)
    amount=models.CharField(max_length=225)
    datetime=models.CharField(max_length=225)

class items(models.Model):
    item_id=models.AutoField(primary_key=True)
    owner=models.ForeignKey(owners,on_delete=models.CASCADE)
    item_name=models.CharField(max_length=225)
    quantity=models.CharField(max_length=225)
    rent_per_item=models.CharField(max_length=225)
    description=models.CharField(max_length=225)
    image=models.FileField()

class images(models.Model):
    img_id=models.AutoField(primary_key=True)
    vehicle=models.ForeignKey(vehicles,on_delete=models.CASCADE)
    img=models.FileField()
    title=models.CharField(max_length=225)

class feedback(models.Model):
    feedback_id=models.AutoField(primary_key=True)
    booking=models.ForeignKey(booking,on_delete=models.CASCADE)
    rating=models.CharField(max_length=225)
    description=models.CharField(max_length=225)
    datetime=models.CharField(max_length=225)



class chatz(models.Model):
    chat_id=models.AutoField(primary_key=True)
    from_id = models.ForeignKey(login,on_delete=models.CASCADE,related_name="from_id")
    to_id = models.ForeignKey(login,on_delete=models.CASCADE,related_name="to_id")
    message = models.CharField(max_length=225)
    date_time = models.CharField(max_length=225)
    
    