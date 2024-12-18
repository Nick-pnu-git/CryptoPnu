def modular_inverse(a, p):
   #Обчислює обернений елемент за модулем p.
   return pow(a, p - 2, p)

def is_on_curve(x, y, p):
   #Перевіряє, чи належить точка (x, y) заданій еліптичній кривій.
   return (y ** 2) % p == (x ** 3 - x + 3) % p






def add_points(P, Q, p):
   #Додає дві точки P і Q на еліптичній кривій.
   if P == (None, None):  # Точка на нескінченності
       return Q
   if Q == (None, None):  # Точка на нескінченності
       return P


   x1, y1 = P
   x2, y2 = Q


   if P != Q:  # Якщо точки різні
       m = (y2 - y1) * modular_inverse(x2 - x1, p) % p  # Нахил прямої між точками
   else:  # Якщо точки однакові
       m = (3 * x1 ** 2 - 1) * modular_inverse(2 * y1, p) % p  # Нахил дотичної


   x3 = (m ** 2 - x1 - x2) % p
   y3 = (m * (x1 - x3) - y1) % p


   return (x3, y3)


if __name__ == "__main__":
   # Задана еліптична крива y^2 = x^3 - x + 3 (mod 127)
   p = 127  # Просте число
   P = (71, 46)  # Точка P
   Q = (75, 6)   # Точка Q


   # Перевірка належності точок до кривої
   is_P_on_curve = is_on_curve(P[0], P[1], p)
   is_Q_on_curve = is_on_curve(Q[0], Q[1], p)


   print(f"Точка P {P} {'належить' if is_P_on_curve else 'не належить'} кривій.")
   print(f"Точка Q {Q} {'належить' if is_Q_on_curve else 'не належить'} кривій.")


   if is_P_on_curve and is_Q_on_curve:
       # Обчислення суми точок P + Q
       R = add_points(P, Q, p)
       print(f"P + Q = {R}")
