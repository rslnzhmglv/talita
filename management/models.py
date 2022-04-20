from django.core.validators import validate_integer
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .utils import phn_validator, iin_validator, file_path
# Create your models here.


class CustomManager(BaseUserManager):
    def create_user(self, email, password):
        user = self.model(email=email, password=password)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        print(email_)
        return self.get(email=email_)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')
    date_joined = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')

    USERNAME_FIELD = 'email'

    objects = CustomManager()

    def get_short_name(self):
        return self.email

    def get_natural_key(self):
        return self.email

    def __str__(self):
        return self.email


class IdentificationData(models.Model):
    photo = models.ImageField(upload_to=file_path, blank=True, null=True, verbose_name='Фотография')
    iin = models.CharField(
        max_length=12,
        unique=True,
        db_index=True,
        validators=[iin_validator],
        verbose_name='ИИН'
    )
    date_of_birth = models.DateField(blank=True, verbose_name='Дата рождения')

    class Meta:
        abstract = True


class AddressAndContacts(models.Model):
    phone_number = models.CharField(
        validators=[phn_validator],
        max_length=12,
        unique=True,
        verbose_name='Номер телефона'
    )
    city = models.CharField(max_length=30, verbose_name='Город')
    street = models.CharField(max_length=30, verbose_name='Улица')
    house = models.CharField(max_length=4, validators=[validate_integer], verbose_name='Номер дома')
    apartment = models.CharField(max_length=4, blank=True, validators=[validate_integer], verbose_name='Номер квартиры')

    class Meta:
        abstract = True


class EmployeeDocuments(models.Model):
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Владелец'
    )
    file = models.FileField(upload_to=file_path, verbose_name='Файл')
    uploaded = models.DateTimeField(auto_now_add=True, verbose_name='Загружено')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменено')

    class Meta:
        ordering = ['uploaded']
        verbose_name = 'справки/документы'
        verbose_name_plural = '/справки/документы'

    def __str__(self):
        return f'Загружено {self.uploaded}'


class Employee(CustomUser, IdentificationData, AddressAndContacts):
    WORK_STATUS = (
        ('AW', 'На работе'),
        ('OH', 'В отпуске'),
        ('SL', 'На больничном'),
        ('OE', 'За свой счет'),
        ('DW', 'Уволен')
    )
    position = models.ForeignKey(
        'Position',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='employees',
        verbose_name='Должность'
    )
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    second_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Отчество')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    status = models.CharField(max_length=2, choices=WORK_STATUS, default='AW', db_index=True, verbose_name='Статус')

    class Meta:
        ordering = ['status']
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.last_name} {self.first_name[0]}.'


class Branch(models.Model):
    city = models.CharField(max_length=50, db_index=True, verbose_name='Город')
    name = models.CharField(max_length=50, db_index=True, verbose_name='Название филиала')
    supervisor = models.ForeignKey(
        Employee,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='branch_supervisor',
        verbose_name='Руководитель филиала'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиал'

    def __str__(self):
        return f' Филиал {self.name} г. {self.city}'


class Position(models.Model):
    office = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name='positions',
        verbose_name='Филиал'
    )
    name = models.CharField(max_length=50, db_index=True, verbose_name='Название')

    class Meta:
        ordering = ['office']
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return f'{self.name} г. {self.office.city}'



