# cs 61A
## lecture 6:recursion

```
def split(n)
 return n // 10, n % 10
```
```
def sum_digits(n)
 if n < 10:
  return n
 else:
  all_but_last, last = split(n)
  return sum_digital(all_but_last) + last
```
* base case
* recursive case
  
```
#factorial
def fact(n)
  if n == 0:
    return1
  else:
    return n * fact(n-1)
```
### mtual recursion
two different functions call each other

the Luhn Algroithm
```
def luhn_sum()
  if n < 10:
    return n
  else:
    all_but_last,last= split(n)
    return luhn_sum_double(all_but_last)+last

def luhn_sum_double(n):
  all_but_last, last= split(n)
  luhn_digit = sum_digits(2 * last)
  if n < 10:
    return luhn_digit
  else:
    return luhn_sum(all_but_last) + luhn_digit
```
```
def sum_digit_iter(n):
  digit_sum=0
  while n > 0:
    n,last = split(n)
    digit_sum = digit_sum + last
  return digit_sum
```
```
def cascade(n)
  if n < 10:
    print(n)
  else:
    print(n)
    cascade(n//10)
    print(n)
```
```
#cascade(123)output:
123
12
1
12
123
```
```
#another implementation

def cascade(n):
  print(n)
  if n>= 10:
    cascade(n//10)
    print(n)
```
inverse cascade
```
def inverse_cascade(n):
  grow(n)
  print(n)
  shrink(n)
def f_then_g(f,n,g):
  if n:
    f(n)
    g(n)

grow = lambda n: f_then_g(grow, print, n//10)
shrink = lambda n: f_then_g(print, shrink, n//10)