# views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from assignments.models import Assignment, Problem, CodeRun
from assignments.forms import CodeRunForm
from django.conf import settings
import os
import uuid
import subprocess
from pathlib import Path

def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignment_list.html', {'assignments': assignments})

def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    problems = assignment.problem_set.all()
    return render(request, 'assignment_detail.html', {'assignment': assignment, 'problems': problems})

def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    error_message = None

    if request.method == "POST":
        form = CodeRunForm(request.POST)
        action = request.POST.get('action')

        if form.is_valid():
            submission = form.save(commit=False)
            submission.problem = problem
            submission.save()

            if action == "run":
                output = run_code(submission.language, submission.code, submission.input_data)
                submission.output_data = output
                submission.save()
                return render(request, "results.html", {"submission": submission})

            elif action == "submit":
                test_cases = problem.test_cases  # Define how you get test cases
                correct_results = problem.correct_results  # Define how you get correct results
                results = submit_code(submission.language, submission.code, test_cases, correct_results)
                submission.output_data = results
                submission.save()
                return render(request, "results.html", {"submission": submission})

        else:
            error_message = "Form is not valid. Please check your inputs."

    else:
        form = CodeRunForm()

    return render(request, 'problem_detail.html', {'problem': problem, 'form': form, 'error_message': error_message})

def run_code(language, code, input_data):
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())

    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    with open(input_file_path, "w") as input_file:
        input_file.write(input_data)

    with open(output_file_path, "w") as output_file:
        pass  # This will create an empty file

    if language == "cpp":
        executable_path = codes_dir / unique
        compile_result = subprocess.run(
            ["g++", str(code_file_path), "-o", str(executable_path)]
        )
        if compile_result.returncode == 0:
            with open(input_file_path, "r") as input_file:
                with open(output_file_path, "w") as output_file:
                    subprocess.run(
                        [str(executable_path)],
                        stdin=input_file,
                        stdout=output_file,
                    )
    elif language == "py":
        # Code for executing Python script
        with open(input_file_path, "r") as input_file:
            with open(output_file_path, "w") as output_file:
                subprocess.run(
                    ["python3", str(code_file_path)],
                    stdin=input_file,
                    stdout=output_file,
                )

    # Read the output from the output file
    with open(output_file_path, "r") as output_file:
        output_data = output_file.read()

    return output_data

def submit_code(language, code, test_cases, correct_results):
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    submission_results = []

    for idx, case in enumerate(test_cases):
        unique = str(uuid.uuid4())
        code_file_name = f"{unique}.{language}"
        input_file_name = f"{unique}.txt"
        output_file_name = f"{unique}.txt"

        code_file_path = codes_dir / code_file_name
        input_file_path = inputs_dir / input_file_name
        output_file_path = outputs_dir / output_file_name

        # Write code to file
        with open(code_file_path, "w") as code_file:
            code_file.write(code)

        # Write input data to file
        input_data = case["input"]
        with open(input_file_path, "w") as input_file:
            input_file.write(input_data)

        # Prepare output file for storing outputs
        with open(output_file_path, "w") as output_file:
            pass  # Empty file creation

        if language == "cpp":
            # Compile C++ code
            executable_path = codes_dir / unique
            compile_result = subprocess.run(
                ["g++", str(code_file_path), "-o", str(executable_path)]
            )
            if compile_result.returncode == 0:
                # Execute code
                with open(output_file_path, "w") as output_file:
                    subprocess.run(
                        [str(executable_path)],
                        stdin=open(input_file_path),
                        stdout=output_file,
                    )
        elif language == "py":
            # Execute Python code
            with open(output_file_path, "w") as output_file:
                subprocess.run(
                    ["python3", str(code_file_path)],
                    stdin=open(input_file_path),
                    stdout=output_file,
                )

        # Read output from file
        with open(output_file_path, "r") as output_file:
            output_data = output_file.read().strip()

        # Compare output with expected result
        expected_output = case["expected_output"]
        if output_data == expected_output:
            result = "Passed"
        else:
            result = "Failed"

        # Store result
        submission_results.append({
            "test_case": idx + 1,
            "input": input_data,
            "expected_output": expected_output,
            "output": output_data,
            "result": result,
        })

    return submission_results
