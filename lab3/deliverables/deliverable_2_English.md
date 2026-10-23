# Lab 3 - Deliverable 2

Huang Boyu | 24020036026 | Group 8

## A. Rotor Configuration

Question A asks whether changing propellers 3 and 4 and reversing their rotation still allows independent position and heading control. Use the exercise numbering: in top view, x points right and y upward. Rotor positions are (-a,a), (-a,-a), (a,-a), (a,a), with a=d/sqrt(2). For u_i=omega_i squared, [f,tau_x,tau_y,tau_z]^T=Fu. This numbering is separate from the simulator numbering.

![Figure A1. Exercise configurations a and b.](assets_current/drone_spinning.png)

![Equation (A1). Allocation matrices for the two configurations.](assets_current/theory_matrices.png)

Table A1. Configuration analysis for positive coefficients

| Configuration | Result | Meaning |
| --- | --- | --- |
| a | rank=4; |det|=16a^2c_f^3c_d | Four independent control components |
| b | rank=3; tau_z=-c_d tau_x/(a c_f) | Roll and yaw are coupled, not independently assignable |

For positive a, c_f and c_d, the normal matrix has a nonzero determinant and rank 4. In configuration b, the first three rows are independent, but row 4 equals row 2 multiplied by -c_d/(a c_f), giving rank 3. Changing roll moment therefore forces a linked change in yaw moment. Position and yaw cannot be assigned independently in general. Special motions that satisfy this constraint may still be possible.

## B. Drag Compensation

Question B asks how the given drag model could improve tracking. Estimate the drag first, then ask the rotors for an opposing force. R maps body vectors to the world frame, so compute body velocity as v_b=R^T v before using the model.

![Equation (B1)](assets_current/drag.png)

D=diag(0.1,0.1,0.2). The product is component by component. Drag opposes the velocity and grows with its squared magnitude along each axis. With world z pointing upward, the force balance is:

![Equation (B2)](assets_current/dynamics.png)

Set e_x=x-x_d and e_v=v-v_d. Transform the estimated drag to the world frame and subtract it from the baseline force. Subtracting the external force requests a force in the opposite direction:

![Equation (B3)](assets_current/compensation.png)

Construct the desired attitude from the compensated force and project it onto the current thrust axis:

![Equation (B4)](assets_current/orientation.png)

If attitude tracking makes the thrust vector close to A, substitution into the force balance gives Equation (B5). A good estimate cancels most of the disturbance. Model error and noisy velocity leave a residual, so a flight comparison is still needed to establish any improvement.

![Equation (B5)](assets_current/drag_error.png)

Table B1. Derivation and proposed validation

| Item | Scope in this work |
| --- | --- |
| Work completed | Derivation only; not added to the flight code or tested in a flight comparison |
| How to check it | Keep the path, gains and initial state fixed; compare errors and commands with compensation on and off |


References: MIT VNAV Lab 3 Exercises (2023); Lee et al., IEEE CDC, 2010, pp. 5420-5425.
