# Generated by Django 2.0.3 on 2018-03-31 19:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Aureas_App', '0002_auto_20180331_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='listmodel',
            name='upload',
            field=models.FilePathField(default=django.utils.timezone.now, match='.*', path='static', recursive=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='listmodel',
            name='choice',
            field=models.CharField(choices=[('Colostethus fraterdanieli', 'Colostethus fraterdanieli'), ('Diasporus gularis', 'Diasporus gularis'), ('New folder', 'New folder')], max_length=2),
        ),
    ]
