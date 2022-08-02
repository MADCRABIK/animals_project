# Generated by Django 4.0.6 on 2022-08-02 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('general_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalToGoodHands',
            fields=[
                ('generalanimalmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='general_data.generalanimalmodel')),
            ],
            options={
                'verbose_name': 'Животное в добрые руки',
                'verbose_name_plural': 'Животные в добрые руки',
            },
            bases=('general_data.generalanimalmodel',),
        ),
    ]