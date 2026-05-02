from django import forms


class from_to_Form(forms.Form):
    CHOICES = (
        ('NA' ,'None'),
        ('SEC', 'Senior Citizen'),
        ('STD', 'Student'),
    )
    From = forms.CharField(max_length=100)
    To = forms.CharField(max_length=100)
    Date = forms.DateField()
    Category = forms.ChoiceField(choices=CHOICES)

class user_Form(forms.Form):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = forms.CharField(max_length=100)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    Phone_no = forms.CharField(max_length=12)
    DoB = forms.DateField()
    Account_no = forms.CharField(max_length=20)
    CVV = forms.CharField(max_length=5)
    Expiry = forms.DateField()

class cancelation_form(forms.Form):
    PNR = forms.CharField(max_length=10)
    Phone_no = forms.CharField(max_length=12)

class train_form(forms.Form):
    Train_No = forms.IntegerField()
    Date = forms.DateField()

class revenue_form(forms.Form):
    From_Date = forms.DateField()
    To_Date = forms.DateField()

class route_form(forms.Form):
    Route_id = forms.IntegerField()


