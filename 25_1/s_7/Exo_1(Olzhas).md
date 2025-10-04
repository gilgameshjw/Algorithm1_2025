Fundamental Algorithm Techniques - Problem Set #1 Analysis
This document provides a detailed analysis and proposed solutions for Problem Set #1, due on 

October 4, 2025.

Problem 1: Sparse Vector Search (Find the single '1')

Problem Description: Consider a sparse vector v of size n with only zeros and a single '1':

v=[0,0,...,1,...,0]

The goal is to find the position of the '1' using divide and conquer.

(a) Recursive Pseudo-Code for Divide and Conquer
The requirement is to implement the binary divide-and-conquer method recursively without creating a copy of the vector, stopping when the vector is decomposed into size 1. This is achieved by passing the original vector along with indices defining the current sub-range.

Binary Divide (m=2)
This function will recursively divide the current range [start,end] into two halves. Since the vector contains only one '1', we only need to search the sub-range that contains it.



// Function to find the index of the single '1' in a sparse vector v
// The search is restricted to the range [start, end]
function FIND_ONE_BINARY(v, start, end):
    // Base Case: Vector fully decomposed to size 1
    if start == end:
        if v[start] == 1:
            return start // Found the position
        else:
            return NULL // Should not happen if a '1' is guaranteed

    // Divide Step: Find the midpoint
    mid = floor((start + end) / 2)

    // Conquer/Filter Step: Determine which half contains the '1'
    // This requires a quick check of the left sub-array (e.g., a summation)

    // Optimization: Since we know the vector is sparse (single '1'), 
    // we only need to check if the '1' is in the left half.
    // A simple, non-copy check (e.g., 'CheckForOne' function) must be used.
    
    // The cost of this 'check' dominates the complexity.
    // If 'CheckForOne' takes O(k) for a range of size k:
    
    // Check the left half: [start, mid]
    if CONTAINS_ONE(v, start, mid): 
        return FIND_ONE_BINARY(v, start, mid)
    else:
        // The '1' must be in the right half: [mid + 1, end]
        return FIND_ONE_BINARY(v, mid + 1, end)
Note: The function CONTAINS_ONE(v,start,end) needs to iterate over the sub-array to check for a '1'. Its cost is O(end−start+1) which will be crucial for complexity analysis.

m-ary Divide (m≪n)
This function divides the current range into m equal (or nearly equal) sub-ranges.



function FIND_ONE_M_ARY(v, start, end, m):
    // Base Case
    if start == end:
        if v[start] == 1:
            return start
        else:
            return NULL
            
    // Divide Step: Calculate sub-array size and ranges
    n_current = end - start + 1
    sub_size = floor(n_current / m)
    
    // Conquer/Filter Step: Iterate through the m sub-ranges
    for i = 0 to m - 1:
        // Define the sub-range [sub_start, sub_end]
        sub_start = start + i * sub_size
        if i < m - 1:
            sub_end = start + (i + 1) * sub_size - 1
        else:
            // The last sub-range handles any remainder
            sub_end = end

        // Optimization: Check only the current sub-range
        if CONTAINS_ONE(v, sub_start, sub_end):
            // Recursively search the sub-range that contains the '1'
            return FIND_ONE_M_ARY(v, sub_start, sub_end, m)
            
    return NULL // Should not be reached if '1' exists
(b) Complexity Analysis of Divide and Conquer
The crucial step in this algorithm is the 

filtering step: determining which sub-range contains the '1'. As noted, this check requires iterating over (or effectively summing) one or more sub-arrays.

Let T(n) be the time complexity for a vector of size n.
The recurrence relation is:

T(n)=a⋅T(n/m)+f(n)

Where:

a: number of recursive calls made (in this case, a=1 because we only recurse on the branch containing the '1').

m: the division factor (n/m is the size of the subproblem).

f(n): the cost of the divide/filter step (the cost to figure out which sub-problem to call).

Binary Division (m=2)
The algorithm checks the left half (size n/2) to see if it contains the '1'. This check, 

CONTAINS_ONE, costs O(n/2), or O(n) overall.


Recurrence Relation:

T(n)=1⋅T(n/2)+O(n)
Complexity O(n) (Using Master Theorem) [Master Theorem Case 3]:
Compare f(n)=O(n) with n 
log 
m
​
 a
 =n 
log 
2
​
 1
 =n 
0
 =1. Since f(n)=O(n) is polynomially larger than n 
0
 , and a⋅f(n/m)=1⋅O(n/2)= 
2
1
​
 O(n)≤c⋅O(n) for c=1/2<1, the complexity is dominated by f(n).

O(T(n))=O(n)
Tertiary Division (m=3)
The algorithm checks the first sub-range (size n/3), then the second (size n/3), stopping when it finds the '1' or defaults to the third. In the worst case, it checks the first two sub-ranges, costing 

O(n/3)+O(n/3)=O(n).


Recurrence Relation:

T(n)=1⋅T(n/3)+O(n)
Complexity O(n) (Using Master Theorem) [Master Theorem Case 3]:
Compare f(n)=O(n) with n 
log 
m
​
 a
 =n 
