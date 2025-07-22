# school/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Subject

@login_required
@permission_required('school.can_view', raise_exception=True)
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {'subjects': subjects})

@login_required
@permission_required('school.can_create', raise_exception=True)
def create_subject(request):
    if request.method == 'POST':
        name = request.POST['name']
        Subject.objects.create(name=name, teacher=request.user)
        return redirect('subject_list')
    return render(request, 'create_subject.html')

@login_required
@permission_required('school.can_edit', raise_exception=True)
def edit_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.name = request.POST['name']
        subject.save()
        return redirect('subject_list')
    return render(request, 'edit_subject.html', {'subject': subject})

@login_required
@permission_required('school.can_delete', raise_exception=True)
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()
    return redirect('subject_list')
