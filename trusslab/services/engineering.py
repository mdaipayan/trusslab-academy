"""Small, testable calculations used by the educational sandboxes."""
from __future__ import annotations

from math import isfinite


def solve_indeterminate_triangle_areas(areas_mm2: tuple[float, float, float]) -> dict[str, float]:
    """Use the redundant-reaction equation reported in the supplied triangle notes.

    Area ordering is A1=AB, A2=AC, A3=BC. Areas are in mm²; forces are returned in kN.
    This function reproduces the source equation, not an independent DSM re-analysis.
    """
    if len(areas_mm2) != 3:
        raise ValueError("Exactly three areas are required: AB, AC and BC.")
    if any(not isfinite(float(area)) or float(area) <= 0 for area in areas_mm2):
        raise ValueError("Areas must be finite and positive.")
    a1, a2, a3 = (float(area) for area in areas_mm2)
    numerator = 80000.0 / a1 - 11250.0 / a2 + 156250.0 / a3
    denominator = 4000.0 / a1 + 1687.5 / a2 + 7812.5 / a3
    if denominator <= 0 or not isfinite(denominator):
        raise ValueError("The flexibility denominator must be finite and positive.")
    reaction = -numerator / denominator
    result = {
        "R": reaction,
        "F_AB": 20.0 + reaction,
        "F_AC": 0.75 * reaction - 5.0,
        "F_BC": -1.25 * (20.0 + reaction),
    }
    if not all(isfinite(value) for value in result.values()):
        raise ValueError("The selected areas exceed the supported numeric range; use realistic positive areas in mm².")
    return result



def solve_vertical_load_truss_compatibility(areas_mm2: tuple[float, float, float]) -> dict[str, float | dict[str, float]]:
    """Solve a 3-4-5 pin-jointed truss with a 10 kN downward joint-C load.

    A=(0,0), B=(4,0), C=(0,3) m. A is a pin, B is a vertical roller,
    and C has a horizontal redundant reaction R. A positive member force is
    tension; R positive means rightward. All members share the same E, which
    cancels from the force-method ratio. Areas are AB, AC, BC in mm².
    The released primary forces are (0, -10, 0) kN and unit-load member
    forces are (1, 0.75, -1.25), with lengths (4, 3, 5) m.
    """
    if len(areas_mm2) != 3:
        raise ValueError("Exactly three areas are required: AB, AC and BC.")
    if any(not isfinite(float(area)) or float(area) <= 0 for area in areas_mm2):
        raise ValueError("Areas must be finite and positive.")
    a_ab, a_ac, a_bc = (float(area) for area in areas_mm2)
    # Common E omitted because it cancels from numerator and denominator.
    numerator = (-10.0 * 0.75 * 3.0) / a_ac
    denominator = (1.0**2 * 4.0) / a_ab + (0.75**2 * 3.0) / a_ac + ((-1.25)**2 * 5.0) / a_bc
    if denominator <= 0 or not isfinite(denominator):
        raise ValueError("The flexibility denominator must be finite and positive.")
    reaction = -numerator / denominator
    result = {
        "R": reaction,
        "F_AB": reaction,
        "F_AC": -10.0 + 0.75 * reaction,
        "F_BC": -1.25 * reaction,
        "compatibility_terms": {"numerator": numerator, "denominator": denominator},
    }
    numeric_outputs = [reaction, result["F_AB"], result["F_AC"], result["F_BC"], numerator, denominator]
    if not all(isfinite(value) for value in numeric_outputs):
        raise ValueError("The selected areas exceed the supported numeric range; use realistic positive areas in mm².")
    return result


def single_member_sizing(area_mm2: float, load_kn: float, length_m: float,
                         allowable_stress_mpa: float, density_kg_m3: float = 7850.0) -> dict[str, float | bool]:
    """Compute stress and material mass for a single axial member sandbox.

    This is a didactic sizing illustration, not a truss design/code check.
    """
    values = (area_mm2, load_kn, length_m, allowable_stress_mpa, density_kg_m3)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("Sizing inputs must be finite.")
    if area_mm2 <= 0 or load_kn < 0 or length_m <= 0 or allowable_stress_mpa <= 0 or density_kg_m3 <= 0:
        raise ValueError("Area, length, allowable stress and density must be positive; load cannot be negative.")
    stress = load_kn * 1000.0 / area_mm2  # kN -> N; N/mm² = MPa
    volume_m3 = area_mm2 * 1e-6 * length_m
    mass_kg = density_kg_m3 * volume_m3
    if not all(isfinite(value) for value in (stress, volume_m3, mass_kg)):
        raise ValueError("The inputs exceed the supported numeric range; use realistic engineering values and consistent units.")
    return {
        "stress_mpa": stress,
        "volume_m3": volume_m3,
        "mass_kg": mass_kg,
        "feasible_by_stress": stress <= allowable_stress_mpa,
    }
