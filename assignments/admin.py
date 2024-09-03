# admin.py
from django.contrib import admin
from assignments.models import Assignment, Problem, CodeRun

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'assignment', 'description', 'constraints', 'sample_input', 'sample_output', 'test_cases', 'correct_results')

admin.site.register(Assignment)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(CodeRun)
from django.apps import AppConfig


class AssignmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assignments'
