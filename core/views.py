from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import Equipment, MaintenanceRequest, MaintenanceTeam, Technician, WorkCenter, MaintenanceLog, EquipmentCategory
from .forms import EquipmentForm, MaintenanceRequestForm, WorkCenterForm, MaintenanceLogForm

from django import forms

from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """
    Overview of maintenance status.
    """
    # Critical Equipment (Health < 30%)
    critical_equipment = Equipment.objects.filter(health__lt=30).count()
    
    # Open Requests (Pending vs Overdue)
    open_requests_qs = MaintenanceRequest.objects.exclude(stage__in=['Repaired', 'Scrap'])
    total_open = open_requests_qs.count()
    
    now = timezone.now()
    # Note: scheduled_date is DateTimeField now
    overdue_requests = open_requests_qs.filter(scheduled_date__lt=now).count()
    pending_requests = total_open - overdue_requests
    
    total_techs = Technician.objects.count()
    if total_techs > 0:
        utilization = int((total_open / (total_techs * 5)) * 100)
    else:
        utilization = 0
    
    recent_activity = MaintenanceRequest.objects.select_related('equipment', 'work_center', 'assigned_to', 'created_by').order_by('-updated_at')[:5]

    context = {
        'critical_count': critical_equipment,
        'open_count': total_open,
        'pending_count': pending_requests,
        'overdue_count': overdue_requests,
        'tech_utilization': utilization,
        'recent_activity': recent_activity,
    }
    return render(request, 'core/dashboard.html', context)

# --- Equipment Views ---

@login_required
def equipment_list(request):
    query = request.GET.get('q')
    equipments = Equipment.objects.select_related('category', 'work_center', 'maintenance_team').all()
    
    if query:
        equipments = equipments.filter(
            Q(name__icontains=query) | 
            Q(serial_number__icontains=query) |
            Q(department__icontains=query)
        )
        
    return render(request, 'core/equipment_list.html', {'equipments': equipments})

@login_required
def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    request_count = equipment.requests.count()
    return render(request, 'core/equipment_detail.html', {
        'equipment': equipment,
        'request_count': request_count
    })

@login_required
def equipment_create(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'core/form.html', {'form': form, 'title': 'Add Equipment'})

# --- Work Center Views ---

@login_required
def work_center_list(request):
    work_centers = WorkCenter.objects.all()
    return render(request, 'core/work_center_list.html', {'work_centers': work_centers})

@login_required
def work_center_create(request):
    if request.method == 'POST':
        form = WorkCenterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('work_center_list')
    else:
        form = WorkCenterForm()
    return render(request, 'core/form.html', {'form': form, 'title': 'Add Work Center'})

# --- Category Views ---

@login_required
def category_list(request):
    categories = EquipmentCategory.objects.annotate(count=Count('equipment'))
    return render(request, 'core/category_list.html', {'categories': categories})

class CategoryForm(forms.ModelForm):
    class Meta:
        model = EquipmentCategory
        fields = '__all__'

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'core/form.html', {'form': form, 'title': 'Add Category'})

# --- Request Views ---

@login_required
def request_list(request):
    # Kanban Board View
    # Filtering: Can filter by equipment if passed in GET
    equipment_name = request.GET.get('q')
    
    qs = MaintenanceRequest.objects.all().select_related('equipment', 'work_center', 'assigned_to')
    if equipment_name:
        qs = qs.filter(equipment__name__icontains=equipment_name)

    stages = []
    # (Stage Name, QuerySet, ID for Sortable)
    for stage_code, stage_label in MaintenanceRequest.STAGE_CHOICES:
        stages.append((stage_label, qs.filter(stage=stage_code), stage_code))

    return render(request, 'core/kanban.html', {
        'stages': stages
    })

@login_required
def request_create(request):
    initial_data = {}
    if 'equipment_id' in request.GET:
        initial_data['equipment'] = request.GET.get('equipment_id')
    
    # Pre-fill date from calendar click
    if 'date' in request.GET:
        initial_data['scheduled_date'] = request.GET.get('date')

    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            maintenance_request = form.save(commit=False)
            maintenance_request.created_by = request.user
            maintenance_request.save()
            return redirect('request_list')
    else:
        form = MaintenanceRequestForm(initial=initial_data)
    
    # Pass work centers for dynamic JS if needed, though form handles choices
    return render(request, 'core/request_form.html', {'form': form})

@login_required
def request_update(request, pk):
    req = get_object_or_404(MaintenanceRequest, pk=pk)
    
    # Handle Log submission
    if request.method == 'POST' and 'submit_log' in request.POST:
        log_form = MaintenanceLogForm(request.POST)
        if log_form.is_valid():
            log = log_form.save(commit=False)
            log.request = req
            log.created_by = request.user
            log.save()
            return redirect('request_update', pk=pk)
    
    # Handle Request Update
    if request.method == 'POST' and 'submit_request' in request.POST:
        form = MaintenanceRequestForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            return redirect('request_list')
    
    else:
        form = MaintenanceRequestForm(instance=req)
        log_form = MaintenanceLogForm()

    logs = req.logs.select_related('created_by').order_by('-created_at')

    return render(request, 'core/request_form.html', {
        'form': form, 
        'request_obj': req,
        'log_form': log_form,
        'logs': logs
    })

@login_required
def get_equipment_details(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    data = {
        'category': equipment.category.name if equipment.category else '',
        'department': equipment.department,
        'team_id': equipment.maintenance_team.id if equipment.maintenance_team else None,
        'team_name': equipment.maintenance_team.name if equipment.maintenance_team else '',
        'work_center_id': equipment.work_center.id if equipment.work_center else None
    }
    return JsonResponse(data)

def update_request_stage(request, pk):
    # API View
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        new_stage = data.get('stage')
        req = get_object_or_404(MaintenanceRequest, pk=pk)
        req.stage = new_stage
        req.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def calendar_view(request):
    return render(request, 'core/calendar.html')

def request_events(request):
    events = []
    # V2: Use scheduled_date (DateTimeField)
    requests = MaintenanceRequest.objects.filter(scheduled_date__isnull=False)
    
    for req in requests:
        events.append({
            'title': f"{req.subject}",
            'start': req.scheduled_date.isoformat(),
            'url': f"/requests/{req.pk}/edit/",
            'color': '#ef4444' if req.priority == 'Critical' else ('#10b981' if req.stage == 'Repaired' else '#f59e0b')
        })
            
    return JsonResponse(events, safe=False)
