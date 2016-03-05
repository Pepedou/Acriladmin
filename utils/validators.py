from django.core.validators import RegexValidator

zip_code_regex_validator = RegexValidator(regex=r'^[0-9]{5}', message="El código postal consta de 5 dígitos.")

phone_regex_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                       message="El número telefónico debe ingresarse con el formato: '+999999999'. "
                                               "Se permiten hasta 15 dígitos.")
