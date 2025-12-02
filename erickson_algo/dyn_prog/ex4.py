from math import inf
"""(a) We first make the following observation. If the array begins with a
negative number, then the problem differs in nothing from Exercise 3. Indeed,
the largest possible sum will never have a "wrap-around", since this will only
decrease the sum. Therefore, the only case of interest is when the array begins
with a prefix of non-negative numbers. Observe that this prefix must end
*somewhere*:
    - If it ends at the end of the array, obviously the correct solution equals
    the prefix (i.e., sum of the entire array of non-negative numbers)
    - If it ends earlier, then a subarray that starts with a negative number
    follows. For that subarray, as observed above, the problem is identical to
    Exercise 3. At the very end though, we need to consider *three* candidates:
        - The best sum found so far in this subarray
        - The prefix sum
        - The best sum *that ends at the last element* (exercise 3 gives us
        this "for free") plus the prefix sum, since this is the largest
        possible sum with a wrap-around
The algorithm is again clearly O(n) (one pass) and O(1) space.
"""

def largest_sum(A):      
    
    largest_sum_ending_at_i = None
    largest_sum = 0
    prefix_sum = 0
    prefix_over = False

    for i in range(len(A)):
        if(A[i] < 0 and not prefix_over):
            prefix_over = True
        elif(not prefix_over):
            prefix_sum += A[i]
        if(prefix_over):
            if(largest_sum_ending_at_i is not None):
                largest_sum = max(
                    largest_sum, largest_sum_ending_at_i + A[i], A[i])
            else:
                largest_sum = max(largest_sum, A[i])
            if(largest_sum_ending_at_i is None):
                largest_sum_ending_at_i = A[i]
            else:
                largest_sum_ending_at_i = max(
                    A[i], largest_sum_ending_at_i + A[i])
    if(prefix_over):
        return max(largest_sum, largest_sum_ending_at_i + prefix_sum,
                   prefix_sum)
    else:
        return prefix_sum

arr = [1, -3, -7, -2, 5, 6]
print(str(largest_sum(arr)) + ", expected is " + str(12))
arr = [1, 2, -3, -3, -4, 5, 6]
print(str(largest_sum(arr)) + ", expected is " + str(14))
arr = [1, 2, -3, -1, 7, 3, 8, -1]
print(str(largest_sum(arr)) + ", expected is " + str(20))
arr = [1, 2, -3, -1, 7, 3, 8, -2]
print(str(largest_sum(arr)) + ", expected is " + str(19))
arr = [1, 2, -3, -1, 7, 3, 8, -4]
print(str(largest_sum(arr)) + ", expected is " + str(18))
arr = [1, 2, -3, -1, 7, 3, 8, -3, 1]
print(str(largest_sum(arr)) + ", expected is " + str(19))
arr = [-5, -6, -9, -11]
print(str(largest_sum(arr)) + ", expected is " + str(0))
arr = [1, 7, -7, -11]
print(str(largest_sum(arr)) + ", expected is " + str(8))
arr = [-1, 7, 1, 3, -6]
print(str(largest_sum(arr)) + ", expected is " + str(11))
arr = [5, -3, 5]
print(str(largest_sum(arr)) + ", expected is " + str(10))

"""(b) We will again try to think of the problem in terms of the "vanilla" 
version. For one, if X = 0, this *is* the original problem. If X > 0, we 
observe that the base case of the recursive analysis concerns arrays of length 
n = X. Specifically:
    
    BestSum(A[1...n]) = sum(A[1...n]) if n = X,

since there are no other possible segments of length at least X. If n > X, then
suppose we have recursively computed BestSumEndingAti(A[1...(n - 1)]) and also
BestSum(A[1...(n - 1)]). The introduction of A[n] can only create candidate
sums that end at n. In particular, we can either append A[n] to our "valid
window/range" specified by BestSumEndingAti, or, since this is guaranteed to
have a length of at least X, we can remove its first element and append A[n]
in its place, thus maintaining its current length. There are no other
possibilities for ranges that end at n, and furthermore the best subarray sum
will now be max(BestSum(n - 1), BestSumEndingAti(n)). We notice that the
specification will once again only need two running variables for these, but
we will also need to keep track of the beginning of this sliding window. We
thus have:

    BestEndingAti(A[1...i]) = max(
        BestEndingAti(A[1...(i - 1)]) + A[i],
        BestEndingAti(A[1...(i - 1)]) - A[StartOfWin(i - 1)] + A[i]
        )
    BestSum(A[1...i]) = max(BestSum(A[1...(i - 1)]), BestEndingAti(A[1...i]))
    StartOfWin(i) = 
        StartOfWin(i - 1) if the max resulted from the first case above,
        StartOfWin(i - 1) + 1 if the max resulted from the second case above
        0 if i = 0

We again have O(n) time complexity and O(1) space complexity. In the algorithm
below we implicitly incorporate the "vanilla" version when start_of_window is
negative.
"""

