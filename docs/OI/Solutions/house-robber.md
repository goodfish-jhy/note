# 打家劫舍 I-III

打家劫舍是一套LeetCode上的经典的动态规划题目，由浅入深，这里笔者将分别对每题进行讲解。

## [打家劫舍 I](https://leetcode.cn/problems/house-robber/description/)


对于一个房屋，只存在偷或者不偷两种情况，不难想到设 $f[i]$ 为只偷前 $i$ 家的最大收益。
 
这样，对于第 $i$ 家只需要在偷或者不偷中取最大即可，从而列出这样一个式子：

$$ f[i] = \max(f[i-2] + nums[i], f[i-1])$$

更具体来说：

 - 偷第 $i$ 家：根据题意，这种情况下就不可以再偷第 $i-1$ 家了，所以收益就是只偷前 $i-2$ 家时的最大收益加上第 $i$ 家的收益，即 $f[i] = f[i-2] + nums[i]$。

 - 不偷第 $i$ 家：此时最大收益与只偷前 $i-1$ 家时的收益相同，即 $f[i] = f[i-1]$。  

通过比较这两种情况，选择收益更大的方案作为 $f[i]$ 的值，最终答案就是$f[nums.length]$。

不难注意到，第 $i$ 个只与第 $i-1$ 和 $i-2$ 个有关，所以只需要维护两个数据即可：

```cpp
class Solution {
public:
    int rob(vector<int>& nums) {
        int n = nums.size(), p1 = 0, p2 = nums[0], tmp;
        for (int i = 1; i < n; ++i) {
            tmp = p2;
            p2 = max(p2, p1 + nums[i]);
            p1 = tmp;
        }
        return p2;
    }
};
```

## [打家劫舍 II](https://leetcode.cn/problems/house-robber-ii/description/)

与上一题相比，本题将房屋改为环形排列（首尾相连），此时不能同时盗窃第一间和最后一间房屋，其他条件均不变。

为简化问题，我们可将环形拆解为两个线性问题分别处理：

 - 首先计算偷第一间时不偷最后一间的最大金额；
 
 - 再计算偷最后一间时不偷第一间的最大金额；
 
 - 最终比较这两种情况，取其中的最大值作为最终解。

```cpp
class Solution {
public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        if (n == 0) return 0;
        if (n == 1) return nums[0];
        return max(robRange(nums, 0, n-2), // 偷首不偷尾
                   robRange(nums, 1, n-1)); // 偷尾不偷首   
    }

private:
    // 辅助函数：处理从start到end的线性盗窃问题
    int robRange(vector<int>& nums, int start, int end) {
        int prev = 0, curr = 0;
        for (int i = start; i <= end; ++i) {
            int temp = max(curr, prev + nums[i]);
            prev = curr;
            curr = temp;
        }
        return curr;
    }
};
```