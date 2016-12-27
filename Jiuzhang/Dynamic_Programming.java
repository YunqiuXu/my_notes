 // Dynamic Programming

//1. Triangle
//1.1 Divide and Conquer: O(2^n)
int divideConquer(int x, int y){
    if(x == n){
        return 0;
    }
    return A[x][y] + Math.min(dfs(x+1, y), dfs(x+1, y+1));
    //[1,1] --> [2,1] or [2,2]
    //[1,0] --> [2,0] or [2,1] --> [2,1] is visited twice
}
divideConquer(0, 0);

//1.2 DivideConquer + Memorization: O(n^2)
int divideConquer(int x, int y){
    if(x == n){
        return 0;
    }
    //Integer.MAX_VALUE --> this node has not been visited
    if(hash[x][y] != Integer.MAX_VALUE){
        return hash[x][y]; //avoid revisiting
    }
    hash[x][y] = A[x][y] + Math.min(dfs(x+1, y), dfs(x+1, y+1));
    return hash[x][y];
}
hash[*][*] = Integer.MAX_VALUE
divideConquer(0, 0);

//1.3 Dynamic Programming : 
//1.3.1 from bottom to top
// condition
A[i][j] : value of current position
f[i][j] : start from (i.j) to last level, the smallest length of path
// initialization: last level
for(int i = 0; i < n; i++){
    f[n-1][i] = A[n-1][i];
}
// loop
for(int i = n - 2; i >= 0; i--){ //start from the second last level
    for(int j = 0; j <= i; j++){
        f[i][j] = Math.min(f[i+1][j], f[i+1][j+1]) + A[i][j];
    }
}
// result
f[0][0]

//1.3.2 from top to bottom -- recommand
//initialization
f[0][0] = A[0][0];
//initialize the left(first element) and right(last element) part of triangle
//only one way
for(int i = 1; i < n; i++){
    f[i][0] = f[i-1][0] + A[i][0];
    f[i][i] = f[i-1][i-1] + A[i][i];
}
//top down
for(int i = 1; i < n; i++){
    for(int j = 1; j < i; j++){
        //core equation
        f[i][j] = Math.min(f[i-1][j], f[i-1][j-1]) + A[i][j];
    }
}
//result: use for loop to find the minimum of f[n-1][*]
Math.min(f[n-1][0], f[n-1][1], f[n-1][2], ...)

/////////////////////////////////////////////////
//2. conditions
//2.1 when to use
a. maximum / minimum
b. check whether accessible
c. count the paths

//2.2 when not to use
a. give all the paths
b. the input is a set(can swap the elements), not list

//2.3 6 kinds of dynamic programming
axis / sequence / double sequence / divide / bag / interval

/////////////////////////////////////////////////
//3. axis-related dynamic programming
//state: 
f[x][y] --> from start to (x, y)
//3.1 Minimum Path Sum 
state: f[x][y] --> the shortest path from start to (x,y)
how to reach (x, y): from (x-1, y) or (x, y-1)
function: f[x][y] = min(f[x-1][y], f[x][y-1]) + A[x][y]
initiaze: 
    f[i][0] = f[i-1][0] + grid[i][0]
    f[0][i] = f[0][i-1] + grid[0][i]
answer: f[n-1][m-1]

public int minPathSum(int[][] grid){
    if(grid == null || grid.length == 0 || grid[0].length == 0){
        return 0;
    }
    int M = grid.length;
    int N = grid[0].length;
    int[][] sum = new int[M][N];

    //initialization: the 0th row and 0th column
    //so you do not to check whether sum[i-1][j], sum[i][j-1] are exist later
    sum[0][0] = grid[0][0];
    for(int i = 1; i < M; i++){
        sum[i][0] = sum[i-1][0] + grid[i][0];
    }
    for(int i = 1; i < N; i++){
        sum[0][i] = sum[0][i-1] + grid[0][i];
    }

    for(int i = 1; i < M; i++){
        for(int j = 1; j < N; j++){
            sum[i][j] = Math.min(sum[i-1][j], sum[i][j-1]) + grid[i][j];
        }
    }

    return sum[M-1][N-1];
}

