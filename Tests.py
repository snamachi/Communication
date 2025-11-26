from Original import communicate as ogcomm
from OriginalCoarse import communicate as coarscomm
from Surprisal import communicate as surcomm 
from Aumann import communicate as acomm
from AumannCoarse import communicate as acoarscomm
from AumannSur import communicate as asurcomm
from Final import communicate as fincomm

import random
import numpy as np
import matplotlib.pyplot as plt
from math import floor
from mpmath import bell
from mpmath import e
from mpmath import factorial
from mpmath import power

#pdf for number of bins
def make_pdf(n):
	def pdf(k):
		numer = power(k, n)
		denom = factorial(k) * e * bell(n)
		return numer / denom
	return pdf

#cdf for number of bins
def make_cdf(pdf):
	def cdf(k):
		sum=0
		for j in range(k+1):
			sum+=pdf(j)
		return sum
	return cdf

#Given uniform sample and desired cdf
#Returns sample from cdf
def find_interval(u, cdf):
	k = 1
	while True:
			(left, right) = (cdf(k-1), cdf(k))
			if (left < u) & (u <= right):
				return k
			k += 1

#Simulates cdf
def simulate(cdf):
	u = random.random()
	return find_interval(u, cdf)
	
#Given list of worlds
#Draws uniformly from set of possible partitions
def partition(lst):
	#Draws number of bins k
	pdf=make_pdf(len(lst))
	cdf=make_cdf(pdf)
	k=simulate(cdf)
	partition=[[] for i in range(k)]
	
	for i in range(1,len(lst)+1):
		u=random.random()
		partition[floor(u*k)].append(i)
	
	return [x for x in partition if x!=[]]

##############################################################
# Histogram of iterations until agreement for OG and coarse OG
##############################################################

"""
counts_A=[]
counts_B=[]

n=10
event=list(range(3,3*n+1,3))

for i in range(200):
	print(i)
	agent_A=partition(list(range(1,3*n+1)))
	agent_B=partition(list(range(1,3*n+1)))
	world=1+floor(3*n*random.random())
	
	og_rep=ogcomm(world, [1/(3*n)]*(3*n), event, agent_A, agent_B)
	coars_rep=coarscomm(world, [1/(3*n)]*(3*n), event, agent_A, agent_B)
	
	counts_A.append(len(og_rep[0]))
	counts_B.append(len(coars_rep[0]))

label_A, count_A=np.unique(np.array(counts_A), return_counts=True)
plt.bar(label_A,count_A,align='center')
plt.gca().set_xticks(label_A)
plt.show()
plt.close()
label_B, count_B=np.unique(np.array(counts_B), return_counts=True)
plt.bar(label_B,count_B,align='center')
plt.gca().set_xticks(label_B)
plt.show()
plt.close()
"""


######################################################################
# Histogram of iterations until agreement for coarse Aumann and final
######################################################################


counts_A=[]
dists_A=[]
counts_B=[]
dists_B=[]

n=10
	
for i in range(25):
	
	print(i)

	p=random.random()
	tosses_A=floor(n*random.random())
	tosses_B=floor(n*random.random())

	heads_A=0
	for i in range(tosses_A):
		heads_A+=(random.random()<p)

	heads_B=0
	for i in range(tosses_B):
		heads_B+=(random.random()<p)

	a_rep=acoarscomm(n,(tosses_A,heads_A),(tosses_B,heads_B))
	afin_rep=fincomm(n,(tosses_A,heads_A),(tosses_B,heads_B))
	
	a_dist=abs(a_rep[1][0]-a_rep[1][1])
	afin_dist=abs(afin_rep[1][0]-afin_rep[1][1])
	dists_A.append(a_dist)
	dists_B.append(afin_dist)
		
	counts_A.append(len(a_rep[0][0])-1)
	counts_B.append(len(afin_rep[0][0])-1)

avg_A=sum(dists_A)/len(dists_A)
avg_B=sum(dists_B)/len(dists_B)
LEG=["Posterior (Average Distance="+str(avg_A)[0:4]+")","Posterior+Surprise (Average Distance="+str(avg_B)[0:4]+")"]
label_A, count_A=np.unique(np.array(counts_A), return_counts=True)
plt.bar(label_A,count_A,width=0.5)
plt.gca().set_xticks(label_A)
label_B, count_B=np.unique(np.array(counts_B), return_counts=True)
plt.bar(label_B+0.5,count_B,width=0.5)
plt.xlabel("Time to Convergence (Iterations)")
plt.ylabel("Frequency of Time (%)")
plt.legend(LEG,loc=1)
plt.show()
plt.close()

	
###############################################
# Frequency of agreement for surprisal protocol 
###############################################

"""
counts=[]
for n in range(1,21):
	event=list(range(3,3*n+1,3))
	count=0
	print(n)
	for i in range(200):
		print(i)
		agent_A=partition(list(range(1,3*n+1)))
		agent_B=partition(list(range(1,3*n+1)))
		world=1+floor(3*n*random.random())
		reports=surcomm(world, [1/(3*n)]*(3*n), event, agent_A, agent_B)
		if reports[1][0]==reports[1][1]:
			count+=1
	counts.append(count/200)

x = range(1,21)
y = counts
plt.plot(x, y)

plt.xlabel('# of worlds/3')
plt.ylabel('Frequency of agreement')
plt.grid(True)
plt.show()
plt.close()
"""

######################################################
# Frequency of agreement for Aumann surprisal protocol 
######################################################

"""
counts=[]
for n in range(1,21):
	count=0
	print(n)
	for i in range(200):
		print(i)

		p=random.random()
		tosses_A=floor(n*random.random())
		tosses_B=floor(n*random.random())

		heads_A=0
		for i in range(tosses_A):
			heads_A+=(random.random()<p)

		heads_B=0
		for i in range(tosses_B):
			heads_B+=(random.random()<p)

		reports=asurcomm(n,(tosses_A,heads_A),(tosses_B,heads_B))
		if reports[1][0]==reports[1][1]:
			count+=1

	counts.append(count/200)

x = range(1,21)
y = counts
plt.plot(x, y)

plt.xlabel('# of worlds/3')
plt.ylabel('Frequency of agreement')
plt.grid(True)
plt.show()
plt.close()
"""
