# filepath: edtech_project/education/admin.py
from django.contrib import admin
from .models import UploadedContent

admin.site.register(UploadedContent)