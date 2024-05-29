from django.core.exceptions import ValidationError

from django.core.validators import RegexValidator, EmailValidator

phone_regex = RegexValidator(regex=r'^\d{9,15}$', message="El número de teléfono debe contener entre 9 y 15 dígitos.")
 

import re


def valida_cedula(value):
    cedula = str(value)
    if not cedula.isdigit():
        raise ValidationError('La cédula debe contener solo números.')

    longitud = len(cedula)
    if longitud != 10:
        raise ValidationError('La cédula debe tener 10 dígitos.')

    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    total = 0
    for i in range(9):
        digito = int(cedula[i])
        coeficiente = coeficientes[i]
        producto = digito * coeficiente
        if producto > 9:
            producto -= 9
        total += producto

    digito_verificador = (total * 9) % 10
    if digito_verificador != int(cedula[9]):
        raise ValidationError('La cédula no es válida.')

def valida_ruc(value):
    ruc = str(value)
    if not ruc.isdigit():
        raise ValidationError('El RUC debe contener solo números.')

    longitud = len(ruc)
    if longitud != 13:
        raise ValidationError('El RUC debe tener 13 dígitos.')

    coeficientes = [3, 2, 7, 6, 5, 4, 3, 2, 7, 6, 5, 4]
    total = 0
    for i in range(12):
        digito = int(ruc[i])
        coeficiente = coeficientes[i]
        producto = digito * coeficiente
        total += producto

    residuo = total % 11
    digito_verificador = 11 - residuo if residuo != 0 else 0

    if digito_verificador != int(ruc[12]):
        raise ValidationError('El RUC no es válido.')

def valida_ruc_o_cedula(value):
    cedula = str(value)
    if not cedula.isdigit():
        raise ValidationError('La cédula/RUC debe contener solo números.')

    longitud = len(cedula)
    
    if longitud == 10:
        # Validación de cédula
        coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        total = 0
        for i in range(9):
            digito = int(cedula[i])
            coeficiente = coeficientes[i]
            producto = digito * coeficiente
            if (producto > 9):
                producto -= 9
            total += producto

        digito_verificador = (total * 9) % 10
        if digito_verificador != int(cedula[9]):
            raise ValidationError('La cédula no es válida.')
    elif longitud == 13:
        # Validación de RUC
        coeficientes = [3, 2, 7, 6, 5, 4, 3, 2, 7, 6, 5, 4]
        total = 0
        for i in range(12):
            digito = int(cedula[i])
            coeficiente = coeficientes[i]
            producto = digito * coeficiente
            total += producto

        residuo = total % 11
        digito_verificador = 11 - residuo if residuo != 0 else 0

        if digito_verificador != int(cedula[12]):
            raise ValidationError('El RUC no es válido.')
    else:
        raise ValidationError('La cédula debe tener 10 dígitos o el RUC debe tener 13 dígitos.')


def valida_telefono_ecuador(value):
    telefono = str(value)
    if not telefono.isdigit():
        raise ValidationError('El número de teléfono debe contener solo números.')

    celular_pattern = re.compile(r'^09\d{8}$')
    convencional_pattern = re.compile(r'^0[2-7]\d{7}$')

    if not (celular_pattern.match(telefono) or convencional_pattern.match(telefono)):
        raise ValidationError('El número de teléfono no es válido. Debe ser un número de celular o un número de teléfono convencional de Ecuador.')


def validar_email(value):
    pass