from django import forms
from .models import Account




class RegistrationForm(forms.ModelForm): 
    """Representation of the register model"""     
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})) # Isso aqui não irá para o banco, serve apenas para validar o passw.
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'phone_number', 'email', 'password']
        labels = {
            
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'phone_number': 'Phone Number',
            'email': 'E-mail',
            'password': 'Password',
        }
        
    def clean(self): 
        """It allows checking if two or more inputs form are equal."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data        


