//Jiuzhang Array & Numbers

//1. Sorted Array
*****************************
//1.1 Merge Sorted Array: merge B into A
//A = [1,2,6,empty,empty], B = [4,5] --> [1,2,4,5,6]
//Hint: merge from the last position
class Solution {
    /**
     * @param A: sorted integer array A which has m elements, 
     *           but size of A is m+n
     * @param B: sorted integer array B which has n elements
     * @return: void
     */
    public void mergeSortedArray(int[] A, int m, int[] B, int n) {
        int i = m-1, j = n-1, index = m + n - 1;
        while (i >= 0 && j >= 0) {
            if (A[i] > B[j]) {
                A[index--] = A[i--];
            } else {
                A[index--] = B[j--];
            }
        }
        while (i >= 0) {
            A[index--] = A[i--];
        }
        while (j >= 0) {
            A[index--] = B[j--];
        }
    }
}

*****************************
//1.2 Median of two sorted arrays
//A = [1,2,3,4,5,6], B = [2,3,4,5] --> return 3.5

/** Method:
* If we just merge and count --> the time complexity is O(m+n)
* We need O(log(m+n))
* set K = (m + n) / 2
* then our goal is to find Kth element
*/
/** 思路: 
     * 我们建立一个辅助函数用于寻找 kth 元素
     * 比较两个数组k/2 th的元素A[k/2],B[k/2]
     * 若A[k/2] < B[k/2], 说明A[0:k/2]这些元素一定在kth 元素的前面
     * 因此我们可以将数组A缩短为A[k/2:]
     */
public class Solution {
    public double findMedianSortedArrays(int A[], int B[]) {
        int len = A.length + B.length;
        if (len % 2 == 1) {
            return findKth(A, 0, B, 0, len / 2 + 1);
        }
        return (
            findKth(A, 0, B, 0, len / 2) + findKth(A, 0, B, 0, len / 2 + 1)
        ) / 2.0;
    }

    // find kth number of two sorted array
    public static int findKth(int[] A, int A_start,
                              int[] B, int B_start,
                              int k){       
        if (A_start >= A.length) {
            return B[B_start + k - 1];
        }
        if (B_start >= B.length) {
            return A[A_start + k - 1];
        }

        if (k == 1) {
            return Math.min(A[A_start], B[B_start]);
        }
        
        int A_key = A_start + k / 2 - 1 < A.length
                    ? A[A_start + k / 2 - 1]
                    : Integer.MAX_VALUE;
        int B_key = B_start + k / 2 - 1 < B.length
                    ? B[B_start + k / 2 - 1]
                    : Integer.MAX_VALUE; 
        
        if (A_key < B_key) {
            return findKth(A, A_start + k / 2, B, B_start, k - k / 2);
        } else {
            return findKth(A, A_start, B, B_start + k / 2, k - k / 2);
        }
    }
}

//Similar Question: Wood Cut

-----------------------------------------------------------
//2. Subarray
//2.1 Best time to buy and sell stock I/II/III
// this is similar to Maximum Subarray
// e.g. [3,2,3,1,2] can be transfered as [-1,1,-2,1]
// if we buy in Day 0 and sell in Day 1 --> profit is -1
*****************************
//Best time to buy and sell stock II


