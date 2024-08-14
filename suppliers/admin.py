from django.contrib import admin
from . import models


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'company', 'trade', 'email', 'address', 'neighborhood', 'city',
                    'state', 'country', 'zipcode', 'phone', 'fax', 'cnpj')
    search_fields = ('name','company', 'trade')


admin.site.register(models.Supplier, SupplierAdmin)
