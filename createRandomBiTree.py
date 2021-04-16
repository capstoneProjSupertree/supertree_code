import treelib
from treelib import Node, Tree
import random
import math
import os


def createTree(setNo,n,m,c):
    tree=Tree()
    tree.create_node("", "root")
    node=[]
    for i in range(n):
        node.append(str(i))
    a=random.randint(1,n-1)
    b=a
    while a==b:
        b=random.randint(1,n-1)
    #print(a)
    #print(b)
    tree.create_node(str(a), str(a), parent="root")
    tree.create_node(str(b), str(b), parent="root")
    node.pop(a)
    if a<b:
        node.pop(b-1)
    else:
        node.pop(b)
    branch=["root"]



    for minSet in range(n-2):    
        #print(node)
        #print(branch)
        new=random.randint(0,len(node)-1)
        #print(node[new])
        
        if len(branch)>1:
            upper=branch[random.randint(0,len(branch)-1)]
        else:
            upper="root"
        #print(upper)
            
        children=tree.children(upper)
        if len(children)>1:
            lower=children[random.randint(0,len(children)-1)].identifier
        else:
            lower=children[0].identifier
        #print(lower)
        #tree.create_node("test", "test", parent=lower)

        bName='B'+str(len(branch))
        #tree.create_node(bName, bName, parent=upper)
        tree.create_node('', bName, parent=upper)
        branch.append(bName)

        tree.move_node(lower, bName)
        tree.create_node(node[new], node[new], parent=bName)
        node.pop(new)

    if detail=="1":
        tree.show()


    #********generate min set of triplet********
    triplet=[]
    tripletIndex=[]
    leafAmount=[]

    for b in branch:
        if b=="root":
            continue

        leafIndex=[]
        leaf=[]
        bChild=tree.children(b)
        #print(bChild)
        
        if 'B' in bChild[0].identifier:
            lLeaf=tree.leaves(bChild[0].identifier)
            #print(b,lLeaf,'\n')
            leaf.append(len(lLeaf))
            i_index=random.randint(0,len(lLeaf)-1)
            i=lLeaf[i_index].identifier
        else:
            i=bChild[0].identifier
            leaf.append(1)
        
        if 'B' in bChild[1].identifier:
            rLeaf=tree.leaves(bChild[1].identifier)
            #print(b,rLeaf,'\n')
            leaf.append(len(rLeaf))
            j_index=random.randint(0,len(rLeaf)-1)
            j=rLeaf[j_index].identifier
        else:
            j=bChild[1].identifier
            leaf.append(1)
        
        k_list=tree.children(tree.parent(b).identifier)
        for sib in k_list:
            if sib.identifier!=b:
                if 'B' in sib.identifier:
                    sib_leaf=tree.leaves(sib.identifier)
                    #print(b,sib_leaf,'\n')
                    leaf.append(len(sib_leaf))
                    k_index=random.randint(0,len(sib_leaf)-1)
                    k=sib_leaf[k_index].identifier
                else:
                    k=sib.identifier
                    leaf.append(1)
                    
        triplet.append([i,j,k])
        leafAmount.append(leaf)

    minTriplet=n-2

    if detail==1:
        print("minimal triplet set:")
        print(triplet)
        print("length =",len(triplet))
        print()

        
	
    #********generate redundant triplet********
    while len(triplet) < round(m*(c/100)):
        b_index=random.randint(1,len(branch)-1)        

        bChild=tree.children(branch[b_index])
        if leafAmount[b_index-1][0] > 1:
            lLeaf=tree.leaves(bChild[0].identifier)
            i_index=random.randint(0,len(lLeaf)-1)
            i=lLeaf[i_index].identifier
            #print('i_index=',i_index)
            #print(lLeaf)
        else:
            i=triplet[b_index-1][0]
            
        if leafAmount[b_index-1][1] > 1:
            rLeaf=tree.leaves(bChild[1].identifier)
            r_index=random.randint(0,len(rLeaf)-1)
            j=rLeaf[r_index].identifier
            #print('r_index=',r_index)
            #print(rLeaf)        
        else:
            j=triplet[b_index-1][1]

        if leafAmount[b_index-1][2] > 1:
            k_list=tree.children(tree.parent(branch[b_index]).identifier)
            for sib in k_list:
                if sib.identifier!=branch[b_index]:
                    sib_leaf=tree.leaves(sib.identifier)
                    k_index=random.randint(0,len(sib_leaf)-1)
                    k=sib_leaf[k_index].identifier
                    #print(sib_leaf)
                    #print('k_index=',k_index)
        else:
            k=triplet[b_index-1][2]
            leafIndex.append(-1)

        #triplet.append([b_index,i,j,k])
        triplet.append([i,j,k])
        #print("len(triplet)",len(triplet),"round(m*(1-(c/100)))",round(m*(1-(c/100))))

    if detail==1:
        print("triplet set R with no error:")
        print(triplet)
        print("length =",len(triplet))
        print()

	
    #********generate error triplet********
    error_set=[]
    for no_of_error in range(round(m*(1-(c/100)))):
        swap_tri=random.randint(0,len(triplet)-1)
        incon_tri=triplet[swap_tri].copy()
        s_index=random.randint(0,1)
        temp=incon_tri[s_index]
        incon_tri[s_index]=incon_tri[2]
        incon_tri[2]=temp
        error_set.append(incon_tri)
        
        if len(triplet)+len(error_set) > m:
            pop_tri_index=random.randint(0,len(triplet)-1)
            triplet.pop(pop_tri_index)
            
    opt=len(triplet)
    triplet=triplet+error_set

    if detail==1:
        print("error triplet set:")
        print(error_set)
        print("triplet set R with error:")
        print(triplet)
        print("length =",len(triplet))
        print()

        
            
    #********mix the order of triplet set********
    ranOrderTriplet=[]
    while len(triplet) > 0:
        pop_index=random.randint(0,len(triplet)-1)
        ranOrderTriplet.append(triplet.pop(pop_index))

    

    filename=path+"/testcase_"+group+"/random_triplet_"+str(setNo)+".txt"
    text_file = open(filename, "w")
    text_file.write(str(opt))
    text_file.write(str(ranOrderTriplet))
    text_file.close()

    filename=path+"/testcase_"+group+"_TMC/random_triplet_TMC_"+str(setNo)+".dat"
    text_file = open(filename, "w")
    for t in ranOrderTriplet:
        text_file.write(t[0])
        text_file.write(",")
        text_file.write(t[1])
        text_file.write("|")
        text_file.write(t[2])
        text_file.write(" ")
    text_file.close()

    return opt



n=int(input("n:"))
m=int(input("m:"))
c=-2
while c < -1 or c <50:
    c=int(input("c%(50 to 100, -1 for random):"))
no_of_set=int(input("number of triplet set:"))
group=input("name of test case group:")
detail=input("show detail?(0/1):")

path=os.getcwd()
try:
    os.mkdir(path+"/testcase_"+group)
except OSError:
    a=0
try:
    os.mkdir(path+"/testcase_"+group+"_TMC")
except OSError:
    a=0

ratio=[]
optimal=[]
for setNo in range(no_of_set):
    if c == -1:
        ratio.append(random.randint(50,100))
    else:
        ratio.append(c)
    optimal.append(createTree(setNo,n,m,ratio[setNo]))
    
if c == -1:
    print("inconsistent ratio c% =",ratio)

filename=path+"/testcase_"+group+"_TMC/optimal.txt"
text_file = open(filename, "w")
for opt in optimal:
    text_file.write(str(opt)+" ")
text_file.close()
