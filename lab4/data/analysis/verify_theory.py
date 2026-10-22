"""Exact rational KKT solutions and constraint-count checks for Lab4 D1/D2."""
import json
from pathlib import Path
import sympy as s

answers = []
for n in [1, 2, 3]:
    Q = s.Matrix(n, n, lambda i, j: s.Rational((i+1)*(j+1), i+j+1))
    for extra in ([False, True] if n > 1 else [False]):
        A, b = s.ones(1, n), s.Matrix([1])
        if extra:
            A = A.col_join(s.Matrix([[i+1 for i in range(n)]]))
            b = b.col_join(s.Matrix([-2]))
        K = (2*Q).row_join(A.T).col_join(A.row_join(s.zeros(A.rows)))
        v = (K.inv() * s.zeros(n, 1).col_join(b))[:n, 0]
        assert A*v == b
        t = s.symbols('t')
        poly = sum(v[i]*t**(i+1) for i in range(n))
        cost = (v.T*Q*v)[0]
        assert s.integrate(s.diff(poly, t)**2, (t, 0, 1)) == cost
        answers.append({'degree': n, 'end_velocity_minus2': extra,
                        'Q': str(Q), 'A': str(A), 'b': str(b),
                        'coefficients': [str(x) for x in v],
                        'polynomial': str(poly), 'cost': str(cost)})
for r in range(1, 8):
    for k in range(1, 9):
        assert 2*k + 2*(r-1) + 2*(r-1)*(k-1) == 2*r*k
        assert (r+1)*k+r-1 + (r-1)*(k-1) == 2*r*k
path = Path(__file__).resolve().parent / 'theory_verification.json'
path.write_text(json.dumps(answers, ensure_ascii=False, indent=2), encoding='utf-8')
print(path.read_text())
