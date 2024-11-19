from django.shortcuts import render
import numpy as np
import random
import copy
import time
import sys
import json
from django.http import HttpResponse

# Create your views here.

sys.setrecursionlimit(2000)
def sudoko_main_box():                  #Sudoku base structure
    a=np.array([[0]*9]*9)
    return(a) 
def sudoku_row(a,r):                    #elements of the particular row
    r1=[]
    for i in range(len(a[r[0]])):
        r1.append([r[0],i])
    return(r1)

def sudoku_column(a,c):                 #elements of the particular column
    b=[]
    for i in range (9):
        b.append([i,c[1]])
    return b

def cell_list(a):                       #locations of all the cell
    l=[]
    #print(a,'cell_list')
    for i in range(len(a)):
        for j in range(len(a[i])):
            l.append([i,j])
    return(l)

class box_def:                          #elements of that particular block
    def r(loc):
        rn=loc[0]
        if rn<3 and rn>=0:
            return [0,3]
        if rn<6 and rn>=3:
            return [3,6]
        if rn<9 and rn>=6:
            return [6,9]

    def c(loc):
        cn=loc[1]
        x=[]
        if cn<3 and cn>=0:
            bn=box_def.r(loc)
            for i in range(0,3):
                for j in range(bn[0],bn[1]):
                    x.append([j,i])
        if cn<6 and cn>=3:
            bn=box_def.r(loc)
            for i in range(3,6):
                for j in range(bn[0],bn[1]):
                    x.append([j,i])
        if cn<9 and cn>=6:
            bn=box_def.r(loc)
            for i in range(6,9):
                for j in range(bn[0],bn[1]):
                    x.append([j,i])
        return(x)
def rem_list(a,r,l):                        #removes all the locations that are blocked         
    for j in box_def.c(r):
        if j in l:
            l.remove(j)
    for j in sudoku_row(a,r):
        if j in l:
            l.remove(j)
    for j in sudoku_column(a,r):
        if j in l:
            l.remove(j)
    return(l)

def ran(l,i,a):                             # fills the values randomly
    r=random.choice(l)
    a[r[0]][r[1]]=i
    l=rem_list(a,r,l)
    return(l,a)

def man(l,i,a,C,a1,l1):                     #algorithm for filling the values
    C+=1
    if C>1999:
        #print(a)
        return a1
    try:
        for j in range(9):
            l,a=ran(l,i,a)
        #print(i)
        #print(a,"new")
        return(a)
    except (IndexError):
        l=copy.deepcopy(l1)
        a=copy.deepcopy(a1)
        #print(i,"hi")
        return(man(l,i,a,C,a1,l1))
            
def solution(start=time.time()):                             # returns the final output
    try:
        a=sudoko_main_box()
        for i in range(1,10):
            a1=copy.deepcopy(a)
            l=cell_list(a)
            #print(l)
            l1=copy.deepcopy(l)
            #print(len(l))
            for k in l:
                if a[k[0]][k[1]]!=0:
                    l1.remove(k)
            l=copy.deepcopy(l1)
            if len(l)%9!=0:
                print("ERROR")
            C=0
            #print(i)
            b=copy.deepcopy(man(l,i,a,C,a1,l1))
            #print(b)
            if np.array_equal(b,a1):
                return(solution())  
            a=copy.deepcopy(b)
        #print(a,'sol')
        return(a)
    except:
        return solution()


"""
    print(a)
    end=time.time()
    Time=end-start
    return(Time)
"""
start=time.time()
a1=copy.deepcopy(solution())

def dict_Creation(a,list_empty_cells,list_empty_cells1):#correct
    d=dict()
    d1=dict()
    l=cell_list(a)
    list_empty_cells1=[]
    for i in l:
        if a[i[0]][i[1]]==0:
            if i not in list_empty_cells1:
                list_empty_cells1.append(i)
    for i in range(1,10):
        l1=cell_list(a)                 #possible places where value of i could be added
        li=[]                           #places where the number is already filled
        for j in l1:#l change to l1
            if a[j[0]][j[1]]==i:
                li.append(j)
        if len(li)!=9:
            for j in li:
                l1=rem_list(a,j,l1)
            l2=copy.deepcopy(l1)
            for j in l1:
                if a[j[0]][j[1]]!=0:
                    l2.remove(j)
            l1=copy.deepcopy(l2)
            if len(li)+len(l2)==9:
                for j in l1:
                    a[j[0]][j[1]]=i
                    l2.remove(j)
                    #list_empty_cells.remove(j)
                l1=copy.deepcopy(l2)
            if np.count_nonzero(a == i)!=9:
                d[i]=l1
    for i in d:                          # this is to check if any other place mention in the notes dictionary are now filled
        l1=[]
        for j in d[i]:
            if a[j[0]][j[1]]==0:
                l1.append(j)
        d[i]=l1
    return d,a

