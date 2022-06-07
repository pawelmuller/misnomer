# [Misnomer](https://en.wikipedia.org/wiki/Misnomer)
> a name that does not suit what it refers to, or the use of such a name

## Functional requirements
- Running Misnomer scripts from text files
- Local variables
- Strong and static typing
- Built-in types: `int`, `float` and `string`
- Possibility to write your own functions
- A `while()` loop
- A conditional `if` statement
- Arithmetic operations: addition, subtraction, multiplication, division
- Logic operations: negation, comparison
- Errors (thrown by interpreter)
- Possibility to print output to the terminal
- Possibility to input some data from the terminal


## Non-functional requirements
- Recursion limit
- Call arguments are copied, not referenced
- Interpreted by Python
- Lexer should escape special characters in strings and translate different line endings correctly


## Requirements analysis
Since it ought to be possible to run Misnomer scripts from text files, there is a need to specify their path easily.
Therefore, it must not be hardcoded into the interpreter but instead given as a run parameter.
Additionally, the recursion limit should be changeable,
so I will add a run flag to allow the user to set a non-default value.

Because the interpreter will be written in Python:
- the integer will derive its unlimited precision and the float
will have precision equal to the C double on your machine
- the recursion limit will default to less than 1000: 900 should be a safe number 
- source code reader class will not handle line endings explicitly, since it's provided by
[`io.TextIOWrapper`](https://docs.python.org/3.10/library/io.html?highlight=textiowrapper#io.TextIOWrapper)

Additionally, there is a default limit for string length that equals 1000 characters.


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
As well as maximum string length limit:
```shell
python misnomer.py path_to_script.mnm --max_string_length 2000
```

## Exemplary code snippets
1. The program execution starts from the `main()`:
    ```bash
    main() returns int {
        print("Hello world!");
        return 0;
    }
    ```

2. You can use local variables:
    ```bash
    var my_integer: int = 0;
    var my_float: float = 1.5;
    var my_string: string = "penguin";
    ```

3. There is a conditional statement available:
    ```bash
    if (a == 1) {
        print("a = 1!");
    } else if (a == 2) {
        print("a = 2!");
    } else {
        print("a is not 1 and not 2!");
    }
    ```

4. It is possible to define your own functions:
    ```bash
    foo(a: int) returns int{
        a = a+1;
        return a;
    }
    ```
   You can define variables within `()` braces and return an optional function result using the `return` keyword.
   You can choose from the following return types: `int`, `float`, `string` and `nothing`.

6. You can use a `while()` loop when you want to repeat the same set of instructions many times:
    ```bash
    while (a != 100) {
        a = a+1;
        print("a = ", a);
    }
    ```

7. It is possible to print a concatenation of the multiple parameters:
    ```bash
    var a: string = "hundred";
    var b: int = 100;
    
    print("You can put even a ", a, "(", b, ") parameters here!");
    ```

8. Users can be made to input some value into the running program:
    ```bash
    var user_input: str = input("Please type something: ");
    ```
   Input parameters work the same as the `print()` function.
    ```

9. There are builtin functions for casting different types:
    ```bash
    var user_input_1: string = to_string(123456);
    var user_input_2: int = to_int("123456");
    var user_input_3: float = to_float("123.456");
    ```
