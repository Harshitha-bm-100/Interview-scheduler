from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0004_interviewer_relations'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='interview',
            index=models.Index(
                fields=['date', 'start_time'],
                name='interview_date_start_idx',
            ),
        ),
    ]
