import math
from Surprisal import KL
from Original import which_chunk, unionchnks, measure, posterior

def coarsen(s):
	if 0<=s<1/3:
		return "L"
	elif 1/3<=s<2/3:
		return "M"
	else:
		return "H"
		
#Given initial prior, surprisal, possible ppriors, event, info partition, other's
#info partition, and other's possible chunks
#Returns possible chunks consistent
#with reported surprisal
def pssblchnks(prior, coarsur, pssblpriors, event, part, chnks, opp_part, opp_chnks):
	new_chnks=[]
	for i in range(len(part)):
		if pssblpriors[i]==None:
			chunk_sur="Undefined"
		elif len(set(part[i]) & set(unionchnks(opp_part, opp_chnks)))!=0:
			chunk_sur=KL(posterior(prior, event, part[i], opp_part, opp_chnks),pssblpriors[i])
		else:
			chunk_sur="Undefined"
		if chunk_sur!="Undefined" and coarsen(chunk_sur)==coarsur:
			new_chnks.append(i)
			
	return list(set(new_chnks) & set(chnks))

#Given true state of world, initial prior, event, and
#both agents' information partitions
#Simulates communication process and returns
#list of reported posteriors for both agents
def communicate(world, prior, event, agent_A, agent_B):
	chunk_A=which_chunk(world,agent_A)
	chunk_B=which_chunk(world,agent_B)
	
	oldchnks_A=[]
	newchnks_A=list(range(len(agent_A)))
	
	oldchnks_B=[]
	newchnks_B=list(range(len(agent_B)))
	
	prior_A=measure(prior,event)
	prior_B=measure(prior,event)
	
	priors_A=[prior_A for i in range(len(agent_A))]
	priors_B=[prior_B for i in range(len(agent_B))]
	
	A_report=[]
	B_report=[]
	
	while (set(newchnks_A)!=set(oldchnks_A) or set(newchnks_B)!=set(oldchnks_B)):
		oldchnks_A=newchnks_A
		oldchnks_B=newchnks_B
			
		post_A=posterior(prior, event, chunk_A, agent_B, oldchnks_B)
		sur_A=KL(post_A,prior_A)
		prior_A=post_A
		coarsur_A=coarsen(sur_A)
		A_report.append(coarsur_A)
		
		newchnks_A=pssblchnks(prior, coarsur_A, priors_A, event, agent_A, oldchnks_A, agent_B, oldchnks_B)
		priors_A=[posterior(prior, event, agent_A[i], agent_B, oldchnks_B) if i in newchnks_A else None for i in range(len(agent_A))]

		post_B=posterior(prior, event, chunk_B, agent_A, oldchnks_A)
		sur_B=KL(post_B,prior_B)
		prior_B=post_B
		coarsur_B=coarsen(sur_B)
		B_report.append(coarsur_B)
		
		newchnks_B=pssblchnks(prior, coarsur_B, priors_B, event, agent_B, oldchnks_B, agent_A, oldchnks_A)
		priors_B=[posterior(prior, event, agent_B[i], agent_A, oldchnks_A) if i in newchnks_B else None for i in range(len(agent_B))]
		
	return ((A_report, B_report),(post_A,post_B))
	
	
#world=1
#prior=[1/9]*9
#event=[3,4]
#agent_A=[[1,2,3],[4,5,6],[7,8,9]]
#agent_B=[[1,2,3,4],[5,6,7,8],[9]]
	
#print(communicate(world,prior,event,agent_A,agent_B))
