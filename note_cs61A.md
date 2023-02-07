# cs 61A

## lecture 6:recursion

```python
def split(n)
 return n // 10, n % 10
```

```python
def sum_digits(n)
 if n < 10:
  return n
 else:
  all_but_last, last = split(n)
  return sum_digital(all_but_last) + last
```

* base case
* recursive case
  
```python
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

```python
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

```python
def sum_digit_iter(n):
  digit_sum=0
  while n > 0:
    n,last = split(n)
    digit_sum = digit_sum + last
  return digit_sum
```

```python
def cascade(n)
  if n < 10:
    print(n)
  else:
    print(n)
    cascade(n//10)
    print(n)
```

```python
#cascade(123)output:
123
12
1
12
123
```

```python
#another implementation

def cascade(n):
  print(n)
  if n>= 10:
    cascade(n//10)
    print(n)
```

inverse cascade

```python
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
```

## lecture 7 tree recursion

```python
def fib(n)
  if n == 0:
    return 0
  elif n == 1:
    return 1
  else:
    return fib(n-2)+fib(n-1)
```

```python
from ucb import trace

@trace
def fib(n)
  if n == 0:
    return 0
  elif n == 1:
    return 1
  else:
    return fib(n-2)+fib(n-1)

#output:
#fib(0):
#fib(0) -> 0
#0
```

### path

path(M,N) = path(M-1,N)+path(M,N-1)

### knapsack

def knap(n,k):
  
  if n == 0:
    return k == 0
  with_last = knap(n//10,k-n%10)
  without_last = knap(n//10,k)
  return with_last or without_last

### counting partitions

```python
def count_partitions(n,m):
  if n == 0:
    return 1
  elif n < 0
    return 0 
  elif m == 0:
    return 0
  else:
    with_m = count_paetitions(n-m, m)
    without_m = count_aprtitions(n,m-1)
    return with_m + without_m
```

### binary print

### implementing a function

```python
def remove(n, digit):

#>>>remove(231,3)
#21
#>>>remove(243132,2)
#4313

ekpt,digits = 0,0
while n > 0:
  n,last = n//10, n % 10
  if last != digit:
    kept = kept/10+last
    digits = digits + 1
    return round(kept *10 ** (digits-1))
```