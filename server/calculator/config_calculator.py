import re


class ExpressionCalculation:
    def __init__(self):
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '(': 0}  # Определение приоритетов операторов

    def split_expression(self, expression):
        expression = expression.replace(' ', '')
        # С помощью регулярного выражения разбиваем строку по операторам, учитывая отрицательные числа и неявное умножение
        tokens = re.findall(r'\d+\.\d+|\d+|[\+\-\*\/\^\(\)]', expression)
        new_tokens = []
        i = 0
        while i < len(tokens):
            if tokens[i] == '-' and (i == 0 or tokens[i - 1] in '(-+'):
                # Если минус обозначает отрицательное число
                new_tokens.append(tokens[i] + tokens[i + 1])
                i += 2
            elif tokens[i].isdigit() and i + 1 < len(tokens) and tokens[i + 1] == '(':
                # Неявное умножение: число перед открывающей скобкой
                new_tokens.append(tokens[i])
                new_tokens.append('*')
                i += 1
            elif tokens[i] == ')' and i + 1 < len(tokens) and tokens[i + 1].isdigit():
                # Неявное умножение: закрывающая скобка перед числом
                new_tokens.append(tokens[i])
                new_tokens.append('*')
                i += 1
            else:
                new_tokens.append(tokens[i])
                i += 1

        # Проверка на недопустимые символы
        for token in new_tokens:
            if token not in self.precedence and not token.replace('.', '', 1).lstrip('-').isdigit():
                raise ValueError('Некорректное выражение: недопустимые символы')

        return new_tokens

    def validate_expression(self, tokens):
        stack = []
        for token in tokens:
            if token == '(':
                stack.append(token)
            elif token == ')':
                if not stack or stack[-1] != '(':
                    raise ValueError('Некорректное выражение: несогласованные скобки')
                stack.pop()
        if stack:
            raise ValueError('Некорректное выражение: несогласованные скобки')

    def conversion_tokens(self, tokens):
        numbers = []
        operators = []

        i = 0
        while i < len(tokens):
            if tokens[i].replace('.', '', 1).lstrip(
                    '-').isdigit():  # Если текущий токен — число, добавляем его в стек чисел
                numbers.append(float(tokens[i]))
            elif tokens[i] == '(':  # Если текущий токен — открывающая скобка, добавляем её в стек операторов
                operators.append(tokens[i])
            elif tokens[
                i] == ')':  # Если текущий токен — закрывающая скобка, выполняем все операции до открывающей скобки
                while operators and operators[-1] != '(':
                    self.apply_top_operator(numbers, operators)
                operators.pop()
            elif tokens[i] in self.precedence:
                # Если текущий токен — оператор, выполняем операции с более высоким или равным приоритетом
                while operators and self.precedence[operators[-1]] >= self.precedence[tokens[i]]:
                    self.apply_top_operator(numbers, operators)
                operators.append(tokens[i])

            i += 1

        while operators:
            self.apply_top_operator(numbers, operators)

        return numbers[0]

    def apply_top_operator(self, numbers, operators):  # Выполняем операции
        if len(numbers) < 2:
            raise ValueError('Некорректное выражение: недостаточно операндов для операции')
        b = numbers.pop()
        a = numbers.pop()
        op = operators.pop()
        numbers.append(self._apply_operator(a, b, op))

    def _apply_operator(self, a, b, op):  # Операции
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0:
                raise ValueError('Делить на ноль нельзя')
            return a / b
        elif op == '^':
            return a ** b

    def evaluate(self, expression):
        try:
            expression = expression.replace(',', '.')  # если была введена ',' вместо точки
            tokens = self.split_expression(expression)
            self.validate_expression(tokens)
            result = self.conversion_tokens(tokens)
            return round(result, 10)  # Использование функции round позволяет выводить числа с плавающей точкой
        except Exception as e:
            return None