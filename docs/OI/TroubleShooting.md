# TroubleShooting

!!! Abstract
    在这里记录一些代码常见的问题，尤其是OI方面的。

## 1. 混用 C\C++ 风格输入输出

在一般情况下，混用 C\C++ 风格输入输出并不会有太大问题，但如果解绑了缓冲区就需要注意，例如：

!!! example

    ```cpp
    #include <iostream>
    #include <cstdio>

    int main() {
        std::ios::sync_with_stdio(false);  // 解绑C++与C的I/O流
        std::cout << "C++ output\n";
        printf("C output\n");
        
        // 可能导致输出顺序混乱
        return 0;
    }
    ```

这种情况下，由于解绑了同步机制，C++的cout和C的printf会使用各自的缓冲区，导致输出顺序可能与代码书写顺序不一致。更严重的问题是，如果同时使用C++的cin和C的scanf，可能会引发缓冲区冲突：

!!! example

    ```cpp
    #include <iostream>
    #include <cstdio>

    int main() {
        std::ios::sync_with_stdio(false);
        int x, y;
        std::cin >> x;      // 可能从C缓冲区读取数据
        scanf("%d", &y);    // 可能从C++缓冲区读取数据
        // 导致数据读取错误
        return 0;
    }
    ```

## 2. `round()` 取整输出

当数字非常大或非常小时，即使使用 round() 取整后，默认输出也可能自动转为科学计数法：

!!! example

    ```cpp
    #include <iostream>
    #include <cmath>

    int main() {
        double huge = 1.23456789e20;
        std::cout << std::round(huge) << std::endl;  
        // 输出：1.23457e+20
        return 0;
    }
    ```

想要解决只要将`round(huge)`替换为`(int)round(huge)`即可。

## 3. `memset()`

在竞赛中，我们常使用 `memset()` 函数赋予数组初值，但需要注意 `memset()` 实是 **按字节填充内存**。

填充 `char`、`unsigned char`等多字节类型时，任何填充值都是安全的，例如：

!!!​ exmaple

    ```cpp
    char str[5];
    memset(str, 'A', 5);  // 每个字节变为 'A'，符合预期
    ```

填充 `int`、`float` 等多字节类型时，​仅当填充值为 $0$ 或 $-1$ 时安全。因为它们的二进制表示为全 $0$ 或全 $1$。

!!! example

    !!! success

        ```cpp
        int arr[10];
        memset(arr, 0, sizeof(arr));  // 所有元素为 0，符合预期
        ```
    
    !!! failure
    
        ```cpp
        int arr[3];
        memset(arr, 1, sizeof(arr));  // 每个int变为 0x01010101（十进制16843009），非预期的1
        ```

可以使用C++的 `std::fill​` 来实现其他类型的填充

!!! example

    ```cpp
    int arr[10];
    std::fill(arr, arr + 10, 42);  // 每个元素为42，符合预期
    ```
