from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        label="Ονοματεπώνυμο",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Το ονοματεπώνυμό σας",
            }
        ),
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Το email σας",
            }
        ),
    )

    phone = forms.CharField(
        label="Τηλέφωνο",
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Το τηλέφωνό σας (προαιρετικό)",
            }
        ),
    )

    subject = forms.CharField(
        label="Θέμα",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Θέμα μηνύματος",
            }
        ),
    )

    message = forms.CharField(
        label="Μήνυμα",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Γράψτε το μήνυμά σας...",
                "rows": 6,
            }
        ),
    )