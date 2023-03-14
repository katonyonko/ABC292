import io
import sys

_INPUT = """\
6
5 6 7
5 1 9 3 8
4 9
2 10
1 0
3 0
3 30
5 100
1 100
"""

sys.stdin = io.StringIO(_INPUT)
case_no=int(input())
for __ in range(case_no):
    class lazy_segtree():
        def update(self,k):self.d[k]=self.op(self.d[2*k],self.d[2*k+1])
        def all_apply(self,k,f):
            self.d[k]=self.mapping(f,self.d[k])
            if (k<self.size):self.lz[k]=self.composition(f,self.lz[k])
        def push(self,k):
            self.all_apply(2*k,self.lz[k])
            self.all_apply(2*k+1,self.lz[k])
            self.lz[k]=self.identity
        def __init__(self,V,OP,E,MAPPING,COMPOSITION,ID):
            self.n=len(V)
            self.log=(self.n-1).bit_length()
            self.size=1<<self.log
            self.d=[E for i in range(2*self.size)]
            self.lz=[ID for i in range(self.size)]
            self.e=E
            self.op=OP
            self.mapping=MAPPING
            self.composition=COMPOSITION
            self.identity=ID
            for i in range(self.n):self.d[self.size+i]=V[i]
            for i in range(self.size-1,0,-1):self.update(i)
        def set(self,p,x):
            assert 0<=p and p<self.n
            p+=self.size
            for i in range(self.log,0,-1):self.push(p>>i)
            self.d[p]=x
            for i in range(1,self.log+1):self.update(p>>i)
        def get(self,p):
            assert 0<=p and p<self.n
            p+=self.size
            for i in range(self.log,0,-1):self.push(p>>i)
            return self.d[p]
        def prod(self,l,r):
            assert 0<=l and l<=r and r<=self.n
            if l==r:return self.e
            l+=self.size
            r+=self.size
            for i in range(self.log,0,-1):
                if (((l>>i)<<i)!=l):self.push(l>>i)
                if (((r>>i)<<i)!=r):self.push(r>>i)
            sml,smr=self.e,self.e
            while(l<r):
                if l&1:
                    sml=self.op(sml,self.d[l])
                    l+=1
                if r&1:
                    r-=1
                    smr=self.op(self.d[r],smr)
                l>>=1
                r>>=1
            return self.op(sml,smr)
        def all_prod(self):return self.d[1]
        def apply_point(self,p,f):
            assert 0<=p and p<self.n
            p+=self.size
            for i in range(self.log,0,-1):self.push(p>>i)
            self.d[p]=self.mapping(f,self.d[p])
            for i in range(1,self.log+1):self.update(p>>i)
        def apply(self,l,r,f):
            assert 0<=l and l<=r and r<=self.n
            if l==r:return
            l+=self.size
            r+=self.size
            for i in range(self.log,0,-1):
                if (((l>>i)<<i)!=l):self.push(l>>i)
                if (((r>>i)<<i)!=r):self.push((r-1)>>i)
            l2,r2=l,r
            while(l<r):
                if (l&1):
                    self.all_apply(l,f)
                    l+=1
                if (r&1):
                    r-=1
                    self.all_apply(r,f)
                l>>=1
                r>>=1
            l,r=l2,r2
            for i in range(1,self.log+1):
                if (((l>>i)<<i)!=l):self.update(l>>i)
                if (((r>>i)<<i)!=r):self.update((r-1)>>i)
        def max_right(self,l,g):
            assert 0<=l and l<=self.n
            assert g(self.e)
            if l==self.n:return self.n
            l+=self.size
            for i in range(self.log,0,-1):self.push(l>>i)
            sm=self.e
            while(1):
                while(l%2==0):l>>=1
                if not(g(self.op(sm,self.d[l]))):
                    while(l<self.size):
                        self.push(l)
                        l=(2*l)
                        if (g(self.op(sm,self.d[l]))):
                            sm=self.op(sm,self.d[l])
                            l+=1
                    return l-self.size
                sm=self.op(sm,self.d[l])
                l+=1
                if (l&-l)==l:break
            return self.n
        def min_left(self,r,g):
            assert (0<=r and r<=self.n)
            assert g(self.e)
            if r==0:return 0
            r+=self.size
            for i in range(self.log,0,-1):self.push((r-1)>>i)
            sm=self.e
            while(1):
                r-=1
                while(r>1 and (r%2)):r>>=1
                if not(g(self.op(self.d[r],sm))):
                    while(r<self.size):
                        self.push(r)
                        r=(2*r+1)
                        if g(self.op(self.d[r],sm)):
                            sm=self.op(self.d[r],sm)
                            r-=1
                    return r+1-self.size
                sm=self.op(self.d[r],sm)
                if (r&-r)==r:break
            return 0

    def read_input(flg):
        if flg==0: 
            N,B,Q=map(int,input().split())
            a=list(map(int,input().split()))
            query=[list(map(int,input().split())) for _ in range(Q)]
        else:
            from random import randint
            N,B,Q=randint(0,5*10**5),randint(0,10**9),1000
            a=[randint(0,10**9) for _ in range(N)]
            query=[[randint(1,N),randint(0,100)] for _ in range(Q)]
        return N,B,Q,a,query

    def solve(N,B,Q,a,query):
        res=[]
        ta=a.copy()
        b=[0]
        for i in range(N): b.append(b[-1]+ta[i]-B)
        def operate(x,y): return max(x,y)
        def mapping(x,y): return x+y
        def composition(x,y): return x+y
        lst=lazy_segtree(b[1:],operate,-10**20,mapping,composition,0)
        for _ in range(Q):
            c,x=query[_]
            c-=1
            lst.apply(c,N,x-ta[c])
            ta[c]=x
            if lst.all_prod()>=0:
                idx=lst.max_right(0,lambda x: True if x<0 else False)
                res.append(lst.get(idx)/(idx+1)+B)
            else: res.append(lst.get(N-1)/N+B)
        return res

    def naive(N,B,Q,a,query):
        res=[]
        for _ in range(Q):
            c,x=query[_]
            c-=1
            a[c]=x
            tmp=0
            cnt=0
            for i in range(N):
                tmp+=a[i]
                cnt+=1
                if tmp>=B*(i+1): break
            res.append(tmp/cnt)
        return res

    N,B,Q,a,query=read_input(0)
    print(*solve(N,B,Q,a,query),sep='\n')