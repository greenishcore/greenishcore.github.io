# cs 61B

## lecture 1

### HW 0A

#### variable declaration

```java
int i = 0;
```

#### types
*boolean
*int
*double
*string
*char

#### comments

`//xsx`

#### while loop

```java
int i = 0;
while (i < 10) {
    System.out.println(i);
    i++;
}
```

#### for loop

```java
for (int i = 0; i < 10; i ++) {
    System.out.println(i);
}
```

#### condition

if
elif

and &&
or ||
not !
== ==

#### exponention

```java
int x = Math.poe(2,10);
```

#### function declaration and  usage

```java
public static String greet(String name) {
    return "Hello, " + name;
}
System.out.println(greet("Josh"));
```

#### strings

```python
s = "hello"
s += " world"
s += str(5)
s_length = len(s)
substr = s[1:5]
c = s[2]
if "hello" in s:
    print("\"hello\" in s")

for letter in s:
    print(letter)
```

```java
String s = "hello";
s += " world";
s += 5;
int sLength = s.length();
String substr = s.substring(1, 5);
char c = s.charAt(2);
if (s.indexOf("hello") != -1) {
    System.out.println("\"hello\" in s");
}
for (int i = 0; i < s.length(); i++) {
    char letter = s.charAt(i);
    System.out.println(letter);
}
```