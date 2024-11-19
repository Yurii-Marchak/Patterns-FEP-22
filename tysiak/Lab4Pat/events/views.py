# events/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import FootballEvent
from .forms import FootballEventForm
from .services import FootballEventFacade

def fetch_and_save_events(request):
    facade = FootballEventFacade()  # Використання фасаду
    facade.fetch_and_save_events()  # Отримання і збереження подій
    return redirect('event_info')  # Повернення на сторінку з усіма подіями

def event_info(request, event_id=None):
    events = FootballEvent.objects.all()
    facade = FootballEventFacade()  # Для можливих оновлень із API

    if event_id:  # Якщо передано ID, обробляємо редагування
        event = get_object_or_404(FootballEvent, id=event_id)
        form = FootballEventForm(request.POST or None, instance=event)
    else:  # Інакше - створення нової події
        form = FootballEventForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()  # Зберігаємо нову або редаговану подію
        return redirect('event_info')

    if 'delete_event_id' in request.GET:  # Видалення події за переданим ID
        delete_event_id = request.GET['delete_event_id']
        delete_event = get_object_or_404(FootballEvent, id=delete_event_id)
        delete_event.delete()
        return redirect('event_info')

    return render(request, 'events/info.html', {  # Зміна на 'info.html'
        'events': events,
        'form': form,
        'edit_event_id': event_id
    })
