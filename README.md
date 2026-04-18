## Overview

The system creates a layered circular structure where curves are generated through controlled scaling, data tree manipulation, and interpolation. The result is a woven network of NURBS curves
---

## Workflow

- Circle generation
- Parametric scaling (gradient + controlled randomness)
- Curve division into data trees
- List shifting and reversal
- Data tree transposition (matrix logic)
- Curve interpolation
 
---

## Parameters

 base_center → Base point of the system 

 radius      → Initial circle radius 

 ampli       → Vertical spacing between circles 

 count       → Number of circle layers 

 num_seg     → Division count per circle 

 min_scale   → Minimum scale factor 

 max_scale   → Maximum scale factor 

 rand_amp    → Random variation amplitude 

 seed        → Random seed (optional) 

---

## Outputs

 crvs      → Main woven curves 

 rev_crvs  → Secondary (reverse) curve system 

 outline   → Boundary circles 
