# [Misnomer](https://en.wikipedia.org/wiki/Misnomer)
> a name that does not suit what it refers to, or the use of such a name

## Functional requirements
- Running Misnomer scripts from text files
- Local variables
- Strong and static typing
- Built-in types: `integer`, `float` and `string`
- Possibility to write your functions
- A `while()` loop
- A conditional `if` statement
- Arithmetic operations: addition, subtraction, multiplication, division
- Logic operations: negation, comparison
- Error handling
- Possibility to print output to the terminal
- Possibility to input some data from the terminal


## Non-functional requirements
- Recursion limit
- Call arguments are copied, not referenced
- Interpreted by Python
- Lexer should escape special characters in strings and translate different line endings correctly


## Requirements analysis
Since it ought to be possible to run Misnomer scripts from text files, there is a need to specify their path easily.
Therefore, it must not be hardcoded into the interpreter but instead given a run parameter.
Additionally, the recursion limit should be changeable,
so I will add a run flag to allow the user to set a non-default value.

Because the interpreter will be written in Python:
- the integer will derive its unlimited precision and the float
will have precision equal to the C double on your machine
- the recursion limit will default to 1000 
- source code reader class will not handle line endings explicitly, since it's provided by
[`io.TextIOWrapper`](https://docs.python.org/3.10/library/io.html?highlight=textiowrapper#io.TextIOWrapper)




## Error handling
Misnomer will catch casual errors and stop executing the script with the proper notification.


## Running the interpreter
You will be able to interpret any file written in Misnomer by running:
```shell
python misnomer.py path_to_script.mnm
```
You will need Python 3.10 to run the interpretation.

### Optional arguments
It is possible to run the interpreter with different settings. At the moment you can specify your own recursion limit:
```shell
python misnomer.py path_to_script.mnm --recursion_limit 30
```

## Exemplary code snippets
*At the moment, the snippets show what the language is supposed to look like in the future.*
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
   You can define variables within `()` braces and return an optional function result using the `return` keyword.


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
   Input parameters work the same as the `print()` function.
