t,e=[],{}
c,NN_q0,VB_q0,qF_NN,NN_NN,VB_NN,IN_NN,NN_VB,IN_VB,DT_VB,DT_IN,NN_DT,NN,VB,IN,DT=0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

f1=open("viterbi_corpus.txt","r")
for line in f1:	
	words=line.strip().split(" ")
	x=[]	
	for w in words:
		c+=1
		if w in e.keys():
			e[w]+=1
		else:
			e[w]=1
		tag=w.split("/")
		x.append(tag[1])
	t.append(x)
	
for x in t:
	for y in range(len(x)-1):
		if y==0: 
			if x[y]=="NN":
				NN_q0+=1
			elif x[y]=="VB":
				VB_q0+=1
		if y==len(x)-2 and x[y+1]=="NN":
			qF_NN+=1
		if x[y]=="NN" and x[y+1]=="NN":
			NN_NN+=1
		elif x[y]=="NN" and x[y+1]=="VB":
			VB_NN+=1
		elif x[y]=="NN" and x[y+1]=="IN":
			IN_NN+=1
		elif x[y]=="VB" and x[y+1]=="NN":
			NN_VB+=1
		elif x[y]=="VB" and x[y+1]=="IN":
			IN_VB+=1
		elif x[y]=="VB" and x[y+1]=="DT":
			DT_VB+=1
		elif x[y]=="IN" and x[y+1]=="DT":
			DT_IN+=1
		elif x[y]=="DT" and x[y+1]=="NN":
			NN_DT+=1
		
for x in t:
	for y in range(len(x)):
		if x[y]=="NN":
			NN+=1
		elif x[y]=="VB":
			VB+=1
		elif x[y]=="IN":
			IN+=1
		elif x[y]=="DT":
			DT+=1

for a in e.keys():
	temp=[]
	temp=a.split("/")
	if temp[1]=="NN":
		e[a]/=NN
	elif temp[1]=="VB":
		e[a]/=VB
	elif temp[1]=="IN":
		e[a]/=IN
	elif temp[1]=="DT":
		e[a]/=DT

print("\nEmisson Probabilities :\n")
for x,y in e.items():
	print("P(%s) = %.3f"%(x,y))

N_N=NN_NN/NN
V_N=VB_NN/NN
I_N=IN_NN/NN
N_V=NN_VB/VB
I_V=IN_VB/VB
D_V=DT_VB/VB
D_I=DT_IN/IN
N_D=NN_DT/DT
N_q0=NN_q0/len(t)
V_q0=VB_q0/len(t)
qF_N=qF_NN/NN

print("\nTransmission Probabilities :\n")
print("P(N/N) = %.3f\nP(V/N) = %.3f\nP(I/N) = %.3f\nP(N/V) = %.3f"%(N_N,V_N,I_N,N_V))
print("P(I/V) = %.3f\nP(D/V) = %.3f\nP(D/I) = %.3f\nP(N/D) = %.3f"%(I_V,D_V,D_I,N_D))
print("P(N/q0) = %.3f\nP(V/q0) = %.3f\nP(qF/N) = %.3f"%(N_q0,V_q0,qF_N))

s="people eat all day"

vit_mat=[]
words=s.strip().split(" ")
for i in range(len(words)+1):
	x=[]
	vit_mat.append(x)
for w in range(len(words)):
	for k in e.keys():
		temp=[]
		temp=k.split("/")
		if temp[0]==words[w]:
			if w==0:
				if temp[1]=="NN":
					vit_mat[w].append(e[k]*N_q0)
					vit_mat[w].append(temp[1])
					f=0
				elif temp[1]=="VB":
					vit_mat[w].append(e[k]*V_q0)
					vit_mat[w].append(temp[1])
					f=1
			else:
				if temp[1]=="NN":
					if f==0:
						vit_mat[w].append(e[k]*N_N*vit_mat[w-1][0])
						vit_mat[w].append("NN")
					elif f==1:
						vit_mat[w].append(e[k]*N_V*vit_mat[w-1][0])
						vit_mat[w].append("VB")
					elif f==3:
						vit_mat[w].append(e[k]*N_D*vit_mat[w-1][0])
						vit_mat[w].append("DT")
					f=0
				elif temp[1]=="VB":
					if f==0:
						vit_mat[w].append(e[k]*V_N*vit_mat[w-1][0])
						vit_mat[w].append("NN")
					f=1
				elif temp[1]=="IN":
					if f==0:
						vit_mat[w].append(e[k]*I_N*vit_mat[w-1][0])
						vit_mat[w].append("NN")
					elif f==1:
						vit_mat[w].append(e[k]*I_V*vit_mat[w-1][0])
						vit_mat[w].append("VB")
					f=2
				elif temp[1]=="DT":
					if f==1:
						vit_mat[w].append(e[k]*D_V*vit_mat[w-1][0])
						vit_mat[w].append("VB")
					elif f==2:
						vit_mat[w].append(e[k]*D_I*vit_mat[w-1][0])
						vit_mat[w].append("IN")
					f=3

vit_mat[w+1].append(qF_N*vit_mat[w][0])
vit_mat[w+1].append("NN")

print("Viterbi Matrix : \n")
print("qF\t    NIL    \t    NIL    \t    NIL    \t    NIL    \t%0.3e %s"%(vit_mat[4][0],vit_mat[4][1]))
print("DT\t    NIL    \t    NIL    \t%0.3e %s\t    NIL    \t    NIL"%(vit_mat[2][0],vit_mat[2][1]))
print("IN\t    NIL    \t    NIL    \t    NIL    \t    NIL    \t    NIL")
print("VB\t    NIL    \t%0.3e %s\t    NIL    \t    NIL    \t    NIL"%(vit_mat[1][0],vit_mat[1][1]))
print("NN\t%0.3f %s\t    NIL    \t    NIL  \t%0.3e %s\t    NIL"%(vit_mat[0][0],vit_mat[0][1],vit_mat[3][0],vit_mat[3][1]))
print()
print("\t  "+words[0]+"\t    "+words[1]+"\t\t    "+words[2]+"\t\t    "+words[3]+"\t")

print('\nPOS tagging for each word of the sentence "'+s+'" :\n')

for w in range(len(words)):
	print(words[w]+" : "+vit_mat[w+1][1])