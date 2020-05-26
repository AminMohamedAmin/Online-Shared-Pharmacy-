from django import forms

PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range(1,11)]


class CartAddProductForm(forms.Form):
    # TODO: Define form fields here
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int, widget=forms.NumberInput(attrs={'class' : 'w3-white', 'style' : 'width:100px; border-radius: 5px; padding: 5px', 'min':'1', 'max':'10', }))
    update = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)