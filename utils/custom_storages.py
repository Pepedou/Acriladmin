from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(S3BotoStorage):
    """
    This class is used to store static content in a different
    subdirectory in the Amazon Web Services bucket.
    """
    location = settings.STATICFILES_LOCATION

    def accessed_time(self, name):
        pass

    def created_time(self, name):
        pass

    def path(self, name):
        pass


class MediaStorage(S3BotoStorage):
    """
    This class is used to store media content in a different
    subdirectory in the Amazon Web Services bucket.
    """
    location = settings.MEDIAFILES_LOCATION

    def accessed_time(self, name):
        pass

    def created_time(self, name):
        pass

    def path(self, name):
        pass
