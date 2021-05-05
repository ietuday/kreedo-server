from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import FileSystemStorage
class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = True

class FileStorage(S3Boto3Storage):
    location = 'files'
    file_overwrite = True

class LocalStorage(FileSystemStorage):
    location = 'files'
    file_overwrite = True

    