*****************************
//2.2 Max Subarray I/II/III/IV
we need to use prefixSum here
prefixSum[k] = the sum of first kth elements
!!sum[i:j] = prefix[j] - prefix[i-1]!!
//Max Subarray II
//Find two non-overlapping subarrays with the maximum sum, return the largest sum
//e.g. [1,3,-1,2,-1,2] --> [1,3] + [2,-1,2] = 7
public class Solution {
    /**
     * @param nums: A list of integers
     * @return: An integer denotes the sum of max two non-overlapping subarrays
     */
    public int maxTwoSubArrays(ArrayList<Integer> nums) {
        //left[i] --> the maximum subarray of nums[0:i]
        //right[j] --> the maximum subarray of nums[j:]
        int size = nums.size();
        int[] left = new int[size];
        int[] right = new int[size];
        int sum = 0;
        int minSum = 0;
        int max = Integer.MIN_VALUE;
        for(int i = 0; i < size; i++){
            sum += nums.get(i);
            max = Math.max(max, sum - minSum);
            minSum = Math.min(sum, minSum);
            left[i] = max;
        }
        sum = 0;
        minSum = 0;
        max = Integer.MIN_VALUE;
        for(int i = size - 1; i >= 0; i--){
            sum += nums.get(i);
            max = Math.max(max, sum - minSum);
            minSum = Math.min(sum, minSum);
            right[i] = max;
        }

        //then we try to find a breakline i that achieves the maximum left[i]+right[i+1]
        max = Integer.MIN_VALUE;
        for(int i = 0; i < size - 1; i++){
            max = Math.max(max, left[i] + right[i + 1]);
        }
        return max;
    }
}
*****************************
//2.3 Minimum Subarray 
//-1 * all the elements, then find the maximum subarray
*****************************
//2.4 Maximum Subarray Difference
//similar to Max Subarray II and Minimum Subarray
//find the largest [sumA - sumB]
/** Method:
* find leftMax, leftMin, rightMax, rightMin
* compare (leftMax - rightMin) and (rightMax - leftMin)
*/
public class Solution {
    /**
     * @param nums: A list of integers
     * @return: An integer indicate the value of maximum difference between two
     *          Subarrays
     */
    public int maxDiffSubArrays(int[] nums) {
        // write your code here
        int size = nums.length;
        int[] left_max = new int[size];
        int[] left_min = new int[size];
        int[] right_max = new int[size];
        int[] right_min = new int[size];
        int[] copy = new int[size];
        /*Get negative copy*/
        for(int i = 0; i < size; i++){
            copy[i] = -1 * nums[i];
        }
        int max = Integer.MIN_VALUE;
        int sum = 0;
        int minSum = 0;
        /*Forward: get max subarray*/
        for(int i = 0; i < size; i++){
            sum += nums[i];
            max = Math.max(max, sum - minSum);
            minSum = Math.min(sum, minSum);
            left_max[i] = max;
        }
        /*Backward: get max subarray*/
        max = Integer.MIN_VALUE;
        sum = 0;
        minSum = 0;
        for(int i = size - 1; i >= 0; i--){
            sum += nums[i];
            max = Math.max(max, sum - minSum);
            minSum = Math.min(sum, minSum);
            right_max[i] = max;
        }
        /*Forward: get min subarray*/
        max = Integer.MIN_VALUE;
        sum = 0;
        minSum = 0;
        for(int i = 0; i < size; i++){
            sum += copy[i];
            max = Math.max(max, sum - minSum);
            minSum = Math.min(sum, minSum);
            left_min[i] = -1 * max;
        }
        /*Backward: get min subarray*/
        max = Integer.MIN_VALUE;
        sum = 0;
        minSum = 0;
        for(int i = size - 1; i >= 0; i--){
            sum += copy[i];
            max = Math.max(max, sum - minSum);
            minSum = Math.min(sum, minSum);
            right_min[i] = -1 * max;
        }

        int diff = 0;
        for(int i = 0; i < size - 1; i++){
            diff = Math.max(diff, Math.abs(left_max[i] - right_min[i + 1]));
            diff = Math.max(diff, Math.abs(left_min[i] - right_max[i + 1]));
        }
        return diff;
    }
} 
*****************************
//2.5 Subarray Sum
//find a subarray whose sum is 0, return the start and end index
//e.g. [-3,1,2,-3,4] --> [0,2] or [1,3]
We need to find same elements in sum[j] and sum[i-1]
--> use hash table

*****************************
//2.6 Subarray Sum Closest
//find the sum that is closest to 0
|sum[i] - sum[j]| ~ 0

Step 1: get all sums
Step 2: sort the sum array //nlogn
Step 3: find the element E in sum array that is closest to 0
Step 4: Similar to 2.5 find the subarray whose sum is E

