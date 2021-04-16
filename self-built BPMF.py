import treelib
from treelib import Node, Tree
import os, psutil
import random

def buildTree(T):
    if len(T)>1:
        for subTree in T:
            if len(subTree)>1:
                tree.create_node("", str(subTree),str(T))
            else:
                tree.create_node(str(subTree[0]), str(subTree[0]),str(T))
            buildTree(subTree)

def LCA(a,b):
    #print("a",a,"b",b)
    if tree.parent(a)==tree.parent(b):
        p=tree.parent(a).identifier
        parent=p
        #print("a parent:",parent)
        #print("b parent:",tree.parent(b).identifier)
        return tree.parent(b).identifier
    else:
        if tree.level(a)>tree.level(b):
            return LCA(tree.parent(a).identifier,b)
        elif tree.level(a)<tree.level(b):
            return LCA(a,tree.parent(b).identifier)
        else:
            return LCA(tree.parent(a).identifier,tree.parent(b).identifier)
        

def BPMF(if_p,r_type):
    r_pick=0
    print("")
    print("if-penalty:",if_p,"ratio type:",r_type)
    T=[]
    for n in nodes:
        T.append([n])
    
    M=[]

    row01=['-']
    for a in range(len(nodes)):
        row01.append(T[a].copy())
    M=[row01]

    for a in range(len(nodes)):
        row1=[T[a].copy()]
        #row2=[T[a]]
        for b in range(len(nodes)):
            row1.append([])
            #row2.append(0)
        M.append(row1)
        #e_score.append(row2)

    for trp in triplet:
        '''
        for r in M:
            print(r)
            '''
        i=nodes.index(trp[0])+1
        j=nodes.index(trp[1])+1
        if i < j:
            temp=i
            i=j
            j=temp
        #print(i,j)
        M[i][j].append(trp[2])  
    buildM=True
    while len(T)>1:
        e_score=[M[0].copy()]
        for a in range(1,len(M[0])):
            row=[M[0][a].copy()]
            for b in T:
                row.append(0)
            addRow=row.copy()
            e_score.append(row)

        if(detail=='1'):
            print(T)
            print('M')
            for r in M:
                print(r)
            print("")
        
        firstScore=True
        maxScore=0
        maxV1=[]
        maxV2=[]
        maxT=0
        for t1 in range(1,len(M[0])):
            for t2 in range(t1+1,len(M[0])):
                #print('t1:',t1,'t2:',t2)
                v1=e_score[0].index(M[0][t1])
                v2=e_score[0].index(M[0][t2])
                #print('v1:',v1,'v2:',v2)
                if v1 < v2:
                    temp=v1
                    v1=v2
                    v2=temp
                
                xInV=0
                for m in M[v1][v2]:
                    if (m in M[0][v1]) or (m in M[0][v2]):
                        xInV+=1
                e_score[v1][v2]=len(M[v1][v2])-xInV

                if e_score[v1][v2]>0 and (r_type==1 or if_p==1):
                    #print("r_type==1 or if_p==1")
                    #panelty needed
                    panelty=0
                    treeWithPenalty=[]
                    for m in M[v1][v2]:
                        for n in range(1,len(e_score[0])):
                            if m in e_score[0][n]:
                                v3=n
                                v3_content=m
                        #print('v3 =',v3,"=",M[v3][0])
                        #print('v3_content =',m)


                        #print("treeWithPenalty =",treeWithPenalty)
                        if v3 not in treeWithPenalty:
                            for content in M[v2][v3]:
                                for compare in M[0][v1]:
                                    if (compare == content) and (v3_content not in M[0][v1]): #(compare!= v3_content):   #and (compare not in M[v1][v2]):
                                        #print("v1 =",compare)
                                        #print("["+str(M[v2][0])+"]["+str(M[v3][0])+" =",M[v2][v3])
                                        panelty+=1
                                        treeWithPenalty.append(v3)
                                        #print("panelty =",panelty)
                            for content in M[v3][v2]:
                                for compare in M[0][v1]:
                                    if (compare == content) and (v3_content not in M[0][v1]): #(compare!= v3_content):
                                        #print("v1 =",compare)
                                        #print("["+str(M[v3][0])+"]["+str(M[v2][0])+" =",M[v3][v2])
                                        panelty+=1
                                        treeWithPenalty.append(v3)
                                        #print("panelty =",panelty)
                            for content in M[v1][v3]:
                                for compare in M[0][v2]:
                                #if dummy==1:
                                    #print("compare =",compare,"content =",content)
                                    if (compare == content) and (v3_content not in M[0][v2]): #(compare!= v3_content):
                                        #print("v2 =",compare)
                                        #print("["+str(M[v1][0])+"]["+str(M[v3][0])+" =",M[v1][v3])
                                        panelty+=1
                                        treeWithPenalty.append(v3)
                                        #print("panelty =",panelty)
                            for content in M[v3][v1]:
                                for compare in M[0][v2]:
                                    #print("compare =",compare,"content =",content)
                                    if (compare == content) and (v3_content not in M[0][v2]): #(compare!= v3_content):
                                        #print("v2 =",compare)
                                        #print("["+str(M[v3][0])+"]["+str(M[v1][0])+" =",M[v3][v1])
                                        panelty+=1
                                        treeWithPenalty.append(v3)
                                        #print("panelty =",panelty)

                            
                    #print("panelty =",panelty)
                    #print("")
                      
                    if r_type==0:   #if_p==1, r_type==0
                        #print("r_type==0")
                        e_score[v1][v2]-=panelty
                        
                    elif r_type==2:     #if_p==1, r_type==2
                        #print("r_type==2")
                        #e_score[v1][v2]=e_score[v1][v2]-panelty/total
                        #print("if_p==1, r_type==2")
                        new_score=(e_score[v1][v2]-panelty)/len(M[v1][v2])
                        #print("e_score["+M[0][v1][0]+"]["+M[0][v2][0]+"] = ("+str(e_score[v1][v2])+" - "+str(panelty)+")/"+str(len(M[v1][v2]))+" = "+str(new_score))
                        e_score[v1][v2]=new_score
                        
                        
                    else:   #r_type==1
                        #print("r_type==1")
                        if if_p==0:
                            #print("if_p==0")
                            e_score[v1][v2]=e_score[v1][v2]/(e_score[v1][v2]+panelty)
                        else:
                            #print("if_p==1")
                            #if_p==1
                            e_score[v1][v2]=(e_score[v1][v2]-panelty)/(e_score[v1][v2]+panelty)

                elif e_score[v1][v2]>0 and r_type==2:     #r_type!=1, #if_p!=1, r_type==2
                    #print("r_type==2")
                    #e_score[v1][v2]=e_score[v1][v2]/total
                    #print("r_type!=1, #if_p!=1, r_type==2")
                    e_score[v1][v2]=e_score[v1][v2]/len(M[v1][v2])



                if firstScore is True:
                    maxScore=e_score[v1][v2]
                    maxV1.append(v1)
                    maxV2.append(v2)
                    maxT=len(M[v1][v2])-xInV
                    firstScore=False
                    if(detail=='1'):
                        print("maxScore: e_score["+str(v1)+"]["+str(v2)+"] =",maxScore)
                elif e_score[v1][v2]>maxScore:
                    maxScore=e_score[v1][v2]
                    maxV1=[v1]
                    maxV2=[v2]
                    maxT=len(M[v1][v2])-xInV
                    if(detail=='1'):
                        print("maxScore: e_score["+str(v1)+"]["+str(v2)+"] =",maxScore)
                elif e_score[v1][v2]==maxScore:
                    if r_type!=0 or if_p==1:
                        if(detail=='1'):
                            print("v1:",v1)
                            print("v2:",v2)
                            print("maxV1:",maxV1)
                            print("maxV2:",maxV2)
                            print("len(M[v1][v2])-xInV =",len(M[v1][v2])-xInV)
                            print("maxT =",maxT)
                        
                        if (len(M[v1][v2])-xInV)>maxT:
                            maxV1=[v1]
                            maxV2=[v2]
                            maxT=len(M[v1][v2])-xInV
                        elif (len(M[v1][v2])-xInV)==maxT:
                            maxV1.append(v1)
                            maxV2.append(v2)
                    else:
                        maxV1.append(v1)
                        maxV2.append(v2)
                '''
                if(detail=='1'):
                    print(maxV1)
                    print(maxV2)
                    '''
                    

        pick_index=0
        if len(maxV1)>1:
            pick_index=random.randint(0,len(maxV1)-1)
            r_pick+=1

        pick_maxV1=maxV1[pick_index]
        pick_maxV2=maxV2[pick_index]

            
        if(detail=='1'):
            print('e_score')
            for r in e_score:
                print(r)
            print("e_score[",pick_maxV1,",",pick_maxV2,"]=",e_score[pick_maxV1][pick_maxV2])
            print(maxScore)
            print('')
        


        #merge trees with max e_score
        T[pick_maxV2-1]=[T[pick_maxV2-1]]
        T[pick_maxV2-1].append(T[pick_maxV1-1])
        T.pop(pick_maxV1-1)


        if buildM is True:
            #update M
            M[0][pick_maxV2]+=M[0][pick_maxV1]            
            M[pick_maxV2][0]+=M[0][pick_maxV1]

            for m_index in range(0,len(T)+2): #+2 because the tree pair in T are merged
                if m_index<pick_maxV2:
                     M[m_index].pop(pick_maxV1)
                else:
                    for f in range(1,m_index):
                        if m_index==pick_maxV2:
                            M[m_index][f]+=M[pick_maxV1][f]
                        elif f==pick_maxV2:
                            if m_index<pick_maxV1 and len(M[pick_maxV1][m_index])>0:
                                M[m_index][f]+=M[pick_maxV1][m_index]
                            elif m_index>=pick_maxV1 and len(M[m_index][pick_maxV1])>0:
                                M[m_index][f]+=M[m_index][pick_maxV1]
                            M[m_index].pop(pick_maxV1)
                    if len(M[m_index])>len(M[m_index-1]):
                        M[m_index].pop(len(M[m_index])-1)
                                
            M.pop(pick_maxV1)



    tree.create_node("", str(T[0]))  #create root with all nodes as node id
    buildTree(T[0])

    if(detail=='1'):
        print(T) 
        tree.show()

    #calculate approximate ratio
    satisfy=0

    #print(triplet)

    for trp in triplet:
        LCA_ij=LCA(trp[0],trp[1])
        #print("LCA_ij:",LCA_ij)
        LCA_ik=LCA(trp[0],trp[2])
        #print("LCA_ik:",LCA_ik)
        if tree.level(LCA_ij)>tree.level(LCA_ik):
            satisfy+=1
            #print(trp)

    print("number of triplet satified in opt =",opt)
    print("input triplet =",len(triplet))      
    print("satisfied triplet =",satisfy)
    fitPercent=satisfy/len(triplet)
    print("triplet fit percentage =",round(fitPercent,6))
    errorRatio=opt/satisfy
    print("error ratio =",round(opt/satisfy,6))
    print("random picked time =",r_pick)
    return satisfy,fitPercent,errorRatio,r_pick




