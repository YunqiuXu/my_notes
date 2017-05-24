## LCS
def lcs(list_a, list_b):
    if list_a == None or list_b == None or len(list_a) == 0 or len(list_b) == 0:
        return 0

    ## init a 2-D array
    mat = [[0 for i in range(len(list_b) + 1)] for j in range(len(list_a) + 1)] # a rows , b cols

    for i in range(1, len(list_a) + 1):
        for j in range(1, len(list_b) + 1):
            if list_a[i - 1] == list_b[j - 1]:
                mat[i][j] = mat[i-1][j-1] + 1
            else :
                mat[i][j] = max(mat[i][j-1],mat[i-1][j])

    return mat[len(list_a)][len(list_b)]

## LIS
def lis(list_a):
    lis_length = 0
    if list_a == None or len(list_a) == 0:
        return lis_length

    ## init a 2-D array
    length_list = [0] * (len(list_a))

    for i in range(0, len(list_a)):
        length_list[i] = 1
        for j in range(i):
            if list_a[i] > list_a[j] and length_list[j] + 1 > length_list[i]:
                length_list[i] = length_list[j] + 1

    return max(length_list)


## Subsequence: the kind of methods to get pattern from deleting some letter from pattern
def subsequence(pattern, string):
    if pattern == None or string == None:
        return 0

    mat = [[0 for col in range(len(string) + 1)] for row in range(len(pattern) + 1)] # pattern rows, string cols

    for row in range(len(pattern) + 1): # no method to get 'xxx' from ''
        mat[row][0] = 0
    for col in range(len(string) + 1): # only one method to get '' from 'xxx': remove all letters
        mat[0][col] = 1

    for row in range(1, len(pattern) + 1):
        for col in range(1, len(string) + 1):
            if pattern[row] != string[col]:
                mat[row][col] = mat[row][col-1]
            else:
                mat[row][col] = mat[row][col-1] + mat[row-1][col-1]

    return mat[len(pattern)][len(string)]

## Find the prime less than k:
## 2 --> 4,6,8,10,...
## 3 --> 6,9,12,...
def get_prime(k):
    result = []
    label_list = [True] * k
    if k <= 1:
        return result

    for i in range(2, k):
        if label_list[i] == True:
            result.append(i)
            label_list[i] = False
            for j in range(i, k):
                if i * j < k and label_list[i * j] == True:
                    label_list[i * j] = False

    return result


## Selection sort
def selection_sort(l):
    if l == None or len(l) <= 1:
        return l

    for i in range(len(l) - 1):
        curr_min_index = l.index(min(l[i + 1:])) # the index
        l[i], l[curr_min_index] = l[curr_min_index], l[i]

    return l

## Insertion sort
def insertion_sort(l):
    if l == None or len(l) <= 1:
        return l

    for i in range(1,len(l)):
        key = l[i]
        j = i - 1
        while l[j] > key and j >= 0:
            l[j + 1] = l[j]
            j -= 1
        l[j + 1] = key

    return l

## Pattern matching: brutal force
def pattern_matching_brutal_force(pattern, string):
    if string == None or pattern == None or len(pattern) > len(string):
        return -1

    m = len(pattern)
    n = len(string)
    for i in range(n-m+1):
        j = 0 # if no match, next loop will begin and j will be reset to 0
        while j < m and pattern[j] == string[i + j]: # match in current place
            j += 1

        if j == m:
            return i

    return -1

## KMP
def failure_function(s):
    F = [0] * len(s)

    prefix_list = []
    suffix_list = []
    for i in range(len(s) - 1):
        prefix_list.append(s[ : i+1])
        suffix_list.insert(0, s[i+1 : ])

    for i in range(len(prefix_list)):
        if prefix_list[i] == suffix_list[i]:
            F[i+1] = F[i] + 1
        else:
            F[i+1] = F[i]

    return F


def KMP(pattern, string):
    if string == None or pattern == None or len(pattern) > len(string):
        return -1

    n = len(string)
    m = len(pattern)
    i = 0
    j = 0

    F = failure_function(string)

    while i < n:
        if pattern[j] == string[i]:
            if j == m - 1:
                return i - j
            else:
                i += 1
                j += 1
        else:
            if j > 0:
                j = F[j-1]
            else:
                i += 1
    return -1


