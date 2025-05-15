from django.shortcuts import render, redirect, get_object_or_404
from .models import note
from .forms import NoteForm
from django.db.models.functions import TruncDate


def note_list(request):
    # Grouping notes by date and ordering by date
    notes = note.objects.annotate(date_only=TruncDate('created_at'))
    
    # Create a dictionary to store grouped notes by date
    grouped_notes = {}
    for notee in notes:
        if notee.date_only not in grouped_notes:
            grouped_notes[notee.date_only] = []  # Create an empty list if this date is not yet in the dictionary
        grouped_notes[notee.date_only].append(notee)  # Append the note to the list for the specific date
    grouped_notes = dict(sorted(grouped_notes.items(), reverse=True))
    return render(request, 'noteapp/note_list.html', {'grouped_notes': grouped_notes})



def add_note(request):
    if request.method=='POST':
        form=NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form=NoteForm()
    return render(request,'noteapp/add_note.html',{'form':form})




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




def delete_note(request, id):
    Note=get_object_or_404(note, id=id)
    Note.delete()
    return redirect('note_list')   