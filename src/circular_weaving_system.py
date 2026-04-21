
"""
Inputs:
- base_center  → base location of the system
- radius       → initial circle radius
- ampli        → vertical spacing between circles
- count        → number of circle layers (>= 2)
- num_seg      → number of divisions per circle (>= 3)
- min_scale    → minimum scale factor
- max_scale    → maximum scale factor
- rand_amp     → randomness amplitude (>= 0)
- seed         → random seed for reproducibility
"""

import Grasshopper as ghc
import ghpythonlib.components as gh
import random

# Seed control (optional reproducibility)
if seed is not None:
    random.seed(seed)


# ---------------------------------------------
# 1. Generate Circles
# ---------------------------------------------
def create_circles(base_center, radius, ampli, count):
    """Create vertically stacked circles."""
    if count < 2:
        raise ValueError("count must be at least 2")

    circle = gh.Circle(gh.XYPlane(base_center), radius)
    dup_circles = gh.LinearArray(circle, gh.UnitZ(ampli), count)[0]
    return dup_circles


# ---------------------------------------------
# 2. Scale Circles
# ---------------------------------------------
def scale_circles(circles, min_scale, max_scale, rand_amp):
    """Randomly scale each circle around its center."""
    
    if rand_amp < 0:
        raise ValueError("rand_amp must be >= 0")

    scaled = []

    for i, crc in enumerate(circles):
        n = len(circles) - 1
        t = i / float(n) if n > 0 else 0

        factor = (min_scale + (max_scale - min_scale) * t) * \
                 random.uniform(1 - rand_amp, 1 + rand_amp)

        area = gh.Area(crc)
        center = area[1]

        scaled.append(gh.Scale(crc, center, factor)[0])

    return scaled


# ---------------------------------------------
# 3. Divide Circles
# ---------------------------------------------
def divide_circles(scaled_circles, num_seg):
    """Divide circles into points stored in a DataTree."""
    
    if num_seg < 3:
        raise ValueError("num_seg must be at least 3")

    points = ghc.DataTree[object]()

    for i, crv in enumerate(scaled_circles):
        path = ghc.Kernel.Data.GH_Path(i)
        pts = gh.DivideCurve(crv, num_seg, False)[0]

        for pt in pts:
            points.Add(pt, path)

    return points


# ---------------------------------------------
# 4. Shift Lists
# ---------------------------------------------
def shift_lists(points):
    """Shift each branch and its reversed version."""
    
    shifted = ghc.DataTree[object]()
    reversed_shifted = ghc.DataTree[object]()

    for i in range(points.BranchCount):
        path = points.Path(i)
        branch = points.Branch(i)

        forward = gh.ShiftList(branch, i, True)
        backward = gh.ShiftList(gh.ReverseList(branch), i, True)

        for pt in forward:
            shifted.Add(pt, path)

        for pt in backward:
            reversed_shifted.Add(pt, path)

    return shifted, reversed_shifted


# ---------------------------------------------
# 5. Transpose Tree (Matrix Flip)
# ---------------------------------------------
def transpose_tree(tree):
    """Transpose DataTree (rows → columns)."""
    
    flipped = ghc.DataTree[object]()

    for i in range(tree.BranchCount):
        for j, item in enumerate(tree.Branch(i)):
            path = ghc.Kernel.Data.GH_Path(j)
            flipped.Add(item, path)

    return flipped


# ---------------------------------------------
# 6. Generate NURBS Curves
# ---------------------------------------------
def generate_curves(tree):
    """Interpolate curves from each branch."""
    
    curves = []

    for i in range(tree.BranchCount):
        curves.append(gh.Interpolate(tree.Branch(i), 3, False, 1)[0])

    return curves


# =============================================
# MAIN PIPELINE
# =============================================

circles = create_circles(base_center, radius, ampli, count)

scaled_circles = scale_circles(circles, min_scale, max_scale, rand_amp)

points = divide_circles(scaled_circles, num_seg)

shifted, reversed_shifted = shift_lists(points)

flipped = transpose_tree(shifted)
flipped_rev = transpose_tree(reversed_shifted)

crvs = generate_curves(flipped)
rev_crvs = generate_curves(flipped_rev)

outline = scaled_circles[:1] + scaled_circles[-1:]

