import math 
from Surprisal import KL
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


def pssblchnks(coarse, coarsur, priors, chnks, opp_chnks):
	newchnks=[]
	for j in chnks:
		if priors[j-1]==None:
			pass
		elif coarsen(KL(expectation(j,opp_chnks),priors[j-1]))==coarsur:
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
	
	prior_A=1/2
	prior_B=1/2
	
	priors_A=[prior_A for i in range(1,1+n*(n+3)//2)]
	priors_B=[prior_B for i in range(1,1+n*(n+3)//2)]
	
	A_report=[]
	B_report=[]
	
	while (set(new_A)!=set(old_A) or set(new_B)!=set(old_B)):
		old_A=new_A
		old_B=new_B
			
		post_A=expectation(j_A, old_B)
		coarse_A=coarsen(post_A)
		sur_A=KL(post_A,prior_A)
		coarsur_A=coarsen(sur_A)
		prior_A=post_A
		A_report.append((coarse_A,coarsur_A))
		
		new_A=pssblchnks(coarse_A, coarsur_A, priors_A, old_A, old_B)
		priors_A=[expectation(j, old_B) if j in new_A else None for j in range(1,1+n*(n+3)//2)]
		
		post_B=expectation(j_B, old_A)
		coarse_B=coarsen(post_B)
		sur_B=KL(post_B,prior_B)
		coarsur_B=coarsen(sur_B)
		prior_B=post_B
		B_report.append((coarse_B,coarsur_B))

		new_B=pssblchnks(coarse_B, coarsur_B, priors_B, old_B, old_A)
		priors_B=[expectation(j, old_A) if j in new_B else None for j in range(1,1+n*(n+3)//2)]
		
	return ((A_report, B_report),(post_A,post_B))

#print(communicate(8,(8,2),(6,3)))
