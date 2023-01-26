# Team (16):
Muhaimin Badar
Nicholas D. Bivens

# Running the program
The program follows the specification required by the assignment to run as a script. (python3 freqnumber.py "k={k};input={infile};output={outfile};")

Or use our test script: ./runsc.sh for the given 10 test cases

# Program description:
This program given an input file parses integers and real numbers and then displays their frequency.

# Implementation:
1. The file reading function was developed as a recursive function called readNext. The function keeps track of a partial list for the partially read input, at the end returning the entire list(s) when no more input is found.
2. We developed a custom string to integer function called strToInt which we utilize for all our conversions from string -> integer.
3. We also developed a similar float function but it was failing one of the test cases and we could not debug it in time so we decided to use float().
4. For an argument parser we decided to use python's syntactical sugar since it is not relevant to the assignment. 
5. inList is a lambda function that traverses a list to search for an element (linear search)
6. listLength is a lambda function that reduces the list to return the size of the list.
7. Filter duplications is a complicated lambda function that removes duplicate elements from the list (we have commented on the algorithm in the program)
8. getFreq is a lambda function that maps a given list u to its frequency in v.  This is achieved by reducing list v and adding 1 if an instance u[i] is found.
9. For our sorting algoritm we used mergeSort which has O(nlogn) time complexity.
10. To print the list we created a recursive function called printList.


# Test cases:
The program passes all 10 provided test cases. 


# Optional criteria (+10 pts)
Our program theoretically handles Rare/extreme cases as we built it relying on recursive principle(s). Numbers are printed if they exist, merge sort has an additional clause to handle same frequencies, etc. We did not test it beyond the provided 10 test cases.


# Optional SQL handling (+20 pts+)
Our program cannot handle this yet due to recursion stack and memory limits. We have figured out a path on how to approach this problem if we have time at the end of the semester. The data will need to be offloaded on virtual memory (files) and managed appropriately.