//3.2 Unique Path (how many unique paths)
state: f[x][y] --> the number of paths from start to (x,y)
function: f[x][y] = f[x-1][y] + f[x][y-1]
initialize: f[0][i] = f[i][0] = 1
answer: f[n-1][m-1]

//3.3 Climbing Stairs
state: f[i] --> the sum of methods to ith position
function: f[i] = f[i-1] + f[i-2]
initialize: f[0] = 1, f[1] = 2 
answer: f[n]

//3.4 Jump Game
state: f[i] --> whether I can jump to ith position
function f[i] = (f[j] == true, j < i && j can reach i)
initialize: f[0] = true
answer: f[n-1]

public boolean canJump(int[] A){
    boolean[] can = new boolean[A.length];
    can[0] = true;

    for(int i = 1; i < A.length; i++){
        for(int j = 0; j < i; j++){
            if(can[j] == true && j + A[j] >= i){
                can[i] = true;
                break;
            }
        }
    }

    return can[A.length - 1];
}
//3.5 Jump Game II
state: f[i] --> the shortest steps to reach ith position
function: f[i] = MIN{f[j]+1, j<i && j can reach i}
initialize: f[0] = 0
answer: f[n-1]

public int jump(int[] A){
    int[] steps = new int[A.length];
    steps[0] = 0;
    for(int i = 1; i < A.length; i++){
        steps[i] = Integer.MAX_VALUE; //init: can not reach
        for(int j = 0; j < i; j++){
            if(steps[j] != Integer.MAX_VALUE && j + A[j] >= i){
                /** Version 1:
                steps[i] = steps[j] + 1;
                break;
                */
                /** Version 2*/
                steps[i] = Math.min(steps[i], steps[j] + 1);
            }
        }
    }
    return steps[A.length - 1];
}

/////////////////////////////////////////////////
//4. sequence related DP
!!!!!!!!!!!!!!!!!!!!!!!!
对于序列相关的DP, 一般有N个字符/数字, 我们需要开N+1容量的数组, 将第0个位置单独拿出来初始化
!!!!!!!!!!!!!!!!!!!!!!!!
state: f[i] --> ith position/ digit/ letter
function: f[i] = f(f[j]), j is a position before i 
initialize: f[0]...
answer: f[n-1]
//4.1 Palindrome Partitioning II
//e.g. "aab" --> return 1 --> partition 1 time to "aa"+"b"
state : f[i] --> the least partition times for string[0:i]
            //or can be partitioned into i+1 substrings
    f[0] --> "" --> -1
        because f["aa"] = f[""] + 1 = 0
    f[1] --> "a" --> 0
    f[2] --> "aa" --> 0
    f[3] --> "aab" --> 1 
        "aa|b" --> 1 + f["aa"]
        "a|ab" --> invalid

    "abac|c" --> 1 + f["abac"]
    "aba|cc" --> 1 + f["aba"]
function: f[i] = MIN{f[j]+1}, that satisfy:
    j<i && j+1 ~ i is valid
initialize: f[i] = i - 1 (f[0] = -1)
answer: f[n], n = s.length

public class Solution{
    //test whether s[j+1 ~ i] is valid palindrome string
    private boolean isPalindrome(String s, int start, int end){
        for(int i = start, j = end; i < j; i++, j--){
            if(s.charAt(i) != s.charAt(j)){
                return false;
            }
        }
        return true;
    }

