from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0004_jobopening_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobopening',
            old_name='interviewer',
            new_name='interviewers',
        ),
    ]
