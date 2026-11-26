"""Landscape Current poll: two answers, as in Figma 56:212822."""
import sys
p = sys.argv[1]; s = open(p).read()
a = 'var O = [["Arsenal", 41], ["Real Madrid", 17], ["Bayern Munich", 21], ["Barcelona", 21]]'
assert s.count(a) == 1
s = s.replace(a, 'var O = [["Bayern Munich", 56], ["Real Madrid", 44]]')
open(p, 'w').write(s); print("land-poll-two ok")
