from import_export import resources
from .models import device, oem, model
import math
from django.core.exceptions import ValidationError
import re
import datetime

class DeviceResource(resources.ModelResource):
    class Meta:
        model = device
        fields = ("imei","wfi_mac","iccid","mdn","assignee",'assigned_date',"purpose","comment","oem","model","delivery",'return_date')
        import_id_fields =  ('imei',)
        exclude = ('id',)

    # def export(self):

    def before_import_row(self, row, **kwargs):
        name = str(row.get('oem'))
        brand,_create = oem.objects.get_or_create(name=name.lower().strip())
        row['oem'] = brand.id

        modelName = str(row.get('model'))
        brandModelData = {"name": modelName.lower().strip(), "oem": name.lower().strip()}
        # artist_id, created = Track.objects.get_or_create(artist=Artist(title=artist.title))
        brand_model,_create = model.objects.get_or_create(name=modelName.lower().strip(),oem=brand)
        row['model'] = brand_model.id

        imei = str(row.get('imei'))
        imei = imei.strip(".0")

        if not re.match(r'^[0-9]+$',str(imei)):
            raise ValidationError("Imei, Please enter valid Imei!.")

        row['imei'] = imei

        assign_date = str(row.get('assigned_date'))
        assign_date = assign_date.strip()
        if len(assign_date) != 0:
            date_format = '%Y-%m-%d'
            try:
                row['assigned_date']  = datetime.datetime.strptime(assign_date, date_format)
            except ValueError:
                raise ValidationError("Incorrect data format, should be YYYY-MM-DD")

        return_date = str(row.get('return_date'))
        return_date = return_date.strip()
        if len(return_date) != 0:
            date_format = '%Y-%m-%d'
            try:
                row['return_date']  = datetime.datetime.strptime(return_date, date_format)
            except ValueError:
                raise ValidationError("Incorrect data format, should be YYYY-MM-DD")

    # def before_export(self, queryset, *args, **kwargs):
    #     """
    #     Override to add additional logic. Does nothing by default.
    #     """
    #     """
    #         SELECT "device_device"."id", "device_device"."imei", "device_device"."wfi_mac",
    #         "device_device"."iccid", "device_device"."imsi", "device_device"."mdn", "device_device"."assignee",
    #         "device_device"."assigned_date", "device_device"."purpose", "device_device"."return_date",
    #         "device_device"."comment", "device_device"."oem_id", "device_device"."model_id",
    #         "device_device"."delivery" FROM "device_device" ORDER BY "device_device"."id" DESC
    #     """
    #     print(queryset)

    # def after_export(self, queryset, data, *args, **kwargs):
    #     """
    #     Override to add additional logic. Does nothing by default.
    #     """
    #     data.dict[0]['oem'] = "Dasarathi"
    #     # print(data.get('oem'))

