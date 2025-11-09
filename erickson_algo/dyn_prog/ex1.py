"""
(a) Good "candidates" for this are integer multiples of the bill values. We can
iterate over these and if we find that the greedy count for one of them
exceeds (amount) // (bill we are examining), then we know the greedy
algorithm will fail. Running the program below demonstrates that the
greedy algorithm *should* fail for 455. We have that:

455 = 91*5, i.e., this can be done with 5 91-dollar bills
The greedy algorithm would choose: 1*365 + 1*52 + 1*28 + 1*7 + 3*1 = 7
bills. The intuitive idea is that some multiples of the bill values may
end up yielding "awkward" (e.g. 455 - 365 = 90, "just below" 91) remainders 
when subtracting the biggest possible bill iteratively.
"""

amount = 0
denominations = [1, 4, 7, 13, 28, 52, 91, 365]

def count_greedy(amount):
    count = 0
    while(amount > 0):
        #doing linear search for simplicity
        for i in range(len(denominations)):
            if(i == len(denominations) - 1 or denominations[i + 1] > amount):
                break
        count += 1
        amount -= denominations[i]
    return count
count_greedy(365)
for i in range(6):
    for d in denominations:
        target = d*i
        if(count_greedy(target) > i):
            print("Greedy algorithm will fail for " + str(target))

"""
(b) A naive but correct solution would be the following. Let X be the target 
amount and B[1...n] be the available denominations. Then the result we seek
can be expressed as:

    min_bills(X, B) = min_{i=1...n} {min_bills(X - B[i], B) + 1, if X - B[i] > 0} 
    if X is not equal to any B[i], otherwise 1

i.e., iterate over all possible bill choices, each of which contributes 1 to
the number of bills, and use the minimum number of bills required for forming
the target amount minus that bill value. This algorithm is correct because
1) the base case is correct. There is no better way of forming a B[i]-dollar
value other than using 1 B[i] dollar bill
2) supposing that the algorithm functions correctly for all values < X, then
the best choice for X *must* be one of the n bills, and clearly whatever this
choice is, the remaining amount must have been formed optimally as well
"""
calls = 0
def min_bills_slow(target, denominations):
    global calls
    calls += 1
    min_bills = None
    choices = []
    if(target < 0):
        return None, []
    for d in denominations:
        if(target - d == 0):
            return 1, [d]
        else:
            tmp, tmp_choices = min_bills_slow(target - d, denominations)
            if(tmp is None):
                continue
            if(min_bills is None):
                min_bills, choices = tmp, tmp_choices
            elif(tmp < min_bills):
                min_bills, choices = tmp, tmp_choices + [d]
    return min_bills + 1, choices

example = 45
denominations = [1, 4, 7, 13, 28, 52, 91, 365]
print("Minimum number of bills for {0}: {1}".format(
   example, min_bills_slow(example, denominations)))
print("Took {0} calls".format(calls))

"""
(c) To turn this into a dynamic programming algorithm, we observe that we
are interested in k different values, and that each of them depends on
n subproblems for which k - B[i] < k *strictly*. Therefore we can memoize
values of the function in a 1-D array of size k. Specifically:
    1) we first initialize elements arr[b[i]] with 1 for each denomination
    2) we loop through arr from 1 to k, and for each element j lookup at most n
    different (already computed) values, j - B[i]. We assign the minimum + 1
    to arr[j].
The runtime here will be O(k*n).
"""
def min_bills_fast(target, denominations):
    memo = [None for _ in range(target + 1)]
    choices = [[] for _ in range(target + 1)]
    for d in denominations:
        if(d <= target):
            memo[d] = 1
            choices[d] = [d]

    for x in range(1, target + 1):
        if(memo[x] is not None):
            continue
        best_d = None
        for d in denominations:
            if(x < d):
                continue
            if(memo[x] is None):
                best_d = d
                memo[x] = memo[x - d]
            elif(memo[x - d] < memo[x]):
                best_d = d
                memo[x] = memo[x - d]
        choices[x] = choices[x - best_d] + [best_d]
        memo[x] += 1
    return memo[target], choices[target]

example = 456
denominations = [1, 4, 7, 13, 28, 52, 91, 365]
print("Minimum number of bills for {0}: {1}".format(
    example, min_bills_fast(example, denominations)))
