import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0002_application_availabilitywindow_interview_jobopening_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobopening',
            name='deadline',
            field=models.DateField(default=datetime.date(2026, 12, 31)),
            preserve_default=False,
        ),
    ]
