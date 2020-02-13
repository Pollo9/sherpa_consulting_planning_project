# Generated by Django 2.2.9 on 2020-02-13 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bdd_consultants',
            old_name='nom_prenom',
            new_name='mdp',
        ),
        migrations.AddField(
            model_name='bdd_consultants',
            name='nom',
            field=models.CharField(default=' ', max_length=400),
        ),
        migrations.AddField(
            model_name='bdd_consultants',
            name='nom_de_compte',
            field=models.CharField(default=' ', max_length=400),
        ),
        migrations.AddField(
            model_name='bdd_consultants',
            name='prenom',
            field=models.CharField(default=' ', max_length=400),
        ),
    ]
