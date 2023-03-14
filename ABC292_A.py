import io
import sys

_INPUT = """\
6
abc
a
abcdefghjiklnmoqprstvuwxyz
"""

sys.stdin = io.StringIO(_INPUT)
case_no=int(input())
for __ in range(case_no):
  print(input().upper())