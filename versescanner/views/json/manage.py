from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden

from versescanner.util.filemanager import sync_files, sync_db
from versescanner.models import Author, Genre, Opus, Period


def sync_files(request):
    if request.user.is_superuser:
        sync_files()
        return HttpResponse(status=204)
    return HttpResponseForbidden()


def sync_db(request):
    if request.user.is_superuser:
        sync_db()
        return HttpResponse(status=204)
    return HttpResponseForbidden()


def get_member_list(request):
    if request.user.is_superuser:
        objects = User.objects.all()
        for d in objects:
            d.password = ''
        data = serializers.serialize('json', objects)
        return HttpResponse(data, content_type='application/json')
    return HttpResponseForbidden()


def post_meta(request):
    if not (request.user.is_superuser and request.method == 'POST'):
        return HttpResponseForbidden()
    dct = request.POST.dict()
    if 'period' in dct:
        dct['period'] = Period.objects.get(id=dct['period'])
        model = Author(**dct)
    else:
        dct['author'] = Author.objects.get(id=dct['author'])
        dct['genre'] = Genre.objects.get(id=dct['genre'])
        model = Opus(**dct)
    model.save()
    return HttpResponse(status=200)
