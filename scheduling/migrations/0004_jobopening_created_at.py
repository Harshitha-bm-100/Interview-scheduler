import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0003_jobopening_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobopening',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='jobopening',
            options={'ordering': ['-created_at']},
        ),
    ]