''''''
class con2():                    #checks that if a number can only be placed at one location in a row or column or box
    def r(d,q,list_empty_cells1,list_empty_cells):
        #print("hey")
        for i in d:
            r=[]
            #print(d)
            #print(i)
            #print(d[i])
            for j in d[i]:
                r.append(j[0])
            for j in r:
                #print(j)
                if r.count(j)==1:
                    loc=d[i][r.index(j)]
                    #print(q)
                    q[loc[0]][loc[1]]=i
                    #print(q)
                    if loc in list_empty_cells1:
                        list_empty_cells1.remove(loc)
        d,q=dict_Creation(q,list_empty_cells,list_empty_cells1)
        if list_empty_cells1==None:
            return(q,[])
        else:
            return(q,list_empty_cells1)

    def box(d,z,list_empty_cells1):
        for i in d:
            box_dict=dict()
            box_list=[]
            wrong_loc=[]
            for j in d[i]:
                box_dict[tuple(j)]=box_def.c(j)
            for k,j in box_dict.items():
                if j not in box_list:
                    box_list.append(j)
                else:
                    wrong_loc.append(list(box_dict.keys())[list(box_dict.values()).index(j)])
                    wrong_loc.append(k)
            for j in box_dict.keys():
                if j not in wrong_loc:
                    z[j[0]][j[1]]=i
                    if j in list_empty_cells1:
                        list_empty_cells1.remove(j)
        if list_empty_cells1==None:
            return z,[]
        else:
            return z,list_empty_cells1

    def c(d,y,list_empty_cells1,list_empty_cells):        
        for i in d:
            c=[]
            for j in d[i]:
                c.append(j[1])
            for j in c:
                if c.count(j)==1:
                    loc=d[i][c.index(j)]
                    y[loc[0]][loc[1]]=i
                    if loc in list_empty_cells1:
                        list_empty_cells1.remove(loc)
        y,list_empty_cells1=con2.r(d,y,list_empty_cells1,list_empty_cells)
        if list_empty_cells1==None:
            return(y,[])
        else:
            y,list_empty_cells1=con2.box(d,y,list_empty_cells1)
            return(y,list_empty_cells1)
def solver(x,list_empty_cells,list_empty_cells1,a2,c):
    x=copy.deepcopy(x)
    a1=copy.deepcopy(x)#a1 sudoku to given to user
    d,x=dict_Creation(x,list_empty_cells,list_empty_cells1)
    while np.count_nonzero(x==0)!=0:
        a3=copy.deepcopy(x)#a3 check if no new changes are made
        d,x=dict_Creation(x,list_empty_cells,list_empty_cells1)
        #print("hi")
        for i in d:
            i1=copy.deepcopy(d[i])
            for j in d[i]:
                if j not in list_empty_cells:
                    i1.remove(j)
            d[i]=i1
        '''
        d1=dict()
        for i in d:
            d1[i]=len(d[i])
        '''
        l=cell_list(x)
        x,list_empty_cells1=con2.c(d,x,list_empty_cells1,list_empty_cells)
        if np.array_equal(a3,x):
            #print(a,'a')
            break
    #print(id(x),'x')
    if(np.array_equal(x,a2)):#a2 fully filled sudoku
        #print(a1,'a1')
        #print(True)
        return(True)
    else:
        #print(False)
        return False
        #a,list_empty_cells,list_empty_cells1,a2,c= Disappear(c)
        #solver(a,list_empty_cells,list_empty_cells1,a2,c)
''''''
def com_disappear(l,a,list_empty_cells):
    b=random.choice(l)
    if b in list_empty_cells:
        while b in list_empty_cells:
            b=random.choice(l)
    #print(a)
    a[b[0]][b[1]]=0
    #print(a)
    #a1=copy.deepcopy(a)
    list_empty_cells.append(b)
    return(a,list_empty_cells,b)
    