group=input("testcase group: ")
no_of_set=int(input("number of triplet set: "))
detail=input("show detail?(0/1): ")
path=os.getcwd()

consis_rate=[]
satisfy=[0,0,0,0,0,0]
fitPercent=[0,0,0,0,0,0]
errorRatio=[0,0,0,0,0,0]
rand_pick=[0,0,0,0,0,0]
avgOpt=0

for setNo in range(no_of_set):
    filename=path+"/testcase_"+group+"/random_triplet_"+str(setNo)+".txt"
    f = open(filename, "r")
    #print(f.read())

    print("")
    data=f.read()
    #print("data=",data)

    '''
    data=input("input triplet list:\n")
    if data=="1":
        data="0[['3', '1', '4'], ['2', '4', '5'], ['4', '1', '0'], ['1', '0', '2'], ['0', '1', '4']]"
        print("data=",data)
    elif data=="2":
        data="5[['2', '0', '4'], ['2', '4', '5'], ['3', '2', '1'], ['0', '1', '4'], ['2', '4', '3'], ['5', '1', '0']]"
        print("data=",data)
    elif data=="3":
        data="0[['0', '1', '4'], ['3', '5', '2'], ['4', '0', '5'], ['3', '2', '0'], ['5', '2', '0'], ['4', '1', '0']]"
        print("data=",data)
        '''

    '''
    if_p=int(input("if-penalty:"))
    r_type=int(input("ratio type:"))
    '''

    #process = psutil.Process(os.getpid())

    nodes=set()
    #R=data[1:len(data)-2]
    R=data
    index=0
    triplet=[]
    t=[]
    integer=[]
    opt=-1
    for s in R:     #reading the inputted string as list of triplet
        if s != '[' and s != ']' and s != "'" and s != ',' and  s != ' ':
            integer.append(s)
        else:
            if len(integer)>0:
                content=''.join(integer)
                if opt==-1:
                    opt=int(content)
                    avgOpt+=opt
                else:
                    t.append(content)
                    nodes.add(str(content))
                    if len(t)==3:
                        triplet.append(t)
                        #print(t)
                        t=[]
                integer=[]

    nodes=list(nodes)
    nodes.sort()

    
    print("")
    print("Round",setNo+1)


    m=len(triplet)
    n=len(nodes)
    #print(triplet)
    print("number of triplet (m) =",m)
    #print(nodes)
    print("number of taxa (n) =",n)
    con=round(opt/m,6)
    print("consistent triplet rate =",con)
    consis_rate.append(con)
    
    
    tree = Tree()
    st,fp,er,rp=BPMF(0,0)
    satisfy[0]+=st
    fitPercent[0]+=fp
    errorRatio[0]+=er
    rand_pick[0]+=rp

    tree = Tree()
    st,fp,er,rp=BPMF(1,0)
    satisfy[1]+=st
    fitPercent[1]+=fp
    errorRatio[1]+=er
    rand_pick[1]+=rp

    
    tree = Tree()
    st,fp,er,rp=BPMF(0,1)
    satisfy[2]+=st
    fitPercent[2]+=fp
    errorRatio[2]+=er
    rand_pick[2]+=rp

    tree = Tree()
    st,fp,er,rp=BPMF(1,1)
    satisfy[3]+=st
    fitPercent[3]+=fp
    errorRatio[3]+=er
    rand_pick[3]+=rp
    

    tree = Tree()
    st,fp,er,rp=BPMF(0,2)
    satisfy[4]+=st
    fitPercent[4]+=fp
    errorRatio[4]+=er
    rand_pick[4]+=rp

    
    tree = Tree()
    st,fp,er,rp=BPMF(1,2)
    satisfy[5]+=st
    fitPercent[5]+=fp
    errorRatio[5]+=er
    rand_pick[5]+=rp
    


