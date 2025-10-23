# TroubleShooting

!!! Abstract
    在这里记录一些代码常见的问题，尤其是 OI 方面的。

## 1. 混用 C / C++ 风格的输入输出

在一般情况下，混用 C 与 C++ 的输入输出不会出现严重问题，但在 **解绑缓冲区**（即关闭同步）时需要格外留意，例如：

!!! example

    ```cpp
    #include <iostream>
    #include <cstdio>

    using namespace std;

    int main() {
        ios::sync_with_stdio(false);  // 解绑 C++ 与 C 的 I/O 流
        cout << "C++ output\n";
        printf("C output\n");
        // 可能导致输出顺序混乱
        return 0;
    }
    ```

此时，`cout` 与 `printf` 各自使用独立的缓冲区，输出顺序可能与代码书写顺序不一致。更严重的是，若同时使用 `cin` 与 `scanf`，可能会出现缓冲区冲突：

!!! example

    ```cpp
    #include <iostream>
    #include <cstdio>
    
    using namespace std;

    int main() {
        ios::sync_with_stdio(false);
        int x, y;
        cin >> x;      // 可能从 C 缓冲区读取数据
        scanf("%d", &y);    // 可能从 C++ 缓冲区读取数据
        // 导致数据读取错误
        return 0;
    }
    ```

## 2. `round()` 取整后仍出现科学计数法

当数值非常大或非常小时，即使使用 `round()` 取整，默认输出仍可能自动转为科学计数法：

!!! example

    ```cpp
    #include <iostream>
    #include <cmath>

    using namespace std;

    int main() {
        double huge = 1.23456789e20;
        cout << round(huge) << endl;  
        // 输出：1.23457e+20
        return 0;
    }
    ```

解决办法是将 `round(huge)` 强制转换为整数：

!!! example

    ```cpp
    #include <iostream>
    #include <cmath>

    int main() {
        double huge = 1.23456789e20;
        cout << (int)round(huge) << endl;  
        return 0;
    }
    ```

## 3. `memset()` 填充多字节类型

在竞赛中常用 `memset()` 为数组赋初值，但需注意 **`memset()` 按字节填充内存**。

- 对 `char`、`unsigned char` 等单字节类型，任意填充值都是安全的，例如：

!!! example

    ```cpp
    char str[5];
    memset(str, 'A', 5);  // 每个字节均为 'A'，符合预期
    ```

- 对 `int`、`float` 等多字节类型，仅当填充值为 `0` 或 `-1` 时安全，因为它们的二进制表示分别为全 `0` 或全 `1`。

!!! example

    !!! success

        ```cpp
        int arr[10];
        memset(arr, 0, sizeof(arr));  // 所有元素为 0，符合预期
        ```

    !!! failure

        ```cpp
        int arr[3];
        memset(arr, 1, sizeof(arr));  // 每个 int 变为 0x01010101（十进制 16843009），非预期的 1
        ```

若需为其他类型填充值，推荐使用 C++ 的 `std::fill`：

!!! example

    ```cpp
    int arr[10];
    std::fill(arr, arr + 10, 42);  // 每个元素为 42，符合预期
    ```

## 4. Python 中 `str` 格式存储的类型转换

!!! example
    ```bash
    >>> a = [1,1,4,5,1,4]
    >>> b = str(a)
    >>> a
    [1, 1, 4, 5, 1, 4]
    >>> b
    '[1, 1, 4, 5, 1, 4]'
    >>> list(b)
    ['[', '1', ',', ' ', '1', ',', ' ', '4', ',', ' ', '5', ',', ' ', '1', ',', ' ', '4', ']']
    ```

解决方法很简单：使用 `ast.literal_eval()` 将字符串安全地解析回原始对象，记得先 `import ast`。

!!! example
    ```bash
    >>> import ast
    >>> a = [1,1,4,5,1,4]
    >>> b = str(a)
    >>> c = ast.literal_eval(b)
    >>> c
    [1, 1, 4, 5, 1, 4]
    >>> a == c
    True
    ```

`ast.literal_eval(node_or_string)` 是 Python 标准库 `ast`（抽象语法树）模块中的函数，用于安全地计算仅包含 **字面量**（literal）的字符串，并返回对应的 Python 对象。它只会解析以下安全结构：

- 数字（int、float、complex）
- 字符串（str）
- 元组（tuple）
- 列表（list）
- 字典（dict）
- 集合（set）
- 布尔值（True / False）
- `None`

相比 `eval()`，`ast.literal_eval()` 不会执行任何函数调用、变量引用或运算符表达式，因而更加安全可靠。

## 5. GCD函数的几种写法

以下这几种写法本质都是辗转相除法，只是在形式和常数因子上有所不同，通常只记最后一种。

1. While函数

!!! example

    ```cpp
    inline ll gcd(ll a,ll b){
    ll r;
    while(b>0){
        r = a%b;
        a = b;
        b = r;
    }
    return a;
    }
    ```

2. 三目运算符

!!! example

    ```cpp
    inline ll gcd(ll a,ll b){
    ll r;
    while(b>0){
        r = a%b;
        a = b;
        b = r;
    }
    return a;
    }
    ```

3. 位运算

!!! example

    ```cpp
    inline ll gcd(ll a,ll b){
        while(b^=a^=b^=a%=b);
        return a;
    }
    ```
