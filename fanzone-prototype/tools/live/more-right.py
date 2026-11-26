"""Row menu button (...) pinned to the right edge of the row."""
import sys
p = sys.argv[1]; s = open(p).read()
a = '  .fp-item .fp-more:hover { background: var(--surface); color: var(--text); }\n'
assert s.count(a) == 1
s = s.replace(a, a + '  .fp-item .fp-more { margin-left: auto; }\n')
open(p, 'w').write(s); print("more-right ok")
