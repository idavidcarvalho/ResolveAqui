from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.contrib.auth import get_user_model

from .models import Ticket, Area, Problem
from .forms import TicketForm

User = get_user_model()


@login_required
def create_ticket(request):
    # Gestores não podem criar tickets
    if request.user.typeUser == 'Gestor':
        messages.error(request, 'Gestores não podem criar chamados.')
        return redirect('tickets:all_tickets')

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, 'Chamado criado com sucesso.')
            return redirect('tickets:my_tickets')
    else:
        form = TicketForm()
    return render(request, 'chamados/create.html', {'form': form})


@login_required
def my_tickets(request):
    # Gestores são redirecionados para página de gerenciamento
    if request.user.typeUser == 'Gestor':
        return redirect('tickets:all_tickets')

    qs = Ticket.objects.filter(created_by=request.user)
    return render(request, 'chamados/list.html', {'tickets': qs})


@login_required
def ticket_detail(request, pk):
    # Gestores podem ver qualquer ticket, usuários comuns apenas os seus
    if request.user.typeUser == 'Gestor':
        ticket = get_object_or_404(Ticket, pk=pk)
    else:
        ticket = get_object_or_404(Ticket, pk=pk, created_by=request.user)

    # Importar aqui para evitar import circular
    from comments.models import Comment
    from comments.forms import CommentForm

    # Buscar comentários do ticket
    comments = ticket.comments.select_related('author').all()

    # Processar formulário de comentário
    comment_form = None
    can_comment = ticket.status == 'Em andamento'

    if can_comment:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST, request.FILES)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.ticket = ticket
                comment.author = request.user
                comment.save()
                messages.success(request, 'Comentário adicionado com sucesso.')
                return redirect('tickets:detail', pk=ticket.pk)
        else:
            comment_form = CommentForm()

    context = {
        'ticket': ticket,
        'comments': comments,
        'comment_form': comment_form,
        'can_comment': can_comment,
    }
    return render(request, 'chamados/detail.html', context)


# ======================
# VIEWS PARA GESTORES
# ======================

@login_required
def all_tickets(request):
    """View para gestores verem todos os chamados do sistema"""
    # Apenas gestores podem acessar
    if request.user.typeUser != 'Gestor':
        messages.error(request, 'Acesso negado. Apenas gestores podem acessar esta página.')
        return redirect('tickets:my_tickets')

    # Buscar todos os tickets com relacionamentos
    qs = Ticket.objects.select_related('problem', 'problem__area', 'created_by').all()

    # Filtros
    status_filter = request.GET.get('status')
    area_filter = request.GET.get('area')
    problem_filter = request.GET.get('problem')
    user_filter = request.GET.get('user')
    search = request.GET.get('q')

    if status_filter:
        qs = qs.filter(status=status_filter)
    if area_filter:
        qs = qs.filter(problem__area_id=area_filter)
    if problem_filter:
        qs = qs.filter(problem_id=problem_filter)
    if user_filter:
        qs = qs.filter(created_by_id=user_filter)
    if search:
        qs = qs.filter(
            Q(description__icontains=search) |
            Q(address__icontains=search) |
            Q(district__icontains=search)
        )

    # Dados para filtros
    areas = Area.objects.all()
    problems = Problem.objects.select_related('area').all()
    users = User.objects.filter(tickets__isnull=False).distinct()

    context = {
        'tickets': qs,
        'areas': areas,
        'problems': problems,
        'users': users,
        'status_choices': Ticket.STATUS_CHOICES,
        'current_filters': {
            'status': status_filter,
            'area': area_filter,
            'problem': problem_filter,
            'user': user_filter,
            'search': search,
        }
    }
    return render(request, 'chamados/all_tickets.html', context)


@login_required
def update_ticket_status(request, pk):
    """View para gestor alterar status do ticket via AJAX"""
    if request.method != 'POST' or request.user.typeUser != 'Gestor':
        return JsonResponse({'success': False, 'error': 'Acesso negado'}, status=403)

    ticket = get_object_or_404(Ticket, pk=pk)
    new_status = request.POST.get('status')

    if new_status not in dict(Ticket.STATUS_CHOICES):
        return JsonResponse({'success': False, 'error': 'Status inválido'}, status=400)

    ticket.status = new_status
    ticket.save()

    return JsonResponse({
        'success': True,
        'status': new_status,
        'updated_at': ticket.updated_at.strftime('%d/%m/%Y %H:%M')
    })


@login_required
def dashboard(request):
    """Dashboard com estatísticas e gráficos para gestores"""
    if request.user.typeUser != 'Gestor':
        messages.error(request, 'Acesso negado. Apenas gestores podem acessar esta página.')
        return redirect('tickets:my_tickets')

    # Estatísticas gerais
    total_tickets = Ticket.objects.count()
    tickets_abertos = Ticket.objects.filter(status='Aberto').count()
    tickets_em_andamento = Ticket.objects.filter(status='Em andamento').count()
    tickets_finalizados = Ticket.objects.filter(status='Finalizado').count()

    # Problemas mais recorrentes
    top_problems = Problem.objects.annotate(
        total=Count('ticket')
    ).order_by('-total')[:10]

    # Tickets por área
    tickets_por_area = Area.objects.annotate(
        total=Count('problems__ticket')
    ).order_by('-total')

    # Tickets por distrito
    from django.db.models import Value, CharField
    from django.db.models.functions import Coalesce
    tickets_por_distrito = Ticket.objects.values('district').annotate(
        total=Count('id')
    ).order_by('-total')

    # Timeline de tickets (últimos 12 meses)
    from datetime import datetime, timedelta
    from django.db.models.functions import TruncMonth

    twelve_months_ago = datetime.now() - timedelta(days=365)
    tickets_timeline = Ticket.objects.filter(
        created_at__gte=twelve_months_ago
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total=Count('id')
    ).order_by('month')

    context = {
        'total_tickets': total_tickets,
        'tickets_abertos': tickets_abertos,
        'tickets_em_andamento': tickets_em_andamento,
        'tickets_finalizados': tickets_finalizados,
        'top_problems': top_problems,
        'tickets_por_area': tickets_por_area,
        'tickets_por_distrito': tickets_por_distrito,
        'tickets_timeline': tickets_timeline,
    }
    return render(request, 'chamados/dashboard.html', context)
