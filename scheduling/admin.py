from django.contrib import admin
from .models import Interview, InterviewSlot, Interviewer

# Register your models here.

admin.site.register(Interview)
admin.site.register(InterviewSlot)
admin.site.register(Interviewer)

