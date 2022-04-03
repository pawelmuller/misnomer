# [Misnomer](https://en.wikipedia.org/wiki/Misnomer)
> a name that does not suit what it refers to, or the use of such a name


## Exemplary code snippets
*At the moment the snippets show how the language is supposed to look like in the future.*
1. The program execution starts from the `main()`:
    ```bash
    func main() {
        print("Hello world!");
        return 0;
    }
    ```

2. Each part of code can be described using comments:
    ```bash
    func main() {
        print("Hello world!"); # Prints hello world on screen
        return 0;
    }
    ```

4. You can use local variables:
    ```bash
    var my_integer: int = 0;
    var my_float: float = 1.5;
    var my_string: string = "penguin";
    ```

5. There is a conditional statement available:
    ```bash
    if (a == 1) {
        print("a = 1!");
    } else if (a == 2) {
        print("a = 2!");
    } else {
        print("a is not 1 and not 2!");
    }
    ```

6. It is possible to define your own functions:
    ```bash
    func foo(a: int) {
        a = a+1;
        return a;
    }
    ```
   You can define variables within `()` braces and return an optional function result using `return` keyword.


7. You can use a `while()` loop when you want to repeat the same set of instructions many times:
    ```bash
    while (a != 100) {
        a = a+1;
        print("a = ", a);
    }
    ```

8. It is possible to print a concatenation of the multiple parameters:
    ```bash
    var a: string = "hundred";
    var b: int = 100;
    
    print("You can put even a ", a, "(", b, ") parameters here!");
    ```

9. Users can be made to input some value into the running program:
    ```bash
    var user_input: str = input("Please type something: ");
    ```
   Input parameters work the same as in the `print()` function.