def largest_sum_min_len(A, X):
    assert (len(A) >= X)
    best_sum = 0
    best_sum_ending_at_i = 0
    for i in range(X):
        best_sum += A[i]
        best_sum_ending_at_i += A[i]
    if(X > 0):
        start_of_window = 0
    else:
        start_of_window = -1

    for i in range(X, len(A)):
        opt1 = best_sum_ending_at_i + A[i]
        opt2 = opt1 - (A[start_of_window] if start_of_window >= 0 else 0)
        opt3 = A[i] if start_of_window < 0 else None

        if(opt3 is not None and opt3 > opt1):
            best_sum_ending_at_i = opt3
        elif(opt2 > opt1):
            assert start_of_window >= 0
            start_of_window += 1
            best_sum_ending_at_i = opt2
        else:
            best_sum_ending_at_i = opt1
        best_sum = max(best_sum, best_sum_ending_at_i)

    return best_sum

print("----- PART B -----")
arr = [-1, 7, 1, 3, -6]
print(str(largest_sum_min_len(arr, 3)) + ", expected is " + str(11))
print(str(largest_sum_min_len(arr, 4)) + ", expected is " + str(10))
arr = [-1, 7, 1, -13, -6]
print(str(largest_sum_min_len(arr, 4)) + ", expected is " + str(-6))
arr = [-7, -1, -3, -4, 4, 8, 1, 2, 5, -1]
print(str(largest_sum_min_len(arr, 4)) + ", expected is " + str(20))
arr = [-7, -1, -3, -4, 4, 8, 1, 2, 5, -1]
print(str(largest_sum_min_len(arr, 1)) + ", expected is " + str(20))
arr = [-7, -1, -3, -4, -4, -8, -1, -2, -5, -1]
print(str(largest_sum_min_len(arr, 0)) + ", expected is " + str(0))
arr = [-7, -1, -3, -3, -4, -8, -1, -2, -5, -1]
print(str(largest_sum_min_len(arr, 2)) + ", expected is " + str(-3))

arr = [1, -3, -7, -2, 5, 6]
print(str(largest_sum_min_len(arr, 0)) + ", expected is " + str(11))
arr = [1, 2, -3, -3, -4, 5, 6]
print(str(largest_sum_min_len(arr, 0)) + ", expected is " + str(11))
arr = [1, 2, -3, -1, 7, 3, 8, -1]
print(str(largest_sum_min_len(arr, 0)) + ", expected is " + str(18))
arr = [1, 2, -3, -1, 7, 3, 8, -2]
print(str(largest_sum_min_len(arr, 0)) + ", expected is " + str(18))
arr = [1, 2, -3, -1, 7, 3, 8, -4]
print(str(largest_sum_min_len(arr, 0)) + ", expected is " + str(18))
arr = [1, 2, -3, -1, 7, 3, 8, -3, 1]
print(str(largest_sum_min_len(arr, 0)) + ", expected is " + str(18))
arr = [-5, -6, -9, -11]
print(str(largest_sum_min_len(arr, 0)) + ", expected is " + str(0))
arr = [1, 7, -7, -11]
print(str(largest_sum_min_len(arr, 0)) + ", expected is " + str(8))
arr = [-1, 7, 1, 3, -6]
print(str(largest_sum_min_len(arr, 0)) + ", expected is " + str(11))
arr = [5, -3, 5]
print(str(largest_sum_min_len(arr, 0)) + ", expected is " + str(7))
arr = [-1, -10, -11, -20, -20, -20, 80, 80, 10]
print(str(largest_sum_min_len(arr, 3)) + ", expected is " + str(170))

