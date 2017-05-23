
import time
import math
import numpy as np
import pandas as pd

##########################################################

def add2(num):
    return num+2

# Caps a value off if it exceeds Min and Max Values:
def Bound(Min,Value,Max):
    a = max(Min,Value)
    b = min(a,Max)
    return b

def times3(num):
    return num*3 

# Returns the analogous number between limits of 'A' and 'B'
# that correlates with 'n's position between 'a' and 'b'.
# Analogy:  [A < N < B] : [a < n < b]
# Procedure: having 'n', return 'N':
def MAP(A,B,a,b,n):
    DIF = B-A
    dif = b-a
    mar = (n-a)/float(dif)
    N = A+(DIF*mar)
    return N

def Pause(seconds):
    time.sleep(seconds)

########################################################## 
