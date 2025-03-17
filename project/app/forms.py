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

    qr = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Enter QR", "class": "form-control"}
        ),
        label="QR"
    )

    STATION_CHOICES = [
        ('Programing', 'Programming'),
        ('MAC ID Association', 'MAC ID Association'),
        ('HMI test', 'HMI test'),
        ('Functional 1 test', 'Functional 1 test'),
        ('Cell test', 'Cell test'),
        ('Performance Test', 'Performance Test'),
        ('Functional 2 test', 'Functional 2 test'),
        ('Burn-in', 'Burn-in'),
        ('GPS 3', 'GPS 3'),
    ]
    station = forms.ChoiceField(
        required=True,
        choices=STATION_CHOICES,
        widget=forms.widgets.Select(
            attrs={"class": "form-control"}
        ),
        label="Select Station"
    )
    failure = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Enter Failed Description",
                   "class": "form-control"}
        ),
        label="Failure Description"
    )

    class Meta:
        model = Record
        fields = ('qr', 'station', 'failure')


class ReportForm(forms.ModelForm):
    COMPONENT_CHOICES = [
        ('SOOM', 'SOOM'),
        ('Sapphire', 'Sapphire'),
        ('Display', 'Display'),
        ('PIR', 'PIR'),
        ('Voltage issue', 'Voltage issue'),
        ('EG25', 'EG25'),
        ('Antenna', 'Antenna'),
        ('Buzzer', 'Buzzer'),
        ('Other', 'Other'),
    ]
    component = forms.ChoiceField(
        required=True,
        choices=COMPONENT_CHOICES,
        widget=forms.widgets.Select(
            attrs={"class": "form-control"}
        ),
        label="Select Failed Component"
    )

    COMPONENT_STATUS_OPTION = [
        ('Physical Damage', 'Physical Damage'),
        ('Wrong FW', 'Wrong FW'),
        ('Wrong HW', 'Wrong HW'),
        ('Voltage issue', 'Voltage issue'),
        ('Power on', 'Power on'),
        ('MACID format', 'MACID format'),
        ('Other', 'Other'),
    ]

    component_status = forms.ChoiceField(
        required=True,
        choices=COMPONENT_STATUS_OPTION,
        widget=forms.widgets.Select(
            attrs={"class": "form-control"}
        ),
        label="Component Status"
    )

    COMPONENT_REPAIRED_CHOICES = [
        ('Repaired', 'Repaired'),
        ('MRB', 'MRB'),
        ('Reprogrammed', 'Reprogrammed'),
        ('Waiting indications', 'Waiting indications'),
        ('Scrap', 'Scrap'),
    ]

    component_repaired = forms.ChoiceField(
        required=True,
        choices=COMPONENT_REPAIRED_CHOICES,
        widget=forms.widgets.Select(
            attrs={"class": "form-control"}
        ),
        label="Component Repaired"
    )

    notes = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Enter notes", "class": "form-control"}
        ),
        label="Notes"
    )

    SUMARY_CHOICES = [
        ('Repaired/ sent to production', 'Repaired/ sent to production'),
        ('On hold/ waiting materials', 'On hold/ waiting materials'),
        ('Dissasembled/ Qr change', 'Dissasembled/ Qr change'),
    ]

    summary = forms.ChoiceField(
        required=True,
        choices=SUMARY_CHOICES,
        widget=forms.widgets.Select(
            attrs={"class": "form-control"}
        ),
        label="Summary"
    )

    class Meta:
        model = Record
        fields = ('component', 'component_status', 'component_repaired',
                  'notes', 'summary')
