"""Student-facing glossary of the symbols, abbreviations and units used in TrussLab Academy."""
from __future__ import annotations

# Each group is (heading, rows); each row is (symbol, meaning, context/notes).
GLOSSARY: tuple[tuple[str, tuple[tuple[str, str, str], ...]], ...] = (
    (
        "Joints, members and determinacy",
        (
            ("A, B, C, …", "Joint labels", "Letters identify truss joints; A used as a joint label is not the same as A used for area."),
            ("AB, AC, BC, …", "Member labels", "A pair of joint labels identifies the member connecting those joints."),
            ("m", "Number of members", "Used in the plane-truss count Dₛ = m + r − 2j."),
            ("r", "Number of independent support-reaction components", "Count reaction components, not merely the number of supports."),
            ("j", "Number of joints", "Used in the plane-truss count."),
            ("Dₛ", "Degree of static indeterminacy by count", "Dₛ = m + r − 2j for a plane truss; the count is not, by itself, a proof of stability."),
            ("i", "Member index", "A general index used in expressions such as Fᵢ, Aᵢ and Lᵢ; it means ‘member i’."),
        ),
    ),
    (
        "Loads, reactions and member forces",
        (
            ("P", "Applied load", "For example, P = 10 kN downward at joint C."),
            ("Pₓ, Pᵧ", "Horizontal and vertical components of an applied load", "Subscripts x and y indicate direction components."),
            ("Fᵢ or F_AB", "Signed axial member force", "This app uses F for member force. Under its tension-positive convention, F > 0 means tension and F < 0 means compression."),
            ("Fᵢ⁽⁰⁾", "Member force in the released primary structure", "Force caused by the real loading before adding the redundant force or reaction."),
            ("Fₓ, Fᵧ", "Horizontal and vertical force components", "Used in equilibrium equations ΣFₓ = 0 and ΣFᵧ = 0."),
            ("Aₓ, Aᵧ, Bᵧ, Cₓ", "Support-reaction components", "For example, Cₓ is the horizontal reaction at joint C."),
            ("R", "Redundant support reaction", "In the 10 kN compatibility example, R = Cₓ is the extra horizontal reaction."),
            ("X", "Selected internal redundant force", "In the rectangular-truss force-method lesson, X is the axial force in diagonal BD."),
            ("nᵢ", "Unit-load member force", "The signed member force caused by the virtual unit-load case. Lower-case n is reserved for this auxiliary calculation; the actual member force is Fᵢ."),
            ("Σ", "Summation: ‘sum of’", "For example, ΣFₓ = 0 means the sum of horizontal force components is zero."),
            ("M_O, M_A", "Moment about a selected point", "The subscript names the point about which the moments are summed."),
        ),
    ),
    (
        "Material, geometry and response",
        (
            ("A or Aᵢ", "Cross-sectional area", "A is also used as a joint label in diagrams; Aᵢ or context makes the area meaning clear."),
            ("A₁, A₂, A₃", "Areas of members AB, AC and BC", "Used in the source-note triangle equation: A₁ = A_AB, A₂ = A_AC and A₃ = A_BC."),
            ("𝐀 or A-vector", "Vector of member areas", "The optimisation objective uses the vector of all design areas as its design variable."),
            ("L or Lᵢ", "Member length", "The original length of member i."),
            ("E", "Young’s modulus", "A measure of material stiffness; use consistent units."),
            ("EAᵢ", "Axial rigidity", "The product of Young’s modulus and cross-sectional area for member i."),
            ("EAᵢ/Lᵢ", "Axial stiffness of a uniform truss member", "Higher EA/L means less axial deformation for the same force."),
            ("fᵢ = Lᵢ/(EAᵢ)", "Axial flexibility coefficient", "The axial deformation per unit axial force for a uniform member."),
            ("δ", "Axial deformation", "Extension or shortening of a member; sign depends on the chosen convention."),
            ("δ_BD", "Axial deformation of redundant member BD", "The restored bar's own extension or shortening in the internal force-method example."),
            ("Δ_BD⁽⁰⁾, Δ_BD⁽ˣ⁾", "Relative displacement along BD", "The components caused by the real loading and by the redundant force X, respectively, in the released primary structure."),
            ("u_C", "Horizontal displacement of joint C", "In the compatibility example, the horizontal guide requires u_C = 0."),
            ("δ_j, δ_allow", "Displacement and allowable displacement", "The optimisation lesson constrains the magnitude of displacement at a degree of freedom."),
            ("σ", "Normal stress", "For a uniform axial member, σ = F/A when force and area use compatible units."),
            ("σ_allow", "Allowable normal stress", "The stress limit used in the simple optimization/sizing illustration."),
            ("V(𝐀)", "Material volume as a function of areas", "The optimization lesson minimises V = Σ AᵢLᵢ; for a uniform material, self-weight is proportional to volume."),
            ("K", "Stiffness (diagram label)", "Used in the optimization flow diagram to represent structural stiffness."),
        ),
    ),
    (
        "Equilibrium, compatibility and methods",
        (
            ("x, y", "Horizontal and vertical directions", "The app convention usually takes rightward and upward components as positive."),
            ("δ = FL/(EA)", "Axial deformation relation", "Applies to a straight, uniform, linearly elastic member under axial force."),
            ("u_C = 0", "Displacement-compatibility condition", "The restrained joint C cannot translate horizontally in the support arrangement shown."),
        ),
    ),
    (
        "Abbreviations used in the lessons",
        (
            ("DSM", "Direct Stiffness Method", "A structural analysis method referenced in the source-audit lesson."),
            ("PDF", "Portable Document Format", "The file format of the supplied study notes discussed in the source-audit lesson."),
        ),
    ),
    (
        "Units used in examples",
        (
            ("N", "newton", "Unit of force. Do not confuse the unit N with the app’s symbol F for signed axial member force."),
            ("kN", "kilonewton", "1 kN = 1,000 N."),
            ("kN·m", "kilonewton-metre", "Unit of moment; for example, force in kN multiplied by a perpendicular distance in metres."),
            ("m", "metre", "Length unit; in the determinacy equation, m instead denotes the number of members. Read it from context."),
            ("mm", "millimetre", "1 m = 1,000 mm."),
            ("mm²", "square millimetre", "Common area unit in stress and sizing examples."),
            ("MPa", "megapascal", "Stress unit; 1 MPa = 1 N/mm²."),
        ),
    ),
)
