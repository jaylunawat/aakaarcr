from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import ContactMessage, Submission, TaskZero


class CRRegistrationForm(UserCreationForm):
    username = None
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    college = forms.CharField(max_length=200)
    academic_year = forms.ChoiceField(
        choices=(
            ("1st Year (UG)", "1st Year (UG)"),
            ("2nd Year (UG)", "2nd Year (UG)"),
            ("3rd Year (UG)", "3rd Year (UG)"),
            ("4th Year (UG)", "4th Year (UG)"),
            ("Postgraduate / M.Tech / PhD", "Postgraduate / M.Tech / PhD"),
        )
    )

    class Meta:
        model = get_user_model()
        fields = ("full_name", "email", "phone", "college", "academic_year", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if get_user_model().objects.filter(username=email).exists():
            raise ValidationError("An account with this email already exists. Please sign in instead.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        name_parts = self.cleaned_data["full_name"].strip().split(maxsplit=1)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ""
        if commit:
            user.save()
            TaskZero.objects.create(
                user=user,
                crid=f"AK26{user.id:05d}",
                names=self.cleaned_data["full_name"].strip(),
                username=user.username,
                email=user.email,
                emails=user.email,
                colgName=self.cleaned_data["college"].strip(),
                state="",
                city="",
                mobileNo=self.cleaned_data["phone"].strip(),
                dept="",
                whatsappNo=self.cleaned_data["phone"].strip(),
                pincode="",
                address="",
                academic_year=self.cleaned_data["academic_year"],
            )
        return user


class CRLoginForm(AuthenticationForm):
    username = forms.EmailField(label="College email")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = TaskZero
        fields = (
            "names",
            "colgName",
            "state",
            "city",
            "mobileNo",
            "dept",
            "whatsappNo",
            "pincode",
            "address",
            "academic_year",
            "avatar",
        )


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ("link", "file")

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("link") and not cleaned_data.get("file"):
            raise ValidationError("Add either a public evidence link or an upload before submitting.")
        return cleaned_data


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "subject", "message")
