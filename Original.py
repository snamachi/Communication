#Given a world and an info partition
#Returns chunk the world is contained in
def which_chunk(world, part):
	for chunk in part:
		if world in chunk:
			return chunk

#Given info partition and list of chunk indices
#Returns union of chunks corresponding to indices
def unionchnks(part,chnks):
	union=[]
	for i in chnks:
		union+=part[i]
	return union

#Given initial prior and possible worlds
#Returns measures measure of possible worlds
def measure(prior,wrlds):
	measure=0
	for wrld in wrlds:
		measure+=prior[wrld-1]
	return measure

#Given initial prior, event, chunk of agent, other's info partition,
#and list of other's possible chunks
#Returns posterior of agent
def posterior(prior, event, chunk, opp_part, opp_chnks):
	post=measure(prior,set(event) & (set(chunk) & set(unionchnks(opp_part, opp_chnks))))/measure(prior,set(chunk) & set(unionchnks(opp_part, opp_chnks)))
	return post

#Given initial prior, posterior, event, info partition, possible chunks, other's
#info partition, and other's possible chunks
#Returns possible chunks consistent
#with reported posterior
def pssblchnks(prior, post, event, part, chnks, opp_part, opp_chnks):
	newchnks=[]
	for i in range(len(part)):
		if len(set(part[i]) & set(unionchnks(opp_part, opp_chnks)))!=0:
			chunk_post=posterior(prior, event, part[i], opp_part, opp_chnks)
		else:
			chunk_post="Undefined"
		if chunk_post==post:
			newchnks.append(i)
			
	return list(set(newchnks) & set(chnks))

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
	
	A_report=[]
	B_report=[]
	
	while (set(newchnks_A)!=set(oldchnks_A) or set(newchnks_B)!=set(oldchnks_B)):
		oldchnks_A=newchnks_A
		oldchnks_B=newchnks_B
			
		post_A=posterior(prior, event, chunk_A, agent_B, oldchnks_B)
		A_report.append(post_A)
		
		newchnks_A=pssblchnks(prior, post_A, event, agent_A, oldchnks_A, agent_B, oldchnks_B)

		post_B=posterior(prior, event, chunk_B, agent_A, oldchnks_A)
		B_report.append(post_B)
		
		newchnks_B=pssblchnks(prior, post_B, event, agent_B, oldchnks_B, agent_A, oldchnks_A)
		
	return (A_report, B_report)

#world=1
#prior=[1/9]*9
#event=[3,4]
#agent_A=[[1,2,3],[4,5,6],[7,8,9]]
#agent_B=[[1,2,3,4],[5,6,7,8],[9]]
	
#print(communicate(world,prior,event,agent_A,agent_B))

