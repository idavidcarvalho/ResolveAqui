from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Ticket
from .forms import TicketForm


@login_required
def create_ticket(request):
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
    qs = Ticket.objects.filter(created_by=request.user)
    return render(request, 'chamados/list.html', {'tickets': qs})


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, created_by=request.user)
    return render(request, 'chamados/detail.html', {'ticket': ticket})