    //this is a interval-related DP: larger interval relies on smaller one
    //is f[i][j] is valid <--> f[i+1][j-1] is valid && s[i]==s[j]
    //e.g. "abbcbba" <--> "bbcbb" && 'a'=='a'
    private boolean[][] getIsPalindrome(String s){
        boolean[][] isPalindrome = new boolean[s.length()][s.length()];

        //interval = 0 --> single letter
        for(int i = 0; i < s.length(); i++){
            isPalindrome[i][i] = true;
        }
        //interval = 1 --> two letters --> check whether they are same
        for(int i = 0; i < s.length() - 1; i++){
            isPalindrome[i][i+1] = (s.charAt(i) == s.charAt(i+1));
        }
        //interval >= 2
        for(int length = 2; length < s.length(); length++){
            for(int start = 0; start + length < s.length(); start++){
                isPalindrome[start][start+length] = isPalindrome[start+1][start+length-1] && (s.charAt(start) == s.charAt(start+length));
            }
        }
        return isPalindrome;
    }

    public int minCut(String s){
        if(s == null || s.length() == 0){
            return 0;
        }
        //preparation
        boolean[][] isPalindrome = getIsPalindrome(s);
        //initialize
        int[] f = new int[s.length() + 1];
        for(int i = 0; i <= s.length(); i++){
            f[i] = i - 1;
        }
        //main
        for(int i = 1;i <= s.length() ; i++){
            for(int j = 0; j < i; j++){
                if(isPalindrome[j][i-1] == true){
                    f[i] = Math.min(f[i], f[j]+1);
                }
            }
        }
        return f[s.length()];
    }
}

//4.2 Word Break
//check whether a word can be break as words in the dictionary
//e.g. word = "leetcode", dict = ["leet","code"] --> true
//application: you can get the word by searching the subword in dict
state: f[i] --> can the s[0:i] be partitioned?
function: f[i] = OR{f[j]}, j<i, s[j+1 ~ i] is a word in dict;
//if all f[j] are false, then return false
initialize: f[0] = true
answer: f[s.length()]
//A tip: we do not to enum the length of entire text, just the length of longest word in dict
public class Solution{
    private int getMaxLength(Set<String> dict){
        int maxLength = 0;
        for(String word : dict){
            maxLength = Math.max(maxLength, word.length());
        }
        return maxLength;
    }

    public boolean wordBreak(String s, Set<String> dict){
        if(s == null || s.length() == 0){
            return true;
        }

        int maxLength = getMaxLength(dict);
        boolean[] canSegment = new boolean[s.length() + 1];

        canSegment[0] = true;
        for(int i = 1; i <= s.length(); i++){
            canSegment[i] = false;
            for(int lastWordLength = 1; lastWordLength <= maxLength && lastWordLength <= i; lastWordLength++){
                if(canSegment[i-lastWordLength] == false){
                    continue;
                }
                String word = s.substring(i-lastWordLength, i);
                if(dict.contains(word)){
                    canSegment[i] = true;
                    break;
                }
            }
        }
        return canSegment[s.length()];
    }
}

/////////////////////////////////////////////////
//5. double sequence related DP
state: f[i][j] --> first ith elements of first sequence + first jth elements of second sequence
function: f[i][j] --> study the relationship of ith&&jth
initialize: f[i][0], f[0][i]
answer: f[s1.length()][s2.length()]

//5.1 LCS
//e.g. "ABCD", "EACB"
state: lcs[4][4] --> lcs["ABCD"]["EACB"]
function: 
    lcs["ABCD"]["EACB"] = max(lcs["ABCD"]["ABC"], lcs["ABC"]["EACB"])
    if(a[i] == b[j]){
        f[i][j] = max(f[i-1][j], f[i][j-1], f[i-1][j-1] + 1)
    }
    else{
        //"f[i-1][j-1]+0" can be omitted
        f[i][j] = max(f[i-1][j], f[i][j-1]) 
    }
initialize: f[i][0] = 0, f[0][j] = 0
answer: f[a.length()][b.length()]

