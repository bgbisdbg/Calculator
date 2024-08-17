from django.shortcuts import render, redirect


def index(request):
    history = request.session.get('history', [])
    return render(request, 'calculator/index.html', {'history': history})


def calculate(request):
    if request.method == 'POST':
        expression = request.POST.get('expression')
        try:
            result = eval(expression)
            request.session['history'] = request.session.get('history', []) + [(expression, result)]
            return redirect('index')
        except Exception as e:
            history = request.session.get('history', [])
            return render(request, 'calculator/index.html', {'error': str(e), 'history': history})
    return redirect('index')


