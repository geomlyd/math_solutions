"""
(a) We can analyze this recursively as follows. Any partition of A[1...n]
into words must have a first word. This word must end at some index k=1,...n.
The number of valid partitions with this word as the first word is the
number of valid partitions of A[(k + 1)...n]. Therefore, the total number of
valid partitions can be recursively computed by looping over k -assuming
recursive availability of A[(k + 1)...n]- and summing these sub-numbers whenever
IsWOrd(A[1...k]). As a formula:

    NumPart(A[i...j]) = sum(NumPart(A[(k + 1)... j])) if IsWord(A[i...k])
        for k=i, 2, ... n),
    with base case NumPart(A[i...j]) = 1 if i > j

We then want to compute NumPart(A[1...n]). Although this looks like a 2-D 
memoization example at first, we observe that we don't iterate over two indices
at once, but rather just one, so we can basically fill in a 1-D array backwards.
The number of calls to IsWord will be O(n^2) since we check every substring of
A of the form [i...j] for i=1, 2, ..., n and j = i + 1, i + 2, ..., n

"""

# english_dict = set()
words = {"ARTIST", "IS", "OIL", "ART", "A", "TOIL"}

example_str = "ARTISTOIL"

def num_part(A):
    memo = [0 for _ in range(len(A) + 1)]
    memo[len(A)] = 1
    for i in range(len(A) - 1, -1, -1):
        for k in range(i, len(A)):
            substr = A[i:k + 1]
            #print(substr)
            if(substr not in words):
                continue
            memo[i] += memo[k + 1]
    return memo[0]
print(num_part(example_str))

"""
(b) Here we can iterate over both strings at once, and the only thing that
changes is the criterion for counting a "word": i...j is now valid iff
IsWord(A[i...j]) and IsWord(B[i...]). Furthermore, here we are of course
interested in whether *a* partition exists, rather than counting all of them. 
With these in mind we can change the recursion above to:

    CanPartition(A[i...j], B[i...j]) = OR( 
        CanPartition(A[(k + 1)... j]), B[(k + 1)...j]) 
        if (IsWord(A[i...k]) AND IsWord(B[i...k]))
        for k=i, 2, ... n),
    with base case CanPartition(A[i...j], B[i...j]) = True if i > j

Memoization can again be done with a 1-D array, and the total number of
calls to IsWord is again O(n^2).
"""

words = {"BOT", "HEART", "HAND", "SAT", "URNS", "PIN",
         "EAR", "ART", "THE", "HANDS", "SATURN", "SATURNS", "TURN", "TURNS", 
         "SPIN",
         "PIN", "PINS", "START", "TRAP", "TRAPS", "SAND", "AND", "SANDRA",
         "RAG", "RAGS", "SLAP", "LAP", "RAP", "RAPS"}
         
def can_part(A, B):
    assert len(A) == len(B)
    memo = [False for _ in range(len(A) + 1)]
    memo[len(A)] = True
    for i in range(len(A) - 1, -1, -1):
        for k in range(i, len(A)):
            substr1 = A[i:k + 1]
            substr2 = B[i:k + 1]
            if(substr1 not in words or substr2 not in words):
                continue
            if(memo[k + 1]):
                memo[i] = True
                break #short-circuit evaluation of the "or"
    return memo[0]
example1 = "BOTHEARTHANDSATURNSPIN"
example2 = "PINSTARTRAPSANDRAGSLAP"
print(can_part(example1, example2))

"""
(c) Instead of "accumulating" via the "OR" function above, we will simply
accumulate with the sum. Specifically, any partition of A, B into words at
the *same* indices must have a first common index. For that particular index
(i.e., whenever IsWord will be true for both substrings), there are as many
possible ways of partitioning A, B as there are for partitioning the remaining
postfixes. The recursion becomes:

    NumPart(A[i...j], B[i...j]) = sum( 
        NumPart(A[(k + 1)... j]), B[(k + 1)...j]) 
        if (IsWord(A[i...k]) AND IsWord(B[i...k]))
        for k=i, 2, ... n),
    with base case NumPart(A[i...j], B[i...j]) = 1 if i > j

Memoization can again be done with a 1-D array, and the total number of
calls to IsWord is again O(n^2).

"""

words = {"BOT", "HEART", "HAND", "SAT", "URNS", "PIN",
         "EAR", "ART", "THE", "HANDS", "SATURN", "SATURNS", "TURN", "TURNS", 
         "SPIN", "IN", "A", "PINNED", "NED",
         "PIN", "PINS", "START", "TRAP", "TRAPS", "SAND", "AND", "SANDRA",
         "RAG", "RAGS", "SLAP", "LAP", "RAP", "RAPS", "LAPTOP", "TOP"}

def num_part_common_ind(A, B):
    assert len(A) == len(B)
    memo = [0 for _ in range(len(A) + 1)]
    memo[len(A)] = 1
    for i in range(len(A) - 1, -1, -1):
        for k in range(i, len(A)):
            substr1 = A[i:k + 1]
            substr2 = B[i:k + 1]
            if(substr1 not in words or substr2 not in words):
                continue
            memo[i] += memo[k + 1]
    return memo[0]
example1 = "BOTHEARTHANDSATURNSPINNED"
example2 = "PINSTARTRAPSANDRAGSLAPTOP"
print(num_part_common_ind(example1, example2))