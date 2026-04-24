from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from django.utils import timezone

def index(request):
    """Главная страница - показываем список заметок"""
    notes = Note.objects.all().order_by('-created_date')  # новые сверху
    return render(request, 'notes/index.html', {'notes': notes})

def add_note(request):
    """Добавление новой заметки"""
    if request.method == 'POST':
        # пользователь отправил форму
        title = request.POST.get('title')
        text = request.POST.get('text')
        if title and text:
            Note.objects.create(title=title, text=text)
        return redirect('index')
    
    # GET запрос - показываем пустую форму
    return render(request, 'notes/edit.html', {'action': 'add'})

def edit_note(request, note_id):
    """Редактирование заметки"""
    note = get_object_or_404(Note, id=note_id)
    
    if request.method == 'POST':
        # сохраняем изменения
        note.title = request.POST.get('title')
        note.text = request.POST.get('text')
        note.save()
        return redirect('index')
    
    # показываем форму с текущими данными
    return render(request, 'notes/edit.html', {'note': note, 'action': 'edit'})

def delete_note(request, note_id):
    """Удаление заметки"""
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return redirect('index')

def toggle_done(request, note_id):
    """Отметить как выполнено/не выполнено"""
    note = get_object_or_404(Note, id=note_id)
    note.is_done = not note.is_done
    note.save()
    return redirect('index')