from django.contrib import admin

# Register your models here.
from .models import Role,Report,Profile

admin.site.register(Role)
admin.site.register(Report)
admin.site.register(Profile)
