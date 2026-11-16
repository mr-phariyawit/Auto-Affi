# Colliding blocks compute pi (Galperin billiards): maths, physics and simulation algorithm

Research date: 2026-11-13. Evidence labels used below:
- `[SOURCE]` = stated by the linked source (read by me in this session).
- `[VERIFIED: own run]` = I ran a Python script in this session and the numbers below are its output (scripts were throwaway, in the session scratchpad; the algorithms are reproduced as pseudocode here so they can be re-run).
- `[UNVERIFIED]` = from memory or inferred, not checked against a source or a run.

Notation used throughout (ours, chosen for the TikTok layout: wall on the LEFT, x increases to the right):
- small block: mass `m` (= 1 kg), next to the wall, initially at rest. Velocity `v_s`.
- big block: mass `M` (1, 100, 10 000 kg), to the right, initial velocity `-u` (moving left). Velocity `v_b`.
- `theta = arctan(sqrt(m / M))`.
- "Reduced" positions (removes block widths): `x_s` = distance wall -> small block's left face; `x_b` = (distance wall -> big block's left face) minus the small block's width. Then: wall hit when `x_s = 0`, block-block hit when `x_b = x_s`, and always `0 <= x_s <= x_b`.
- WARNING on conventions: 3Blue1Brown's code calls the BIG block `block1`/`m1` and the small block `block2`/`m2` (so his `theta = arctan(sqrt(m2/m1))` is the same angle as ours). Galperin uses `m` (small) and `M` (big) like us.

---

## 1. Exact statement and result; who proved it; caveats

### Takeaway
With mass ratio `M/m = 100^N` (small block at rest between the wall and the big block, perfectly elastic, no friction), the total number of collisions (block-block plus small-block-wall) is the integer formed by the first `N+1` digits of pi: 3, 31, 314, 3141, ... The exact count is `ceil(pi/theta) - 1` with `theta = arctan(10^-N)`; that this always equals `floor(pi * 10^N)` is NOT proven for all N. Galperin proves it "modulo a conjecture" about runs of 9s in pi's digits.