log 
3
​
 1
 =n 
0
 =1. Again, the complexity is dominated by f(n).

O(T(n))=O(n)
Conclusion for (b): The divide-and-conquer approach, when the filtering step requires a search of the sub-array, results in a linear time complexity O(n) for any m.

(c) Collection Cost
The prompt suggests a different interpretation for the cost: once the division reaches size 1, we collect the unique '1' and its position. This implies the 

only cost is the overhead of the recursion and the final collection step. Crucially, it assumes the cost of determining which sub-range contains the '1' is negligible, or O(1).

This is only possible if the problem allowed an oracle to identify the correct branch in O(1) time.

Assuming the cost f(n) is only the overhead of splitting and recursing (O(1)):

Cost f(n) (Overhead/Splitting only):

f(n)=O(1)

Recurrence Relation T(n) (for m=2):

T(n)=T(n/2)+O(1)

Complexity O(logn) or O(n) (Using Master Theorem):


Compare f(n)=O(1) with n 
log 
m
​
 a
 =n 
log 
2
​
 1
 =n 
0
 =1. Since f(n)=Θ(n 
log 
m
​
 a
 ), Master Theorem Case 2 applies.

O(T(n))=O(n 
log 
2
​
 1
 logn)=O(logn)

The complexity is O(logn) 

if and only if the check for the '1' in a sub-range is O(1). This is the ideal goal of a search algorithm like Binary Search and is possible for this specific sparse vector problem if the vector is sorted and we can check v[mid] in O(1) time. For an unsorted sparse vector, the complexity remains O(n) as determined in part (b).

(d) Comparison with Simpler Approach
The 

simpler approach is to run over all indices:


function FIND_ONE_SIMPLE(v, n):
    for i = 0 to n - 1:
        if v[i] == 1:
            return i
Time Complexity: In the best case, the '1' is at index 0 (O(1)). In the worst case, the '1' is at index n−1 or the end (O(n)).

Overall Complexity: The average and worst-case time complexity is O(n).

Comparison:
| Method | Complexity (Worst Case) | Condition for O(logn) |
| :--- | :--- | :--- |
| Simple Iteration | O(n) | Never |
| Divide and Conquer (b) | O(n) | N/A |
| Divide and Conquer (c) | O(logn) | If the filter step is O(1) (like Binary Search) |

Conclusion: The divide-and-conquer approach in its honest implementation (part b) is no better than the simpler approach, as both are O(n). The divide-and-conquer only becomes superior (O(logn)) if a constant-time check can be used to direct the search, like in a classic Binary Search on a sorted array.

Problem 2: School Multiplication

Problem Description: Implement and analyze the standard school multiplication algorithm (base 10) for two large positive integers, x and y, represented by arrays X and Y.

x= 
i=0
∑
n 
x
​
 
​
 X[i]⋅10 
i
 y= 
j=0
∑
n 
y
​
 
​
 Y[j]⋅10 
j
  where n 
x
​
 ≈n 
y
​
 ≈n
1. Multiplication Pseudocode (School Method)
The school method involves:

Multiplying each digit of Y by the entire number X.

Shifting the result based on the position of the digit in Y.

Summing all the intermediate results (with carry).

Фрагмент кода

function SCHOOL_MULTIPLICATION(X, Y, nx, ny):
    // Assume nx and ny are the lengths of X and Y arrays
    // R is the final result array (size max nx + ny)
    R = array of zeros of size (nx + ny) 
    
    // Outer loop: Iterate through each digit of Y
    for j = 0 to ny - 1:
        carry = 0
        // Inner loop: Multiply Y[j] by each digit of X
        for i = 0 to nx - 1:
            // 1. Digit multiplication
            product = X[i] * Y[j] + R[i + j] + carry 
            
            // 2. Separate digit and carry
            R[i + j] = product mod 10
            carry = floor(product / 10)
            
        // 3. Handle final carry for the current row
        R[nx + j] = R[nx + j] + carry 
        // Note: The shifting (multiplication by 10^j) is implicit 
        // by placing the result in R[i + j]
        
    return R // The result vector (potentially needs leading zero removal)
2. Tweak Code for Large Results
The above pseudocode already handles results larger than standard integer limits because:

The numbers 

x and y are represented by vectors/arrays X and Y. This is the standard way to handle large integers (arbitrary-precision arithmetic).

The result 

R is also a vector/array of size up to n 
x
​
 +n 
y
​
 , allowing the product to grow without bound.

The intermediate product product=X[i]⋅Y[j]+R[i+j]+carry will be at most 9×9+9+9=99, which fits well within a standard integer variable.

The main tweak is ensuring the initial input representation is an array of digits (as shown in the pseudocode) and the result R is maintained as an array.

3. Time Complexity
Let 

n be the approximate size of the two numbers (n 
x
​
 ≈n 
y
​
 ≈n).

The outer loop runs n times (for j=0 to n 
y
​
 −1).

The inner loop runs n times (for i=0 to n 
x
​
 −1).

The operations inside the inner loop are O(1) (digit multiplication, addition, and carry logic).

