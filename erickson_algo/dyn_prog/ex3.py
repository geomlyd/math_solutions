"""
(a) We begin by formulating a recursive solution. Let Best(A[1...i]) be
a function that computes the largest sum up to and including i. We then want
Best(A[1...n]). Suppose that recursion gives us Best(A[1...i - 1]). Then, 
the introduction of the new element A[i] creates (i + 1) potential new sums:
all sums ending at i. Observe that if we somehow had available the best sum
*that ends at (i - 1)*, then the only feasible candidates for a new overall
best sum would be that sum plus A[i], or A[i] itself. This can be expressed
as a recursion that involves two functions:

    BestEndingAti(A[1...i]) = max(BestEndingAti(A[1...i - 1]) + A[i], A[i]),
    where BestEndingAti(A[1... i]) = 0 if i < 0

    Best(A[1...i]) = max(Best(A[1...i - 1]), BestEndingAti(A[i - 1] + A[i],
        A[i]),
    where Best(A[1...i]) = 0 if i < 0

At first glance this requires two passes of the array (although it's still
linear), but if we think about it more we can see that Best(A[1...i]) only
depends on values of BestEndingAti(A[1...j]) for j < i, and so these can be
computed in the same loop. Furthermore, because we only ever use i - 1 in the
recursion, two variables suffice instead of an entire array, thus reducing
space complexity to O(1).
"""

def largest_sum(A):
    largest_sum_ending_at_i = 0
    largest_sum = 0

    for i in range(len(A)):
        largest_sum_ending_at_i = max(A[i], largest_sum_ending_at_i + A[i])
        largest_sum = max(
            largest_sum, largest_sum_ending_at_i)

    return largest_sum

arr = [-6, 12, -7, 0, 14, -7, 5]
print(largest_sum(arr))
arr = [-374]
print(largest_sum(arr))
arr = [10, 10, 10, -30, -1, 800, 80]
print(largest_sum(arr))

"""
(b) The reasoning here will be quite similar to the above, except that the
operation of the product introduces the extra complication of signs: a product
that was large as an absolute value but negative may turn positive if the next
A[i] with which it is multiplied is also negative. Nevertheless, once again
the largest product of A[1...i] is either the largest product of A[1... i -1], 
or the largest product *by absolute value*, multiplied by its sign and by A[i], 
or A[i] itself (the only new candidate products are the last two, since A[i]
affects no other contiguous ranges of the array up to i). We thus only need
three variables and one pass through the array.
"""

def largest_product(A):
    largest_product = 1
    largest_by_abs_product_ending_at_i = 0
    sign = 1

    for i in range(len(A)):
        largest_product = max(
            largest_product, largest_by_abs_product_ending_at_i*A[i]*sign,
            A[i])
        if(A[i] < 0):
            if(abs(A[i]) > abs(largest_by_abs_product_ending_at_i*A[i])):
                #if we decide to use a negative A[i] and discard the previous
                #result, the sign is -1
                sign = -1
                largest_by_abs_product_ending_at_i = abs(A[i])
            else:
                #flip the sign if we multiply the result with a new negative 
                #number
                sign = -sign
                largest_by_abs_product_ending_at_i = abs(
                    largest_by_abs_product_ending_at_i*A[i])
        else: #sign stays unchanged if we multiply by positive A[i]
            largest_by_abs_product_ending_at_i = max(
                abs(A[i]), abs(largest_by_abs_product_ending_at_i*A[i]))
    
    return largest_product

arr = [-6, 12, -7, 0, 14, -7, 5]
print(largest_product(arr))
arr = [-374]
print(largest_product(arr))
arr = [10, 10, 10, 0.10, -7000, -1]
print(largest_product(arr))