# TroubleShooting

!!! Abstract
    在这里记录一些代码常见的问题，尤其是OI方面的。

## 1. 混用 C\C++ 风格输入输出

在一般情况下，混用 C\C++ 风格输入输出并不会有太大问题，但如果解绑了缓冲区就需要注意，例如：

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

```cpp
#include <iostream>
#include <cmath>

int main() {
    double huge = 1.23456789e20;
    std::cout << std::round(huge) << std::endl;  
    // 输出：1.23457e+20
    
    double tiny = 1.23456789e-20;
    std::cout << std::round(tiny) << std::endl;  
    // 输出：0（太小会被舍入为0）
    
    return 0;
}
```

想要解决只要将`round(tiny)`替换为`(int)round(tiny)`即可。
