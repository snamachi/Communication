import math
from Original import which_chunk, unionchnks, measure, posterior

#Given agent's posterior and prior
#Returns KL
def KL(posterior,prior):
	if prior==0 or prior==1:
		return 0
	
	elif posterior==0:
		return math.log(1/(1-prior))
		
	elif posterior==1:
		return math.log(1/prior)
	
	else:
		return posterior*math.log(posterior/prior)+(1-posterior)*math.log((1-posterior)/(1-prior))


#Given initial prior, surprisal, possible priors, event, info partition, other's
#info partition, and other's possible chunks
#Returns possible chunks consistent
#with reported surprisal
def pssblchnks(prior, sur, pssblpriors, event, part, chnks, opp_part, opp_chnks):
	new_chnks=[]
	for i in range(len(part)):
		if pssblpriors[i]==None:
			chunk_sur="Undefined"
		elif len(set(part[i]) & set(unionchnks(opp_part, opp_chnks)))!=0:
			chunk_sur=KL(posterior(prior, event, part[i], opp_part, opp_chnks),pssblpriors[i])
		else:
			chunk_sur="Undefined"
		if chunk_sur==sur:
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
		A_report.append(sur_A)
		
		newchnks_A=pssblchnks(prior, sur_A, priors_A, event, agent_A, oldchnks_A, agent_B, oldchnks_B)
		priors_A=[posterior(prior, event, agent_A[i], agent_B, oldchnks_B) if i in newchnks_A else None for i in range(len(agent_A))]

		post_B=posterior(prior, event, chunk_B, agent_A, oldchnks_A)
		sur_B=KL(post_B,prior_B)
		prior_B=post_B
		B_report.append(sur_B)
		
		newchnks_B=pssblchnks(prior, sur_B, priors_B, event, agent_B, oldchnks_B, agent_A, oldchnks_A)
		priors_B=[posterior(prior, event, agent_B[i], agent_A, oldchnks_A) if i in newchnks_B else None for i in range(len(agent_B))]
		
	return ((A_report, B_report),(post_A,post_B))
	
	

