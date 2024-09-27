from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *



def flower_render(request, title, flower_name, image, description, price):
    return render(request, 'flower_flower/flower.html', {"title": title, "flower_name": flower_name, "image": image, "description": description, "price": price})
def flower(request):
    result = request.path.replace('/flowers/', '').replace('/', '')
    flower = Flower.objects.get(pk=result)
    return render(request, 'flower_flower/flower.html', {"flower": flower})
def index(request):
    flowers = Flower.objects.all
    return render(request, 'flower_flower/index.html', {"flowers": flowers})
def buying(request):
    work_time = [["9"], "19:30"]
    id = int(request.path.replace('/buying/', '').replace('/', ''))
    flower = Flower.objects.get(pk=id)
    error = ''
    if request.method == 'POST':
        try:
            if datetime.now().strftime("%H") in work_time[0]:
                if datetime.now().strftime("%M") in work_time[1]:
                    pass
                else:
                    raise Exception
            else:
                raise Exception
            user = User.objects.get(email=request.POST.get('email'))
            Order.objects.create(flower=flower, user=user)
            return redirect('/')
        except Exception:
            error = 'При покупке произошла ошибка: возможно вы заказываете в нерабочее время или вы ввели некорректные данные.'
            flowers = Flower.objects.all
            return render(request, 'flower_flower/index.html', {"flowers": flowers, "error": error})

    return render(request, 'flower_flower/buying.html', {"flower": flower})