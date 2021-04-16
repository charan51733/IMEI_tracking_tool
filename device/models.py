from django.db import models
from django.core.exceptions import ValidationError
import re,datetime



class oem(models.Model):
    name = models.CharField(max_length=100,blank=False,unique=True,null=False)

    def __str__(self):
        return self.name.capitalize()

class model(models.Model):
    name = models.CharField(max_length=100,blank=False,null=False)
    oem = models.ForeignKey(oem,on_delete=models.CASCADE, null=False,blank=False)

    class Meta:
        unique_together = ('oem', 'name',)

    def __str__(self):
        return self.name.upper()

def dateValidate(value):
    date_string = value
    date_string = date_string.strip()
    if len(date_string) != 0:
        date_format = '%m/%d/%Y'
        try:
            date_obj = datetime.datetime.strptime(date_string, date_format)
        except ValueError:
            raise ValidationError("Incorrect data format, should be MM/DD/YYYY")

def validate_imei(value):
    if not re.match(r'^[0-9]{15}$',str(value)):
        raise ValidationError("Imei, Please enter valid Imei!.")

class device(models.Model):

    hardware = [("Early Dev Samples","Early Dev Samples"),("Pre-LE","Pre-LE"),("LE","LE"),("FAI","FAI"),("FFW","FFW"),("VIP KIT","VIP KIT")]

    imei            = models.BigIntegerField(unique=True, null=False,validators =[validate_imei],verbose_name=('IMEI'))
    wfi_mac         = models.CharField(max_length=225,null=True, blank=True,verbose_name=('WFI MAC'))
    iccid           = models.CharField(max_length=225,null=True, blank=True,verbose_name=('ICCID'))
    imsi            = models.CharField(max_length=225,null=True, blank=True,verbose_name=('IMSI'))
    mdn             = models.CharField(max_length=225,null=True, blank=True,verbose_name=('MDN'))
    assignee        = models.CharField(max_length=225,null=True, blank=True,verbose_name=('ASSIGNEE'),default=None)
    assigned_date   = models.CharField(max_length=50,default=datetime.datetime.now().strftime('%m/%d/%Y'),null=True,blank=True,verbose_name=('ASSIGNED DATE'),validators=[dateValidate])
    purpose         = models.CharField(max_length=225,null=True,blank=True,verbose_name=('PURPOSE'))
    return_date     = models.CharField(max_length=50,null=True,blank=True,verbose_name=('RETURN DATE'),validators=[dateValidate])
    comment         = models.TextField(null=True, blank=True,verbose_name=('COMMENT'))
    oem             = models.ForeignKey(oem,on_delete=models.CASCADE,null=False, blank=False,verbose_name=('OEM'))
    model          = models.ForeignKey(model,on_delete=models.CASCADE,null=False, blank=False,verbose_name=('MODEL'))
    hardware_type  = models.CharField(max_length=225, null=False, blank=False,choices=hardware,default=hardware[0],verbose_name=('HARDWARE TYPE'))

    def __str__(self):
        return self.oem.__str__().capitalize() + " - " + self.model.__str__().capitalize()