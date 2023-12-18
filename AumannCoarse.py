import math 

from Aumann import tosses, heads, val, post, prob, expectation

def coarsen(p):
	if 0<=p<1/3:
		return "L"
	elif 1/3<=p<2/3:
		return "M"
	else:
		return "H"

#Given initial prior, posterior, event, info partition, possible chunks, other's
#info partition, and other's possible chunks
#Returns possible chunks consistent
#with reported posterior
def pssblchnks(coarse, chnks, opp_chnks):
	newchnks=[]
	for j in chnks:
		if coarsen(expectation(j,opp_chnks))==coarse:
			newchnks.append(j)		
	return newchnks

#Given true state of world, initial prior, event, and
#both agents' information partitions
#Simulates communication process and returns
#list of reported posteriors for both agents
def communicate(n, A, B):
	j_A=A[0]*(A[0]+1)/2+A[1]
	old_A=[]
	new_A=list(range(1,1+n*(n+3)//2))
	
	j_B=B[0]*(B[0]+1)/2+B[1]
	old_B=[]
	new_B=list(range(1,1+n*(n+3)//2))
	
	A_report=[]
	B_report=[]
	
	while (set(new_A)!=set(old_A) or set(new_B)!=set(old_B)):
		old_A=new_A
		old_B=new_B
			
		post_A=expectation(j_A, old_B)
		coarse_A=coarsen(post_A)
		A_report.append(coarse_A)
		
		new_A=pssblchnks(coarse_A, old_A, old_B)

		post_B=expectation(j_B, old_A)
		coarse_B=coarsen(post_B)
		B_report.append(coarse_B)
		
		new_B=pssblchnks(coarse_B, old_B, old_A)
		
	return ((A_report, B_report), (post_A,post_B))

#maximum number of tosses
#n=8
#A's number of tosses and heads
#tosses_A=8
#heads_A=2
#B's number of tosses and heads
#tosses_B=6
#heads_B=3

#j_A=tosses_A*(tosses_A+1)/2+heads_A
#j_B=tosses_B*(tosses_B+1)/2+heads_B

#print(communicate(n,j_A,j_B))
