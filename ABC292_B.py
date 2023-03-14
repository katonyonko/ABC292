import io
import sys

_INPUT = """\
6
3 9
3 1
3 2
1 2
2 1
3 1
3 2
1 2
3 2
3 3
"""

sys.stdin = io.StringIO(_INPUT)
case_no=int(input())
for __ in range(case_no):
  N,Q=map(int,input().split())
  ans=[0]*N
  for i in range(Q):
    d,x=map(int,input().split())
    if d==1: ans[x-1]+=1
    elif d==2: ans[x-1]+=2
    else:
      if ans[x-1]<2: print('No')
      else: print('Yes')