filename=path+"/testcase_"+group+"/result_random_pick_same_score.txt"
text_file = open(filename, "w")

print("")
print("")
print("***Average result of "+str(no_of_set)+" set of triplet***")
text_file.write("***Average result of "+str(no_of_set)+" set of triplet***\n\n")

print("")
print("number of triplet (m) =",m)
print("number of taxa (n) =",n)
print("consistent triplet rate of each set =",consis_rate)
print("average consistent triplet rate =",round((avgOpt/no_of_set)/m,6))
text_file.write("number of triplet (m) = "+str(m)+"\n")
text_file.write("number of taxa (n) ="+str(n)+"\n")
text_file.write("consistent triplet rate of each set ="+str(consis_rate)+"\n")
text_file.write("average consistent triplet rate ="+str(round((avgOpt/no_of_set)/m,6))+"\n\n")

print_method=[[0,0],[1,0],[0,1],[1,1],[0,2],[1,2]]
first_method=True
min_ratio=0
best_ratio_method=0
max_satisfy=0
best_satisfy_method=0

for method in range(6):
    
    ratio=round(errorRatio[method]/no_of_set,6)
    satisfy_trp=satisfy[method]/no_of_set
    if first_method:
        first_method=False
        min_ratio=ratio
        max_satisfy=satisfy_trp
    else:
        if ratio<min_ratio:
            min_ratio=ratio
            best_ratio_method=method
        if satisfy_trp>max_satisfy:
            max_satisfy=satisfy_trp
            best_satisfy_method=method

    print("")
    print("if-penalty:",print_method[method][0]," ratio type:",print_method[method][1])
    print("satisfied triplet =",satisfy_trp)
    print("triplet fit percentage =",round(fitPercent[method]/no_of_set,6))
    print("error ratio =",ratio)
    print("random picked time = "+str(rand_pick[method]/no_of_set))
    
    text_file.write("if-penalty: "+str(print_method[method][0])+" ratio type: "+str(print_method[method][1])+"\n")
    text_file.write("satisfied triplet = "+str(satisfy_trp)+"\n")
    text_file.write("triplet fit percentage = "+str(round(fitPercent[method]/no_of_set,6))+"\n")
    text_file.write("error ratio = "+str(ratio)+"\n")
    text_file.write("random picked time = "+str(rand_pick[method]/no_of_set)+"\n\n")

print("")
print("Method with smallest error ratio:")
print("if-penalty:",print_method[best_ratio_method][0]," ratio type:",print_method[best_ratio_method][1])
print("error ratio =",min_ratio)

text_file.write("Method with smallest error ratio:\n")
text_file.write("if-penalty: "+str(print_method[best_ratio_method][0])+" ratio type: "+str(print_method[best_ratio_method][1])+"\n")
text_file.write("error ratio = "+str(min_ratio)+"\n\n")

print("")
print("Method with largest number of satisfied triplet:")
print("if-penalty:",print_method[best_satisfy_method][0]," ratio type:",print_method[best_satisfy_method][1])
print("satisfied triplet =",max_satisfy)

text_file.write("Method with largest number of satisfied triplet:\n")
text_file.write("if-penalty: "+str(print_method[best_satisfy_method][0])+" ratio type: "+str(print_method[best_satisfy_method][1])+"\n")
text_file.write("satisfied triplet = "+str(max_satisfy)+"\n\n")

text_file.close()
