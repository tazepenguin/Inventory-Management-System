from django import forms
from .models import Product, Transaction, Location

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'category', 'description', 'unit_price', 'reorder_level']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['product', 'transaction_type', 'quantity', 'source_location', 'destination_location', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source_location'].queryset = Location.objects.filter(is_active=True)
        self.fields['destination_location'].queryset = Location.objects.filter(is_active=True)

    def clean(self):
        cleaned_data = super().clean()
        ttype = cleaned_data.get('transaction_type')
        source = cleaned_data.get('source_location')
        dest = cleaned_data.get('destination_location')
        if ttype == 'IN' and not dest:
            self.add_error('destination_location', 'Destination location is required for stock in.')
        if ttype == 'OUT' and not source:
            self.add_error('source_location', 'Source location is required for stock out.')
        if ttype == 'TRANSFER' and (not source or not dest):
            self.add_error('source_location', 'Both source and destination required for transfer.')
            self.add_error('destination_location', 'Both source and destination required for transfer.')
        return cleaned_data