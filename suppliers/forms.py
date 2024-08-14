from django import forms
from . import models


class SupplierForm(forms.ModelForm):

    class Meta:
        model = models.Supplier
        fields = ['name', 'company', 'trade', 'description', 'email', 'address', 'neighborhood', 'city', 'state', 'country', 'zipcode', 'phone', 'fax', 'cnpj']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'trade': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'neighborhood': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state':forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'fax': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'company': 'Razão Social',
            'trade': 'Nome Fantasia',
            'email': 'E-mail',
            'address': 'Endereço', 
            'neighborhood': 'Bairro',
            'city': 'Cidade',
            'state': 'Estado',
            'country': 'País',
            'zipcode': 'CEP',
            'phone': 'Telefone',
            'fax': 'Fax',
            'cnpj': 'CNPJ',
            
        }
