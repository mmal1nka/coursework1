from django import forms


class ShiphrForm(forms.Form):
    Mess = forms.CharField(max_length=1000, required=False)
    Key = forms.CharField(max_length=1000, required=False)
    EncryptedMessage = forms.CharField(max_length=1000, required=False)
    Mess.widget.attrs.update({'placeholder': "Enter a message: "})
    Key.widget.attrs.update({'placeholder': "Enter a key: "})
