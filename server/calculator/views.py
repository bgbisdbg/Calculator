import re

from django.shortcuts import render, redirect
from calculator.config_calculator import ExpressionCalculation

calculation = ExpressionCalculation()


def index(request):
    history = request.session.get('history', [])
    result = request.session.get('result', None)
    return render(request, 'calculator/index.html', {'history': history, 'result': result})


def calculate(request):
    if request.method == 'POST':
        expression = request.POST.get('expression')

        # Проверка на наличие букв (латинских и русских) в выражении
        if re.search(r'[a-zA-Zа-яА-Я]', expression):
            error = "Укажите корректное выражение"
            history = request.session.get('history', [])
            return render(request, 'calculator/index.html', {'error': error, 'history': history})

        try:
            result = calculation.evaluate(expression)
            history = request.session.get('history', [])
            history.append((expression, result))
            request.session['history'] = history
            request.session['result'] = result
            return redirect('index')
        except ValueError as e:
            error = str(e)
            history = request.session.get('history', [])
            return render(request, 'calculator/index.html', {'error': error, 'history': history})
        except Exception as e:
            error = "Укажите корректное выражение"
            history = request.session.get('history', [])
            return render(request, 'calculator/index.html', {'error': error, 'history': history})

    return redirect('index')

def clear_history(request):
    if request.method == 'POST':
        request.session['history'] = []
        request.session['result'] = None
    return redirect('index')