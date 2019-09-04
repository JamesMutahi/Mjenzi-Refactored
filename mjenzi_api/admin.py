from django.contrib import admin

from .models import Project, Materials, , Reports

admin.site.register(Project)
admin.site.register(Materials)
admin.site.register(Reports)
admin.site.register(Requests)
