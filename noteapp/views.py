from django.shortcuts import render, redirect, get_object_or_404
from .models import note
from .forms import NoteForm
from django.db.models.functions import TruncDate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required

@login_required
def note_list(request):
    # Grouping notes by date and ordering by date
    notes = note.objects.filter(user=request.user).annotate(date_only=TruncDate('created_at'))
    
    # Create a dictionary to store grouped notes by date
    grouped_notes = {}
    for notee in notes:
        if notee.date_only not in grouped_notes:
            grouped_notes[notee.date_only] = []  # Create an empty list if this date is not yet in the dictionary
        grouped_notes[notee.date_only].append(notee)  # Append the note to the list for the specific date
    grouped_notes = dict(sorted(grouped_notes.items(), reverse=True))
    return render(request, 'noteapp/note_list.html', {'grouped_notes': grouped_notes})


@login_required
def add_note(request):
    if request.method=='POST':
        form=NoteForm(request.POST)
        if form.is_valid():
            note=form.save(commit=False)
            note.user=request.user
            note.save()
            return redirect('note_list')
    else:
        form=NoteForm()
    return render(request,'noteapp/add_note.html',{'form':form})



@login_required
def edit_note(request, id):
    Note = get_object_or_404(note, id=id)
    if request.method=='POST':
        form=NoteForm(request.POST, instance=Note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form=NoteForm(instance=Note)
    return render(request, 'noteapp/edit_note.html', {'form': form})



@login_required
def delete_note(request, id):
    Note=get_object_or_404(note, id=id)
    Note.delete()
    return redirect('note_list')   


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log the user in after signing up
            return redirect('note_list')  # redirect to home page or notes list
    else:
        form = SignUpForm()
    return render(request, 'noteapp/signup.html', {'form': form})





