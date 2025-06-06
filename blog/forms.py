from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label="Ім'я", max_length=100, required=True,
                           widget=forms.TextInput(attrs={"class": "form-control",
                                                         "placeholder": "Введіть ваше ім'я..."}))
    email = forms.EmailField(label="Електронна пошта", required=True,
                             widget=forms.EmailInput(attrs={"class": "form-control",
                                                            "placeholder": "Введіть електронну пошту..."}))
    phone = forms.CharField(label="Номер телефону", max_length=20, required=True,
                            widget=forms.TextInput(attrs={"class": "form-control",
                                                          "placeholder": "Введіть ваш номер телефону..."}))
    message = forms.CharField(label="Питання", required=True,
                              widget=forms.Textarea(attrs={"class": "form-control",
                                                           "placeholder": "Введіть ваше питання тут"}))
