import io
import sys

_INPUT = """\
6
1 1
10 11
"""

sys.stdin = io.StringIO(_INPUT)
case_no=int(input())
for __ in range(case_no):
  A,B=map(int,input().split())
  if A>B: A,B=B,A
  if B>A*2/(3**.5): print(A*2/(3**.5))
  else:
    l,r=0,2000
    for i in range(200):
      mid=(l+r)/2
      if mid<B: l=mid
      else:
        x,y=B-(mid**2-A**2)**.5,A-(mid**2-B**2)**.5
        if x<0 or y<0 or (x**2+y**2)**.5<mid: r=mid
        else: l=mid
    print(l)