def Disappear(c):
    list_empty_cells=[]
    list_empty_cells1=[]
    a=copy.deepcopy(solution())
    a1=copy.deepcopy(a)
    a2=copy.deepcopy(a)
    #print(a,'disappear')
    l=cell_list(a)
    if c==0:
        #print("""          Menu            """)
        #print("""
        #      1.Easy 
        #      2.Medium
        #      3.Hard
        #      """)
        #c=int(input("Enter your choice "))
        c=1
    list_empty_cells=[]
    list_empty_cells1=[]
    if c==1:
        c=0
        i=0
        while i<21:
            #count+=1
            #print(count)
            #print(id(a),'A')
            #print(a,'A')
            a,list_empty_cells,b=com_disappear(l,a,list_empty_cells)
            #print(a,'a')
            #print(id(a),'a')
            while not(solver(a,list_empty_cells,list_empty_cells1,a2,c)):
                #print("hi")
                a[b[0]][b[1]]=a2[b[0]][b[1]]
                list_empty_cells.remove(b)
                a,list_empty_cells,b=com_disappear(l,a,list_empty_cells)
                
            
            i+=1
        return a,a1
    elif c==2:
        c=0
        i=0
        while i<40:
            a,list_empty_cells,b=com_disappear(l,a,list_empty_cells)
            while not(solver(a,list_empty_cells,list_empty_cells1,a2,c)):
                #print("hi")
                a[b[0]][b[1]]=a2[b[0]][b[1]]
                list_empty_cells.remove(b)
                a,list_empty_cells,b=com_disappear(l,a,list_empty_cells)
            i+=1
        return a,a1
    elif c==3:
        c=0
        i=0
        while i < 50:
            a,list_empty_cells,b=com_disappear(l,a,list_empty_cells)
            while not(solver(a,list_empty_cells,list_empty_cells1,a2,c)):
                #print("hi")
                a[b[0]][b[1]]=a2[b[0]][b[1]]
                list_empty_cells.remove(b)
                a,list_empty_cells,b=com_disappear(l,a,list_empty_cells)
            i+=1
        return a,a1
    else:
        print("Error:Invalid choice")
        c=0
        return Disappear(c)
def Easy(request):
    c=1
    dict_val,color,dict_val1_json=Sudoku_Creator(c)
    return render(request,"Sudoku.html",{"d":dict_val,"colour":color, "d1":dict_val1_json})

def Medium(request):
    c=2
    dict_val,color,dict_val1_json=Sudoku_Creator(c)
    return render(request,"Sudoku.html",{"d":dict_val,"colour":color, "d1":dict_val1_json})

def Hard(request):
    c=3
    dict_val,color,dict_val1_json=Sudoku_Creator(c)
    return render(request,"Sudoku.html",{"d":dict_val,"colour":color, "d1":dict_val1_json})