//5.2 Edit Distance
/** Find the minimum steps to convert str1 to str2
* Insert a char
* Delete a char
* Replace a char
*/
state: f[i][j] --> the min steps to convert a[:i] to b[:j]
function: 
    if(a[i] == b[j]){
        //f[i-1][j]+1 --> del a[i]
        //f[i][j-1]+1 --> add a[i]
        f[i][j] = MIN(f[i-1][j]+1, f[i][j-1]+1, f[i-1][j-1])
    }
    else{
        f[i][j] = MIN(f[i-1][j]+1, f[i][j-1]+1, f[i-1][j-1]+1)
    }
initialize: 
    f[i][0] = i; //del i elements
    f[0][j] = j; //add j elements
answer:
    f[a.length()][b.length()]

//5.3 Distinct Subsequences --> get T from S
/** given S/T, count the distinct subsequences of T in S
* e.g. S = "rabbbit", T = "rabbit", return 3
*/
state: f[i][j]: how to choose T[:j] from S[:i], number of methods
function:
    if(S[i-1] == T[j-1]){
        f[i][j] = f[i-1][j] + f[i-1][j-1];
        /** e.g. S = "rabbb", T = "rab" --> f[5][3]
            f["rabb"]["ra"] --> f[4][2]
            + f["rabb"]["rab"] --> f[4][3]
        */
    }
    else{
        f[i][j] = f[i-1][j]
        /** e.g. S = "rabbbit", T = "rabbi"
        f["rabbbit"]["rabbi"] = f["rabbbi"]["rabbi"]
        nothing to do with "t" in S
        */
    }
initialize:
    f[i][0] = 1; //e.g. S = "abc", T = "", only one method --> subS = ""
    f[0][j] = 0; //j > 0, S = "" --> no methods to get T from S
answer:
    f[S.size()][T.size()]

//5.4 Interleaving String
/** Given 3 strings s1/s2/s3 
* check whether s3 is formed by interleaving of s1 and s2
* s1 = "aabcc", s2 = "dbbca"
* s3 = "aadbbcbcac" --> true (s3 = s1 + s2)
* s3 = "aadbbbaccc" --> false
*/
state: 
    f[i][j] --> can s3 be formed by s1[:i] + s2[:j]
function: 
    f[i][j] = (f[i-1][j] && (s1[i-1] == s3[i+j-1])) || (f[i][j-1] && (s2[j-1] == s3[i+j-1]));
initialize:
    f[i][0] = (s1[0...i-1] == s3[0...i-1]);
    f[0][j] = (s2[0...j-1] == s3[0...j-1]);
answer:
    f[s1.size()][s2.size()]

/////////////////////////////////////////////////
//6 Longest Increasing Subsequence
//find the length of LIS

state:
    axis-related: f[i] --> the LIS when I jump to position i
    single-sequence-related: f[i] --> the LIS of first i elements 
    // we should use axis-related !! 
    // if single-sequence-related, f[i] and f[j] are not related
function: 
    f[i] = max{f[j] + 1}, nums[j] <= nums[i]
initialize:
    all f[i] = 1
answer:
    max(f[i])

for(int i = 0; i < n; i++){
    f[i] = 1;
}

for(int i = 1; i < n; i++){
    for(int j = 0; j < i; j++){
        if(nums[j] <= nums[i]){
            f[i] = Math.max(f[i], f[j] + 1);
        }
    }
}

for(int i = 0; i < n; i++){
    lis = Math.max(lis.f[i]);
}

///////////////////////////////////////////////////////////
1. axis-related
state:
    f[x] 表示我从起点走到坐标x
    f[x][y] 表示我从起点走到坐标x,y
function: 研究走到x,y这个点之前的一步 
intialize: 起点
answer: 终点

2. single-sequence-related
state: f[i]表示前i个位置/数字/字母等
function: f[i] = f(f[j]) j是i之前的一个位置 
initialize: f[0]
answer: f[n-1]

3. double-sequence-related
state: f[i][j]代表了第一个sequence的前i个数字/字符,配上第二个sequence 的前j个
function: f[i][j] = 研究第i个和第j个的匹配关系
initialize: f[i][0] 和 f[0][i]
answer: f[s1.length()][s2.length()]
