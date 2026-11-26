"""Current poll: same question and answers as the 80-20 poll (Champions League winner, 4 clubs)."""
import sys
p = sys.argv[1]; s = open(p).read()
rep = [
  ('>Vote for the official MOTM</div>', '>Who will win the Champions League this season?</div>'),
  ('<sc-for list="{{ cpOptions }}" as="o" hint-placeholder-count="3">', '<sc-for list="{{ cpOptions }}" as="o" hint-placeholder-count="4">'),
  ('    const pcts = s.pollPcts || [46, 31, 23];\n    const P = [["kimmich", "Joshua Kimmich"], ["olise", "Michael Olise"], ["kane", "Harry Kane"]];',
   '    const pcts = s.cpPcts || [41, 17, 21, 21];\n    const P = [["arsenal", "Arsenal"], ["realmadrid", "Real Madrid"], ["bayern", "Bayern Munich"], ["barcelona", "Barcelona"]];'),
  ('      cpH: collapsed ? 105 : 277, cpOpen: !collapsed,', '      cpH: collapsed ? 129 : 357, cpOpen: !collapsed,'),
  ("          pick: () => this.setState(st => (st.pollVote || st.cpFinished ? null : { pollVote: id })) };",
   "          pick: () => this.setState(st => {\n            if (st.pollVote || st.cpFinished) return null;\n            const p = (st.cpPcts || [41, 17, 21, 21]).slice();\n            const j = p.indexOf(Math.max(...p.filter((_, k) => k !== i)));\n            const amt = Math.min(6, p[j] - 5); p[i] += amt; p[j] -= amt;\n            return { pollVote: id, cpPcts: p };\n          }) };"),
  ("pollKind: this._pollKind || \"v2\", cpFinished: false, pollVote: null, v3Pcts: [41, 17, 21, 21],",
   "pollKind: this._pollKind || \"v2\", cpFinished: false, pollVote: null, v3Pcts: [41, 17, 21, 21], cpPcts: [41, 17, 21, 21],"),
]
for a, b in rep:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)
open(p, 'w').write(s); print("poll-current-q ok")
