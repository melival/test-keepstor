from django.shortcuts import render
from . import models
import os


def home(request):
    table = models.StoreBase()

    data = {
        'page_title': 'Сводка новостей',
        'data': table
        }

    json_path = os.path.join(
        os.path.abspath('.'),
        'keeper',
        'static',
        'download',
        'store.json')

    print('json_path',json_path)
    table.dump_order_to_json(path=json_path)

    return render(request, 'keeper/table.html', data)
