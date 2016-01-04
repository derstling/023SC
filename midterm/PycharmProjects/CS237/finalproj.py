import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import random
import collections
import heapq



stateVar = 0
globalClock = 0
futureEventsList = []
statistics = 0

# Returns exponential random variates
def nextExponential(lamb):
    return -(math.log(random.random()))/lamb

# WORKS!!
# def testNextExp(n, lamb):
#     x = []
#     for i in range(0,n):
#         x += [nextExponential(lamb)]
#     return sum(x)/n

while futureEventsList != []:
    E = ()

# ------------------------------------------------
# INITIALIZE SIMULATION
# ------------------------------------------------

arrivalRate = 100

# Create list of 10^6 tasks
tasks = []
for i in range(0,pow(10,6)):
    tasks += [(nextExponential(arrivalRate), None, None)]

# testlist = [99, 23, 24, 25, 44, 78]
#
# queue = collections.deque()
#
# for i in range(0, len(testlist)):
#     queue.append(testlist[i])
# for i in range(0, len(testlist)):
#     y = queue.popleft()
#     print(y)

# Global variable to store length of queue
queueLen = 0

# Server is a variable that points to currently processed task
# Once task starts, it runs  its entire service time at once
server = 0

# Events
# ( type_of_event, start_time_of_running_event, ptr_to_task_in_event )

# Future Events List
# A priority (min) queue implemented as a heap
# futureEventsList = []

# testlist = [(99, 'hello'), (23, 'whats'), (24,'good'), (25, 'in')]
# for i in range(0, len(testlist)):
#     heapq.heappush(futureEventsList, testlist[i])
# for i in range(0, len(futureEventsList)):
#     # y = queue.popleft()
#     print(heapq.heappop(futureEventsList))

# Return top of heap (smallest value)
def getMin(h):
    return heapq.heappop(h)

# Insert event e into future events list h
def insert(e, h):
    heapq.heappush(h, e)

## NOTE: HEAPQ WILL ORDER TUPLES CORRECTLY AS LONG AS COMPARISON VALUE
#           IS FIRST VALUE OF TUPLE!!!!!!!1


tasksInput = [[0,1,0],[2,1,0],[5,1,0]]


def simulation():
    # Initlization
    globalClock = 0
    state = 0

    arrivalRate = 100

    # Create list of 10^6 tasks
    tasks = []
    for i in range(0,pow(10,6)):
        tasks += [(nextExponential(arrivalRate), None, None)]
    # print(tasks)

    # Insert all arrival tasks into the future events heap
    # With appropriate arrival times and ptrs to corresponding task
    futureEventsList = []
