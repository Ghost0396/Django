from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record


class SignUpForm(UserCreationForm):
    """
    A form for creating new users. Includes all the required
    fields, plus repeated password verification.
    """
    FIRST_NAME_PLACEHOLDER = 'First Name'
    LAST_NAME_PLACEHOLDER = 'Last Name'
    USERNAME_PLACEHOLDER = 'User Name'
    PASSWORD_PLACEHOLDER = 'Password'
    CONFIRM_PASSWORD_PLACEHOLDER = 'Confirm Password'

    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': FIRST_NAME_PLACEHOLDER}
        )
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': LAST_NAME_PLACEHOLDER}
        )
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
        Initialize the form. Update the widget attributes and labels
        for the username, password1, and password2 fields.
        """
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': self.USERNAME_PLACEHOLDER
        })
        self.fields['username'].label = ''

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': self.PASSWORD_PLACEHOLDER
        })
        self.fields['password1'].label = ''

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': self.CONFIRM_PASSWORD_PLACEHOLDER
        })
        self.fields['password2'].label = ''


class AddRecordForm(forms.ModelForm):
    """
    A form for adding new records. Includes all the required fields.
    """
    input1 = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Input 1", "class": "form-control"}
        ),
        label=""
    )
    input2 = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Input 2", "class": "form-control"}
        ),
        label=""
    )
    input3 = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Input 3", "class": "form-control"}
        ),
        label=""
    )
    input4 = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Input 4", "class": "form-control"}
        ),
        label=""
    )
    INPUT5_CHOICES = [
        ('Option 1', 'Option 1'),
        ('Option 2', 'Option 2'),
        ('Option 3', 'Option 3'),
    ]
    input5 = forms.ChoiceField(
        choices=INPUT5_CHOICES,
        widget=forms.widgets.Select(
            attrs={"class": "form-control"}
        ),
        label=""
    )

    class Meta:
        model = Record
        fields = ('input1', 'input2', 'input3', 'input4', 'input5')
