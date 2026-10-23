# Deliverable 2: Multi-Segment Optimization

Boyu Huang, 24020036026; Group 8

## 1 Assumptions

Consider one-dimensional motion through k+1 prescribed positions, joined by k polynomial segments. Durations are fixed. At the initial and final points, derivatives 1 through r-1 are prescribed. At internal points, these derivatives are free to be chosen, but the values on both sides must agree. A free derivative is an unknown, not a derivative forced to zero.

The objective is J=sum over segments of integral [P_j^(r)(t)]² dt. Minimum snap uses r=4: snap is the fourth derivative of position.

## 2 Degree and coefficient count

The Euler-Lagrange equation gives P_j^(2r)(t)=0. Each segment has degree at most 2r-1 and contains 2r coefficients. There are 2rk coefficients in total. For r=4, this becomes degree seven and 8k coefficients.

Table 1. Conditions for k segments

| **Condition** | **Minimum snap, r=4** | **General order r** |
| --- | --- | --- |
| Prescribed positions at segment ends | 2k | 2k |
| Fixed endpoint derivatives | 6 | 2(r-1) |
| Internal low-order continuity | 3(k-1) | (r-1)(k-1) |
| Internal natural conditions | 3(k-1) | (r-1)(k-1) |
| Complete system | 8k | 2rk |

There are k+1 physical waypoints. Each internal waypoint supplies a position equation for both adjacent segments, so the count is 2+2(k-1)=2k. The outer endpoints supply 2(r-1) fixed derivative equations. Each internal join adds r-1 low-order continuity equations.

## 3 Why natural conditions are needed

Vary the cost and integrate by parts r times. Apart from a factor of two, the boundary terms are:

```text
sum over l=0,...,r-1 of
  (-1)^l * P^(r+l) * delta P^(r-1-l)
```

At an internal waypoint, delta P=0 because position is prescribed. Variations of derivatives 1 through r-1 are free and shared by adjacent segments. Matching their boundary coefficients requires derivatives r through 2r-2 to be continuous. This supplies r-1 natural conditions per join.

The derivative of order 2r-1 multiplies delta P=0 and may jump. For minimum snap, velocity, acceleration, and jerk are explicitly continuous. Derivatives four, five, and six become continuous at the optimum; the seventh need not be.

---PAGE---

## 4 Explicit constraints and the complete system

Natural conditions follow from minimization. They should not all be counted as extra constraints imposed by the user in the quadratic program.

Table 2. Two different counts

| **Count** | **General r** | **For r=4** |
| --- | --- | --- |
| Explicit feasibility equations | (r+1)k+r-1 | 5k+3 |
| Additional natural conditions | (r-1)(k-1) | 3(k-1) |
| Complete optimality system | 2rk | 8k |

The explicit count is 2k+2(r-1)+(r-1)(k-1). If grouped as waypoint, fixed derivative, and free derivative conditions, the full count is:

```text
Waypoint positions:         2k
Fixed endpoint derivatives: 2(r-1)
Free internal derivatives:  2(r-1)(k-1)
Total:                      2rk
```

The free-derivative group combines low-order continuity and natural optimality. The number of free internal derivative values alone is only (r-1)(k-1).

## 5 Check: three minimum-snap segments

For r=4 and k=3, three degree-seven polynomials contain 24 coefficients.

Table 3. Concrete count

| **Item** | **Number** |
| --- | --- |
| Position equations | 6 |
| Fixed endpoint derivative equations | 6 |
| Low-order continuity equations | 6 |
| Natural optimality equations | 6 |
| Total | 24 |

There are 18 explicit constraints and six natural conditions. The sum matches the 24 coefficients. The archived verification script checks the same identities for several values of r and k.

## 6 Relation to the code

The Lab4 program uses N=10: ten coefficients, or degree at most nine. Its endpoint settings and implementation choices differ from the theoretical setting above. The degree-seven result is not an instruction to change N to seven. Free endpoint conditions, different fixed derivatives, or optimized durations require a new count.

Source: MIT VNAV Lab4, individual Deliverable 2. https://vnav.mit.edu/labs_2023/lab4/exercises.html
