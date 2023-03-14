import io
import sys

_INPUT = """\
6
4 3
2 4
3 1
4 3
292 0
5 8
1 2
2 1
1 3
3 1
1 4
4 1
1 5
5 1
3 3
1 2
2 3
3 1
"""

sys.stdin = io.StringIO(_INPUT)
case_no=int(input())
for __ in range(case_no):
  def dfs(G,r=0):
    used=[False]*len(G)
    parent=[-1]*len(G)
    st=[]
    st.append(r)
    while st:
      x=st.pop()
      if used[x]==True:
        continue
      used[x]=True
      for v in G[x]:
        if v==parent[x]:
          continue
        parent[v]=x
        st.append(v)
    return parent

  N,M=map(int,input().split())
  G=[set() for _ in range(N)]
  ans=0
  for i in range(M):
    u,v=map(lambda x: int(x)-1, input().split())
    G[u].add(v)
  for i in range(N):
    p=dfs(G,i)
    for j in range(N):
      if i!=j and p[j]!=-1 and j not in G[i]:
        ans+=1
  print(ans)