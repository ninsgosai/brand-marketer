from django import forms
from django.contrib.auth.forms import UserCreationForm
from BrandBoosterUser.models import Account
from .models import Company_Info, Category
from phonenumber_field.formfields import PhoneNumberField

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=60,widget=forms.TextInput(attrs={'placeholder':'firstname','class':'form-control','style':'height:55px;border-radius:0px;'}))
    last_name = forms.CharField(max_length=60,widget=forms.TextInput(attrs={'placeholder':'lastname','class':'form-control','style':'height:55px;border-radius:0px;'}))
    email = forms.EmailField(max_length=60,widget=forms.TextInput(attrs={'placeholder':'email','class':'form-control','style':'height:55px;border-radius:0px;'}))
    mobile_number = forms.CharField(max_length=60,widget=forms.TextInput(attrs={'placeholder':'mobile number','class':'form-control','style':'height:55px;border-radius:0px;','value':'+91'}))
    password1 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder':'password','class':'form-control','style':'background-color:white;height:55px;border-radius:0px;'}))
    password2 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder':'confirm password','class':'form-control','style':'background-color:white;height:55px;border-radius:0px;'}))
    class Meta:
        model = Account
        fields = ("first_name","last_name","email","mobile_number","password1","password2")
    
    # def is_valid(self):
    #     self.mobile_number = PhoneNumberField.( str( "+91"+str(self.data['mobile_number']) ) )
    #     print(self.mobile_number)
    #     return super(RegistrationForm, self).is_valid()

class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company_Info

        fields = ['company_name', 'company_category','custom_category', 'company_short_info', 'company_long_info', 'company_ceo', 'company_address',
            'company_city','company_state','company_pincode','company_phone','company_whatsapp','company_telephone', 'company_email', 'company_domain', 'company_photo','cover_image']
        
        labels = {
            'company_name': 'Company name',
            'company_category': 'Category',
            'company_short_info': 'Tag line',
            'company_long_info': 'Description',
            'company_ceo': 'Contact person',
            'company_address': 'Address',
            'company_city':'City',
            'company_state':'State',
            'company_pincode':'Pincode',
            'company_email': 'Email',
            'company_phone': 'Phone number',
            'company_whatsapp' : 'Whatsapp Number',
            'company_telephone': 'Telephone number',
            'company_domain': 'Website',
            'company_photo': 'Logo',
            'cover_image' : 'Cover Image'
        }
        
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_name', 'required':'true'}),
            'company_category': forms.Select(attrs={'class': 'form-control', 'id': 'company_category', 'required':'true'}),
            'custom_category': forms.TextInput(attrs={'class': 'form-control', 'id': 'custom_category'}),
            'company_short_info': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_short_info', 'required':'true'}),
            'company_short_info': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_short_info', 'required':'true'}),
            'company_long_info': forms.Textarea(attrs={'class': 'form-control', 'id': 'company_long_info', 'rows': '4', 'required':'true'}),
            'company_ceo': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_ceo', 'required':'true'}),
            'company_address': forms.Textarea(attrs={'class': 'form-control', 'id': 'company_address', 'rows': '4', 'required':'true'}),
            'company_city': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_city', 'required':'true'}),
            'company_state': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_state', 'required':'true'}),
            'company_pincode': forms.NumberInput(attrs={'class': 'form-control', 'id': 'company_pincode', 'required':'true'}),
            'company_email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'company_email', 'required':'true'}),
            'company_phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_phone', 'required':'true', 'value':'+91' ,'maxlength':''}),
            'company_whatsapp': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_whatsapp', 'required':'true', 'value':'+91' ,'maxlength':''}),
            'company_telephone': forms.NumberInput(attrs={'class': 'form-control', 'id': 'company_telephone'}),
            'company_domain': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_domain', 'required':'true' ,'value':'http://'}),
            'company_photo': forms.FileInput(attrs={'class': 'form-control', 'id': 'company_photo', 'required':'true', 'accept':'image/*'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control', 'id': 'company_video', 'required':'true', 'accept':'image/*'})
        }

class CompanyEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.Company_Info = Company_Info
        super(CompanyEditForm, self).__init__(*args, **kwargs)
        self.fields['company_photo'] = forms.ImageField(label='Logo', initial= Company_Info.company_photo,required=False)
        self.fields['cover_image'] = forms.ImageField(label='Cover image', initial= Company_Info.cover_image,required=False)
    
    class Meta:
        model = Company_Info

        fields = ['company_name', 'company_category','custom_category' ,'company_short_info', 'company_long_info', 'company_ceo', 'company_address',
            'company_city','company_state','company_pincode','company_phone','company_whatsapp','company_telephone', 'company_email', 'company_domain', 'company_photo','cover_image']
        
        labels = {
            'company_name': 'Company name',
            'company_category': 'Category',
            'company_short_info': 'Tag line',
            'company_long_info': 'Description',
            'company_ceo': 'Contact person',
            'company_address': 'Address',
            'company_city':'City',
            'company_state':'State',
            'company_pincode':'Pincode',
            'company_email': 'Email',
            'company_phone': 'Phone number',
            'company_whatsapp': 'WhatsApp number',
            'company_telephone': 'Telephone number',
            'company_domain': 'Website',
            'company_photo': 'Logo',
            'cover_image' : 'Cover Image'
        }
        
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_name', 'required':'true'}),
            'company_category': forms.Select(attrs={'class': 'form-control', 'id': 'company_category', 'required':'true'}),
            'custom_category': forms.TextInput(attrs={'class': 'form-control', 'id': 'custom_category'}),
            'company_short_info': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_short_info', 'required':'true'}),
            'company_long_info': forms.Textarea(attrs={'class': 'form-control', 'id': 'company_long_info', 'rows': '4', 'required':'true'}),
            'company_ceo': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_ceo', 'required':'true'}),
            'company_address': forms.Textarea(attrs={'class': 'form-control', 'id': 'company_address', 'rows': '4', 'required':'true'}),
            'company_city': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_city', 'required':'true'}),
            'company_state': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_state', 'required':'true'}),
            'company_pincode': forms.NumberInput(attrs={'class': 'form-control', 'id': 'company_pincode', 'required':'true'}),
            'company_email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'company_email', 'required':'true'}),
            'company_phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_phone', 'required':'true', 'value':'+91','maxlength':''}),
            'company_whatsapp': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_whatsapp', 'required':'true', 'value':'+91','maxlength':''}),
            'company_telephone': forms.NumberInput(attrs={'class': 'form-control', 'id': 'company_telephone'}),
            'company_domain': forms.TextInput(attrs={'class': 'form-control', 'id': 'company_domain', 'required':'true','value':'http://'}),
        }