def Sudoku_Creator(c):
    a,a1=copy.deepcopy(Disappear(c))
    color=["a11","a12","a13","a21","a22","a23","a31","a32","a33","a17","a18","a19","a27","a28","a29","a37","a38","a39","a44","a45","a46","a54","a55","a56","a64","a65","a66","a71","a72","a73","a81","a82","a83","a91","a92","a93","a77","a78","a79","a87","a88","a89","a97","a98","a99"]
    #disign pater is managed using color list
    dict_val1={"a11":int(a1[0][0]),"a12":int(a1[0][1]),"a13":int(a1[0][2]),"a14":int(a1[0][3]),"a15":int(a1[0][4]),"a16":int(a1[0][5]),"a17":int(a1[0][6]),"a18":int(a1[0][7]),"a19":int(a1[0][8]),"a21":int(a1[1][0]),"a22":int(a1[1][1]),"a23":int(a1[1][2]),"a24":int(a1[1][3]),"a25":int(a1[1][4]),"a26":int(a1[1][5]),"a27":int(a1[1][6]),"a28":int(a1[1][7]),"a29":int(a1[1][8]),"a31":int(a1[2][0]),"a32":int(a1[2][1]),"a33":int(a1[2][2]),"a34":int(a1[2][3]),"a35":int(a1[2][4]),"a36":int(a1[2][5]),"a37":int(a1[2][6]),"a38":int(a1[2][7]),"a39":int(a1[2][8]),"a41":int(a1[3][0]),"a42":int(a1[3][1]),"a43":int(a1[3][2]),"a44":int(a1[3][3]),"a45":int(a1[3][4]),"a46":int(a1[3][5]),"a47":int(a1[3][6]),"a48":int(a1[3][7]),"a49":int(a1[3][8]),"a51":int(a1[4][0]),"a52":int(a1[4][1]),"a53":int(a1[4][2]),"a54":int(a1[4][3]),"a55":int(a1[4][4]),"a56":int(a1[4][5]),"a57":int(a1[4][6]),"a58":int(a1[4][7]),"a59":int(a1[4][8]),"a61":int(a1[5][0]),"a62":int(a1[5][1]),"a63":int(a1[5][2]),"a64":int(a1[5][3]),"a65":int(a1[5][4]),"a66":int(a1[5][5]),"a67":int(a1[5][6]),"a68":int(a1[5][7]),"a69":int(a1[5][8]),"a71":int(a1[6][0]),"a72":int(a1[6][1]),"a73":int(a1[6][2]),"a74":int(a1[6][3]),"a75":int(a1[6][4]),"a76":int(a1[6][5]),"a77":int(a1[6][6]),"a78":int(a1[6][7]),"a79":int(a1[6][8]),"a81":int(a1[7][0]),"a82":int(a1[7][1]),"a83":int(a1[7][2]),"a84":int(a1[7][3]),"a85":int(a1[7][4]),"a86":int(a1[7][5]),"a87":int(a1[7][6]),"a88":int(a1[7][7]),"a89":int(a1[7][8]),"a91":int(a1[8][0]),"a92":int(a1[8][1]),"a93":int(a1[8][2]),"a94":int(a1[8][3]),"a95":int(a1[8][4]),"a96":int(a1[8][5]),"a97":int(a1[8][6]),"a98":int(a1[8][7]),"a99":int(a1[8][8])}
    dict_val= {"a11":a[0][0],"a12":a[0][1],"a13":a[0][2],"a14":a[0][3],"a15":a[0][4],"a16":a[0][5],"a17":a[0][6],"a18":a[0][7],"a19":a[0][8],"a21":a[1][0],"a22":a[1][1],"a23":a[1][2],"a24":a[1][3],"a25":a[1][4],"a26":a[1][5],"a27":a[1][6],"a28":a[1][7],"a29":a[1][8],"a31":a[2][0],"a32":a[2][1],"a33":a[2][2],"a34":a[2][3],"a35":a[2][4],"a36":a[2][5],"a37":a[2][6],"a38":a[2][7],"a39":a[2][8],"a41":a[3][0],"a42":a[3][1],"a43":a[3][2],"a44":a[3][3],"a45":a[3][4],"a46":a[3][5],"a47":a[3][6],"a48":a[3][7],"a49":a[3][8],"a51":a[4][0],"a52":a[4][1],"a53":a[4][2],"a54":a[4][3],"a55":a[4][4],"a56":a[4][5],"a57":a[4][6],"a58":a[4][7],"a59":a[4][8],"a61":a[5][0],"a62":a[5][1],"a63":a[5][2],"a64":a[5][3],"a65":a[5][4],"a66":a[5][5],"a67":a[5][6],"a68":a[5][7],"a69":a[5][8],"a71":a[6][0],"a72":a[6][1],"a73":a[6][2],"a74":a[6][3],"a75":a[6][4],"a76":a[6][5],"a77":a[6][6],"a78":a[6][7],"a79":a[6][8],"a81":a[7][0],"a82":a[7][1],"a83":a[7][2],"a84":a[7][3],"a85":a[7][4],"a86":a[7][5],"a87":a[7][6],"a88":a[7][7],"a89":a[7][8],"a91":a[8][0],"a92":a[8][1],"a93":a[8][2],"a94":a[8][3],"a95":a[8][4],"a96":a[8][5],"a97":a[8][6],"a98":a[8][7],"a99":a[8][8]}  
    dict_val1_json = json.dumps(dict_val1)
    return (dict_val,color,dict_val1_json)






#Efficiency test
s=0
l=[]
for x in range(0,1000):
    start=time.time()
    l.append(solution(start))
for y in l:
    s+=y
print(s/1000)


