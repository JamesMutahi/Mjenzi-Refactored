from django.contrib import admin

from . import Project, Materials, Requests, Reports

admin.site.register(Project)
admin.site.register(Materials)
admin.site.register(Reports)
admin.site.register(Requests)