### Cited Findings
- Paper: G. A. Galperin, "Playing pool with pi (the number pi from a billiard point of view)", Regular and Chaotic Dynamics, 2003, vol. 8, no. 4, pp. 375-394, DOI 10.1070/RD2003v008n04ABEH000252; author affiliation Eastern Illinois University. `[SOURCE]` — [Mathnet.ru record](https://mathnet.ru/eng/rcd790); [journal page](https://rcd.ics.org.ru/RD2003v008n04ABEH000252/)
- One secondary source (Aperiodical) dates the paper 2013; the journal record says 2003, so 2013 is an error. `[SOURCE]` — [Mathnet.ru record](https://mathnet.ru/eng/rcd790); contradicted by [Aperiodical](https://aperiodical.com/?p=13614)
- Galperin's set-up uses two billiard balls and a wall; the mass ratio "should be chosen to be the N-th power of 100"; one counts ball-ball collisions plus reflections of the small ball off the wall. `[SOURCE]` — [Galperin PDF, sections 1-2](https://www.maths.tcd.ie/~lebed/Galperin.%20Playing%20pool%20with%20pi.pdf)
- Galperin's Theorem as stated: the number of hits `PI(N)` is always finite and is a number with `N+1` digits whose first N digits coincide with the first N decimal digits of pi (starting with 3). He gives `PI(0) = 3`, `PI(1) = 31`, `PI(2) = 314`. `[SOURCE]` — [Galperin PDF, section 3 and Theorem](https://www.maths.tcd.ie/~lebed/Galperin.%20Playing%20pool%20with%20pi.pdf)
- Equal masses (N = 0): the moving ball stops and the still ball takes its velocity, it reflects off the wall, comes back, and transfers the velocity again: 2 collisions + 1 reflection = 3. `[SOURCE]` — [Galperin PDF, section 3](https://www.maths.tcd.ie/~lebed/Galperin.%20Playing%20pool%20with%20pi.pdf)
- Exact formula: the wedge angle is `alpha = arctan(sqrt(m/M)) = arctan(10^-N)`. Lemma 2: the maximal number of reflections in a wedge of angle alpha is `pi/alpha` if that is an integer, else `[pi/alpha] + 1`; when the initial ray is parallel to one side (our case: small block at rest) the count is one fewer. Hence for N >= 1 (where `pi/alpha` is not an integer) `PI(N) = [pi / arctan(10^-N)]`, and for N = 0, `pi/alpha = 4` gives `4 - 1 = 3`. `[SOURCE]` — [Galperin PDF, sections 7-8, eq. 8.1](https://www.maths.tcd.ie/~lebed/Galperin.%20Playing%20pool%20with%20pi.pdf)
- Caveat (important): replacing `arctan(10^-N)` by `10^-N` can change the integer part by at most 1, so `PI(N)` is either `[pi*10^N]` or `[pi*10^N] + 1`. The "+1" case occurs only if the first 2N decimal digits of pi contain a string of N-1 consecutive nines in the right half. Galperin states the theorem is proven "modulo Conjecture" and conjectures the bad case never occurs. `[SOURCE]` — [Galperin PDF, sections 8-10](https://www.maths.tcd.ie/~lebed/Galperin.%20Playing%20pool%20with%20pi.pdf)
- Galperin's evidence for the conjecture: the string 999999999 (nine 9s) does not occur in the first 100,000,000 digits of pi, so he says the method is accurate up to 100 million digits (text says "N <= 10^8" in one place and "at least for N <= 50 million" in another), with a heuristic probability argument beyond that. `[SOURCE]` — [Galperin PDF, section 10](https://www.maths.tcd.ie/~lebed/Galperin.%20Playing%20pool%20with%20pi.pdf)
- 3Blue1Brown's lesson text gives the same counts: equal masses 3; ratio 100 -> 31; 10,000 -> 314; 1,000,000 -> 3,141; the mass ratio must be a power of 100. `[SOURCE]` — [3Blue1Brown lesson "clacks", Jan 13 2019](https://www.3blue1brown.com/lessons/clacks)
- 3Blue1Brown's third lesson states the count as `floor(pi/theta)` and then corrects it: if `pi/theta` is an integer the floor over-counts by one, and the correct formula is `ceil(pi/theta) - 1`. `[SOURCE]` — [3Blue1Brown lesson "clacks-via-light", Feb 3 2019](https://www.3blue1brown.com/lessons/clacks-via-light)
- The three 2019 videos (IDs confirmed via YouTube oEmbed in this session): "The most unexpected answer to a counting puzzle" `HEfHFsfGXjs`; "Why do colliding blocks compute pi?" `jsYwFizhncE`; "How colliding blocks act like a beam of light...to compute pi." `brU5yLm9DZM`. A newer 3Blue1Brown video "Why colliding blocks compute pi" is `6dTyOl1fmDo`. `[SOURCE]` — [video 1](https://www.youtube.com/watch?v=HEfHFsfGXjs); [video 2](https://www.youtube.com/watch?v=jsYwFizhncE); [video 3](https://www.youtube.com/watch?v=brU5yLm9DZM); [newer video](https://www.youtube.com/watch?v=6dTyOl1fmDo)

### Inferences
- `[VERIFIED: own run]` Event/velocity simulation in IEEE doubles gives 3, 31, 314, 3141, 31415, 314159, 3141592, 31415926, 314159265 for N = 0..8. So the TikTok's "3, 31, 314" for 1 kg, 100 kg, 10,000 kg is exactly right.
- `[VERIFIED: own run]` The `ceil(pi/theta) - 1` form matters whenever `pi/theta` is an integer: mass ratio 1 (`pi/theta = 4`) gives 3 collisions, mass ratio 3 (`pi/theta = 6`) gives 5; a naive `int(pi/theta)` in floating point returned 4 and 6 respectively. For the TikTok's first case (1 kg vs 1 kg) do NOT use `floor(pi/theta)`.
- The on-screen claim "digits of pi" is safe for the three cases shown; a general "for every n" claim should be worded as "conjectured/expected" rather than "proven".

### Gaps
- No dedicated English Wikipedia article was found (a Wikipedia API search returned nothing relevant); Wikipedia was therefore not used.
- I did not read the full proof text of Lemma 1/Lemma 2 line by line, only the statements and the surrounding prose (PDF text extraction dropped most formula glyphs).
- Whether anyone has since proven Galperin's conjecture: not searched in depth; I found no source claiming a proof.

---

## 2. Collision formulas, event-driven algorithm, why naive stepping fails, floating-point limits

### Takeaway
Use exact 1D elastic-collision formulas and an event-driven (time-of-impact) loop, or better, skip stepping entirely: collision k happens at the closed-form time `t_k = (x_b0 - x_s0 * tan(theta)/tan(k*theta)) / u`, and block positions at any time t follow from "unfolding" (a rotation). Naive one-check-per-frame stepping gives the right count only at small mass ratios; it distorts timing and miscounts once blocks tunnel.

### Cited Findings
- Elastic collision formula used by The Coding Train sketch: `v1' = (m1 - m2)/(m1 + m2) * v1 + 2*m2/(m1 + m2) * v2` (and symmetrically for block 2); wall hit = reverse the small block's velocity. `[SOURCE]` — [Coding Train sketch (p5.js web editor)](https://editor.p5js.org/codingtrain/sketches/4FuKfd-LJ)
- The Coding Train sketch is a fixed-step simulation with sub-stepping: `timeSteps = 10 ** (digits - 1)` sub-steps per drawn frame, big block velocity `-1 / timeSteps` px per sub-step, collision test = bounding-interval overlap, wall test = `x <= 0`; drawn x of each block is clamped (`constrain(x, xConstraint, width)`) so the blocks do not visibly sink into the wall. `[SOURCE]` — [Coding Train sketch](https://editor.p5js.org/codingtrain/sketches/4FuKfd-LJ)
- The Coding Train video chapters include "Adding timesteps to control approximation" (18:09), "Adding constraints to speed up animation" (24:12) and "Watching collisions up to 11 digits of pi" (26:47). `[SOURCE]` — [Coding Train challenge 139 page](https://thecodingtrain.com/challenges/139-calculating-digits-of-pi-with-collisions)
- 3Blue1Brown's 2019 code does NOT step physics. It tracks one point in rescaled position space `[s1*sqrt(m1), s2*sqrt(m2)]` moving in a straight line at constant velocity, computes `n_clacks = int(angle / theta)` from the point's polar angle, and recovers block positions by rotating the point by `-2*ceil(n_clacks/2)*theta` and taking absolute values, then dividing by `sqrt(mass)`. `[SOURCE]` — [3b1b/videos `_2019/clacks/question.py`](https://github.com/3b1b/videos/blob/master/_2019/clacks/question.py)
- In the same file, clack times are precomputed in closed form (valid only when the small block starts at rest): for `k = 1..int(PI/theta)` the clack point in phase space is `(y / tan(k*theta), y)` and `time = distance to that point / speed`. `[SOURCE]` — [3b1b/videos `_2019/clacks/question.py`](https://github.com/3b1b/videos/blob/master/_2019/clacks/question.py)
- 3Blue1Brown's 2025 rewrite keeps the same idea as a 4-vector state `[x1*sqrt(m1), x2*sqrt(m2), v1*sqrt(m1), v2*sqrt(m2)]`, `theta = atan2(sqrt_m2, sqrt_m1)`, `set_time(t)` = straight-line motion, collisions counted as `int(angle/theta)`, and fold = rotate by `-2*theta*((n+1)//2)` then flip the sign of the second coordinate when n is odd. `[SOURCE]` — [3b1b/videos `_2025/colliding_blocks_v2/blocks.py`](https://github.com/3b1b/videos/blob/master/_2025/colliding_blocks_v2/blocks.py)
- 3Blue1Brown's lesson text says most clacks happen in one burst, and that for many digits the clack frequency becomes astronomically high, so the calculation needs very high numerical precision and long run time. `[SOURCE]` — [3Blue1Brown lesson "clacks"](https://www.3blue1brown.com/lessons/clacks)

### Inferences

Exact collision rules (standard 1D elastic collision; consistent with the Coding Train formula above):

```
block-block (only when v_s > v_b, i.e. approaching):
    v_s' = ((m - M) * v_s + 2 * M * v_b) / (m + M)
    v_b' = ((M - m) * v_b + 2 * m * v_s) / (m + M)
wall (only when v_s < 0):
    v_s' = -v_s
stop when 0 <= v_s <= v_b   (both moving right, small one slower: no more collisions ever)
```

Event-driven (time-of-impact) simulation, `[VERIFIED: own run]` (gives 3 / 31 / 314 and matches the closed forms below to ~1e-13):

```
state: x_s, x_b (reduced positions), v_s = 0, v_b = -u, t = 0, n = 0
events = []
loop:
    t_wall  = (v_s < 0)   ? -x_s / v_s               : INF
    t_block = (v_s > v_b) ? (x_b - x_s) / (v_s - v_b) : INF
    if both INF: break
    dt = min(t_wall, t_block)
    t += dt;  x_s += v_s * dt;  x_b += v_b * dt
    if t_block <= t_wall:
        x_b = x_s                      # snap, kills drift
        (v_s, v_b) = elastic(v_s, v_b) # formulas above
        kind = "block"
    else:
        x_s = 0;  v_s = -v_s
        kind = "wall"
    n += 1
    events.append({t, kind, x_s, x_b, v_s, v_b, index: n})
# rendering: for frame time T, find last event with t <= T, then
#   x = x_event + v_event * (T - t_event);  counter = event.index
```

Closed forms (no loop needed), all `[VERIFIED: own run]` against the event simulation for M = 1, 3, 100, 10 000 with `m = 1, x_s0 = 1, x_b0 = 3, u = 1`:

```
theta = atan(sqrt(m / M))
N_total = ceil(pi / theta) - 1                      # 3, 31, 314
# collision k (k = 1..N_total); odd k = block-block, even k = wall
t_k = (x_b0 - x_s0 * tan(theta) / tan(k * theta)) / u
# velocities after collision n (j = ceil(n / 2)):
v_b = -u * cos(2 * theta * j)
v_s = -u * sqrt(M / m) * sin(2 * theta * j)   if n odd   (just hit by big block, moving left)
v_s = +u * sqrt(M / m) * sin(2 * theta * j)   if n even  (just bounced off wall)

# positions at ANY time t, no stepping (unfold-and-fold):
Qx = sqrt(M) * (x_b0 - u * t);  Qy = sqrt(m) * x_s0
phi = atan2(Qy, Qx)                                  # grows from ~0 towards pi
n   = clamp(ceil(phi / theta) - 1, 0, N_total)       # collisions so far = counter value
rot = -2 * theta * floor((n + 1) / 2)
X = cos(rot) * Qx - sin(rot) * Qy
Y = sin(rot) * Qx + cos(rot) * Qy
if n is odd: Y = -Y
x_b = X / sqrt(M);  x_s = Y / sqrt(m)                # reduced positions; add widths back to draw
```
(20,000 random times per mass ratio: 0 counter mismatches, max position error 1.3e-13.)

Why naive fixed-timestep simulation goes wrong:
- At most one block-block and one wall collision can be resolved per step, but near the turnaround the true collision rate is about `(M/m) * u / x_s0` per second (see section 4), i.e. 10,000 collisions/s for the 10,000 kg case at u = 1 unit/s, x_s0 = 1 unit. A 60 fps step sees ~100+ collisions per frame. The simulation then spreads the burst over hundreds of frames while the big block keeps moving, so the big block is drawn inside the small block / inside the wall, and clack timing is wrong.
- If the collision test is an interval-overlap test, the blocks can tunnel past each other entirely and collisions are lost. `[VERIFIED: own run]` A line-for-line Python port of the Coding Train logic gave: timeSteps = 1 -> 3, 31, 314 correct for ratios 1, 100, 10^4, but **132 instead of 3141** for ratio 10^6; with timeSteps >= 10 it gave 3141.
- `[VERIFIED: own run]` A variant that tests `x_b <= x_s` (half-line, not interval) and only swaps velocities still returned the correct count 3/31/314 at dt = 1/60 with no sub-stepping, because the velocity sequence is independent of positions. So the COUNT can survive a bad integrator, but positions and timing cannot. Do not rely on this.
- Always gate collisions on approach velocity (`v_s > v_b`, `v_s < 0`), otherwise a still-overlapping pair is "collided" twice and the elastic map undoes itself. `[UNVERIFIED]` as a failure seen in the wild; it follows from the collision map being its own inverse.

Floating-point limits:
- `[VERIFIED: own run]` Plain doubles, velocity-only iteration: correct count through mass ratio 100^8 (314,159,265 collisions; ~16 s in pure Python).
- `[UNVERIFIED]` Beyond that, error accumulates over ~3*10^N multiplications and the decision "is there one more collision" depends on a margin that shrinks with N; expect to need arbitrary precision (and hours of run time) well before N ~ 15. For a video that shows only N = 0, 1, 2 this is irrelevant: doubles have ~12 digits of headroom.
- The closed-form `t_k` uses `tan(k*theta)`, which passes through a pole at `k*theta = pi/2`; `1/tan` is well-behaved there (it crosses 0), so compute `cos/sin` rather than `1/tan` to be safe.

### Gaps
- I did not find a written statement from 3Blue1Brown explaining why he chose the closed-form approach over stepping; the claim rests on reading his source code.
- Arbitrary-precision behaviour for N > 8 was not tested.

---

## 3. The circle diagram (velocity phase space) and the wedge billiard (position space)

### Takeaway
Plot the point `(X, Y) = (sqrt(M) * v_b, sqrt(m) * v_s)`. Energy conservation keeps it on a circle of radius `sqrt(M) * u`; each block-block collision jumps along a chord of fixed slope `-sqrt(M/m)`; each wall collision jumps along a vertical chord. Every jump advances the point by an arc of `2*theta`, so the polyline's vertices are simply `R * (-cos a_n, -sin a_n)` with `a_n = +-2*theta*ceil(n/2)`. The count is how many arcs of `2*theta` fit before the point lands in the "end zone".

### Cited Findings
- 3Blue1Brown's solution video/code uses coordinates `x = sqrt(m1) * v1`, `y = sqrt(m2) * v2` (his m1 = big block), draws the energy ellipse rescaled to a circle, labels the momentum line "Slope = -sqrt(m1/m2)", and uses `theta = arctan(sqrt(m2/m1))`. `[SOURCE]` — [3b1b/videos `_2019/clacks/solution1.py`](https://github.com/3b1b/videos/blob/master/_2019/clacks/solution1.py)
- His `CircleDiagramFromSlidingBlocks.get_lines` builds exactly the polyline the TikTok shows: `n_clacks = int(PI/theta)`; for `n = 0..n_clacks`: `angle = 2*theta*((n+1)//2)`, negated when n is even; point = `radius * (-cos(angle), -sin(angle))`; segments join consecutive points. The start point is on the left of the circle (`circle.rotate(PI)` "Nice to have start point on left"). `[SOURCE]` — [3b1b/videos `_2019/clacks/solution1.py`](https://github.com/3b1b/videos/blob/master/_2019/clacks/solution1.py)
- In that scene each segment is revealed at its collision time (`self.wait(time - last_time)` per line), with a red dot at the current point and an optional vector from the origin. `[SOURCE]` — [3b1b/videos `_2019/clacks/solution1.py`](https://github.com/3b1b/videos/blob/master/_2019/clacks/solution1.py)
- The end zone is drawn as the triangle between the positive x-axis and the line of slope `1/sqrt(mass_ratio)` through the origin (green, 30% opacity). `[SOURCE]` — [3b1b/videos `_2019/clacks/solution1.py`](https://github.com/3b1b/videos/blob/master/_2019/clacks/solution1.py)
- Position-space picture (3Blue1Brown): coordinates `x = sqrt(m1)*d1`, `y = sqrt(m2)*d2`; block-block collisions happen on the line `d1 = d2` (slope `sqrt(m2/m1)`), wall collisions on a horizontal line; the two lines form a wedge of angle `theta = arctan(sqrt(m2/m1))`. Energy conservation means the point moves at constant speed; momentum conservation is a dot product with the vector `(sqrt(m1), sqrt(m2))`, which forces angle of incidence = angle of reflection. `[SOURCE]` — [3Blue1Brown lesson "clacks-via-light"](https://www.3blue1brown.com/lessons/clacks-via-light)
- Unfolding: instead of reflecting the trajectory, reflect the wedge; the trajectory becomes a straight line crossing a fan of wedge copies spaced theta apart; the number of bounces is the number of fan lines crossed = `ceil(pi/theta) - 1`. `[SOURCE]` — [3Blue1Brown lesson "clacks-via-light"](https://www.3blue1brown.com/lessons/clacks-via-light)
- Galperin's version: configuration point `(x, y)` = (small ball position, big ball position) lives in the 45-degree angle between the positive y-axis and the ray `y = x`; the linear map `X = sqrt(m)*x`, `Y = sqrt(M)*y` turns it into an angle `alpha` with `tan(alpha) = sqrt(m/M)` in which the point obeys the billiard law (Lemma 1); the count follows by unfolding (Lemma 2). `[SOURCE]` — [Galperin PDF, sections 4-7](https://www.maths.tcd.ie/~lebed/Galperin.%20Playing%20pool%20with%20pi.pdf)

### Inferences

Derivation in our notation (standard; matches the sources above):
- Energy: `(1/2) M v_b^2 + (1/2) m v_s^2 = const`  ->  `X^2 + Y^2 = R^2`, with `R = sqrt(M) * u`.
- Momentum (block-block only): `M v_b + m v_s = const`  ->  `sqrt(M) * X + sqrt(m) * Y = const`  ->  a line of slope `dY/dX = -sqrt(M/m) = -1/tan(theta)`. The post-collision point is the OTHER intersection of that line with the circle.
- Wall: `v_s -> -v_s`  ->  `Y -> -Y`, a vertical chord.
- Angle between a "momentum" chord and a vertical chord is `theta` (the momentum line makes angle theta with the vertical). By the inscribed-angle theorem each chord pair meeting at a point on the circle subtends an arc of `2*theta`. So successive NEW points are spaced `2*theta` apart along the circle, alternating below and above the X axis.
- End condition `0 <= v_s <= v_b`  <=>  `0 <= Y <= X * tan(theta)`: the wedge of angle theta just above the positive X axis. Arcs of `2*theta` are laid down until the point falls into it; total number of chords = `ceil(pi/theta) - 1`.
- Small-angle step: `theta = arctan(10^-N) ~ 10^-N`, so the count is about `pi * 10^N`.

Vertex formula, `[VERIFIED: own run]` (compared with `(sqrt(M)*v_b, sqrt(m)*v_s)` from the event simulation after every collision, max error 7e-14 for M = 1, 100, 10 000):

```
# Circle-diagram vertices. Maths axes: X right, Y up (flip Y for screen coordinates).
theta   = atan(sqrt(m / M))
N_total = ceil(pi / theta) - 1
R_px    = circle radius in pixels;  (cx, cy) = circle centre
P = []
for n in 0 .. N_total:
    j = ceil(n / 2)                # 0,1,1,2,2,3,3,...
    a = 2 * theta * j
    if n is even: a = -a           # n = 0 -> a = 0
    X = -cos(a);  Y = -sin(a)      # unit circle; equals (sqrt(M) v_b, sqrt(m) v_s) / R
    P[n] = (cx + R_px * X,  cy - R_px * Y)     # screen y points down
# segment k (k = 1..N_total) joins P[k-1] -> P[k] and belongs to collision k:
#   odd k  = block-block collision: chord of slope -sqrt(M/m) (steep, down-right)
#   even k = wall collision: exactly vertical chord (X unchanged, Y flips sign)
# reveal segment k when playback time >= t_k (section 2); colour = gradient(k / N_total)
```

What it looks like for the three cases (`[VERIFIED: own run]` for the numbers):
- M = 1 kg: theta = 45 deg, 3 segments. P0 = (-1, 0) left; P1 = (0, -1) bottom; P2 = (0, +1) top; P3 = (+1, 0) right. (Diagonal, vertical diameter, diagonal: a "Z/N" shape.)
- M = 100 kg: theta = 5.71 deg, 31 segments; last collision is block-block (odd count); final velocities v_s = 0.478 u, v_b = 0.9989 u.
- M = 10,000 kg: theta = 0.573 deg, 314 segments, nearly vertical chords sweeping left to right, which reads as a filled fan; last collision is a wall hit (even count); final v_s = 0.1697 u, v_b = 0.9999986 u.
- Parity rule: odd-numbered collisions are block-block (new point in the LOWER half, since the small block is moving left, Y < 0); even-numbered are wall hits (new point in the UPPER half).

Position-space (wedge billiard) construction in our notation, useful as an alternative diagram and as the engine for positions:
- Point `Q = (sqrt(M) * x_b, sqrt(m) * x_s)`. Allowed region: `0 <= Y <= X * tan(theta)`: a wedge of angle theta at the origin. The lower edge (Y = 0) is the wall; the upper edge (x_b = x_s) is block-block contact.
- Initially Q moves horizontally left at speed `sqrt(M) * u` along the line `Y = sqrt(m) * x_s0` (small block at rest), i.e. parallel to the lower edge. That is exactly Galperin's "initial ray parallel to one side" case, hence "one fewer than the maximum".
- Unfolded, the trajectory is that same horizontal line continued forever; it crosses the rays at angles `theta, 2*theta, ..., k*theta < pi`. Crossing ray k at `X = Y0 / tan(k*theta)` gives the `t_k` formula in section 2.

### Gaps
- The TikTok's exact axis orientation, start point and colour gradient were not available to me (I did not see the clip); the construction above reproduces 3Blue1Brown's diagram (start at left, lines revealed per collision). Mirror or rotate as needed to match the clip.
- I did not transcribe the inscribed-angle argument from the video itself (the lesson page for video 2 exposes no text); it is reconstructed from the source code plus standard geometry.

---

## 4. Collision timeline: counts, clustering, and how animators handle the burst

### Takeaway
Collisions are not evenly spread: they follow a `sin^2` rate profile peaking when the big block turns around, with peak rate about `(M/m) * u / x_s0` collisions per second. For 10,000 kg, 88% of the 314 clacks fall in a 0.1 s window at real-time speed, over 100 per video frame. Animators therefore precompute collision times, slow time down around the burst, and rate-limit sounds and flashes.

### Cited Findings
- 3Blue1Brown describes the set-up as heavily over-idealized and notes that most clacks happen in one burst. `[SOURCE]` — [3Blue1Brown lesson "clacks"](https://www.3blue1brown.com/lessons/clacks)
- On the sound: a footnote in the lesson says he added a small clack sound even though perfectly energy-conserving collisions would be silent; it is there to draw attention to the count. The page does not say how the sound was recorded or synthesized. `[SOURCE]` — [3Blue1Brown lesson "clacks"](https://www.3blue1brown.com/lessons/clacks)
- Sound handling in his 2019 code: sound file `clack.wav` (slow-motion scenes use `slow_clack.wav`); sounds are added after the scene from the precomputed clack times, skipping any clack closer than `min_time_between_sounds = 0.004` s to the previous one, each at `gain = -20`. `[SOURCE]` — [3b1b/videos `_2019/clacks/question.py`](https://github.com/3b1b/videos/blob/master/_2019/clacks/question.py)
- Flash handling in the same code: a yellow `Flash` at each clack location, skipping clacks within `min_time_between_flashes = 1/30` s of the previous one. `[SOURCE]` — [3b1b/videos `_2019/clacks/question.py`](https://github.com/3b1b/videos/blob/master/_2019/clacks/question.py)
- Block size in his code is logarithmic in mass: width `1 + 0.25 * log10(mass)`; the label is formatted like "10,000 kg". `[SOURCE]` — [3b1b/videos `_2019/clacks/question.py`](https://github.com/3b1b/videos/blob/master/_2019/clacks/question.py)
- His 2025 code plays `clack.wav` at most once per rendered frame (it checks whether the collision count changed since the last frame, then adds one sound with a negative time offset back to the exact collision time), and removes each flash after 0.25 s. It also has a `reverse_clack.wav` for time running backwards. `[SOURCE]` — [3b1b/videos `_2025/colliding_blocks_v2/blocks.py`](https://github.com/3b1b/videos/blob/master/_2025/colliding_blocks_v2/blocks.py)
- The Coding Train sketch plays its clack at most once per drawn frame (a boolean `clackSound` set inside the sub-step loop, `clack.play()` once after it), and updates the counter once per frame. `[SOURCE]` — [Coding Train sketch](https://editor.p5js.org/codingtrain/sketches/4FuKfd-LJ)
- In the circle-diagram scene, any precomputed collision time above 300 s is replaced by "previous + 1 s" before waiting. `[SOURCE]` — [3b1b/videos `_2019/clacks/solution1.py`](https://github.com/3b1b/videos/blob/master/_2019/clacks/solution1.py)

### Inferences

Timeline numbers, `[VERIFIED: own run]`, for `m = 1, u = 1 unit/s, x_s0 = 1 unit, x_b0 = 3 units` (first contact at t = 2 s, turnaround near t = x_b0/u = 3 s):

| Big mass | Collisions | First -> last collision | Within 0.1 s of turnaround | Within 0.5 s | Within 1.0 s | Smallest gap | Max per frame @30 fps | @60 fps | Big block's closest approach (reduced) |
|---|---|---|---|---|---|---|---|---|---|
| 1 kg | 3 | t = 2, 3, 4 s | n/a | n/a | n/a | 1 s | 1 | 1 | 1.0 |
| 100 kg | 31 | 2.000 -> 4.926 s | 9 (29%) | 24 (77%) | 28 (90%) | 0.00998 s | 3 | 2 | 0.0998 |
| 10,000 kg | 314 | 2.000 -> 8.892 s | 275 (88%) | 307 (98%) | 311 (99%) | 0.0001 s | 128 | 103 | 0.0100 |

Closed-form description of the clustering (follows from `t_k`; consistent with the table):
- Let `phi = k * theta` be the unfolded angle. Collision rate `dk/dt = (u * sqrt(M/m) / (x_s0 * theta)) * sin^2(phi)`. It is tiny at the start and end (phi near 0 or pi) and peaks at `phi = pi/2` (big block momentarily stopped) at about `(M/m) * u / x_s0` per second: 1/s, 100/s, 10,000/s for the three cases with the geometry above.
- The big block's minimum reduced distance from the wall is about `x_s0 * sqrt(m/M)`: it stops one-tenth (100 kg) or one-hundredth (10,000 kg) of the small block's starting gap from the small block's resting contact point. On a 1080 px wide frame the small block's travel during the burst is a few pixels: it visually "buzzes" in place.
- The tail is long: after the burst the last few collisions are seconds apart (the small block is slow and chasing the wall while the big one leaves). For 10,000 kg the final collision is at 8.89 s versus the burst at ~3 s. An edit may reasonably cut away before the very last clack, but then the counter must still reach 314.
- Everything scales trivially: times scale with `x/u`; choosing a smaller `x_s0` (small block closer to the wall) makes the burst sharper, a larger one spreads it out.

Practical recipe for a 28 s vertical video (design inference, not from a source):
- Precompute `t_k` for all k (closed form). Define a monotone time-warp `tau(T)` from video time T to simulation time (e.g. full speed during approach, slow by 10x-50x inside the burst window, full speed again for the tail). Label the slow part "slow motion", as the reference clip does. Everything (block positions via the fold formula, counter = number of `t_k <= tau(T)`, diagram segments revealed) is a pure function of `tau(T)`, so frames can be rendered in any order and the counter can never drift from the animation.
- Counter: with 100+ collisions per frame the number will jump in steps of dozens even in moderate slow motion; that is physically correct. To make every increment visible in the 314 case at 60 fps you would need the burst slowed by roughly 100x or more.
- Audio: schedule one clack per collision but drop any closer than a few milliseconds to the previous one (3Blue1Brown uses 4 ms), or cap at one per frame (Coding Train, 3Blue1Brown 2025). Under time-warp, apply the threshold in VIDEO time, not simulation time. 250 Hz (4 ms spacing) of overlapping clicks sounds like a buzz/whine rising and falling in pitch, which is the recognisable sound of the original videos. `[UNVERIFIED]` as to exactly how it sounds in a given mix.
- Flashes: cap at about one per frame (3Blue1Brown: 1/30 s minimum spacing).
- Circle diagram: reveal segment k at `tau(T) >= t_k`; during the burst many segments appear per frame, which is what makes the fan "fill in" quickly.

### Gaps
- How 3Blue1Brown produced the clack recording itself (foley, synthesis, library sound): not found in any source I read. `clack.wav` is referenced by name only.
- I did not find a transcript of the original video to confirm his spoken remarks about the simulation; the "over-idealized / one burst / silent collisions" points come from the written lesson adaptation.
- The reference TikTok's actual time-remap curve and sound design were not analysed here (out of scope for this note).

---

## 5. Existing open-source implementations

### Takeaway
There are two canonical references: 3Blue1Brown's manim scenes (closed-form, no physics stepping, CC BY-NC-SA so not reusable in a monetised clip) and The Coding Train's p5.js challenge 139 (sub-stepped fixed-timestep, no explicit licence on the sketch). The maths is simple enough that a clean-room implementation from sections 2-3 is the safer and shorter route.

### Cited Findings
- 3b1b/videos, Python (manim, 3b1b's own version, not Manim Community). Files for the 2019 trilogy: `_2019/clacks/question.py`, `_2019/clacks/solution1.py`, `_2019/clacks/solution2/` (`block_collision_scenes.py`, `mirror_scenes.py`, `position_phase_space.py`, `pi_creature_scenes.py`, `simple_scenes.py`, `wordy_scenes.py`), `_2019/clacks/all_s2_scenes.py`, `_2019/clacks/name_bump.py`. Files for the 2025 remake: `_2025/colliding_blocks_v2/blocks.py`, `grover.py`, `supplements.py`, `digits_of_pi.txt`. `[SOURCE]` — [3b1b/videos repository](https://github.com/3b1b/videos); [`_2019/clacks`](https://github.com/3b1b/videos/tree/master/_2019/clacks); [`_2025/colliding_blocks_v2`](https://github.com/3b1b/videos/tree/master/_2025/colliding_blocks_v2)
- Licence: the repository README says the manim library is MIT, but the contents of the videos repository are under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0). `[SOURCE]` — [3b1b/videos README](https://github.com/3b1b/videos/blob/master/README.md); [manim licence](https://github.com/3b1b/manim/blob/master/LICENSE.md)
- Approach (2019): `Block`, `Wall`, `SlidingBlocks`, `ClackFlashes`, `BlocksAndWallScene` and subclasses with masses such as 1e0, 1e1, 1e4, 1e6, 1e10 and `1/tan(PI/5)**2`; phase-space point tracker; precomputed `(location, time)` clack data; `LightBouncing` scene for the mirror analogy. `[SOURCE]` — [`question.py`](https://github.com/3b1b/videos/blob/master/_2019/clacks/question.py)
- Lesson pages with credits and source links: video 1 (Jan 13 2019), video 2 (Jan 20 2019), video 3 (Feb 3 2019), by Grant Sanderson; text adaptations by Josh Pullen. `[SOURCE]` — [clacks](https://www.3blue1brown.com/lessons/clacks); [clacks-solution](https://www.3blue1brown.com/lessons/clacks-solution); [clacks-via-light](https://www.3blue1brown.com/lessons/clacks-via-light)
- The Coding Train, Coding Challenge 139 "Calculating Digits of Pi with Collisions" by Daniel Shiffman: p5.js sketch at editor.p5js.org/codingtrain/sketches/4FuKfd-LJ (files `sketch.js`, `block.js`, assets `block.png`, `clack.wav`); YouTube ID `PoW8g67XNxA`; credits 3Blue1Brown and links Galperin's paper. `[SOURCE]` — [challenge page](https://thecodingtrain.com/challenges/139-calculating-digits-of-pi-with-collisions); [p5 sketch](https://editor.p5js.org/codingtrain/sketches/4FuKfd-LJ); [video](https://www.youtube.com/watch?v=PoW8g67XNxA)
- Related Coding Train repo CodingTrain/Pi-Day-2019 (Processing; folders `PiDayCollisions`, `PiDayCollisionsBig`, `PiDayCollisionsOptics`, `LOLBox2D`); GitHub reports no licence for it. The Coding Train website repo is MIT. `[SOURCE]` — [CodingTrain/Pi-Day-2019](https://github.com/CodingTrain/Pi-Day-2019); [CodingTrain/thecodingtrain.com](https://github.com/CodingTrain/thecodingtrain.com)
- Others seen in search results (not inspected in depth): simon-tiger/Pool_Pi (Processing, no licence reported by GitHub); a marimo notebook "colliding-blocks-and-pi" on Hugging Face Spaces; a cut-the-knot exposition of Galperin's argument. `[SOURCE]` — [simon-tiger/Pool_Pi](https://github.com/simon-tiger/Pool_Pi); [marimo notebook](https://huggingface.co/spaces/marimo-team/colliding-blocks-and-pi/blob/bf52b958203898d531d306b04e3b7f933ea7e5ad/notebook.py); [cut-the-knot](https://www.cut-the-knot.org/blue/nicollier_galperin_ctk.shtml)

### Inferences
- Because 3b1b's scene code is NonCommercial + ShareAlike, copying it into a monetised/affiliate TikTok pipeline is a licence risk; the underlying maths and the formulas in this note are not copyrightable, so re-implement from them. (Not legal advice.)
- The Coding Train p5 sketch has no stated licence on the sketch itself; treat it as reference reading, not as code to copy. Its `clack.wav` asset likewise has no stated licence.
- For a deterministic frame-by-frame renderer (HyperFrames, canvas, three.js, ffmpeg frames), the closed-form approach is strictly better than either reference implementation's runtime loop: no state, no sub-steps, exact counter, seekable.
- Possible bug to avoid when porting 3b1b's idea: `int(PI/theta)` over-counts by one when `pi/theta` is an integer (equal masses). That matches the guard in his circle scene that clamps collision times above 300 s. `[UNVERIFIED]` that this is the reason for the guard; the over-count itself is `[VERIFIED: own run]`.

### Gaps
- Licences of the marimo notebook and of community p5 sketches were not checked.
- I did not find the Coding Train sketch for challenge 139 inside a licensed GitHub repo; only the p5 web-editor copy was read.
- `clack.wav` provenance (3b1b and Coding Train) unknown; a clack sound should be sourced or synthesized independently.
