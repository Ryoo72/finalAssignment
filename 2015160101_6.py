#original auther : Ryoo Kwangrok_ kwangrok21@naver.com 2015160101 Dept. of Physics
#search.txt를 input 디렉토리 안밖으로 찾아내고 input디렉토리 유무를 확인하여 입력값을 읽어내며 입력 파일 개수에 제한이 없는 코드
#last update _ 2017.06.20

import os
#from functools import reduce

class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def is_empty(self):
        return self.items == []

class Node:
    def __init__(self, newval,newcol):
        self.val = newval
        self.left = None
        self.right = None
        self.color = newcol
        self.p = None

class RedBlackTree:
    def __init__(self):
        self.nil = Node(None,"BLACK")
        self.root = self.nil
#사용자정의변수
        self.noData = []
        self.insertAmount = 0
        self.deleteAmount = 0
        self.nodeAmount = 0
        self.bnodeAmount = 0
        self.Temp_bheight = 0
        self.max_bheight = 1
        self.bh = 0
        self.itertest = 1
        
    def successor(self,x):
        if x!= self.nil and x.right != self.nil :
            return self.minimum(x.right)
        y=x.p
        while y != self.nil and x == y.right:
            x=y
            y=y.p
        return y

    def predecessor(self,x):
        if x!= self.nil and x.left != self.nil:
            return self.maximum(x.left)
        y=x.p
        while y != self.nil and x==y.left:
            x=y
            y=y.p
        return y

    def RBinsert(self,tree,n):
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if n.val < x.val:
                x = x.left
            else:
                x = x.right
        n.p = y
        if y == self.nil:
            self.root = n
        elif n.val < y.val:
            y.left = n
        else:
            y.right = n
        n.left = self.nil
        n.right = self.nil
        n.color = "RED"
        self.insertFixup(self.root,n)

    def insertFixup(self,tree,n):
        while n.p.color == "RED":
            if n.p == n.p.p.left:
                y = n.p.p.right
                if y.color == "RED":
                    n.p.color = "BLACK"
                    y.color = "BLACK"
                    n.p.p.color = "RED"
                    n = n.p.p

                elif n == n.p.right:
                    n = n.p
                    self.leftRotate(tree,n)
                else:
                    n.p.color = "BLACK"
                    n.p.p.color = "RED"
                    self.rightRotate(tree,n.p.p)
            else:
                y = n.p.p.left
                if y.color == "RED":
                    n.p.color = "BLACK"
                    y.color = "BLACK"
                    n.p.p.color = "RED"
                    n = n.p.p
                elif n == n.p.left:
                    n = n.p
                    self.rightRotate(tree,n)
                else:
                    n.p.color = "BLACK"
                    n.p.p.color = "RED"
                    self.leftRotate(tree,n.p.p)
        self.root.color = "BLACK"

    def leftRotate(self,tree,x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.p = x
        y.p = x.p
        if x.p == self.nil:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y

    def rightRotate(self,tree,y):
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.p = y
        x.p = y.p
        if y.p == self.nil:
            self.root = x
        elif y == y.p.right:
            y.p.right = x
        else:
            y.p.left = x
        x.right = y
        y.p = x

    def print(self,tree,level):
        #print("fasdfsafsafsa",tree.val)
        if tree.right != self.nil:
            self.print(tree.right,level + 1)
        for i in range(level):
            print('   ', end='')
        print(tree.val,tree.color)
        if tree.left != self.nil:
            self.print(tree.left, level + 1)

    def RBprint(self,tree,level):
        if tree.right != self.nil:
            self.RBprint(tree.right,level + 1)
        for i in range(level):
            print('   ', end='')
        if tree.color == "RED":
            print("R")
        else:
            print("B")
        if tree.left != self.nil:
            self.RBprint(tree.left, level + 1)

    def RBtransplant(self,tree,u,v):
        if u.p == self.nil:
            self.root = v
            #에러 기록.
            #여기에서 self.root 대신 tree를 써서 어려운 에러가 났었음.
            #그 이유는 tree가 고쳐지는거지, tree.root가 고쳐지는게 아니라서
            #트랜스플랜트를 빠져나가니까 다시 원상복귀 되는 악랄한 오류가 남.
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p


    def RBdelete(self,tree,i):
        z = self.search(self.root,i)
        if z == self.root and z.left == self.nil and z.right == self.nil:
            self.root = self.nil
        if z == self.nil:
            self.noData.append(i)
        else:#original source
            self.deleteAmount+=1
            self.nodeAmount-=1
            y = z
            y_original_color = y.color
            if z.left == self.nil:
                x = z.right
                self.RBtransplant(tree,z,z.right)
            elif z.right == self.nil:
                x = z.left
                self.RBtransplant(tree,z,z.left)
            else:
                y = self.minimum(z.right)
                y_original_color = y.color
                x = y.right
                if y.p == z:
                    x.p = y
                else:
                    self.RBtransplant(tree,y,y.right)
                    y.right = z.right
                    y.right.p = y
                self.RBtransplant(tree,z,y)
                y.left = z.left
                y.left.p = y
                y.color = z.color
                if z.p == self.nil:
                    tree = y
            if y_original_color == "BLACK":
                self.RBdeleteFixup(tree,x)

    def minimum(self,x):
        while x.left != self.nil:
            x=x.left
        return x

    def maximum(self,x):
        while x.right != self.nil:
            x=x.right
        return x

    def RBdeleteFixup(self,tree,x):
        while x != self.root and x.color == "BLACK":
            if x == x.p.left:
                w = x.p.right
                if w.color == "RED":
                    w.color = "BLACK"
                    x.p.color = "RED"
                    self.leftRotate(tree,x.p)
                    w = x.p.right
                if w.left.color == "BLACK" and w.right.color == "BLACK":
                    w.color = "RED"
                    x = x.p
                else:
                    if w.right.color == "BLACK":
                        w.left.color = "BLACK"
                        w.color = "RED"
                        self.rightRotate(tree,w)
                        w = x.p.right
                    w.color = x.p.color
                    x.p.color = "BLACK"
                    w.right.color = "BLACK"
                    self.leftRotate(tree,x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.color == "RED":
                    w.color = "BLACK"
                    x.p.color = "RED"
                    self.rightRotate(tree,x.p)
                    w = x.p.left
                if w.right.color == "BLACK" and w.left.color == "BLACK":
                    w.color = "RED"
                    x = x.p
                else:
                    if w.left.color == "BLACK":
                        w.right.color = "BLACK"
                        w.color = "RED"
                        self.leftRotate(tree,w)
                        w = x.p.left
                    w.color = x.p.color
                    x.p.color = "BLACK"
                    w.left.color = "BLACK"
                    self.rightRotate(tree,x.p)
                    x = self.root
        x.color = "BLACK"

    def search(self,x,k):#x가 가변적인 노드, k가 찾으려는 노드의 값
        if x == self.nil:
            return self.nil
        elif k == x.val:
            return x
        if k < x.val:
            return self.search(x.left,k)
        else:
            return self.search(x.right,k)

    def searchThree(self,x,k):#x가 가변적인 노드, k가 찾으려는 노드의 값
        if k < x.val:
            if x.left == self.nil:
                return self.predecessor(x),self.nil,x
            elif x.left.val == k:
                return self.predecessor(x.left),x.left,self.successor(x.left)
            else:
                return self.searchThree(x.left,k)
        else:
            if x.right == self.nil:
                return x,self.nil,self.successor(x)
            elif x.right.val == k:
                return self.predecessor(x.right),x.right,self.successor(x.right)
            else:
                return self.searchThree(x.right,k)

    def Input(self,val):
        if val > 0:#insert
            self.nodeAmount+=1
            self.insertAmount+=1
            self.RBinsert(self.root, Node(val,"RED"))
        elif val < 0:#delete
            self.RBdelete(self.root, -1 * val)
        else:#case of 0 exit the program
            print("else?")
            pass

    def inorder(self,tree):

        if tree == self.nil:
            if tree.p != None:
                if tree.p.color == "BLACK":#흑인 부모일경우
                    self.Temp_bheight-=1
            return
        else:
            if tree.color == "BLACK":#bnodeAmount 세기
                self.bnodeAmount+=1
            #딸네로 갈거임
            if tree.left.color == "BLACK":#흑인 딸일경우
                self.Temp_bheight+=1
                if self.max_bheight < self.Temp_bheight:
                    self.max_bheight=self.Temp_bheight
            self.inorder(tree.left)#    let's go to 딸
            #딸네 갔다가 내 집으로 돌아옴

            #**********내집*************
            #print(tree.val, end=' ')#   Me
            #**************************

            #아들네로 갈거임
            if tree.right.color == "BLACK":#흑인 아들일경우
                self.Temp_bheight+=1
                if self.max_bheight < self.Temp_bheight:
                    self.max_bheight=self.Temp_bheight
            self.inorder(tree.right)#   let's go to 아들
            #아들네 갔다가 내 집으로 돌아옴

            #**********내집*************

            #**************************

    def printInorder(self,tree):
        if tree == self.nil:
            return
        else:
            self.printInorder(tree.left)
            if tree.color == "RED":
                print(tree.val,"R")
            else:
                print(tree.val,"B")
            self.printInorder(tree.right)

    def blackheight(self,tree):
        if tree == self.nil:
            print("bh = 1")
        else:
            bnode = tree
            while self.itertest == 1:
                if bnode.color == "BLACK":
                    self.bh+=1
                if bnode.left == self.nil:
                    print("bh =",self.bh)
                    self.itertest = 0
                else:
                    bnode = bnode.left


road = './input/'
kiminonamaewa = []

def search():
    doWeSearch = "False"
    searchLocation = "./search.txt"
    #input 파일이 있을 때는 글로 들어가서 찾을 것. 
    if os.path.isdir('./input'):
        filenames = os.listdir(road)
    else:
        filenames = os.listdir('./')
        
    #input폴더 안에 search가 있을 경우.    
    if os.path.exists(searchLocation):    
        doWeSearch = "True"
    elif os.path.exists('./input/search.txt'):
        searchLocation = './input/search.txt'
        doWeSearch = "True"    
    
    for filename in filenames:
        if filename[-4:]==".txt" and filename != "search.txt" and filename[:6] != "output":
            kiminonamaewa.append(filename)
    return kiminonamaewa,doWeSearch,searchLocation

def main():
    abcloop = 0
    
    kiminonamaewa,doWeSearch,searchLocation = search()
    
    print(doWeSearch,searchLocation)
    for abc in kiminonamaewa:
        if abc == kiminonamaewa[0]:
            if abcloop == 1:
                break
            abcloop += 1    
        rbt = RedBlackTree()
        
        if os.path.isdir('./input'):
            f = open(road+abc, 'r')
        else:
            f = open(abc, 'r')
            
        lines = f.readlines()
        for line in lines:
            number=int(line)
            if number != 0:
                rbt.Input(number)
            else:
                break
        f.close()

        rbt.inorder(rbt.root)

        print("filename =",abc)#filename =
        print("total =",rbt.nodeAmount)#total =
        print("insert =",rbt.insertAmount)#insert =
        print("deleted =",rbt.deleteAmount)#deleted =
        print("miss =",len(rbt.noData))#miss =
        print("nb =",rbt.bnodeAmount)#nb =
        rbt.blackheight(rbt.root)#bh =
        rbt.printInorder(rbt.root)#inorder traversal

        if doWeSearch == "True":#search 파일이 있으면 찾아라
            
            ff = open(searchLocation, 'r')
                
            outputf = open("output.txt", 'w')
            #입력마다 출력 이름 다르게 하기
            #outputf = open("outputOf"+abc+".txt", 'w') 
           
            lines = ff.readlines()
            for line in lines:
                number=int(line)
                if number != 0:
                    l = rbt.searchThree(rbt.root,number)
                    outes = ['NIL']*3

                    for i in range(3):
                        if l[i] != None:
                            outes[i] = str(l[i].val)

                    datas = outes[0]+" "+outes[1]+" "+outes[2]
                    #using lambda function
                    #datas = reduce(lambda x, y: x+" "+y,outes)
                    print(datas)    
                    outputf.write(datas+"\n")
                else:
                    break
            ff.close()
            outputf.close()
            print(" ")
            
if __name__ == '__main__':
    main()
