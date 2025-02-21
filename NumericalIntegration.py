import math
import matplotlib.pyplot as plt
import numpy as np


# Определение функций для интегрирования
def func1(x): return x ** 2


def func2(x): return math.sin(x)


def func3(x): return math.exp(x)


def func4(x):
    if x == 0:
        raise ValueError("Функция 1/x не определена в x=0")
    return 1 / x


def func5(x):
    if x <= 0:
        raise ValueError("Функция ln(x) не определена для x <= 0")
    return math.log(x)


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
        try:
            result = (func(a) + func(b)) / 2 + sum(func(a + i * h) for i in range(1, n))
            return result * h
        except ValueError as e:
            print(f"Ошибка: {e}")
            return None

    @staticmethod
    def simpson(func, a, b, n):
        if n % 2 == 1:
            n += 1  # Симпсон работает только для четного n
        h = (b - a) / n
        try:
            result = (func(a) + func(b) +
                      4 * sum(func(a + i * h) for i in range(1, n, 2)) +
                      2 * sum(func(a + i * h) for i in range(2, n, 2)))
            return result * h / 3
        except ValueError as e:
            print(f"Ошибка: {e}")
            return None


# Правило Рунге для оценки точности
def runge_rule(integral_n, integral_2n, p):
    return abs(integral_2n - integral_n) / (2 ** p - 1)


# Функция вычисления интеграла с заданной точностью
def calculate_integral(func, a, b, epsilon, method, p):
    n = 4  # Начальное количество разбиений
    max_iterations = 1000
    integral_n = method(func, a, b, n)
    if integral_n is None:
        return None, n

    for _ in range(max_iterations):
        n *= 2
        integral_2n = method(func, a, b, n)
        if integral_2n is None:
            return None, n
        error = runge_rule(integral_n, integral_2n, p)
        if error < epsilon:
            return integral_2n, n
        integral_n = integral_2n

    print("Достигнуто максимальное количество итераций.")
    return integral_n, n


# Функция для отображения графика
def plot_function(func, a=-10, b=10, points=1000):
    x = np.linspace(a, b, points)
    y = []
    for val in x:
        try:
            y.append(func(val))
        except ValueError:
            y.append(float('nan'))
    y = np.array(y)

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
    print("Выберите функцию для интегрирования:")
    for i, (desc, _) in functions.items():
        print(f"{i}. {desc}")

    try:
        func_choice = int(input("Введите номер функции: "))
        if func_choice not in functions:
            raise ValueError
    except ValueError:
        print("Некорректный выбор функции.")
        return

    func_desc, func = functions[func_choice]
    print(f"Вы выбрали функцию: {func_desc}. Закройте график, чтобы продолжить.")
    plot_function(func)

    try:
        a = float(input("Введите нижний предел интегрирования: "))
        b = float(input("Введите верхний предел интегрирования: "))
        epsilon = float(input("Введите точность вычисления: "))
    except ValueError:
        print("Ошибка ввода данных.")
        return

    methods = {
        1: NumericalIntegration.rectangle_left,
        2: NumericalIntegration.rectangle_right,
        3: NumericalIntegration.rectangle_middle,
        4: NumericalIntegration.trapezoid,
        5: NumericalIntegration.simpson
    }
    print("Выберите метод интегрирования:")
    print("1. Метод прямоугольников (левый)")
    print("2. Метод прямоугольников (правый)")
    print("3. Метод прямоугольников (средний)")
    print("4. Метод трапеций")
    print("5. Метод Симпсона")

    try:
        method_choice = int(input("Введите номер метода: "))
        method = methods.get(method_choice)
        if not method:
            raise ValueError
    except ValueError:
        print("Некорректный выбор метода.")
        return

    p = 2 if method_choice != 5 else 4
    if func in [func4, func5] and (a <= 0 or b <= 0):
        print("Интеграл не существует из-за разрыва на границе.")
        return

    try:
        result, intervals = calculate_integral(func, a, b, epsilon, method, p)
        if result is not None:
            print(f"Значение интеграла: {result}")
            print(f"Число разбиений интервала: {intervals}")
    except OverflowError:
        print("Интеграл не существует — расходящийся интеграл.")


if __name__ == "__main__":
    main()
