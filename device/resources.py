from import_export import resources
from .models import device, oem, model
from django.core.exceptions import ValidationError
import re
import datetime
from django.utils.encoding import force_str

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

        if not re.match(r'^[0-9]{15}$',str(imei)):
            raise ValidationError("Imei, Please enter valid Imei!.")

        row['imei'] = imei

        assign_date = str(row.get('assigned_date'))
        assign_date = assign_date.strip()
        if len(assign_date) != 0:
            date_format = '%m/%d/%Y'
            try:
                datetime.datetime.strptime(assign_date, date_format)
                row['assigned_date'] = assign_date
            except ValueError:
                raise ValidationError("Incorrect data format, should be MM/DD/YYYY")

        return_date = str(row.get('return_date'))
        return_date = return_date.strip()
        if len(return_date) != 0:
            date_format = '%m/%d/%Y'
            try:
                datetime.datetime.strptime(return_date, date_format)
                row['return_date'] = return_date
            except ValueError:
                raise ValidationError("Incorrect data format, should be MM/DD/YYYY")



class DeviceExportResource(resources.ModelResource):
    class Meta:
        model = device
        fields = ("imei","wfi_mac","iccid","mdn","assignee",'assigned_date',"purpose","comment","oem__name","model__name","delivery",'return_date')
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

        if not re.match(r'^[0-9]{15}$',str(imei)):
            raise ValidationError("Imei, Please enter valid Imei!.")

        row['imei'] = imei

        assign_date = str(row.get('assigned_date'))
        assign_date = assign_date.strip()
        if len(assign_date) != 0:
            date_format = '%m/%d/%Y'
            try:
                datetime.datetime.strptime(assign_date, date_format)
                row['assigned_date'] = assign_date
            except ValueError:
                raise ValidationError("Incorrect data format, should be MM/DD/YYYY")

        return_date = str(row.get('return_date'))
        return_date = return_date.strip()
        if len(return_date) != 0:
            date_format = '%m/%d/%Y'
            try:
                datetime.datetime.strptime(return_date, date_format)
                row['return_date'] = return_date
            except ValueError:
                raise ValidationError("Incorrect data format, should be MM/DD/YYYY")

    def get_export_headers(self):
        headers = [
            force_str(field.column_name) for field in self.get_export_fields()]

        headers[headers.index("oem__name")] = "oem"
        headers[headers.index("model__name")] = "model"
        return headers