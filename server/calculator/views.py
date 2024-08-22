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
        try:
            result = calculation.evaluate(expression)
            history = request.session.get('history', [])
            history.append((expression, result))
            request.session['history'] = history
            request.session['result'] = result
            return redirect('index')
        except Exception as e:
            history = request.session.get('history', [])
            return render(request, 'calculator/index.html', {'error': str(e), 'history': history})
    return redirect('index')


