import re


class ExpressionCalculation:
    def __init__(self):
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '(': 0} # Определение приоритетов операторов

    def split_expression(self, expression): # Функция для разделения строки
        expression = expression.replace(' ', '')
        # С помощью регулярного выражения разбиваем строку по операторам.
        tokens = re.findall(r'\d+|\+|\-|\*|\/|\(|\)', expression)
        new_tokens = []
        for i in range(len(tokens)): # Цикл для определения неявного умножения
            if tokens[i] == '(' and i > 0 and (tokens[i - 1].isdigit() or tokens[i - 1] == ')'):
                new_tokens.append('*')
            new_tokens.append(tokens[i])
        return new_tokens

    def conversion_tokens(self, tokens):
        numbers = []
        operators = []

        i = 0
        while i < len(tokens):
            if tokens[i].isdigit(): # Если текущий токен — число, добавляем его в стек чисел
                numbers.append(int(tokens[i]))
            elif tokens[i] == '(': # Если текущий токен — открывающая скобка, добавляем её в стек операторов
                operators.append(tokens[i])
            elif tokens[i] == ')': # Если текущий токен — закрывающая скобка, выполняем все операции до открывающей скобки
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

    def apply_top_operator(self, numbers, operators): #Выполняем операции
        b = numbers.pop()
        a = numbers.pop()
        op = operators.pop()
        numbers.append(self._apply_operator(a, b, op))

    def _apply_operator(self, a, b, op): # Операции
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0:
                raise ValueError("Делить на ноль нельзя")
            return a // b

    def evaluate(self, expression):
        try:
            tokens = self.split_expression(expression)
            result = self.conversion_tokens(tokens)
            return result
        except Exception as e:
            return str(e)
