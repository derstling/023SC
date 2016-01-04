import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import random

studentgpas = 'C:/Users/hwa/Downloads/StudentGPAData.csv'

stud = pd.read_csv(studentgpas)
popCount = stud['GPA'].count()

# Problem 1a
popMean = stud['GPA'].sum()/popCount

# Problem 1b
def xbar(n):
	sampleSet = []
	for i in range(0, n):
		selection = random.randint(0,popCount-1)
		sampleSet += [stud[selection:selection+1]['GPA'].values[0]]
	return sum(sampleSet)/n

def testSampleMean(M, n):
	sampleMeans = []
	for i in range(0, M):
		sampleMeans += [xbar(n)]
	return sum(sampleMeans)/M


