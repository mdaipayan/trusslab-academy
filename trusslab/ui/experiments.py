"""Module-specific, inspectable what-if experiments."""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from trusslab.domain.models import LessonModule
from trusslab.services.engineering import single_member_sizing, solve_indeterminate_triangle_areas, solve_vertical_load_truss_compatibility


class ExperimentRenderer:
    """Render the small experiment attached to a lesson, when available."""

    @classmethod
    def render(cls, module: LessonModule) -> None:
        handlers = {
            "determinate_area": cls.determinate_area,
            "truss_compatibility": cls.truss_compatibility,
            "indeterminate_triangle": cls.indeterminate_triangle,
            "force_method_audit": cls.force_method_audit,
            "optimization_sandbox": cls.optimization_sandbox,
        }
        if module.experiment_id:
            handlers[module.experiment_id]()

    @staticmethod
    def determinate_area() -> None:
        st.markdown("### Mini-lab · Change area, observe stress")
        st.caption("Source setup: AB carries 20 kN in the ideal determinate example. Change only the cross-sectional area.")
        area = st.slider("Area of AB (mm²)", 500, 2000, 1000, 100, key="exp_determinate_area")
        force_kn = 20.0
        stress = force_kn * 1000.0 / area
        a, b = st.columns(2)
        a.metric("F_AB · member force", f"{force_kn:.1f} kN", "fixed by equilibrium")
        b.metric("Normal stress", f"{stress:.1f} MPa", f"{stress / 20.0:.1f}× vs. 1000 mm²")
        areas = np.arange(500, 2001, 100)
        stresses = force_kn * 1000.0 / areas
        fig = go.Figure(go.Scatter(x=areas, y=stresses, mode="lines+markers",
                                   line={"color": "#0d9488", "width": 3},
                                   hovertemplate="Area = %{x} mm²<br>Stress = %{y:.1f} MPa<extra></extra>"))
        fig.add_trace(go.Scatter(x=[area], y=[stress], mode="markers", marker={"size": 12, "color": "#d18b14"}, name="Selected area"))
        fig.update_layout(title="Stress falls as area rises for a fixed force", xaxis_title="Area (mm²)", yaxis_title="Stress (MPa)", height=300, margin={"l": 10, "r": 10, "t": 55, "b": 20}, paper_bgcolor="#fff", plot_bgcolor="#fff")
        st.plotly_chart(fig, width="stretch", config={"displaylogo": False})
        st.info("Stress = F/A. This simplified experiment fixes the ideal determinate member force; it does not assess buckling or code compliance.")

    @staticmethod
    def truss_compatibility() -> None:
        st.markdown("### Mini-lab · Change truss member areas")
        st.caption("Real pin-jointed 3–4–5 truss. P = 10 kN acts downward at joint C; A is pinned, B is a vertical roller, and C has a horizontal guide. The force-method calculation assumes the same E for every member; E cancels from the redundant-reaction ratio.")
        columns = st.columns(3)
        area_ab = columns[0].slider("Area AB (mm²)", 500, 4000, 1000, 250, key="exp_truss_compat_ab")
        area_ac = columns[1].slider("Area AC (mm²)", 500, 4000, 1000, 250, key="exp_truss_compat_ac")
        area_bc = columns[2].slider("Area BC (mm²)", 500, 4000, 1000, 250, key="exp_truss_compat_bc")
        response = solve_vertical_load_truss_compatibility((area_ab, area_ac, area_bc))
        st.metric("Horizontal redundant reaction R", f"{response['R']:.3f} kN", help="Positive means the support reaction is to the right under the displayed convention.")
        rows = []
        for member, area, key in (("AB", area_ab, "F_AB"), ("AC", area_ac, "F_AC"), ("BC", area_bc, "F_BC")):
            force = response[key]
            rows.append({"Member": member, "Area (mm²)": area, "Member force F (kN)": round(force, 3), "Nature": "Tension" if force > 1e-8 else "Compression" if force < -1e-8 else "Zero"})
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
        terms = response["compatibility_terms"]
        st.markdown("**Compatibility calculation**")
        st.latex(r"R=-\frac{\sum_i F_i^{(0)}n_iL_i/(EA_i)}{\sum_i n_i^2L_i/(EA_i)}")
        st.caption(f"For the selected areas, the common E cancels. Flexibility denominator = {terms['denominator']:.6g} (length/area units); released-truss displacement numerator = {terms['numerator']:.6g} (force × length/area units).")
        fig = go.Figure(go.Bar(x=[row["Member"] for row in rows], y=[row["Member force F (kN)"] for row in rows],
                               marker_color=["#16845a" if row["Member force F (kN)"] >= 0 else "#c43c4b" for row in rows],
                               text=[f"{row['Member force F (kN)']:.3f}" for row in rows], textposition="outside",
                               hovertemplate="%{x}<br>Signed member force F = %{y:.3f} kN<extra></extra>"))
        fig.update_layout(title="Member force F under the selected areas", yaxis_title="Signed member force F (kN)", height=300,
                          margin={"l": 10, "r": 10, "t": 55, "b": 20}, paper_bgcolor="#fff", plot_bgcolor="#fff")
        st.plotly_chart(fig, width="stretch", config={"displaylogo": False})
        st.info("This is a truss force-method model: loads act at joints and members carry axial force. Positive force is tension; negative force is compression. The model is educational and does not check buckling or design-code requirements.")

    @staticmethod
    def indeterminate_triangle() -> None:
        st.markdown("### Mini-lab · Change one area, watch forces redistribute")
        st.caption("This demonstrator reproduces the supplied PDF's redundant-reaction equation. A₁ = AB, A₂ = AC, A₃ = BC; areas in mm², forces in kN.")
        columns = st.columns(3)
        area1 = columns[0].slider("A₁ · AB (mm²)", 500, 4000, 1000, 500, key="exp_ind_a1")
        area2 = columns[1].slider("A₂ · AC (mm²)", 500, 4000, 1000, 500, key="exp_ind_a2")
        area3 = columns[2].slider("A₃ · BC (mm²)", 500, 4000, 1000, 500, key="exp_ind_a3")
        response = solve_indeterminate_triangle_areas((area1, area2, area3))
        st.metric("Redundant reaction R = Cₓ", f"{response['R']:.3f} kN")
        rows = []
        for key, area in (("F_AB", area1), ("F_AC", area2), ("F_BC", area3)):
            force = response[key]
            rows.append({"Member": key.replace("F_", ""), "Area (mm²)": area, "Signed member force F (kN)": round(force, 3), "Nature": "Tension" if force > 1e-8 else "Compression" if force < -1e-8 else "Zero"})
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
        fig = go.Figure(go.Bar(x=[row["Member"] for row in rows], y=[row["Signed member force F (kN)"] for row in rows], marker_color=["#16845a" if row["Signed member force F (kN)"] >= 0 else "#c43c4b" for row in rows], text=[f"{row['Signed member force F (kN)']:.3f}" for row in rows], textposition="outside", hovertemplate="%{x}<br>Signed member force F = %{y:.3f} kN<extra></extra>"))
        fig.update_layout(title="Signed member force F under the selected areas", yaxis_title="Member force F (kN)", height=300, margin={"l": 10, "r": 10, "t": 55, "b": 20}, paper_bgcolor="#fff", plot_bgcolor="#fff")
        st.plotly_chart(fig, width="stretch", config={"displaylogo": False})
        st.caption("Positive force = tension; negative force = compression under the lesson's convention. The calculation reproduces the source equation and is not an independent DSM re-analysis.")

    @staticmethod
    def force_method_audit() -> None:
        st.markdown("### Source audit · Verify the denominator")
        st.caption("The PDF lists the following unit-load terms for equal E and A. The sum is recomputed here from those displayed terms.")
        terms = [("AB", 0.8**2 * 4000), ("BC", 0.6**2 * 3000), ("CD", 0.8**2 * 4000), ("DA", 0.6**2 * 3000), ("AC", 1.0**2 * 5000)]
        total = sum(value for _, value in terms)
        rows = [{"Primary member": name, "n²L term (mm)": round(value)} for name, value in terms]
        rows.append({"Primary member": "Sum of displayed terms", "n²L term (mm)": total})
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
        st.warning(f"The displayed terms sum to {total:,} mm, not the 13,400 mm stated in the PDF. Its reported X = −1.3433 kN requires instructor verification; the compatibility convention should also be clarified before using that value as an answer key.")

    @staticmethod
    def optimization_sandbox() -> None:
        st.markdown("### Mini-lab · Explore a one-member sizing trade-off")
        st.caption("Fixed axial load and member length; educational stress-only illustration. This is not a full truss optimizer or a code design check.")
        c1, c2 = st.columns(2)
        area = c1.slider("Cross-sectional area (mm²)", 100, 2000, 800, 50, key="exp_opt_area")
        allowable = c2.slider("Allowable stress (MPa)", 50, 250, 150, 10, key="exp_opt_allowable")
        result = single_member_sizing(area_mm2=area, load_kn=100, length_m=2.5, allowable_stress_mpa=allowable)
        cols = st.columns(3)
        cols[0].metric("Normal stress", f"{result['stress_mpa']:.1f} MPa")
        cols[1].metric("Material volume", f"{result['volume_m3']:.5f} m³")
        cols[2].metric("Approx. steel mass", f"{result['mass_kg']:.1f} kg")
        if result["feasible_by_stress"]:
            st.success("The selected area satisfies the displayed stress limit in this simplified model.")
        else:
            st.error("The selected area exceeds the displayed stress limit. Increasing area lowers stress but uses more material.")
        areas = np.arange(100, 2001, 25)
        stresses = 100_000.0 / areas
        fig = go.Figure(go.Scatter(x=areas, y=stresses, mode="lines", line={"color": "#0d9488", "width": 3}, name="Stress"))
        fig.add_hline(y=allowable, line_dash="dash", line_color="#c43c4b", annotation_text="Allowable stress")
        fig.add_trace(go.Scatter(x=[area], y=[float(result["stress_mpa"])], mode="markers", marker={"size": 12, "color": "#d18b14"}, name="Selected design"))
        fig.update_layout(title="Feasibility boundary for the chosen load", xaxis_title="Area (mm²)", yaxis_title="Stress (MPa)", height=300, margin={"l": 10, "r": 10, "t": 55, "b": 20}, paper_bgcolor="#fff", plot_bgcolor="#fff")
        st.plotly_chart(fig, width="stretch", config={"displaylogo": False})
        st.info("For this one member, weight is proportional to A·L. A real truss optimization needs all member lengths/areas, equilibrium or a stiffness solver, stress and displacement constraints, and additional engineering checks.")
