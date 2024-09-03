# models.py
from django.db import models
from django.utils import timezone

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default="No description provided")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title}: {self.description[:50]}"  # Adjust as needed

    def total_problems(self):
        return self.problem_set.count()

class Problem(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(default="No description provided")
    constraints = models.TextField(default="No constraints provided")
    sample_input = models.TextField(default="No sample input provided")
    sample_output = models.TextField(default="No sample output provided")
    test_cases = models.TextField(default="No test cases provided")
    correct_results = models.TextField(default="No correct_results")  # JSON or plain text format
    time_constraint = models.CharField(max_length=50, null=True, blank=True)
    memory_constraint = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.title}"
    
# new model is created
class CodeRun(models.Model):
    language = models.CharField(max_length=100)
    code = models.TextField()
    input_data = models.TextField(null=True,blank=True)
    output_data = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)