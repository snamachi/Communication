import math 

def tosses(j):
	return math.floor(((8*j+1)**(0.5)-1)/2) 
	
def heads(j):
	n=tosses(j)
	return j-(n*(n+1)//2)
	
def val(heads,tosses):
	return (heads+1)/(tosses+2)
	
def post(j_opp,j_self):
	pH=val(heads(j_self),tosses(j_self))
	heds=heads(j_opp)
	toses=tosses(j_opp)
	return math.comb(toses,heds)*(pH**heds)*((1-pH)**(toses-heds))

#Given initial prior, event, chunk of agent, other's info partition,
#and list of other's possible chunks
#Returns of agent
def prob(j_self, j_opp, opp_chnks):
	num=0
	total=0
	for j in opp_chnks:
		total+=post(j,j_self)
		if j==j_opp:
			num=post(j_opp,j_self)
			
	return num/total
	
def expectation(j_self, opp_chnks):
	heds=0
	toses=0
	ex=0
	for j_opp in opp_chnks:
			heds=heads(j_self)+heads(j_opp)
			toses=tosses(j_self)+tosses(j_opp)
			ex+=val(heds,toses)*prob(j_self,j_opp,opp_chnks)
	return ex

#Given initial prior, posterior, event, info partition, possible chunks, other's
#info partition, and other's possible chunks
#Returns possible chunks consistent
#with reported posterior
def pssblchnks(post, chnks, opp_chnks):
	newchnks=[]
	for j in chnks:
		if expectation(j,opp_chnks)==post:
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
		A_report.append(post_A)
		
		new_A=pssblchnks(post_A, old_A, old_B)

		post_B=expectation(j_B, old_A)
		B_report.append(post_B)
		
		new_B=pssblchnks(post_B, old_B, old_A)
		
	return (A_report, B_report)

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
