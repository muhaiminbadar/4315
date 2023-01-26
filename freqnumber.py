# %% [markdown]
# **Library includes**

# %%
import sys
from typing import List
from functools import reduce


# %% [markdown]
# **Reading in the input:**
# Extract the k & file name(s) - convert to recursive?
def getArguments(str):
  for x, y in [(pair.split("=")) for pair in str.split(";")]:
    if x == "k":
      k = int(y)
    elif x == "input":
      inputFrom = y
    elif x == "output":
      outputTo = y

  return k, inputFrom, outputTo


# %% [markdown]
# **Parse the input w/ lambdas, etc**
# %%
strToInt = lambda s: reduce(lambda x, y: x * 10 + y,
                            map(lambda c: ord(c) - 48, iter(s)))

#strToFloat = lambda s: reduce(lambda x, y: x / 10 + y, map(lambda x: (ord(x[1]) - 48)/x[0], enumerate(s))) -- not working
def strToFloat(str, integral=0, fractional=0, fPos=0):
  print(str)
  if not str:
    return integral + fractional
  if str[0] == '.':
    return strToFloat(str[1:], integral, fractional, 1)
  if fPos > 0:
    return strToFloat(str[1:], integral,
                      fractional + (ord(str[0]) - 48) / pow(10, fPos),
                      fPos + 1)
  return strToFloat(str[1:], integral * 10 + (ord(str[0]) - 48), fractional,
                    fPos)


isDecimal = lambda x: x == '.'
isNumeric = lambda x: ('0' <= x <= '9')
isMinus = lambda x: x == '-'
isAlphabetical = lambda x: ('A' <= x <= 'Z') or ('a' <= x <= 'z')


def readNext(f,
             integerList: List[int] = [],
             floatList: List[float] = [],
             reading: str = "",
             isFloat: bool = False,
             mul=1):
  char = f.read(1)  # Read next char from input
  if not char:
    if reading:  # Check if input exists, then put into appropriate Integer/Float list
      return [
        integerList + [mul * strToInt(reading)], floatList
      ] if not isFloat else [integerList, floatList + [mul * float(reading)]]
    else:
      return [integerList, floatList]

  if isAlphabetical(char):
    return readNext(
      f, integerList,
      floatList)  # Encountered an invalid char, discard and read next:
  else:
    if not reading and isMinus(char):
      return readNext(f, integerList, floatList, reading, isFloat, -1)
    elif reading and isDecimal(char):
      return readNext(
        f, integerList, floatList, reading + char, True, mul
      )  # Check whether the char read was '.' or not; we can later use this information to push the item in the correct list.
    elif isNumeric(char):
      return readNext(f, integerList, floatList, reading + char, isFloat, mul)
    else:  # Valid seperator found for a valid input string, then push and recurse
      if reading:  # Check if input exists, then put into appropriate Integer/Float list
        return readNext(f, integerList + [mul * strToInt(reading)],
                        floatList) if not isFloat else readNext(
                          f, integerList, floatList + [mul * float(reading)])
      return readNext(f, integerList, floatList)


# %% [markdown]
# **For every unique element, assosciate a frequency:**

# %%
# Map each unique element to its frequency

# Filter duplicates - search list for a given element x, if x exists further in the list, deal with it later by currentList + f(x[1:]]); if it doesnt exist then [x] + currentList + f(x[1:])
inList = lambda x, l: x == l[0] or inList(x, l[1:]
                                          ) if l else False  #x[0] in x[1:]

listLength = lambda arr: reduce(lambda a, b: a + 1, [0] + arr)
filterDuplicates = lambda l: (lambda u, a: u(u, a))(
  (lambda f, x: x if listLength(x) <= 1 else
   (f(f, x[1:]) if inList(x[0], x[1:]) else ([x[0]] + f(f, x[1:])))), l
)  # Source: https://stackoverflow.com/questions/41522601/python-removing-duplicates-in-list-only-by-using-filter-and-lambda

# Search frequency - how many times m exists in arr
#GetFrequency = lambda arr, m: reduce(lambda a, b: a + 1 if b == m else a, [0] + arr)
getFreq = lambda u, v: list(
  map(lambda x: reduce(lambda a, b: a + 1 if b == x else a, [0] + v), u))

# %% [markdown]
#
# *   Merge Sort Big-O(nlogn)
# *  Custom Merge function
# TODO: Maybe improve efficiency by not calling freqFunc all the time (store in a parallel array?)
# %%


# Sort unique elements by their associated frequency:
def merge(left, right, freqFunc):  # sorted according to freq here?
  #print(freqFunc(temp))
  if not left:
    return right
  if not right:
    return left
  x = freqFunc([left[0]])
  y = freqFunc([right[0]])
  if x > y:
    temp = merge(left[1:], right, freqFunc)
    return [left[0]] + temp
  elif x == y:  # Handle edge case where equal frequences, then sort by the lower number instead.
    if left[0] < right[0]:
      temp = merge(left[1:], right, freqFunc)
      return [left[0]] + temp
    else:
      temp = merge(left, right[1:], freqFunc)
      return [right[0]] + temp
  temp = merge(left, right[1:], freqFunc)
  return [right[0]] + temp


def MergeSort(arr, freqFunc):
  size = listLength(arr)

  if size == 1:
    return arr

  m = size // 2
  left = MergeSort(arr[:m], freqFunc)
  right = MergeSort(arr[m:], freqFunc)
  return merge(left, right, freqFunc)


# %%
def printList(stream, elements, freq, count):
  if count == 0 or not elements:
    return

  output = str(elements[0]) + " " + str(freq[0]) + "\n"
  stream.write(output)
  new_freq = freq[1:]
  printList(stream, elements[1:], new_freq,
            count - 1 if new_freq and new_freq[0] != freq[0] else count)


# %%


def main():
  sys.setrecursionlimit(10000)  # just incase
  launch_argument = sys.argv[1]

  if launch_argument:
    #launch_argument = "k=3;input=tc5.txt;output=tc5out.txt"
    k, inputFrom, outputTo = getArguments(launch_argument)
    print(k, inputFrom, outputTo)
  else:
    print("Invalid input parameters")
    exit()
  iFile = open(inputFrom, "r")
  integers, reals = readNext(iFile)

  print("Ints:", integers)
  print("Reals:", reals)

  # Done with the file, now close it.
  iFile.close()

  uniqueIntegers = filterDuplicates(integers)
  #intFreq = getFreq(uniqueIntegers, integers)
  #print("Integers:", uniqueIntegers, "->", intFreq)

  uniqueReals = filterDuplicates(reals)
  #realFreq = getFreq(uniqueReals, reals)
  #print("Reals:", uniqueReals, "->", realFreq)

  sortedInts = MergeSort(uniqueIntegers, lambda x: getFreq(x, integers))
  sortedIntFreq = getFreq(sortedInts, integers)

  #print(sortedInts, sortedIntFreq)

  sortedReals = MergeSort(uniqueReals, lambda x: getFreq(x, reals))
  sortedRealFreq = getFreq(sortedReals, reals)

  #print(sortedReals, sortedRealFreq)

  # Print to file
  oFile = open(outputTo, "w")
  if sortedInts:
    oFile.write("integer:\n")
    printList(oFile, sortedInts, sortedIntFreq, k)
  if sortedReals:
    oFile.write("real:\n")
    printList(oFile, sortedReals, sortedRealFreq, k)
  oFile.close()
  return


if __name__ == '__main__':  # Run as script
  sys.exit(main())
