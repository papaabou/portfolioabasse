from django.shortcuts import render, get_object_or_404
from .models import Client
from django.core.paginator import Paginator

def client_list(request):
    qs = Client.objects.all().order_by("created")
    total_clients_count = qs.count()

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    clients = paginator.get_page(page_number)

    return render(
        request,
        "client/client_list.html",
        {
            "clients": clients,
            "total_clients_count": total_clients_count,
        },
    )

def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    return render(
        request,
        "client/client_detail.html",
        {
            "client": client,
        },
    )