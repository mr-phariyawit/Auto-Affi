# Concept backlog: counter-and-reveal maths/physics shorts in the "How many clacks?" template

Researcher notes, 2026-11-13. Evidence labels used throughout:

- **[RUN]** = number recomputed this session with a local Python script (exact arithmetic or direct simulation). Script: `/private/tmp/claude-501/-Users-phariyawit-jiap-Documents-Auto-Affi/60de24d6-1f6e-40c3-841c-2858e5ea0fc1/scratchpad/v.py` (temporary, not in repo).
- **[OPENED]** = source page was fetched or returned in search results this session.
- **[REF]** = standard reference URL given from prior knowledge; the page was NOT opened this session. The maths stated is textbook-standard, but the link itself and any YouTube video ID marked [REF] are unverified and should be click-checked before publishing.
- Difficulty (1-5), visual appeal, and saturation ratings are researcher judgement, not measurements.

## Key question 1: Which phenomena have a simple simulation plus a surprising number or shape as payoff? (ranked backlog, with per-concept implementation detail)

### Takeaway
37 candidates are listed below in three tiers. The closest matches to the clacks template are the ones with a **deterministic integer counter** whose final value is itself the reveal (lattice points in a circle giving 317 / 31,417 / 3,141,549; Tower of Hanoi 7 / 15 / 31; Moser's circle 8 / 16 / 31; Collatz 27 taking 111 steps; coprime pairs giving 0.6079 = 6/pi^2); probabilistic ones (darts, Buffon, Monty Hall) fit the format but need an on-screen "approximately" and a fixed random seed.

### Cited Findings

Baseline being cloned:
- Colliding blocks: with mass ratio 100^(d-1) the collision count equals the first d digits of pi; counts 3, 31, 314, 3141, 31415 for ratios 1, 100, 10^4, 10^6, 10^8 **[RUN]** — [3Blue1Brown lesson "clacks"](https://www.3blue1brown.com/lessons/clacks) [OPENED in search]; original paper G. Galperin, "Playing Pool with pi", Regular and Chaotic Dynamics 8:4 (2003) 375-394, as cited by [ThatsMaths](https://thatsmaths.com/2019/05/09/bouncing-billiard-balls-produce-pi/) [OPENED in search].

#### Tier A — deterministic counter, number IS the reveal (best template fit, easiest to keep correct)

1. **Lattice points in a circle (Gauss circle problem)** — RANK 1
   - Hook: "How many dots fit inside?"
   - Counter: integer grid points with x^2+y^2 <= r^2, lit up one by one (spiral or row sweep).
   - Rounds: r = 10, 100, 1000 → **317, 31,417, 3,141,549** **[RUN]**.
   - Reveal: count / r^2 → 3.17, 3.1417, 3.141549 → pi. Secondary diagram: the dot count shown as unit squares tiling the disc (area = pi r^2).
   - Difficulty 1. Appeal: high (same "digits of pi appear" beat as clacks). Saturation: low (judgement; no short found in search).
   - Ref: [Wikipedia: Gauss circle problem](https://en.wikipedia.org/wiki/Gauss_circle_problem) [REF].
2. **Tower of Hanoi** — RANK 2
   - Hook: "How many moves?" Counter: moves. Rounds: 3, 4, 5 discs → **7, 15, 31** (2^n - 1) **[RUN]**; flash 10 discs = 1023.
   - Reveal: always one less than a power of 2. Secondary diagram: binary counter ticking in sync (disc moved = bit flipped) .
   - Difficulty 2. Appeal: medium-high (satisfying motion). Saturation: medium.
   - Ref: [Wikipedia: Tower of Hanoi](https://en.wikipedia.org/wiki/Tower_of_Hanoi) [REF].
3. **Moser's circle problem (the pattern that breaks)** — RANK 3
   - Hook: "How many pieces?" Counter: regions when n points on a circle are fully connected.
   - Rounds: 4, 5, 6 points → **8, 16, 31** (not 32). Full sequence 1, 2, 4, 8, 16, 31, 57 **[RUN]** from 1 + C(n,2) + C(n,4).
   - Reveal: "32?" struck through → 31. Secondary diagram: the doubling row 1-2-4-8-16 with the 31 in red.
   - Difficulty 2 (region colouring via planar-graph faces, or precomputed polygons). Appeal: high (broken expectation). Saturation: low-medium.
   - Ref: [Wikipedia: Dividing a circle into areas](https://en.wikipedia.org/wiki/Dividing_a_circle_into_areas) [REF]; 3Blue1Brown has a long-form video on it [REF, URL not checked].
4. **Collatz / 3n+1 "hailstone"** — RANK 4
   - Hook: "How many steps to reach 1?" Counter: steps; second readout: current value.
   - Rounds: 9 → 19 steps; 97 → 118 steps; 871 → 178 steps (these are the longest under 10 / 100 / 1000) **[RUN]**. Alternative single-shock version: 6 → 8 steps, 7 → 16 steps, 27 → **111 steps, peak 9232** **[RUN]**.
   - Reveal: always ends 4-2-1. Secondary diagram: hailstone height graph (value vs step).
   - Difficulty 1. Appeal: medium-high. Saturation: medium-high (very popular topic).
   - Ref: [Wikipedia: Collatz conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture) [REF]; Veritasium "The Simplest Math Problem No One Can Solve" [REF, URL not checked].
5. **Coprime pairs → 6/pi^2**
   - Hook: "How many pairs share no factor?" Counter: coprime (a,b) in an N x N grid, cells lighting up.
   - Rounds: N = 10, 100, 1000 → **63, 6,087, 608,383** → fraction 0.63, 0.6087, 0.608383 **[RUN]**; limit 6/pi^2 = 0.6079271 **[RUN]**.
   - Reveal: pi appears with no circle anywhere. Secondary diagram: "visible from the origin" lattice-point picture.
   - Difficulty 1. Appeal: medium-high. Saturation: low.
   - Ref: [Wikipedia: Coprime integers (probability of coprimality)](https://en.wikipedia.org/wiki/Coprime_integers) [REF].
6. **Kaprekar's constant 6174**
   - Hook: "Where does every number end up?" Counter: iterations (sort digits descending minus ascending).
   - Rounds: three different 4-digit starts, e.g. 3524 reaches 6174 in 3 steps **[RUN]**; all 4-digit numbers with at least two distinct digits reach 6174 in **at most 7 steps**, none fail **[RUN]**.
   - Reveal: 6174 → 7641 - 1467 = 6174 (fixed point) **[RUN]**. Secondary diagram: tree of all starts funnelling to 6174.
   - Difficulty 1. Appeal: medium (digits only; needs strong motion design). Saturation: medium.
   - Ref: [Wikipedia: 6174](https://en.wikipedia.org/wiki/6174) [REF].
7. **Times-table cardioid on a circle (Mathologer)**
   - Hook: "What shape do the times tables draw?" Counter: lines drawn (point k joined to point m*k mod N).
   - Rounds: x2, x3, x4 with N = 200 points → cardioid (1 cusp), nephroid (2 cusps), 3-cusped epicycloid; multiplier m gives m-1 cusps.
   - Reveal: a heart from the 2-times table. Secondary diagram: light rays reflecting in a coffee cup (cardioid caustic).
   - Difficulty 1. Appeal: very high. Saturation: medium-high.
   - Ref: [The Coding Train challenge 133](https://thecodingtrain.com/challenges/133-time-tables-cardioid-visualization) [OPENED in search]; Mathologer "Times Tables, Mandelbrot and the Heart of Mathematics" (posted Christmas 2019 per search results; video URL not verified).
8. **Langton's ant**
   - Hook: "How many steps until order appears?" Counter: steps.
   - Rounds: 100 steps (symmetric), 1,000 (chaotic blob), ~11,000 (highway).
   - Reveal: after roughly 10,000 steps the ant builds a repeating diagonal "highway" with period 104; in my run the 104-step periodic displacement (2,2) held from step ~9,900 onward **[RUN]**. Secondary diagram: zoomed-out trail.
   - Difficulty 1. Appeal: high. Saturation: medium.
   - Ref: [Wikipedia: Langton's ant](https://en.wikipedia.org/wiki/Langton%27s_ant) [REF]; Coding Train challenge #89 [OPENED in search summary].
9. **Bouncing DVD logo corner hit**
   - Hook: "Will it hit the corner?" Counter: wall bounces (or seconds).
   - Rounds: three screen/logo size combinations with short, long, and "never" cycles.
   - Reveal: corner hit is predictable: with 45-degree unit-speed motion the logo returns to a corner state at lcm(W - w, H - h); worked example 16x10 screen, 4x2 logo → lcm(12, 8) = 24 **[RUN]** — [Lost Math Lessons blog](https://lostmathlessons.blogspot.com/2016/03/bouncing-dvd-logo.html) [OPENED in search]; [Wikipedia: DVD screensaver](https://en.wikipedia.org/wiki/DVD_screensaver) [OPENED in search]. Secondary diagram: unfolded-billiard grid with a straight diagonal line.
   - Difficulty 1. Appeal: high (nostalgia). Saturation: high as a meme, low as a maths reveal.
10. **Pendulum wave**
    - Hook: "When do they line up again?" Counter: seconds (or swings of the longest pendulum).
    - Rounds: 5, 10, 15 pendulums, or one continuous run with checkpoints at T/2 (two groups in antiphase) and T.
    - Reveal: all realign exactly at T. Harvard's apparatus: 15 pendulums, the longest makes 51 oscillations in 60 s, each next one makes one more, the 15th makes 65; all back in sync at 60 s — [Harvard Natural Sciences Lecture Demonstrations](https://sciencedemonstrations.fas.harvard.edu/presentations/pendulum-waves) [OPENED in search]. Ideal small-angle lengths for that tuning: 34.4 cm down to 21.2 cm **[RUN]**. For a 30 s clip rescale (e.g. N = 20..34 swings in 20 s).
    - Secondary diagram: top-down view of the bobs forming travelling/standing waves.
    - Difficulty 2 (pure sinusoids, no integration needed). Appeal: very high. Saturation: high for the physical demo, medium for coded versions.
11. **Sum of odd numbers = perfect squares**
    - Hook: "1 + 3 + 5 + ... = ?" Counter: running sum. Rounds: first 3, 10, 100 odd numbers → 9, 100, 10,000 **[RUN]**.
    - Reveal/diagram: L-shaped gnomons building a square. Difficulty 1. Appeal: medium. Saturation: medium. Ref: [Wikipedia: Square number](https://en.wikipedia.org/wiki/Square_number) [REF].
12. **Josephus problem**
    - Hook: "Who is the last one standing?" Counter: eliminations; reveal the survivor seat.
    - Rounds: n = 10, 41, 100 (every 2nd eliminated, seats numbered from 1) → survivors **5, 19, 73** **[RUN]** (formula 2L+1 where n = 2^m + L).
    - Secondary diagram: n in binary with the leading bit rotated to the end.
    - Difficulty 2. Appeal: medium-high. Saturation: medium. Ref: [Wikipedia: Josephus problem](https://en.wikipedia.org/wiki/Josephus_problem) [REF]; Numberphile "The Josephus Problem" [REF, URL not checked].
13. **Logistic map bifurcation**
    - Hook: "How many values does it settle on?" Counter: number of distinct long-run values.
    - Rounds: r = 2.8 → 1; r = 3.2 → 2; r = 3.5 → 4; then r = 3.9 → chaos. Second period-doubling at r = 1 + sqrt(6) = 3.4495 **[RUN]**.
    - Secondary diagram: the full bifurcation diagram being swept out.
    - Difficulty 1. Appeal: high. Saturation: medium. Ref: [Wikipedia: Logistic map](https://en.wikipedia.org/wiki/Logistic_map) [REF]; Veritasium "This equation will change how you see the world" [REF, URL not checked].
14. **Pascal's triangle mod 2 → Sierpinski triangle**
    - Hook: "Colour the odd numbers." Counter: rows. Rounds: 8, 32, 128 rows. Reveal: Sierpinski triangle. Difficulty 1. Appeal: high. Saturation: medium. Ref: [Wikipedia: Pascal's triangle](https://en.wikipedia.org/wiki/Pascal%27s_triangle) [REF].
15. **Ulam prime spiral**
    - Hook: "Where do the primes land?" Counter: primes found. Rounds: 10x10, 100x100, 400x400 spiral. Reveal: diagonal streaks. Difficulty 1. Appeal: medium-high. Saturation: medium. Ref: [Wikipedia: Ulam spiral](https://en.wikipedia.org/wiki/Ulam_spiral) [REF].
16. **Benford's law on powers of 2**
    - Hook: "How often does it start with 1?" Counter: leading-digit tallies for 2^1..2^n. Rounds: n = 10, 100, 1000.
    - Reveal: 30.1% start with 1 (301 of the first 1000 powers; log10(2) = 0.30103) **[RUN]**. Diagram: 9-bar histogram.
    - Difficulty 1. Appeal: medium. Saturation: low-medium. Ref: [Wikipedia: Benford's law](https://en.wikipedia.org/wiki/Benford%27s_law) [REF].
17. **Sorting algorithm race**
    - Hook: "How many comparisons?" Counter: comparisons. Rounds: bubble vs insertion vs quick/merge on the same shuffled bars.
    - Reveal: order-of-magnitude gap (n^2 vs n log n). Diagram: bar chart + audio pitch.
    - Difficulty 1. Appeal: high. Saturation: very high. Ref: Timo Bingmann, ["15 Sorting Algorithms in 6 Minutes"](https://www.youtube.com/watch?v=kPRA0W1kECg) [OPENED — title confirmed]; [Wikipedia: Sorting algorithm](https://en.wikipedia.org/wiki/Sorting_algorithm) [REF].
18. **Lissajous figures**
    - Hook: "What does 3:2 look like?" Counter: frequency ratio / lobes. Rounds: 1:1 (circle/ellipse), 1:2, 3:2 … irrational ratio never closes. Difficulty 1. Appeal: medium-high. Saturation: medium. Ref: [Wikipedia: Lissajous curve](https://en.wikipedia.org/wiki/Lissajous_curve) [REF].

#### Tier B — probabilistic or convergent (fits, but needs "approximately" on screen)

19. **Monte Carlo pi (darts in a circle)** — Hook: "How many land inside?" Counter: darts inside / total, and 4 x ratio. Rounds: 100, 10,000, 1,000,000 darts. Reveal: 4 x inside/total → pi. Diagram: quarter circle in a square. Difficulty 1. Appeal: medium-high. Saturation: high. Ref: [Wikipedia: Monte Carlo method](https://en.wikipedia.org/wiki/Monte_Carlo_method) [REF].
20. **Buffon's needle** — Hook: "How many cross a line?" Counter: crossings / drops. Rounds: 100, 1,000, 100,000 needles. Reveal: with needle length = line spacing, P(cross) = 2/pi = 0.6366 **[RUN]**, so 2 x drops / crossings → pi. Diagram: the angle-vs-distance rectangle with the sine curve. Difficulty 2. Appeal: high. Saturation: medium. Ref: [Wikipedia: Buffon's needle problem](https://en.wikipedia.org/wiki/Buffon%27s_needle_problem) [REF].
21. **Galton board** — Hook: "Where will the balls pile up?" Counter: balls dropped. Rounds: 10, 100, 3,000 balls. Reveal: bell curve; overlay binomial/normal curve. Difficulty 1 if each ball is a sequence of left/right coin flips animated on pegs, 3-4 if real rigid-body physics. Appeal: very high. Saturation: high. Ref: [Wikipedia: Galton board](https://en.wikipedia.org/wiki/Galton_board) [REF].
22. **Chaos game (Sierpinski)** — Hook: "Random dots. What appears?" Counter: points plotted. Rounds: 100, 1,000, 50,000. Reveal: Sierpinski triangle (dimension log 3 / log 2 = 1.585 **[RUN]**). Difficulty 1. Appeal: very high. Saturation: medium-high. Ref: [Wikipedia: Chaos game](https://en.wikipedia.org/wiki/Chaos_game) [REF]; [Coding Train chaos game topic](https://thecodingtrain.com/challenges/lang/all/topic/chaos-game) [OPENED in search].
23. **Birthday paradox** — Hook: "How many people until two share a birthday?" Counter: people entering a room. Rounds: 10, 23, 57 people → P(match) 11.7%, 50.7%, 99.0% **[RUN]** (365 equally likely days). Diagram: lines between all pairs (23 people = 253 pairs). Difficulty 1-2. Appeal: medium. Saturation: high. Ref: [Wikipedia: Birthday problem](https://en.wikipedia.org/wiki/Birthday_problem) [REF].
24. **100 prisoners (loop strategy)** — Hook: "Can all 100 find their number?" Counter: wins / trials. Rounds: random guessing (0 wins), loop strategy over 1,000 trials. Reveal: 31.18% success (1 - sum_{k=51}^{100} 1/k = 0.311828 **[RUN]**), limit 1 - ln 2 = 30.69% **[RUN]**. Diagram: permutation cycles drawn as loops; fail iff a loop is longer than 50. Difficulty 2. Appeal: medium-high. Saturation: medium (Veritasium made it famous). Hard to do language-free. Ref: [Veritasium video page](https://www.veritasium.com/videos/2022/7/5/the-riddle-that-seems-impossible-even-if-you-know-the-answer) [OPENED in search]; [Wikipedia: 100 prisoners problem](https://en.wikipedia.org/wiki/100_prisoners_problem) [REF].
25. **Monty Hall simulation** — Hook: "Stay or switch?" Counter: wins for stay vs switch. Rounds: 10, 100, 10,000 games. Reveal: 1/3 vs 2/3. Diagram: 3-branch tree. Difficulty 2. Appeal: medium. Saturation: very high. Needs rules text. Ref: [Wikipedia: Monty Hall problem](https://en.wikipedia.org/wiki/Monty_Hall_problem) [REF].
26. **e from random numbers** — Hook: "How many random numbers until the sum passes 1?" Counter: draws per trial, running average. Rounds: 10, 1,000, 200,000 trials. Reveal: average → e; my 200,000-trial run gave 2.7188 **[RUN]**. Diagram: stacked bars filling a unit tube. Difficulty 1. Appeal: medium. Saturation: low. Ref: [Wikipedia: e (mathematical constant)](https://en.wikipedia.org/wiki/E_(mathematical_constant)) [REF — the stochastic-representation section; not opened].
27. **Hat-check / derangements → 1/e** — Hook: "Does anyone get their own hat?" Counter: trials with zero matches. Reveal: fraction → 1/e = 0.3679 (already 0.36788 at n = 10) **[RUN]**. Difficulty 1. Appeal: medium. Saturation: low. Ref: [Wikipedia: Derangement](https://en.wikipedia.org/wiki/Derangement) [REF].
28. **Random walk returning home (Pólya)** — Hook: "Does it ever come home?" Counter: steps until return. Rounds: 1D, 2D, 3D. Reveal: return is certain in 1D and 2D, only about 34% in 3D. Difficulty 2. Appeal: medium. Saturation: low. Ref: [Wikipedia: Random walk](https://en.wikipedia.org/wiki/Random_walk) [REF].
29. **Basel problem** — Hook: "1 + 1/4 + 1/9 + ... = ?" Counter: partial sum. Rounds: 10, 100, 1,000 terms → 1.54977, 1.63498, 1.64393 **[RUN]**. Reveal: pi^2/6 = 1.644934 **[RUN]**. Diagram: shrinking squares of side 1/n stacked. Difficulty 1. Appeal: medium. Saturation: medium. Ref: [Wikipedia: Basel problem](https://en.wikipedia.org/wiki/Basel_problem) [REF]; 3Blue1Brown has a lighthouse-proof video [REF, URL not checked].
30. **Leibniz series for pi** — Counter: terms; 4 x partial sum at 10, 100, 1,000 terms = 3.04184, 3.13159, 3.14059 **[RUN]**. Difficulty 1. Appeal: low-medium. Ref: [Wikipedia: Leibniz formula for pi](https://en.wikipedia.org/wiki/Leibniz_formula_for_%CF%80) [REF].

#### Tier C — shape/motion reveal, weak or no counter (good variety pieces, less template-pure)

31. **Fourier epicycles drawing a shape** — Hook: "How many circles to draw this?" Counter: circles used (1, 10, 100). Reveal: recognisable outline. Difficulty 3 (needs a path + DFT). Appeal: very high. Saturation: high. Ref: 3Blue1Brown "But what is a Fourier series?" [REF, URL not checked]; Coding Train Fourier series challenge [OPENED in search summary].
32. **Double pendulum chaos** — Hook: "Same start. Same ending?" Counter: seconds until two (or 100) near-identical pendulums visibly diverge. Rounds: initial angle difference 1 degree, 0.01, 0.0001. Difficulty 3. Appeal: very high. Saturation: high. Ref: [Wikipedia: Double pendulum](https://en.wikipedia.org/wiki/Double_pendulum) [REF]; Coding Train challenge #93 [OPENED in search summary].
33. **Brachistochrone race / tautochrone** — Hook: "Which ramp wins?" Counter: stopwatch. Rounds: straight vs circular arc vs cycloid; then tautochrone: three start heights on a cycloid arrive together. Difficulty 3. Appeal: high. Saturation: medium. Ref: [Wikipedia: Brachistochrone curve](https://en.wikipedia.org/wiki/Brachistochrone_curve) [REF]; [Wikipedia: Tautochrone curve](https://en.wikipedia.org/wiki/Tautochrone_curve) [REF].
34. **Cycloid from a rolling circle** — Hook: "How big is the area under one arch?" Counter: circle-areas poured in. Reveal: exactly 3 circles; arch length = 8r. Difficulty 2. Appeal: medium-high. Saturation: low-medium. Ref: [Wikipedia: Cycloid](https://en.wikipedia.org/wiki/Cycloid) [REF].
35. **Golden-angle sunflower** — Hook: "Which angle packs best?" Counter: seeds. Rounds: 90 degrees (4 spokes), 137.0 (spirals with gaps), 137.508 (golden angle **[RUN]**) → even packing with Fibonacci spiral counts. Difficulty 1. Appeal: very high. Saturation: medium. Ref: [Wikipedia: Golden angle](https://en.wikipedia.org/wiki/Golden_angle) [REF].
36. **Newton's cradle** — Counter: balls out vs balls in (1, 2, 3). Reveal is intuitive rather than numerical. Difficulty 2. Appeal: medium. Saturation: high. Ref: [Wikipedia: Newton's cradle](https://en.wikipedia.org/wiki/Newton%27s_cradle) [REF].
37. **Balls bouncing in a circle / "Will the ball escape?"** — Proven viral format (see key question 3) but has no maths reveal; usable as a retention-style variant only. Ref: [Know Your Meme](https://knowyourmeme.com/memes/will-the-ball-escape-ball-bouncing-brainrot) [OPENED].
- Also considered and parked: Pythagorean water proof (famous as a physical demo; a coded fluid version is difficulty 4 and the "simulation" would be faked), Mandelbrot zoom (no counter), Abelian sandpile, Rule 30, dragon curve, Lorenz attractor.

### Inferences
- **Easiest to build first (difficulty 1, deterministic, one shared framework of "grid/number line + counter + three rounds + overlay diagram")**: lattice points in a circle, coprime pairs, Collatz, Kaprekar, sum of odds, Langton's ant, times-table cardioid, logistic map, Ulam spiral, Pascal mod 2, golden-angle sunflower.
- **Most visually striking**: pendulum wave, times-table cardioid, chaos game, golden-angle sunflower, Galton board, double pendulum, Fourier epicycles, Langton's ant.
- **Best overall (easy x striking x faithful to the "number reveal")**, suggested production order: (1) lattice points in a circle, (2) Tower of Hanoi, (3) Moser 31, (4) Collatz 27, (5) times-table cardioid, (6) pendulum wave, (7) Langton's ant, (8) coprime 6/pi^2, (9) chaos game, (10) Galton board.
- Lattice-points-in-a-circle is the nearest sibling of clacks: same "digits of pi appear in a count" beat and the same secondary diagram (a circle), but trivially cheap to simulate and free of floating-point risk.
- A series could be themed: "pi hides here" (clacks, lattice points, coprime pairs, Buffon, darts, Basel) and "the pattern breaks / order appears" (Moser, Langton, Collatz, logistic map).
- Concepts needing rules explained in words (Monty Hall, 100 prisoners, birthday, Josephus) are the weakest fit for a language-free format.

### Gaps
- The @mathmango1 TikTok itself was not found by search, so its exact on-screen structure, duration, and view count are unconfirmed here; the template description comes from the task brief only.
- Saturation ratings are judgement. No TikTok/Shorts search-volume or hashtag data was retrieved for any individual concept.
- Wikipedia/MathWorld/Cut-the-Knot pages marked [REF] were not opened this session; MathWorld and Cut-the-Knot were not consulted at all.
- Specific YouTube URLs for Mathologer, 3Blue1Brown (Fourier, Basel, Moser), Numberphile (Josephus), and Veritasium (Collatz, logistic map) were not verified; only titles are given.
- The Coding Train full challenge list was not opened; only challenges #89 (Langton's ant), #93 (double pendulum), #133 (times tables) and the chaos game were confirmed via search summaries, and the summary noted inconsistent episode numbering across mirror sites.

## Key question 2: Per-concept spec fields (hook, counter, 3-round escalation, reveal, secondary diagram, difficulty, appeal, saturation, primary reference)

### Takeaway
All nine fields are filled per concept in the ranked list under key question 1 (kept in one place to avoid duplication); the summary table below is the quick-scan version for the top 12.

### Cited Findings
Sources for each row are the per-concept references given under key question 1. Numbers marked [RUN] there were recomputed this session.

| # | Concept | Counter | Round 1 → 2 → 3 | Reveal | Diff | Appeal | Saturation |
|---|---|---|---|---|---|---|---|
| 1 | Lattice points in circle | dots inside | r=10 → 100 → 1000: 317 → 31,417 → 3,141,549 | count/r^2 → pi | 1 | high | low |
| 2 | Tower of Hanoi | moves | 3 → 4 → 5 discs: 7 → 15 → 31 | 2^n - 1 | 2 | med-high | medium |
| 3 | Moser's circle | regions | 4 → 5 → 6 points: 8 → 16 → 31 | not 32 | 2 | high | low-med |
| 4 | Collatz | steps | 9 → 97 → 871: 19 → 118 → 178 | always 4-2-1 | 1 | med-high | med-high |
| 5 | Times-table cardioid | lines | x2 → x3 → x4 | 1, 2, 3 cusps | 1 | very high | med-high |
| 6 | Pendulum wave | seconds | checkpoints T/3, T/2, T | all realign at T | 2 | very high | high (physical) |
| 7 | Langton's ant | steps | 100 → 1,000 → 11,000 | highway, period 104 | 1 | high | medium |
| 8 | Coprime pairs | coprime cells | N=10 → 100 → 1000: 63 → 6,087 → 608,383 | 6/pi^2 = 0.6079 | 1 | med-high | low |
| 9 | Chaos game | points | 100 → 1,000 → 50,000 | Sierpinski triangle | 1 | very high | med-high |
| 10 | Galton board | balls | 10 → 100 → 3,000 | bell curve | 1-4 | very high | high |
| 11 | Kaprekar 6174 | iterations | three different starts | all hit 6174 in <= 7 | 1 | medium | medium |
| 12 | DVD corner hit | bounces | three screen sizes | lcm(W-w, H-h) | 1 | high | high (meme) |

- Colliding-blocks reference counts for calibrating the series opener: 3, 31, 314 at mass ratios 1, 100, 10,000 — [3Blue1Brown](https://www.3blue1brown.com/lessons/clacks) [OPENED in search]; reproduced **[RUN]**.

### Inferences
- A single framework needs only five reusable parts: (a) title/question card, (b) integer counter with tick sound, (c) round controller with a speed-up curve (rounds 2-3 must be time-compressed: e.g. 3,141,549 dots cannot be shown one by one), (d) main canvas, (e) secondary-diagram overlay. Every Tier A concept maps onto these.
- Round 3 in almost every concept needs fast-forward; the counter should keep ticking audibly while the visual batches updates, as the clacks video does.

### Gaps
- Target duration fit (20-40 s) per concept was not prototyped; timing is untested.
- No rendering or code was produced; difficulty scores are estimates.

## Key question 3: Which concepts have verified examples of going viral as shorts (URLs and observed counts)?

### Takeaway
Hard, sourced view counts were found only for the "ball bouncing in a circle" Shorts genre (up to ~67 million views on one Short) and for long-form originals (Veritasium 100 prisoners ~18M, 3Blue1Brown colliding blocks ~5M, Bingmann sorting >1M by 2014); **no verified TikTok/Shorts view or like counts were obtained for any of the maths-reveal concepts**, including the @mathmango1 clip.

### Cited Findings
- "Will the Ball Escape? / Ball Bouncing Brainrot" is a documented YouTube Shorts genre that first went viral in November 2023 — [Know Your Meme](https://knowyourmeme.com/memes/will-the-ball-escape-ball-bouncing-brainrot) [OPENED].
- Examples and counts as reported by Know Your Meme (snapshot from roughly early-to-mid 2024, not re-checked on YouTube; no like counts given) — [Know Your Meme](https://knowyourmeme.com/memes/will-the-ball-escape-ball-bouncing-brainrot):
  - satisfying.ba11s, 7 Nov 2023, square in shrinking square: ~191,000 views in five months — https://www.youtube.com/watch?v=mUns7QevB2g
  - Jack's Physics, 28 Nov 2023, ball grows and speeds up each bounce: ~945,000 views in five months — https://www.youtube.com/watch?v=GPJqda-ThrY
  - satisfying.ba11s (spelled "ba11ls" in the entry), 29 Nov 2023, bounces play Crystal Castles "Kerosene": ~38 million views in five months — https://www.youtube.com/watch?v=rgjeRfHFjms
  - satisfying.ba11s, 28 Dec 2023: ~67 million views in four months — https://www.youtube.com/watch?v=Peo-DIOmmRo
  - CodeCraftedPhysics, 26 Jan 2024, "Will the ball manage to escape this time?": ~4.4 million views in three months (the entry's footnote URL appears to be a citation error, so no reliable link).
- A blogger reports seeing "a popular video on TikTok" demonstrating the colliding-blocks pi computation (no creator named, no counts) — [mattmcal blog, Sept 2024](https://mattmcal.blogspot.com/2024/09/between-block-and-hard-place.html) [OPENED in search snippet only].
- 3Blue1Brown "Why colliding blocks compute pi" (long-form): 5.2M views per an undated third-party aggregator snapshot — [rosetta.to](https://rosetta.to/u/3blue1brown/why-colliding-blocks-compute-pi) [OPENED in search snippet]. This is the follow-up explainer; the count for the original puzzle video was not retrieved.
- Veritasium "The Riddle That Seems Impossible Even If You Know The Answer" (100 prisoners, long-form, published 30 June 2022): 18.2M-18.5M views per aggregator snapshots — [rosetta.to](https://rosetta.to/u/veritasium/the-riddle-that-seems-impossible-even-if-you-know-the-answer) [OPENED in search snippet].
- Timo Bingmann "15 Sorting Algorithms in 6 Minutes" passed 1 million views in October 2014, with views arriving "in spikes" — [panthema.net, author's own blog](https://panthema.net/2014/1026-1.000.000-Views-of-Sound-of-Sorting-YouTube-Video/) [OPENED in search snippet]. Current count not retrieved.
- A creator experiment ("I Used Code to Go Viral on Social Media", Green Code) posting ball simulations plus maze and sorting videos reported 16,216 TikTok views and 6 followers after one week; most-viewed videos were those with more editing and voice — [Recapio digest](https://recapio.com/digest/i-used-code-to-go-viral-on-social-media-by-green-code) [OPENED in search snippet; this is an AI-generated secondary summary, not the original video — low reliability].
- Harvard's pendulum-wave demonstration video exists at https://www.youtube.com/watch?v=yVkdfJ9PkRQ (title "Pendulum Waves" confirmed by fetch); view count could not be read.

### Inferences
- The only format with hard evidence of tens-of-millions Shorts performance is the no-maths "satisfying bounce + melody" simulation. The clacks-style "counter + numerical reveal" format has anecdotal evidence only (the brief's @mathmango1 clip and one blog mention).
- The Green Code data point (16K views in a week from a new account) is a caution that code-generated simulations do not go viral by default; that source is weak, so treat it as a caution rather than a benchmark.
- Borrowing the proven retention devices from the bounce genre (a sound per event that speeds up, escalating density) is consistent with what the clacks format already does with its clack sound.

### Gaps
- YouTube watch pages returned no metadata to the fetch tool (three attempts), so no live view/like counts were verified for any video. All counts above are third-party snapshots with unknown or old dates.
- TikTok could not be searched or read with the available tools; zero TikTok view/like counts were verified. The @mathmango1 clip's numbers are unknown.
- No verified viral short was found for: Galton board, Monte Carlo pi, Buffon's needle, Collatz, Kaprekar, times-table cardioid, Langton's ant, chaos game, double pendulum, pendulum wave (coded), DVD logo, Tower of Hanoi, Moser's circle, lattice points. Absence here means "not found in 15 tool calls", not "does not exist". A manual pass in the TikTok/YouTube apps is needed.

## Key question 4: Which concepts are mathematically delicate, and what must be stated on screen to stay correct?

### Takeaway
The main risks are (a) floating-point or time-stepping errors silently changing a count, (b) presenting a probabilistic estimate or slow-converging sum as if it produced exact digits, and (c) overclaiming unproven statements (Collatz, and the clacks digit pattern for all mass ratios).

### Cited Findings
- **Colliding blocks**: the digits-of-pi count holds for mass ratios that are powers of 100 with perfectly elastic collisions and no friction — [3Blue1Brown](https://www.3blue1brown.com/lessons/clacks); Galperin 2003 via [ThatsMaths](https://thatsmaths.com/2019/05/09/bouncing-billiard-balls-produce-pi/). A secondary source in search results notes that the pattern's validity for every power is not fully proven (it depends on a property of pi's digits) — search summary of the 3Blue1Brown material, not independently verified. Event-driven simulation in double precision reproduced 3, 31, 314, 3141, 31415 **[RUN]**; a fixed-timestep simulation will miss collisions at high mass ratios. On screen: "elastic collisions, no friction".
- **Lattice points in a circle**: the counts 317 / 31,417 / 3,141,549 are exact integers **[RUN]**, but they approximate pi r^2 — they are not literally "the digits of pi" (317, not 314). On screen: "count ÷ r^2 → pi" or "approximately". Ref: [Wikipedia: Gauss circle problem](https://en.wikipedia.org/wiki/Gauss_circle_problem) [REF].
- **Collatz**: that every start reaches 1 is an unproven conjecture — [Wikipedia: Collatz conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture) [REF]. Do not write "always"; write "every number ever tested". Step counts depend on convention (I counted each halving and each 3n+1 as one step: 27 → 111 steps, peak 9232 **[RUN]**).
- **Moser's circle**: 31 requires points in general position (no three chords through one interior point); six equally spaced points give 30 regions, not 31 — [Wikipedia: Dividing a circle into areas](https://en.wikipedia.org/wiki/Dividing_a_circle_into_areas) [REF; the 30-for-regular-hexagon fact is from memory, not re-derived this session]. Place points irregularly.
- **Kaprekar 6174**: holds for 4-digit numbers with at least two different digits, keeping leading zeros (e.g. 0999); repdigits like 1111 give 0 — verified for all 4-digit inputs, max 7 steps **[RUN]**; [Wikipedia: 6174](https://en.wikipedia.org/wiki/6174) [REF].
- **Langton's ant**: the highway after about 10,000 steps is observed for the empty starting grid; that it emerges from every finite starting pattern is unproven — [Wikipedia: Langton's ant](https://en.wikipedia.org/wiki/Langton%27s_ant) [REF]. Do not print an exact "step 10,000"; my detection found steady 104-periodicity from about step 9,900 **[RUN]**, and the exact figure depends on how onset is defined.
- **DVD logo**: the lcm rule assumes 45-degree motion at equal integer speed in x and y and integer dimensions; with other speed ratios the logo may never hit a corner exactly — [Lost Math Lessons](https://lostmathlessons.blogspot.com/2016/03/bouncing-dvd-logo.html) [OPENED in search]; the "never, if the ratio is irrational" statement came from a hobbyist page flagged as non-rigorous in search results. Use integer pixel arithmetic, not floats.
- **Pendulum wave**: exact realignment at T requires each pendulum to complete a whole number of oscillations in T — [Harvard demo page](https://sciencedemonstrations.fas.harvard.edu/presentations/pendulum-waves) [OPENED in search]. Simulate with exact sinusoids of the chosen frequencies; integrating real pendulum equations at visible amplitudes will drift because the period depends on amplitude.
- **Monte Carlo pi / Buffon's needle**: results are random estimates. Buffon's P = 2/pi applies only when needle length equals line spacing (general short-needle case 2l/(pi d)) — [Wikipedia: Buffon's needle problem](https://en.wikipedia.org/wiki/Buffon%27s_needle_problem) [REF]. On screen: "≈", show the trial count, and fix the random seed so the published number is reproducible.
- **Birthday paradox**: 50.7% at 23 people assumes 365 equally likely birthdays, no leap day **[RUN]** — [Wikipedia: Birthday problem](https://en.wikipedia.org/wiki/Birthday_problem) [REF].
- **100 prisoners**: 31.18% is the exact probability for 100 prisoners / 50 openings with the loop strategy **[RUN]**; a simulated win rate will fluctuate around it — [Wikipedia: 100 prisoners problem](https://en.wikipedia.org/wiki/100_prisoners_problem) [REF].
- **Monty Hall**: 2/3 requires that the host knows where the prize is and always opens an empty door — [Wikipedia: Monty Hall problem](https://en.wikipedia.org/wiki/Monty_Hall_problem) [REF].
- **Random walk**: return is certain in 1D and 2D (but expected return time is infinite, so a simulation can run very long); about 34% in 3D — [Wikipedia: Random walk](https://en.wikipedia.org/wiki/Random_walk) [REF]. A finite simulation cannot show "never returns"; cap the steps and label it.
- **Basel and Leibniz series**: convergence is slow — 1,000 terms give 1.64393 vs 1.64493 (Basel) and 3.14059 vs 3.14159 (Leibniz) **[RUN]**. Show "→" not "=" for partial sums. Refs: [Basel problem](https://en.wikipedia.org/wiki/Basel_problem), [Leibniz formula](https://en.wikipedia.org/wiki/Leibniz_formula_for_%CF%80) [REF].
- **Benford on powers of 2**: 301 of the first 1,000 powers of 2 start with 1 **[RUN]**; needs big-integer arithmetic (floats lose the leading digit pattern for large exponents). Ref: [Wikipedia: Benford's law](https://en.wikipedia.org/wiki/Benford%27s_law) [REF].
- **Double pendulum**: chaotic; trajectories from any integrator diverge from the true solution after a short time, so the video can truthfully show "tiny differences grow" but not "this is the exact path" — [Wikipedia: Double pendulum](https://en.wikipedia.org/wiki/Double_pendulum) [REF]. Use RK4 or a symplectic integrator with a small step and check energy drift.
- **Logistic map**: cycle counts (1, 2, 4) need burn-in iterations discarded before counting; near bifurcation points (r = 3, r = 3.4495 **[RUN]**) convergence is very slow, so pick r values well inside each window — [Wikipedia: Logistic map](https://en.wikipedia.org/wiki/Logistic_map) [REF].
- **Brachistochrone / tautochrone**: valid for a frictionless sliding bead; a rolling ball changes the times (though not the cycloid's optimality in the ideal model) — [Wikipedia: Brachistochrone curve](https://en.wikipedia.org/wiki/Brachistochrone_curve) [REF].

### Inferences
- Statistical error for the estimators, derived from binomial variance (my derivation, not from a source): darts estimate has standard deviation about 1.64/sqrt(N); Buffon (l = d) about 2.37/sqrt(N). So 1,000,000 darts typically give 3.14 with the third decimal uncertain (sd ≈ 0.0016), and 100,000 needles give sd ≈ 0.0075. The on-screen reveal should stop at the digits the sample size supports (e.g. "≈ 3.14").
- Safest concepts (integer arithmetic only, fully deterministic, proven): Tower of Hanoi, sum of odds, Kaprekar, coprime pairs, lattice points, Pascal mod 2, Josephus, Ulam spiral, times-table cardioid.
- General rule for the framework: compute the counter from exact integer/event-driven logic and treat the animation as a playback of that result, never derive the count from the rendered frames.
- For every probabilistic concept, pre-run with a fixed seed and pick the seed before rendering; do not cherry-pick a seed that happens to give "3.14159", as that would misrepresent the convergence.

### Gaps
- The claim that the clacks digit pattern is not rigorously proven for all powers of 100 comes from a search-result summary of a secondary source; the primary statement (Galperin's paper or the 3Blue1Brown follow-up) was not opened.
- The 3D random-walk return probability (~0.3405) and the "regular hexagon gives 30 regions" fact were not recomputed or source-checked this session.
- Rolling-vs-sliding behaviour on the brachistochrone was not source-checked; if that video is made, verify before stating anything about real balls.
- MathWorld and Cut-the-Knot were suggested sources but were not consulted.
