from django.db import models



class Supplier(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    company = models.CharField(max_length=500)
    trade = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    neighborhood = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    zipcode = models.CharField(max_length=500)
    fax = models.CharField(max_length=500)
    cnpj = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