"""(c) Here the length constraint is reversed. Wrt. the base case of the
recursion, this means that the problem can be solved in the "vanilla" fashion
for A[1...X] (assuming X > 0): any valid solution for the original problem will
by necessity have length at most X. For lengths n > X, the introduction of A[n]
yields new candidate sums that end at n and have length *at most* X. Supposing
therefore we know where the best window that ends at (n - 1) began, then there
are three options for the best window ending at n:
    - Only keep A[n] (and reset this window size to 1)
    - Append A[n] to the window, provided its length was < X (and 
        increment window size)
    - Append A[n] to the window and remove its first element, always possible
        since the previous length was <= X (and keep the window size unchanged)
After this we of course iteratively update the best overall sum. Note that we 
need to keep track of the best window during processing of the first X elements
as well, which is done in the same way as below except that we never need to
"drop" elements from a window. The recursive formulas change as follows:

    BestEndingAti(A[1...i]) = max(
        A[i],
        A[i] + BestEndingAti(A[1...(i - 1)]),
        A[i] + BestEndingAti(A[1...(i - 1)]) - A[BestWinStart(A[1...(i - 1)])]
        )
    BestSum(A[1...i]) = max(
        BestSum(A[1...(i - 1)]), 
        BestEndingAti(A[1...i])
        )
    BestWinStart(A[1...i]) = 
        1, for the first case of the max above
        BestWinStart(A[1...(i - 1)]) + 1, for the second case of the max
        BestWinStart(A[1...(i - 1)]), for the third case of the max

Again, we have O(n) time complexity and O(1) space complexity.
"""

def largest_sum_max_len(A, X):
    if(X == 0):
        return 0
    largest_sum_ending_at_i = 0
    largest_sum = 0
    len_of_win_ending_at_i = 0
    X = min(X, len(A))

    for i in range(X):
        if(A[i] > largest_sum_ending_at_i + A[i]):
            len_of_win_ending_at_i = 1
            largest_sum_ending_at_i = A[i]
        else:
            len_of_win_ending_at_i += 1
            largest_sum_ending_at_i = largest_sum_ending_at_i + A[i]
        largest_sum = max(
            largest_sum, largest_sum_ending_at_i)
        
    for i in range(X, len(A)):
        opt1 = A[i]
        opt2 = -inf
        opt3 = -inf
        
        if(len_of_win_ending_at_i <= X and len_of_win_ending_at_i > 0):
            opt2 = A[i] + largest_sum_ending_at_i - A[
                i - len_of_win_ending_at_i]
            if(len_of_win_ending_at_i < X):
                opt3 = A[i] + largest_sum_ending_at_i
        if(opt1 >= opt2 and opt1 >= opt3):
            len_of_win_ending_at_i = 1
            largest_sum_ending_at_i = opt1
        elif(opt2 > opt1 and opt2 > opt3):
            largest_sum_ending_at_i = opt2
        elif(opt3 >= opt2 and opt3 >= opt1):
            len_of_win_ending_at_i += 1
            largest_sum_ending_at_i = opt3
            pass
        else:
            assert False

        largest_sum = max(
            largest_sum, largest_sum_ending_at_i)
        assert len_of_win_ending_at_i <= X

    return largest_sum

print("----- PART C -----")

arr = [-7, -1, -3, -4, -4, -8, -1, -2, -5, -1]
print(str(largest_sum_max_len(arr, 0)) + ", expected is " + str(0))
print(str(largest_sum_max_len(arr, 1)) + ", expected is " + str(0))
arr = [-1, -10, -11, -20, -20, -20, 80, 80, 10]
print(str(largest_sum_max_len(arr, 1)) + ", expected is " + str(80))
print(str(largest_sum_max_len(arr, 2)) + ", expected is " + str(160))
print(str(largest_sum_max_len(arr, 3)) + ", expected is " + str(170))
print(str(largest_sum_max_len(arr, 5)) + ", expected is " + str(170))
arr = [-1, -10, -11, 80, 80, -20, -20, -20, 10]
print(str(largest_sum_max_len(arr, 30)) + ", expected is " + str(160))

def largest_sum_up_to_X(A, X):
    largest_sum = 0
    largest_sum_ending_at_i = 0

    for i in range(len(A)):
        opt1 = A[i]
        opt2 = A[i] + largest_sum_ending_at_i
        largest_sum_ending_at_i = max(opt1, opt2)
        if(largest_sum_ending_at_i > X and A[i] > X):
            largest_sum_ending_at_i = 0
        elif(largest_sum_ending_at_i > X):
            largest_sum_ending_at_i = A[i]
        largest_sum = max(largest_sum, largest_sum_ending_at_i)

    assert largest_sum <= X
    return largest_sum

print("----- PART D -----")

arr = [1, 2, 3, 14, 5, 1, 1, 19]
print(largest_sum_up_to_X(arr, 21))
        