Therefore, the total number of O(1) operations is O(n⋅n)=O(n 
2
 ).

Time Complexity: 

O(n 
2
 )
4. Divide and Conquer and Karatsuba
The goal of this section is to show how the multiplication can be recast into a divide-and-conquer framework and to recall the complexities of classic algorithms.

Let n be the number of digits. We split x and y into two halves of length n/2 (or ⌈n/2⌉).

x=x 
1
​
 ⋅10 
n/2
 +x 
0
​
 
y=y 
1
​
 ⋅10 
n/2
 +y 
0
​
 
where 

x 
1
​
 ,x 
0
​
 ,y 
1
​
 ,y 
0
​
  are the halves of the numbers (Hint 1).

The product 

x⋅y is:

x⋅y=(x 
1
​
 ⋅10 
n/2
 +x 
0
​
 )(y 
1
​
 ⋅10 
n/2
 +y 
0
​
 )
x⋅y=x 
1
​
 y 
1
​
 ⋅10 
n
 +(x 
1
​
 y 
0
​
 +x 
0
​
 y 
1
​
 )⋅10 
n/2
 +x 
0
​
 y 
0
​
 
x⋅y=z 
2
​
 ⋅10 
n
 +z 
1
​
 ⋅10 
n/2
 +z 
0
​
 

where:

z 
2
​
 =x 
1
​
 y 
1
​
 

z 
1
​
 =x 
1
​
 y 
0
​
 +x 
0
​
 y 
1
​
 

z 
0
​
 =x 
0
​
 y 
0
​
 

Standard Divide and Conquer
This formulation requires four multiplications of size n/2: x 
1
​
 y 
1
​
 , x 
1
​
 y 
0
​
 , x 
0
​
 y 
1
​
 , and x 
0
​
 y 
0
​
 . The additions and shifts (multiplications by 10 
k
 ) take O(n) time.

Recurrence Relation:

T(n)=4T(n/2)+O(n)

Complexity O(n 
2
 ) (Master Theorem):


Compare f(n)=O(n) with n 
log 
m
​
 a
 =n 
log 
2
​
 4
 =n 
2
 . Since f(n)=O(n) is polynomially smaller than n 
2
 , the complexity is dominated by the recursive calls.

O(T(n))=O(n 
2
 )

This shows that a naive divide-and-conquer approach has the same complexity as the school method.

Karatsuba Algorithm
Karatsuba's algorithm is a clever trick to reduce the four multiplications to 

three multiplications of size n/2.

z 
0
​
 =x 
0
​
 y 
0
​
  (1 multiplication)

z 
2
​
 =x 
1
​
 y 
1
​
  (1 multiplication)

z 
3
​
 =(x 
1
​
 +x 
0
​
 )(y 
1
​
 +y 
0
​
 ) (1 multiplication)

Then, the middle term z 
1
​
  is computed using the results of z 
3
​
 ,z 
2
​
 ,z 
0
​
 :

z 
1
​
 =z 
3
​
 −z 
2
​
 −z 
0
​
 =(x 
1
​
 y 
0
​
 +x 
0
​
 y 
1
​
 )

The final result is still x⋅y=z 
2
​
 ⋅10 
n
 +z 
1
​
 ⋅10 
n/2
 +z 
0
​
 .

Recurrence Relation:

T(n)=3T(n/2)+O(n)

Complexity O(n 
1.585
 ) (Master Theorem):


Compare f(n)=O(n) with n 
log 
m
​
 a
 =n 
log 
2
​
 3
 ≈n 
1.585
 . Since f(n) is polynomially smaller than n 
1.585
 , the complexity is dominated by the recursive calls.

O(T(n))=O(n 
log 
2
​
 3
 )≈O(n 
1.585
 )

Karatsuba's algorithm is asymptotically faster than the school method.

5. Sum of Integers by Multiplication
The problem asks to compute the sum of the first 

n integers:

i=1
∑
n
​
 i=1+2+⋯+(n−1)+n= 
2
n(n+1)
​
 

The question is:  
2
1
​
 ⋅mult(v,w) with which v,w gives n!= 
2
n(n+1)
​
 ? Note: there is a typo in the prompt, it asks for n! but provides the formula for ∑ 
i=1
n
​
 i. Assuming the formula is the goal.

The goal is to find v and w such that their multiplication v⋅w equals n(n+1).

Let v=n and w=n+1.

If we define v and w as the numbers n and n+1:

i=1
∑
n
​
 i= 
2
1
​
 ⋅mult(n,n+1)
Example for n=4: ∑ 
i=1
4
​
 i=1+2+3+4=10.

2
1
​
 ⋅mult(4,5)= 
2
1
​
 ⋅20=10
Example for n=5: ∑ 
i=1
5
​
 i=1+2+3+4+5=15.

2
1
​
 ⋅mult(5,6)= 
2
1
​
 ⋅30=15
Answer:
The sum ∑ 
i=1
n
​
 i can be computed by one application of school multiplication:

i=1
∑
n
​
 i= 
2
1
​
 ⋅mult(v,w)

where v=n and w=n+1 (or vice versa).
