from django.contrib.auth.models import User
from django.contrib.gis.db import models
from model_utils import Choices
from django.utils import timezone


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100, null=False)
    contractor_email = models.CharField(max_length=100, null=False)
    description = models.TextField(default="no description")
    location = models.PointField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.project_name


class Materials(models.Model):
    MATERIALS = Choices('Cement', 'Brick', 'Sand', 'Ballast', 'Metal rods', 'Roofing tiles')
    material_name = models.CharField(choices=MATERIALS, default=MATERIALS.Cement, max_length=20)
    # quantity
    quantity = models.IntegerField(null=False)
    # project reference
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='materials')

    def __str__(self):
        return self.name


class Requests(models.Model):
    material = models.ForeignKey(Materials, on_delete=models.CASCADE, related_name='requests')
    quantity = models.IntegerField(null=False)
    photo = models.ImageField(default='projects/default.jpeg', upload_to='projects')
    location = models.PointField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projects')
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("material", "project")


class Reports(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reports')
    report_name = models.CharField(max_length=100, null=False)
    photo = models.ImageField(default='projects/default.jpeg', upload_to='projects')
    location = models.PointField()
    overview = models.TextField(blank=False)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("report_name", "project")


class EmailRecipients(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
