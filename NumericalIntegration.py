import math
from audioop import error

import matplotlib.pyplot as plt
import numpy as np
from fontTools.misc.bezierTools import epsilon


# Определение функций для интегрирования
def func1(x): return x**2
def func2(x): return math.sin(x)
def func3(x): return math.exp(x)
def func4(x): return 1 / x if x != 0 else float('inf')  # Несобственный интеграл
def func5(x): return math.log(x) if x > 0 else float('inf')  # Несобственный интеграл

# Словарь функций с текстовым представлением
functions = {
    1: ("x^2", func1),
    2: ("sin(x)", func2),
    3: ("exp(x)", func3),
    4: ("1/x", func4),
    5: ("ln(x)", func5)
}

# Классы методов интегрирования
class NumericalIntegration:
    @staticmethod
    def rectangle_left(func, a, b, n):
        h = (b - a) / n
        return sum(func(a + i * h) for i in range(n)) * h

    @staticmethod
    def rectangle_right(func, a, b, n):
        h = (b - a) / n
        return sum(func(a + (i + 1) * h) for i in range(n)) * h

    @staticmethod
    def rectangle_middle(func, a, b, n):
        h = (b - a) / n
        return sum(func(a + (i + 0.5) * h) for i in range(n)) * h

    @staticmethod
    def trapezoid(func, a, b, n):
        h = (b - a) / n

        sum = (func(a) + func(b)) / 2
        for i in range(1, n):
            sum += func(a + i * h)

        if n == 4  or n == n:
            print(n, sum * h)

        return sum * h

    @staticmethod
    def simpson(func, a, b, n):
        if n % 2 == 1:
            n += 1  # Симпсон работает только для четного n
        h = (b - a) / n
        result = func(a) + func(b) + 4 * sum(func(a + i * h) for i in range(1, n, 2)) + 2 * sum(func(a + i * h) for i in range(2, n, 2))
        return result * h / 3

# Правило Рунге для оценки точности
def runge_rule(integral_n, integral_2n, p):
    return abs(integral_2n - integral_n) / (2**p - 1)

# Функция вычисления интеграла с заданной точностью
def calculate_integral(func, a, b, epsilon, method, p):
    n = 4  # Начальное количество разбиений
    integral_n = method(func, a, b, n)
    while True:
        n *= 2
        integral_2n = method(func, a, b, n)
        error = runge_rule(integral_n, integral_2n, p)
        if error < epsilon:
            return integral_2n, n
        integral_n = integral_2n

# Функция для отображения графика
def plot_function(func, a=-10, b=10, points=1000):
    x = np.linspace(a, b, points)
    y = np.array([func(val) if np.isfinite(func(val)) else float('nan') for val in x])  # Обработка разрывов
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, label=f"{func.__name__}(x)")
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.title(f"График функции {func.__name__}(x)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()


# Основной код программы
def main():
    # Меню выбора функции
    print("Выберите функцию для интегрирования:")
    for i, (desc, _) in functions.items():
        print(f"{i}. {desc}")

    func_choice = int(input("Введите номер функции: "))
    if func_choice not in functions:
        print("Некорректный выбор функции.")
        return

    func_desc, func = functions[func_choice]

    # Отображение графика выбранной функции
    print(f"Вы выбрали функцию: {func_desc}. Сейчас будет показан её график. Закройте график, чтобы продолжить.")
    plot_function(func)

    # Ввод данных
    a = float(input("Введите нижний предел интегрирования: "))
    b = float(input("Введите верхний предел интегрирования: "))
    epsilon = float(input("Введите точность вычисления: "))

    # Выбор метода
    methods = {
        1: NumericalIntegration.rectangle_left,
        2: NumericalIntegration.rectangle_right,
        3: NumericalIntegration.rectangle_middle,
        4: NumericalIntegration.trapezoid,
        5: NumericalIntegration.simpson
    }
    print("Выберите метод численного интегрирования:")
    print("1. Метод прямоугольников (левый)")
    print("2. Метод прямоугольников (правый)")
    print("3. Метод прямоугольников (средний)")
    print("4. Метод трапеций")
    print("5. Метод Симпсона")
    method_choice = int(input("Введите номер метода: "))
    method = methods.get(method_choice)
    if not method:
        print("Некорректный выбор метода.")
        return

    p = 2 if method_choice != 5 else 4  # Степень точности метода (p = 2 для трапеций и прямоугольников, 4 для Симпсона)

    # Проверка на разрывы в функции
    if func in [func4, func5] and (a <= 0 or b <= 0):
        print("Интеграл не существует из-за разрыва на границе.")
        return

    # Вычисление интеграла
    try:
        result, intervals = calculate_integral(func, a, b, epsilon, method, p)
        print(f"Значение интеграла: {result}")
        print(f"Число разбиений интервала: {intervals}")
    except OverflowError:
        print("Интеграл не существует — расходящийся интеграл.")


if __name__ == "__main__":
    main()