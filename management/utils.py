from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def iin_validator(iin):
    if iin.isdigit and len(iin) == 12:
        return iin
    else:
        raise ValidationError('ИИН введен некорректно')


phn_validator = RegexValidator(
    regex=r'^\+?1?\d{9,12}$',
    message="Введите номер в формате +77012223344"
)


def file_path(instance, filename):
    return f'{instance.iin}/{filename}'
