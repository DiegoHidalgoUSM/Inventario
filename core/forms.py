from django import forms

class ImportForm(forms.Form):
    archivo = forms.FileField(label='Seleccione un archivo Excel')


