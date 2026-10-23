# Deliverable 1: Single-Segment Optimization

Boyu Huang, 24020036026; Group 8

## 1 Problem and notation

Minimize J = integral from 0 to 1 of [P'(t)]² dt, subject to P(0)=0 and P(1)=1. Time and displacement are fixed. Squaring the speed penalizes high-speed peaks. This cost is not a direct measure of electrical energy.

Write P(t)=p1*t+p2*t²+...+pn*t^n. P(0)=0 removes the constant term. With coefficients ordered as p=[p1,...,pn]^T, the quadratic program is:

```text
minimize p^T Q p, subject to A p = b
Q_ij = i*j/(i+j-1), i,j = 1,...,n
```

The expression for Q follows by expanding P'(t)² and integrating each power of t.

## 2 Linear polynomial: Question 1

P(t)=p1*t and P(1)=1 give p1=1. Thus P(t)=t and J=1.

## 3 Quadratic polynomial: Question 2

```text
p = [p1,p2]^T
Q = [[1,1],[1,4/3]], A = [1,1], b = 1
J = p1² + 2*p1*p2 + (4/3)*p2²
```

The constraint gives p1=1-p2. Substitution gives J=1+p2²/3. The minimum is at p2=0: p=[1,0]^T, P(t)=t, J=1.

## 4 Cubic polynomial: Question 3

```text
p = [p1,p2,p3]^T
Q = [[1,1,1],[1,4/3,3/2],[1,3/2,9/5]]
A = [1,1,1], b = 1
```

For L=p^T Qp+lambda^T(Ap-b), stationarity and feasibility give the Karush-Kuhn-Tucker equations:

```text
[2Q  A^T] [p     ] = [0]
[A   0  ] [lambda]   [b]
```

The solution is p=[1,0,0]^T and lambda=-2. Direct substitution gives Ap=1 and 2Qp+A^T*lambda=0. Again P(t)=t and J=1.

---PAGE---

## 5 Extra terminal velocity: Question 4

Now also require P'(1)=-2. The trajectory must reach position 1 while moving in the negative direction. P(t)=t is no longer feasible.

Table 1. Exact solutions with the extra constraint

| **Quantity** | **Quadratic** | **Cubic** |
| --- | --- | --- |
| A | [[1,1],[1,2]] | [[1,1,1],[1,2,3]] |
| b | [1,-2]^T | [1,-2]^T |
| Optimal p | [4,-3]^T | [1/4,9/2,-15/4]^T |
| P(t) | 4t-3t² | t/4+9t²/2-15t³/4 |
| J | 4 | 17/8 = 2.125 |

For the quadratic, p1+p2=1 and p1+2p2=-2 give p1=4 and p2=-3. Integrating (4-6t)² gives J=4.

For the cubic, set p3=c. The constraints give p2=-3-2c and p1=4+c. Substitution into the cost gives:

```text
J(c) = 4+c+(2/15)*c²
J'(c) = 1+(4/15)*c = 0  =>  c = -15/4
J''(c) = 4/15 > 0
```

Therefore p=[1/4,9/2,-15/4]^T. Checking the endpoints gives P(1)=1/4+9/2-15/4=1 and P'(1)=1/4+9-45/4=-2. Exact integration gives J=17/8.

## 6 Why the original solution is a straight line

Cauchy-Schwarz gives integral[P'(t)²]dt >= (integral P'(t)dt)² = 1. Equality requires constant velocity. On this unit interval, P(t)=t. The Euler-Lagrange equation gives the same result, P''(t)=0.

Increasing degree cannot reduce the original cost below 1. With the extra terminal velocity, however, the cubic has useful freedom and reduces the cost from 4 to 17/8. Higher degree helps when it improves a constrained solution, not automatically.

Q is positive definite: every nonzero coefficient vector gives a nonzero derivative with positive squared integral. Hence each feasible finite-dimensional problem has a unique minimum. The archived verify_theory.py script checks the constraints and integrals with exact rational arithmetic.

Source: MIT VNAV Lab4, individual Deliverable 1. https://vnav.mit.edu/labs_2023/lab4/exercises.html
