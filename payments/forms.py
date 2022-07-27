from django.forms import ModelForm
from .models import Payments


class PaymentForm(ModelForm):
    class Meta:
        model = Payments
        fields = ['name', 'amount', 'payment_note']

    def __init__(self,*args, **kwargs):
        super(PaymentForm,self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})    