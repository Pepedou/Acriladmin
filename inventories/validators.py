def validate_file_extension(file, valid_extensions: list):
    """
    Validates that a file has the specified extension(s).
    :param file: The file to assess.
    :param valid_extensions: A list containing strings with the valid
    extensions.
    :return:
    """
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(file.name)[1]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Sólo se soportan archivos con las siguientes extensions: {0}',
                              ', '.join(valid_extensions))