-----------------------------------------------------------
//3. Two Pointers
//3.1 Two Sum
/** Method 1: Hash Table --> O(n)*/
/** Method 2: Two Pointers --> O(nlogn + n)*/
left pointer & right pointer
if the sum > target : rp to left
if the sum < target : lp to right
*****************************
//3.2 Three Sum
//a + b + c = 0 --> find b + c = -a
//O(n^2 + nlogn)

******************************
//3.3 Four Sum
//a --
//b --
//find c + d = -(a + b)

*****************************
//3.3 Partition Array
//this is the core code of quick sort
public class Solution {
    /** 
     *@param nums: The integer array you should partition
     *@param k: As description
     *return: The index after partition
     */
    public int partitionArray(int[] nums, int k) {
        if(nums == null || nums.length == 0){
            return 0;
        }
        
        int left = 0, right = nums.length - 1;
        while (left <= right) {

            while (left <= right && nums[left] < k) {
                left++;
            }

            while (left <= right && nums[right] >= k) {
                right--;
            }

            if (left <= right) {
                int temp = nums[left];
                nums[left] = nums[right];
                nums[right] = temp;
                
                left++;
                right--;
            }
        }
        return left;
    }
}
*****************************
//3.4 Sort Colors
//sort the same color is adjacent
//e.g. [1,0,1,2] --> [0,1,1,2]
public class Solution {
    public void sortColors(int[] a) {
        if (a == null || a.length <= 1) {
            return;
        }
        
        int pl = 0;
        int pr = a.length - 1;
        int i = 0;
        while (i <= pr) {
            if (a[i] == 0) {
                swap(a, pl, i);
                pl++;
                i++;
            } 
            else if(a[i] == 1) {
                i++;
            } 
            else {
                swap(a, pr, i);
                pr--;
            }
        }
    }
    
    private void swap(int[] a, int i, int j) {
        int temp = a[i];
        a[i] = a[j];
        a[j] = temp;
    }
}
*****************************
//3.5 Sort Letters By Case
//"abAcD" --> "acbAD"
public class Solution {
    /** 
     *@param chars: The letter array you should sort by Case
     *@return: void
     */
    public void sortLetters(char[] chars) {
        if(chars == null || chars.length == 0){
            return;
        }

        int i = 0, j = chars.length - 1;
        while ( i <= j) {
            while (i <= j && Character.isLowerCase(chars[i]) ){
                i++;
            }
            while (i <= j && Character.isUpperCase(chars[j]) ){
                j--;
            }
            if (i <= j) {
                char temp = chars[i];
                chars[i] = chars[j];
                chars[j] = temp;
                i++; j--;
            }
        }

    }
}

*****************************
Similar Questions:
Sort Colors II
Interleaving Position and Negative Numbers
//[-,+,+,-,+,-] --> [-,-,-,+,+,+] --> [-,+,-,+,-,+]
//sort them first, then rearrange
class Solution {
    /**
     * @param A: An integer array.
     * @return: void
     */
    int[] subfun(int[] A,int [] B, int len) {
        int[] ans = new int[len];
        for(int i = 0; i * 2 + 1 < len; i++) {
            ans[i * 2] = A[i];
            ans[i * 2 + 1] = B[i];
            }
        if(len % 2 == 1)
            ans[len - 1] = A[len / 2];
        return ans;
    }
    
    public void rerange(int[] A) {
        int[] Ap = new int[A.length];
        int totp = 0;
        int totm = 0;
        int[] Am = new int[A.length];
        int[] tmp = new int[A.length];
        for(int i = 0; i < A.length; i++)
            if(A[i] > 0)
                {
                    Ap[totp] = A[i];
                    totp += 1;
                }
            else
                {
                    Am[totm] = A[i];
                    totm += 1;  
                }   
        if(totp > totm)
            tmp = subfun(Ap, Am, A.length);
        else
            tmp = subfun(Am, Ap, A.length);
        for (int i = 0; i < tmp.length; ++i)
            A[i] = tmp[i];
    }
}
