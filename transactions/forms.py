from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from .models import UserJsonUpload
import json

class SignUpForm(UserCreationForm):  # Inherit from UserCreationForm to handle passwords
    mobile_number = forms.CharField(max_length=15)
    city = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Use password1 and password2

    def save(self, commit=True):
        user = super().save(commit=False)  # Save the user instance
        if commit:
            user.save()  # Save the user instance to the database

            # Save the UserProfile instance with mobile and city fields
            UserProfile.objects.create(
                user=user,
                mobile=self.cleaned_data['mobile_number'],
                city=self.cleaned_data['city']
            )

        return user


class UserJsonUploadForm(forms.ModelForm):
    file_upload = forms.FileField(label="Upload JSON file")

    class Meta:
        model = UserJsonUpload
        fields = ['name', 'place', 'date_of_birth', 'country', 'mobile_number']  

    def save(self, commit=True):
        instance = super().save(commit=False)
        uploaded_file = self.files.get('file_upload')

        if uploaded_file:
            try:
                import json
                data = json.load(uploaded_file)
                instance.json_data = json.dumps(data)  # ✅ Save as text to match model
            except Exception as e:
                raise forms.ValidationError("Invalid JSON file")

        if commit:
            instance.save()
        return instance