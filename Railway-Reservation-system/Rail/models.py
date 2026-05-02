from django.db import models

# Create your models here.

class Trains(models.Model):
    Train_id = models.IntegerField(primary_key=True)
    Train_name = models.CharField(max_length=30)

    def __str__(self):
        return self.Train_name

class Stations(models.Model):
    Station_name = models.CharField(max_length=30)
    Country = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    District = models.CharField(max_length=30)

    def __str__(self):
        return self.Station_name
    
class Routes(models.Model):
    Route_id = models.IntegerField(primary_key=True)
    Train = models.ForeignKey(Trains,on_delete=models.CASCADE)
    Start_station = models.ForeignKey(Stations,on_delete=models.CASCADE,related_name="Start",null=True)
    End_station = models.ForeignKey(Stations,on_delete=models.CASCADE,related_name="End",null=True)
    Start_time = models.DateTimeField(null=False)
    End_time = models.DateTimeField(null=False)
    Distance = models.IntegerField(default=0)    

class Ticket_price(models.Model):
    Route = models.ForeignKey(Routes,on_delete=models.CASCADE,null=False,primary_key=True,default=0)
    Seat_class = models.CharField(max_length=3)
    Taxable_value = models.IntegerField(default=0)
    CGST = models.IntegerField(default=0)
    CESS = models.IntegerField(default=0)


class Seats(models.Model):
    Route = models.ForeignKey(Routes,on_delete=models.CASCADE,primary_key=True)
    Seat_id = models.CharField(max_length=6)
    Available = models.BooleanField(default=False)
    Seat_class = models.CharField(max_length=3)

class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=13)
    DoB = models.DateField(null=True)

class Transactions(models.Model):
    Transaction_id = models.IntegerField(primary_key=True)
    Booking_date = models.DateTimeField(null=False)
    Transaction_Amount = models.IntegerField(null=False)
    Payment_Method = models.CharField(max_length=5)
    Payment_Status = models.CharField(max_length=10)


class Bookings(models.Model):
    Booking_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(Users,on_delete=models.CASCADE,null=False)
    PNR = models.CharField(max_length=10)
    Transaction = models.ForeignKey(Transactions,on_delete=models.CASCADE,null=False)
    Route = models.ForeignKey(Routes,on_delete=models.CASCADE,null=False)
    Seat_no = models.CharField(max_length=6)
    Booking_Status = models.CharField(max_length=5)
    Booking_Catogory = models.CharField(max_length=5)



    

