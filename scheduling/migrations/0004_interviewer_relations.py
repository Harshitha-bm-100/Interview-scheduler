from django.db import migrations, models
import django.db.models.deletion


def copy_interviewer_relations(apps, schema_editor):
    Interview = apps.get_model('scheduling', 'Interview')
    Interviewer = apps.get_model('scheduling', 'Interviewer')
    InterviewSlot = apps.get_model('scheduling', 'InterviewSlot')
    database = schema_editor.connection.alias

    for interview in Interview.objects.using(database).all():
        names = (name.strip() for name in interview.interviewers_text.split(','))
        for name in filter(None, names):
            interviewer, _ = Interviewer.objects.using(database).get_or_create(name=name)
            interview.interviewers.add(interviewer)

    assigned_interviewers = set()
    for slot in InterviewSlot.objects.using(database).all():
        name = slot.interviewer_name.strip()
        if not name:
            raise RuntimeError(
                'Cannot migrate an InterviewSlot without an interviewer name.'
            )
        interviewer, _ = Interviewer.objects.using(database).get_or_create(name=name)
        if interviewer.pk in assigned_interviewers:
            raise RuntimeError(
                f'Multiple InterviewSlot rows exist for {name!r}; keep one availability row per interviewer before migrating.'
            )
        assigned_interviewers.add(interviewer.pk)
        slot.interviewer_id = interviewer.pk
        slot.save(using=database, update_fields=['interviewer'])


def restore_interviewer_names(apps, schema_editor):
    Interview = apps.get_model('scheduling', 'Interview')
    InterviewSlot = apps.get_model('scheduling', 'InterviewSlot')
    database = schema_editor.connection.alias

    for interview in Interview.objects.using(database).all():
        interview.interviewers_text = ', '.join(
            interviewer.name for interviewer in interview.interviewers.all()
        )
        interview.save(using=database, update_fields=['interviewers_text'])

    for slot in InterviewSlot.objects.using(database).all():
        slot.interviewer_name = slot.interviewer.name
        slot.save(using=database, update_fields=['interviewer_name'])


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0003_remove_interviewslot_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interviewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='interview',
            old_name='interviewers',
            new_name='interviewers_text',
        ),
        migrations.RenameField(
            model_name='interviewslot',
            old_name='Interviewer',
            new_name='interviewer_name',
        ),
        migrations.AddField(
            model_name='interview',
            name='interviewers',
            field=models.ManyToManyField(related_name='interviews', to='scheduling.interviewer'),
        ),
        migrations.AddField(
            model_name='interviewslot',
            name='interviewer',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='scheduling.interviewer',
            ),
        ),
        migrations.RunPython(copy_interviewer_relations, restore_interviewer_names),
        migrations.AlterField(
            model_name='interview',
            name='interviewers_text',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='interviewslot',
            name='interviewer_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='interviewslot',
            name='interviewer',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='slot',
                to='scheduling.interviewer',
            ),
        ),
        migrations.RemoveField(
            model_name='interview',
            name='interviewers_text',
        ),
        migrations.RemoveField(
            model_name='interviewslot',
            name='interviewer_name',
        ),
    ]
