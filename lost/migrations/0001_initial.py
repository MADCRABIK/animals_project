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
            name='LostAnimal',
            fields=[
                ('generalanimalmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='general_data.generalanimalmodel')),
                ('place', models.CharField(max_length=200, verbose_name='Где пропал(а)')),
                ('time', models.CharField(max_length=200, verbose_name='Когда пропал(а)')),
                ('special_signs', models.CharField(blank=True, max_length=200, verbose_name='Особые приметы')),
            ],
            options={
                'verbose_name': 'Потерянное животное',
                'verbose_name_plural': 'Потерянные животные',
            },
            bases=('general_data.generalanimalmodel',),
        ),
    ]
