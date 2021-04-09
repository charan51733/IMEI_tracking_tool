from import_export import resources
from .models import device, oem, model
from django.core.exceptions import ValidationError
import re
import datetime
from django.utils.encoding import force_str
import xlrd

class DeviceResource(resources.ModelResource):
    class Meta:
        model = device
        fields = ("imei","wfi_mac","iccid","mdn","assignee",'assigned_date',"purpose","comment","oem","model","delivery",'return_date')
        import_id_fields =  ('imei',)
        exclude = ('id',)


    # def export(self):

    def before_import_row(self, row, **kwargs):
        name = str(row.get('oem'))
        name.strip()

        Error = {}
        if len(name) != 0:
            brand,_create = oem.objects.get_or_create(name=name.lower().strip())
            row['oem'] = brand.id
        else:
            Error.update({'OEM': ["Please enter valid Oem!."]})
            # raise ValidationError("OEM, Please enter valid Oem!.")

        modelName = str(row.get('model'))
        modelName.strip()
        if len(modelName) != 0:
            brandModelData = {"name": modelName.lower().strip(), "oem": name.lower().strip()}
            # artist_id, created = Track.objects.get_or_create(artist=Artist(title=artist.title))
            brand_model,_create = model.objects.get_or_create(name=modelName.lower().strip(),oem=brand)
            row['model'] = brand_model.id
        else:
            Error.update({'MODEL': ["Please enter valid Model!."]})
            # raise ValidationError("MODEL, Please enter valid Model!.")

        dalivery = str(row.get('delivery')).strip()

        if len(dalivery) == 0:
            Error.update({'DELIVERY': ["Please enter valid Delivery!."]})
        else:
            if dalivery not in dict(device.delivary_type).values():
                daliveryStr = ', '.join([str(x) for x in dict(device.delivary_type).values()])
                Error.update({'DELIVERY': ["Please enter valid Delivery!,should be any of these {} ".format(daliveryStr)]})

        assignee = str(row.get('assignee'))
        assignee = assignee.strip()
        if len(assignee) == 0:
            row['assignee'] = None

        imei = str(row.get('imei'))
        imei = int(float(imei))

        if not re.match(r'^[0-9]{15}$',str(imei)):
            Error.update({'IMEI': ["Please enter valid Imei!."]})
            # raise ValidationError("IMEI, Please enter valid Imei!.")

        # imei = str(imei).split('.')[0]
        # print(imei)
        # row['imei'] = imei

        assign_date = row.get('assigned_date')


        if isinstance(assign_date, float):
            datetime_date = xlrd.xldate_as_datetime(assign_date, 0)
            date_object = datetime_date.date()
            assign_date = date_object.strftime('%m/%d/%Y')
        elif isinstance(assign_date, str):
            assign_date = assign_date.strip()

            if len(assign_date) != 0:
                date_format = '%m/%d/%Y'
                try:
                    datetime.datetime.strptime(assign_date, date_format)
                    row['assigned_date'] = assign_date
                except ValueError:
                    Error.update({'Assigned Date': ["Incorrect data format, should be MM/DD/YYYY."]})
                    # raise ValidationError("Incorrect data format, should be MM/DD/YYYY")
        else:
            row['assigned_date'] = None
        return_date = ''
        return_date = row.get('return_date')

        if isinstance(return_date, float):
            datetime_date = xlrd.xldate_as_datetime(return_date, 0)
            date_object = datetime_date.date()
            return_date = date_object.strftime('%m/%d/%Y')
        elif isinstance(return_date, str):
            return_date = return_date.strip()

            if len(return_date) != 0:

                date_format = '%m/%d/%Y'
                try:
                    datetime.datetime.strptime(return_date, date_format)
                    row['return_date'] = return_date
                except ValueError:
                    Error.update({'Return Date': ["Incorrect data format, should be MM/DD/YYYY."]})
                    # raise ValidationError("Incorrect data format, should be MM/DD/YYYY")
        else:
            row['return_date'] = None

        if Error:
            raise ValidationError(Error)


class DeviceExportResource(resources.ModelResource):
    class Meta:
        model = device
        fields = ("imei","wfi_mac","iccid","mdn","assignee",'assigned_date',"purpose","comment","oem__name","model__name","delivery",'return_date')
        import_id_fields =  ('imei',)
        exclude = ('id',)

    def get_export_headers(self):
        headers = [
            force_str(field.column_name) for field in self.get_export_fields()]

        headers[headers.index("oem__name")] = "oem"
        headers[headers.index("model__name")] = "model"
        return headers