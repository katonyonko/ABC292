import io
import sys

_INPUT = """\
6
3 3
2 3
1 1
2 3
5 5
1 2
2 3
3 4
3 5
1 5
13 16
7 9
7 11
3 8
1 13
11 11
6 11
8 13
2 11
3 3
8 12
9 11
1 11
5 13
3 12
6 9
1 10
"""

sys.stdin = io.StringIO(_INPUT)
case_no=int(input())
for __ in range(case_no):
  import sys
  sys.setrecursionlimit(10**6)
  class UnionFind():
    def __init__(self, n):
      self.n = n
      self.parents = [-1] * n
    def find(self, x):
      if self.parents[x] < 0:
        return x
      else:
        self.parents[x] = self.find(self.parents[x])
        return self.parents[x]
    def union(self, x, y):
      x = self.find(x)
      y = self.find(y)
      if x == y:
        return
      if self.parents[x] > self.parents[y]:
        x, y = y, x
      self.parents[x] += self.parents[y]
      self.parents[y] = x
    def size(self, x):
      return -self.parents[self.find(x)]
    def same(self, x, y):
      return self.find(x) == self.find(y)
    def members(self, x):
      root = self.find(x)
      return [i for i in range(self.n) if self.find(i) == root]
    def roots(self):
      return [i for i, x in enumerate(self.parents) if x < 0]
    def group_count(self):
      return len(self.roots())
    def all_group_members(self):
      return {r: self.members(r) for r in self.roots()}
    def __str__(self):
      return '\n'.join('{}: {}'.format(r, self.members(r)) for r in self.roots())

  N,M=map(int,input().split())
  uf=UnionFind(N)
  amari=[0]*N
  for i in range(M):
    u,v=map(lambda x: int(x)-1, input().split())
    if uf.find(u)==uf.find(v): amari[uf.find(u)]+=1
    else: uf.union(u,v)
  roots=uf.roots()
  ans='Yes'
  for i in roots:
    if amari[i]!=1: ans='No'
  print(ans)