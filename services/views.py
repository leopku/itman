# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.generic import list_detail
from itman.services.models import Server, Switch, Service

def server_list(request):
    response = list_detail.object_list(
        request,
        queryset = Server.objects.all(),
    )
    return response
    
def server_detail(request, server_id):
    fields = Server._meta.fields
    server = get_object_or_404(Server, pk=server_id)
    details = {}
    for field in fields:
        details[field.verbose_name] = server.__getattribute__(field.name)
    response = list_detail.object_detail(
        request,
        #queryset = get_object_or_404(Server, id__iexact=server_id),
        queryset = Server.objects.all(),
        object_id = server_id,
        extra_context = {'details': details,},
    )
    return response
