from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

# -----------------------------
# Register Form
# -----------------------------
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": field.label
            })


# -----------------------------
# Update User Info
# -----------------------------
class ProfileUpdateForm(forms.ModelForm):
    """
    Form to handle all fields for updating the user's profile.
    This form combines user info fields with custom profile fields.
    """
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'profile_picture'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap's form-control class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
            })
            # Add a placeholder from the field's label
            if field.label:
                field.widget.attrs.update({
                    "placeholder": field.label
                })

        # Ensure email is a required field
        self.fields['email'].required = True