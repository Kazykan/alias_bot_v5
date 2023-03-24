from math import sqrt


class Calculator:
  #empty constructor
  def __init__(self):
    pass
  #add method - given two numbers, return the addition
  def add(self, x1, x2):
    return x1 + x2
  #multiply method - given two numbers, return the 
  #multiplication of the two
  def multiply(self, x1, x2):
    return x1 * x2
  #subtract method - given two numbers, return the value
  #of first value minus the second
  def subtract(self, x1, x2):
    return x1 - x2
  #divide method - given two numbers, return the value
  #of first value divided by the second
  def divide(self, x1, x2):
    if x2 != 0:
      return x1/x2


def square_eq_solver(a, b, c):
   result = []
   discriminant = b * b - 4 * a * c

   if discriminant == 0:
       result.append(-b / (2 * a))
   elif discriminant > 0:  # <--- изменили условие, теперь
                           # при нулевом дискриминанте
                           # не будут вычисляться корни
       result.append((-b + sqrt(discriminant)) / (2 * a))
       result.append((-b - sqrt(discriminant)) / (2 * a))

   return result

def show_result(data):
   if len(data) > 0:
       for index, value in enumerate(data):
           print(f'Корень номер {index+1} равен {value:.02f}')
   else:
       print('Уравнение с заданными параметрами не имеет корней')

def main():
   a, b, c = map(int, input('Пожалуйста, введите три числа через пробел: ').split())
   result = square_eq_solver(a, b, c)
   show_result(result)


print(Calculator().multiply(2, 3))
