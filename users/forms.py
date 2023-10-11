from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, SetPasswordForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False, label='Электронная почта')
    first_name = forms.CharField(required=False, label='Имя')
    last_name = forms.CharField(required=False, label='Фамилия')
    patronymic = forms.CharField(required=False, label='Отчество')
    # phone = forms.CharField(required=False, label='Телефон')
    phone = forms.CharField(label='Телефон', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 999 123-45-67'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'patronymic', 'phone', 'password1', 'password2')
        exclude = ('type',)

    def save(self, commit=True):

        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    def clean(self):
        phone = self.cleaned_data['phone']
        phone = '+' + ''.join([char for char in phone if char.isdigit()])


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=False, label='Электронная почта',widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=False, label='Имя',widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, label='Фамилия',widget=forms.TextInput(attrs={'class': 'form-control'}))
    patronymic = forms.CharField(required=False, label='Отчество',widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=False, label='Телефон',widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'patronymic', 'phone', 'photo')
        exclude = ('password',)
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['photo'].required = False


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    error_messages = {
        "invalid_login": 
            'НЕВЕРНЫЙ ЛОГИН И/ИЛИ ПАРОЛЬ. Попробуйте снова.'
        ,
        "inactive": "This account is inactive.",
    }
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                "Этот аккаунт не активен.",
                code='inactive',
            )
        if user.ban:
            raise ValidationError(
                "Вы не можете войти, обратитесь к администратору",
                code='fired',
            )

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']


class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput, required=False)
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'patronymic', 'phone', 'photo']
        exclude = ['username', 'sender', 'type']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают. Пожалуйста, введите пароли заново.")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['title', 'city', 'region', 'metro', 'street', 'home_number', 'room_number', 'index', 'info']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True  # Установка title как обязательного поля

    def save(self, commit=True):
        instance = super(AddressForm, self).save(commit=False)
        instance.users = self.initial['user']  # Установка значения user из initial
        if commit:
            instance.save()
        return instance

class AddressEditForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['title', 'city', 'region', 'metro', 'street', 'home_number', 'room_number', 'index', 'info']


class CustomUserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=None,
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].help_text = "Введите новый пароль."

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

