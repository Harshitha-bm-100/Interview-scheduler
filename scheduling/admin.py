from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminUserCreationForm

from .models import Application, AvailabilityWindow, Interview, JobOpening, User


class UserAddForm(AdminUserCreationForm):
    """Admin form for a new account. Role is chosen here."""

    class Meta(AdminUserCreationForm.Meta):
        model = User
        fields = ('username', 'role')


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = UserAddForm
    # Shown on the "add user" page. Role can be recruiter or interviewer.
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'role', 'usable_password', 'password1', 'password2'),
            },
        ),
    )
    # Role stays editable after the account exists.
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = UserAdmin.list_filter + ('role',)


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('position', 'recruiter', 'deadline', 'created_at')
    filter_horizontal = ('interviewers',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'applied_job')


@admin.register(AvailabilityWindow)
class AvailabilityWindowAdmin(admin.ModelAdmin):
    list_display = ('interviewer', 'starts_at', 'ends_at')


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'interviewer', 'starts_at', 'ends_at')
