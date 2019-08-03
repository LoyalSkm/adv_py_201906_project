from django.conf import settings
from django.conf.urls import url
from django.core.cache import cache
from django.shortcuts import render

import pprint
import json_schema


if not settings.configured:
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['']
        }]
    )


def rought_founder(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        context = {}
        FROM_R = request.POST.get('L1')
        TO_R = request.POST.get('L2')
        if ((FROM_R and TO_R) == '') or ((FROM_R or TO_R) == ''):
            context['message'] = 'Оба поля должны быть заполненны'
            return render(request, 'index.html', context)
        if FROM_R == TO_R:
            context['message'] = 'Нет маршрута в один и тот-же город'
            return render(request, 'index.html', context)

        Tru_list = [(FROM_R in json_schema.pap()), (TO_R in json_schema.pap())] #вроверка валидности введённых iata
        if Tru_list == [False, True]:
            context['message'] = f'Возможно вы указали не верный "iata" код города ОТПРАВЛЕНИЯ: {FROM_R}'
            return render(request, 'index.html', context)
        elif Tru_list == [True, False]:
            context['message'] = f'Возможно вы указали не верный "iata" код города ПРИБЫТИЯ: {TO_R}'
            return render(request, 'index.html', context)
        elif Tru_list == [True, True]:
            em_li = []
            em_li_2 = []
            if json_schema.direct_flight(FROM_R, TO_R):
                em_li_2.append(f"Прямой рейс {json_schema.direct_flight(FROM_R, TO_R)} с {FROM_R}: {json_schema.iata_translater(FROM_R)} "
                               f"--> {TO_R}: {json_schema.iata_translater(TO_R)}")
            else:
                em_li_2 = f"Прямого рейса нету"
            for i in range(2):
                em_li.append(json_schema.transfer_flight(FROM_R, TO_R))
            for i in em_li:
                em_li_2.append(f"Рейс с пересадкой {i[0]} с {FROM_R}: {json_schema.iata_translater(FROM_R)} "
                               f"-->{i[1]}: {json_schema.iata_translater(i[1])} "
                               f"--> {TO_R}: {json_schema.iata_translater(TO_R)}")
            result = em_li_2
            cache.add(result, url)
            context['url'] = result
            return render(request, 'index.html', context)
        else:
            context['message'] = f'оба IATA кода не верны'
            return render(request, 'index.html', context)





urlpatterns = [
    url(r'^$', rought_founder)
]


if __name__ == '__main__':
    import sys
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
