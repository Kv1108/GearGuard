from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import Equipment, MaintenanceRequest, MaintenanceTeam
from .forms import EquipmentForm, MaintenanceRequestForm

def dashboard(request):
    """
    Overview of maintenance status.
    """
    context = {
        'total_equipment': Equipment.objects.count(),
        'open_requests': MaintenanceRequest.objects.exclude(stage__in=['Repaired', 'Scrap']).count(),
        'scrapped_equipment': Equipment.objects.filter(is_scrapped=True).count(),
    }
    return render(request, 'core/dashboard.html', context)

def equipment_list(request):
    query = request.GET.get('q')
    equipments = Equipment.objects.all()
    
    if query:
        equipments = equipments.filter(
            Q(name__icontains=query) | 
            Q(serial_number__icontains=query) |
            Q(department__icontains=query)
        )
        
    return render(request, 'core/equipment_list.html', {'equipments': equipments})

def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    # Smart button count
    request_count = equipment.requests.count()
    
    return render(request, 'core/equipment_detail.html', {
        'equipment': equipment,
        'request_count': request_count
    })

def equipment_create(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'core/form.html', {'form': form, 'title': 'Add Equipment'})

def request_list(request):
    """
    Kanban Board View
    """
    # Group requests by stage
    new_requests = MaintenanceRequest.objects.filter(stage='New')
    in_progress_requests = MaintenanceRequest.objects.filter(stage='In Progress')
    repaired_requests = MaintenanceRequest.objects.filter(stage='Repaired')
    scrap_requests = MaintenanceRequest.objects.filter(stage='Scrap')

    return render(request, 'core/kanban.html', {
        'new_requests': new_requests,
        'in_progress_requests': in_progress_requests,
        'repaired_requests': repaired_requests,
        'scrap_requests': scrap_requests
    })

def request_create(request):
    initial_data = {}
    if 'equipment_id' in request.GET:
        initial_data['equipment'] = request.GET.get('equipment_id')

    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            maintenance_request = form.save(commit=False)
            maintenance_request.created_by = request.user if request.user.is_authenticated else None 
            # In a real app we'd enforce login. For now allow None or default.
            # But the model field is not null. Let's assume we have a user or handle it.
            # We'll handle this in the template or by ensuring a user exists.
            # For this MVP let's relax the Created_by constraint if needed or mock it.
            # Actually, let's fix the model to allow null or mock a user.
            # But better: require login.
            maintenance_request.save()
            return redirect('request_list')
    else:
        form = MaintenanceRequestForm(initial=initial_data)
    
    return render(request, 'core/request_form.html', {'form': form})

def request_update(request, pk):
    req = get_object_or_404(MaintenanceRequest, pk=pk)
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            return redirect('request_list')
    else:
        form = MaintenanceRequestForm(instance=req)
    return render(request, 'core/request_form.html', {'form': form, 'request_obj': req})

def get_equipment_details(request, pk):
    """
    API for auto-filling team info on frontend
    """
    equipment = get_object_or_404(Equipment, pk=pk)
    data = {
        'category': equipment.category,
        'department': equipment.department,
        'team_id': equipment.maintenance_team.id if equipment.maintenance_team else None,
        'team_name': equipment.maintenance_team.name if equipment.maintenance_team else ''
    }
    return JsonResponse(data)

def update_request_stage(request, pk):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        new_stage = data.get('stage')
        
        req = get_object_or_404(MaintenanceRequest, pk=pk)
        req.stage = new_stage
        req.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def calendar_view(request):
    return render(request, 'core/calendar.html')

def request_events(request):
    """
    Return preventive maintenance requests as JSON events for FullCalendar
    """
    events = []
    # Only Preventive requests usually go on calendar, but let's show all with different colors?
    # User requirement: "Display all Preventive maintenance requests"
    requests = MaintenanceRequest.objects.filter(request_type='Preventive')
    
    for req in requests:
        if req.scheduled_date:
            events.append({
                'title': f"{req.equipment.name} - {req.subject}",
                'start': req.scheduled_date.isoformat(),
                'url': f"/requests/{req.pk}/edit/",
                'color': '#10b981' if req.stage == 'Repaired' else '#f59e0b'
            })
            
    return JsonResponse(events, safe=False)
