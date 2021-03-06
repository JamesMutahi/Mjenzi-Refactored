# Generated by Django 2.2.4 on 2019-09-11 06:58

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100)),
                ('contractor_email', models.EmailField(max_length=100)),
                ('description', models.TextField(default='no description')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('developer_email', models.EmailField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_name', models.CharField(choices=[('Cement', 'Cement'), ('Brick', 'Brick'), ('Sand', 'Sand'), ('Ballast', 'Ballast'), ('Metal rods', 'Metal rods'), ('Roofing tiles', 'Roofing tiles')], default='Cement', max_length=20)),
                ('quantity', models.IntegerField()),
                ('photo', models.ImageField(upload_to='Requests')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('status', models.CharField(max_length=30, null=True)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='mjenzi_api.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_name', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='Reports')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('overview', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='mjenzi_api.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Materials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_name', models.CharField(choices=[('Cement', 'Cement'), ('Brick', 'Brick'), ('Sand', 'Sand'), ('Ballast', 'Ballast'), ('Metal rods', 'Metal rods'), ('Roofing tiles', 'Roofing tiles'), ('Plywood', 'Plywood'), ('Timber', 'Timber'), ('Glass', 'Glass')], default='Cement', max_length=20)),
                ('quantity', models.IntegerField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='mjenzi_api.Project')),
            ],
        ),
    ]
