# Generated by Django 3.1 on 2020-08-26 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0003_auto_20200825_2152'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeCase',
            fields=[
                ('inputresult_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tools.inputresult')),
            ],
            bases=('tools.inputresult',),
        ),
    ]