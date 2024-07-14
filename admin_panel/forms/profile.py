from django import forms


class PassowrdChangeForm(forms.Form):
    current = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "data-toggle": "password",
            }
        ),
        min_length=5,
    )
    new = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "data-toggle": "password",
            }
        ),
        min_length=6,
    )
    confirm = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "data-toggle": "password",
            }
        ),
        min_length=6,
    )
