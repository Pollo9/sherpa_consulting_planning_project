# Generated by Django 2.2.9 on 2020-02-15 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0002_auto_20200213_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bdd_formateurs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(default=' ', max_length=400)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Formateur',
            },
        ),
    ]