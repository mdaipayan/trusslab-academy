"""Authored learning path based on the three supplied study-note PDFs."""
from __future__ import annotations

from .models import ContentBlock, LessonModule, QuizOption, QuizQuestion


def P(text: str, heading: str = "") -> ContentBlock:
    return ContentBlock(kind="paragraph", heading=heading, text=text)


def BULLETS(*items: str, heading: str = "") -> ContentBlock:
    return ContentBlock(kind="bullets", heading=heading, items=tuple(items))


def STEPS(*items: str, heading: str = "") -> ContentBlock:
    return ContentBlock(kind="steps", heading=heading, items=tuple(items))


def FORMULA(heading: str, formula: str, text: str = "") -> ContentBlock:
    return ContentBlock(kind="formula", heading=heading, formula=formula, text=text)


def CALLOUT(text: str, tone: str = "info", heading: str = "") -> ContentBlock:
    return ContentBlock(kind="callout", heading=heading, text=text, tone=tone)  # type: ignore[arg-type]


def TABLE(heading: str, headers: tuple[str, ...], rows: tuple[tuple[str, ...], ...]) -> ContentBlock:
    return ContentBlock(kind="table", heading=heading, table_headers=headers, table_rows=rows)


def Q(qid: str, prompt: str, answers: tuple[str, str, str, str], correct: str,
      explanation: str, hint: str) -> QuizQuestion:
    options = tuple(QuizOption(chr(65 + i), answer) for i, answer in enumerate(answers))
    return QuizQuestion(qid, prompt, options, correct, explanation, hint)


MODULES: tuple[LessonModule, ...] = (
    LessonModule(
        id="foundations", title="Truss foundations", subtitle="Understand the structure before solving it",
        purpose="Identify the parts and ideal assumptions of a pin-jointed truss.", level="FOUNDATION", minutes=6,
        objectives=("Identify joints, members and supports.", "Explain why triangular arrangements are commonly used.", "State the ideal truss assumptions."),
        diagram_id="basic_truss",
        sections=(
            P("A truss is made of straight members joined at their ends. In the ideal model, each member carries tension or compression."),
            BULLETS("**Joint:** where members meet.", "**Member:** a bar between two joints.", "**Support:** stops selected movement and creates reactions.", "**Load:** apply it at a joint in an ideal truss.", heading="Four things to recognise"),
            FORMULA("Axial stress", r"\sigma=\frac{F}{A}", "F = member force; A = cross-sectional area."),
            CALLOUT("Think of a truss as connected straight bars. Start by locating its joints, supports and loads.", "highlight", "Remember"),
        ),
        quiz=(
            Q("f1", "In the ideal pin-jointed truss model, members primarily carry:", ("Axial tension or compression", "Bending moment only", "Torsion only", "Transverse shear only"), "A", "An ideal truss member is treated as a two-force member, so its principal action is axial tension or compression.", "Think about the two forces acting at the ends of an ideal straight bar."),
            Q("f2", "Where are external loads assumed to act in the ideal truss model?", ("Anywhere along a member", "At joints", "Only at supports", "Only at the centroid"), "B", "The ideal truss assumption places external loads at the joints. Loads applied along a real member may cause bending and require another model or load transfer to joints.", "Recall which locations are used to write joint equilibrium."),
            Q("f3", "Which statement best explains the role of triangular geometry?", ("It guarantees zero deflection", "It removes every support reaction", "Suitable triangulation can provide geometric stability", "It makes all members carry equal force"), "C", "A properly connected triangular arrangement can be stable; the exact stability still depends on connectivity and supports.", "Choose the statement about resisting changes in shape, not about force magnitude."),
        ),
    ),
    LessonModule(
        id="truss-types", title="Read common truss layouts", subtitle="Recognise web patterns and load paths",
        purpose="Distinguish common truss configurations from the arrangement of their web members.", level="FOUNDATION", minutes=7,
        objectives=("Recognise Pratt, Warren and Howe layouts.", "Describe their diagonal patterns.", "Understand that member-force directions depend on the loading and layout."),
        diagram_id="truss_types",
        sections=(
            P("Identify the web pattern first. The name alone does not tell you the force in every member."),
            TABLE("Three common layouts", ("Type", "Easy visual clue", "Typical behaviour under common downward loading"), (
                ("Pratt", "Diagonals slope toward the centre at the bottom", "Diagonals often in tension."),
                ("Warren", "Repeating triangles", "Diagonal forces depend on which joints are loaded."),
                ("Howe", "Diagonal pattern opposite to Pratt", "Diagonals often in compression."),
            )),
            CALLOUT("Always confirm the actual loads and supports before deciding tension or compression.", "warning", "Quick check"),
        ),
        quiz=(
            Q("t1", "Which layout is commonly represented by an alternating triangular web and may have no vertical members?", ("Howe", "Warren", "Pratt", "Portal frame"), "B", "The Warren pattern uses alternating triangular web members and is often drawn without verticals.", "Focus on the zig-zag triangular web rather than the vertical members."),
            Q("t2", "For a typical Pratt truss under downward loading, its diagonal members are commonly described as being in:", ("Tension", "Bending only", "Torsion", "Compression in every case"), "A", "In the typical introductory Pratt case, the diagonals are commonly in tension. A specific design still needs analysis for its actual loading.", "Use the usual Pratt loading description, but avoid universal claims."),
            Q("t3", "Which is the safest way to determine whether a particular member is in tension or compression?", ("Use the truss name only", "Assume every diagonal is in tension", "Analyse the actual loads, supports and geometry", "Assume the longest member is in compression"), "C", "The actual force state follows from the structure and loading. The truss label alone is not enough to determine every force sign.", "Choose the approach that uses the model's real conditions."),
        ),
    ),
    LessonModule(
        id="determinacy", title="Determinacy and stability", subtitle="Count unknowns, then inspect the geometry",
        purpose="Use the plane-truss count as a first check without confusing it with a full stability proof.", level="CORE", minutes=8,
        objectives=("Define m, r and j.", "Compute the determinacy count.", "Explain why the count alone cannot prove geometric stability."),
        diagram_id="determinacy",
        sections=(
            FORMULA("Count unknowns", r"D_s=m+r-2j", "m = members; r = reaction components; j = joints."),
            FORMULA("Example: a simple triangle", r"D_s=3+3-2(3)=0", "The count says determinate, provided the truss is stable."),
            TABLE("Read the result", ("Result", "Meaning"), (("Dₛ = 0", "Determinate by count"), ("Dₛ > 0", "Indeterminate by count"), ("Dₛ < 0", "May be unstable or under-restrained"))),
            CALLOUT("This count is a first check—not a proof of stability. Also inspect the shape and supports.", "highlight", "Remember"),
        ),
        quiz=(
            Q("d1", "A stable plane truss has m = 6 members, r = 3 reaction components and j = 4 joints. What is Dₛ = m + r − 2j?", ("−1", "0", "1", "2"), "C", "Dₛ = 6 + 3 − 2(4) = 9 − 8 = 1. If the geometry is stable and constraints are independent, this is first-degree indeterminacy by count.", "Substitute each count into m + r − 2j and respect the parentheses."),
            Q("d2", "For a stable and properly constrained plane truss, what does m + r = 2j indicate?", ("Two redundant members", "Determinate by count", "Geometric stability is proved in every case", "No support reactions exist"), "B", "Equality indicates determinacy by count, subject to geometric stability and independent restraints. It is not a complete stability proof.", "Separate the numerical count from the geometric check."),
            Q("d3", "Why must the geometry be inspected after calculating Dₛ?", ("The equation does not test every possible mechanism", "It gives the Young's modulus", "It calculates the total steel weight", "It replaces equilibrium equations"), "A", "The count cannot detect all geometric-instability cases or dependent constraints; stability requires a separate check.", "Ask what the member-count equation does not represent explicitly."),
        ),
    ),
    LessonModule(
        id="joints", title="Method of joints", subtitle="Solve the truss one joint at a time",
        purpose="Choose a manageable joint, draw its free-body diagram and use force equilibrium.", level="CORE", minutes=9,
        objectives=("Select a joint with no more than two unknown member forces.", "Apply horizontal and vertical equilibrium.", "Interpret positive and negative force results correctly."),
        diagram_id="method_joints",
        free_body_ids=("joint_c_fbd",),
        sections=(
            P("At an isolated joint, forces must balance. There must be **no unbalanced force**."),
            FORMULA("Two equations at every plane joint", r"\sum F_x=0,\qquad \sum F_y=0", "Take right and up as positive."),
            STEPS("Start at a joint with no more than two unknown member forces.", "Assume unknown member forces pull away from the joint (tension).", "Resolve diagonal forces into horizontal and vertical parts.", "A negative answer means compression under this sign convention.", heading="Method of joints"),
            FORMULA("Example at C: horizontal balance", r"20+\frac45F_{BC}=0\quad\Rightarrow\quad F_{BC}=-25\text{ kN}", "The negative sign means BC is in **25 kN compression**."),
            FORMULA("Then vertical balance", r"-20-\frac35F_{BC}-F_{AC}=0\quad\Rightarrow\quad F_{AC}=-5\text{ kN}", "So AC is in **5 kN compression**."),
        ),
        quiz=(
            Q("j1", "When beginning the method of joints, a useful starting joint usually has:", ("The most connected members", "At most two unknown member forces", "No known forces anywhere in the truss", "At least four unknown member forces"), "B", "Two force-equilibrium equations are available at a plane joint, so no more than two unknown member forces is a practical starting condition.", "Count unknowns at one joint, not every unknown in the truss."),
            Q("j2", "If tension is assumed positive and a calculated member force is −12 kN, what does the sign indicate?", ("12 kN tension", "12 kN compression", "12 kN bending moment", "A zero-force member"), "B", "A negative result means the actual force direction is opposite the assumed tensile direction, so the member is in compression under this convention.", "Interpret the sign relative to your initial assumption."),
            Q("j3", "Which pair of equations is used at a plane joint?", ("ΣFₓ = 0 and ΣFᵧ = 0", "ΣM = 0 and ΣT = 0", "Only ΣM = 0", "Only compatibility equations"), "A", "A joint's force equilibrium in the horizontal and vertical directions provides the two equations for method of joints.", "Choose the pair of in-plane force balances."),
        ),
    ),
    LessonModule(
        id="sections", title="Method of sections", subtitle="Cut where the answer is needed",
        purpose="Find forces in selected members without solving every joint of a large truss.", level="CORE", minutes=8,
        objectives=("Choose a section crossing only a manageable number of unknown members.", "Use section equilibrium to solve selected member forces.", "Pick a moment centre that eliminates unwanted unknowns."),
        diagram_id="method_sections",
        free_body_ids=("section_cut_fbd",),
        sections=(
            P("Cut through the members you want to solve. Keep one side and draw every cut-member force on that free body."),
            FORMULA("Equilibrium of the cut part", r"\sum F_x=0,\quad \sum F_y=0,\quad \sum M_O=0", "Moment = force × perpendicular distance."),
            STEPS("Find the support reactions first.", "Cut through up to three unknown members.", "Keep the easier side and draw the cut-member forces.", "Use moments first when it removes two unknowns.", heading="Four steps"),
            CALLOUT("Use joints to work through the truss. Use sections when you need only a few member forces.", "success", "Which method?"),
        ),
        quiz=(
            Q("s1", "For a typical plane-truss section method using three equilibrium equations, the cut should cross at most how many unknown member forces?", ("One", "Two", "Three", "Five"), "C", "The three independent plane equilibrium equations can normally solve up to three unknown cut-member forces, provided the equations are independent.", "Match the number of unknown cut forces to the three available equilibrium equations."),
            Q("s2", "To isolate one of three unknown cut-member forces using moments, a useful moment centre is where:", ("The largest member meets the bottom chord", "The other two unknown force lines intersect", "The centre of the whole truss lies", "The highest joint is located in every case"), "B", "Taking moments at the intersection of the other two unknown force lines eliminates their moments and can leave one unknown in the equation.", "Look for a point where two unwanted forces have zero moment arm."),
            Q("s3", "The method of sections is especially useful when the goal is to:", ("Find one or a few specific interior-member forces efficiently", "Avoid calculating support reactions in every case", "Replace the truss with a beam without assumptions", "Find only cross-sectional areas"), "A", "A judicious cut lets you solve selected member forces without working through every joint between the support and the target member.", "Focus on what the cut avoids having to solve."),
        ),
    ),
    LessonModule(
        id="determinate-example", title="Worked example: determinate 3–4–5 truss", subtitle="From loads to reactions, member forces and stress",
        purpose="Follow a complete worked example and distinguish force from stress and displacement.", level="APPLIED", minutes=10,
        objectives=("Determine reactions for the supplied 3–4–5 triangle.", "Identify its reported member-force magnitudes and natures.", "Explain how area changes stress while the ideal determinate member force stays fixed."),
        diagram_id="determinate_example", experiment_id="determinate_area",
        free_body_ids=("whole_truss_fbd", "joint_c_fbd"),
        sections=(
            P("Use A = (0,0), B = (4,0), C = (0,3) m. AB = 4 m, AC = 3 m and BC = 5 m. At C, apply 20 kN right and 20 kN down."),
            FORMULA("Support reactions", r"\sum M_A=0:\ 4B_y-20(3)=0\Rightarrow B_y=15\text{ kN}", r"\sum F_y=0\Rightarrow A_y=5\text{ kN};\quad \sum F_x=0\Rightarrow A_x=-20\text{ kN}"),
            FORMULA("Member forces at joint C", r"20+\frac45F_{BC}=0\Rightarrow F_{BC}=-25\text{ kN}", r"-20-\frac35F_{BC}-F_{AC}=0\Rightarrow F_{AC}=-5\text{ kN}"),
            TABLE("Final answer", ("Member", "Signed force", "State"), (("AB", "F_AB = +20 kN", "Tension"), ("AC", "F_AC = −5 kN", "Compression"), ("BC", "F_BC = −25 kN", "Compression"))),
            FORMULA("Stress", r"\sigma=\frac{F}{A}", "Use F in newtons and A in mm²; the answer is MPa."),
            CALLOUT("For this determinate truss, halving A_AB doubles its stress from 20 MPa to 40 MPa. Its member force stays 20 kN for the same loads and geometry.", "highlight", "Force is not stress"),
        ),
        quiz=(
            Q("de1", "In the uploaded 3–4–5 truss example, what vertical reaction is reported at roller B?", ("5 kN upward", "15 kN upward", "20 kN upward", "25 kN downward"), "B", "The notes report Bᵧ = 15 kN upward from taking moments about A: 4Bᵧ − 20(3) = 0.", "Use the moment equation about A given in the lesson."),
            Q("de2", "What member-force state is reported for AB in the worked example?", ("20 kN tension", "20 kN compression", "5 kN tension", "25 kN compression"), "A", "The source notes report F_AB = 20 kN tension after solving the joints.", "Read the member-force summary table and match both magnitude and nature."),
            Q("de3", "For this ideal determinate example, if A_AB halves from 1000 to 500 mm² while F_AB remains 20 kN, what happens to normal stress?", ("It halves from 20 to 10 MPa", "It remains 20 MPa", "It doubles from 20 to 40 MPa", "It becomes zero"), "C", "σ = F/A. Keeping F = 20,000 N and halving A doubles the stress from 20 MPa to 40 MPa.", "Keep the force fixed and compare the inverse dependence of stress on area."),
        ),
    ),
    LessonModule(
        id="truss-compatibility", title="Truss compatibility: redundant support reaction", subtitle="Equilibrium is necessary—but not sufficient",
        purpose="Explain compatibility in a real pin-jointed truss and calculate a redundant support reaction with the force method.", level="APPLIED", minutes=10,
        objectives=("Identify why this triangular truss is externally indeterminate by one degree.", "Distinguish equilibrium equations from a displacement-compatibility condition.", "Calculate the redundant reaction for a 10 kN joint load when all members have equal EA."),
        diagram_id="truss_compatibility", experiment_id="truss_compatibility",
        free_body_ids=("released_truss_fbd", "unit_load_fbd"),
        sections=(
            P("This is a **pin-jointed triangular truss**, not a frame. A is pinned, B is a vertical roller and C has a horizontal guide. The 10 kN downward load **acts directly at joint C**."),
            FORMULA("1 · Count the redundant", r"D_s=m+r-2j=3+4-2(3)=1", "One extra reaction exists: R = Cₓ."),
            FORMULA("2 · Release R and solve the primary truss", r"F_{AB}^{(0)}=0,\quad F_{AC}^{(0)}=-10,\quad F_{BC}^{(0)}=0\text{ kN}", "The superscript (0) means before the extra reaction is added."),
            FORMULA("3 · Unit-load member forces", r"n_{AB}=1,\quad n_{AC}=0.75,\quad n_{BC}=-1.25", "These come from a unit horizontal load to the right at C."),
            FORMULA("4 · Compatibility at C", r"u_C=\sum_i\frac{F_i^{(0)}n_iL_i}{EA_i}+R\sum_i\frac{n_i^2L_i}{EA_i}=0", "The guide prevents horizontal movement, so the final displacement u_C must be zero."),
            FORMULA("5 · Equal E and A: calculate R", r"R=\frac{22.5}{4+1.6875+7.8125}=\frac{22.5}{13.5}=1.667\text{ kN}"),
            FORMULA("Member-force results", r"F_{AB}=+1.667,\quad F_{AC}=-8.750,\quad F_{BC}=-2.083\text{ kN}", "AB is in tension. AC and BC are in compression."),
            CALLOUT("Compatibility means **joint C cannot move horizontally**. It does not mean every member has zero extension.", "highlight", "In plain language"),
        ),
        quiz=(
            Q("tc1", "Where is the 10 kN load applied in this compatibility example?", ("At the midpoint of AC", "At joint C", "Uniformly along BC", "At the center of member AB"), "B", "The force is applied directly at joint C, consistent with the ideal pin-jointed truss model.", "Look at the load arrow and the joint labels in the schematic."),
            Q("tc2", "Why is the triangular truss indeterminate by one degree?", ("It has four members and one joint", "Every triangular truss is indeterminate", "The extra horizontal reaction at C gives m + r − 2j = 1", "Compatibility replaces equilibrium"), "C", "There are m = 3 members, r = 4 reaction components and j = 3 joints; therefore Dₛ = 3 + 4 − 6 = 1.", "Count the horizontal reaction at C as an additional unknown."),
            Q("tc3", "What does the compatibility condition u_C = 0 mean?", ("Every truss member has zero extension", "The final horizontal displacement at restrained joint C is zero", "All member forces are zero", "The load at C must be removed"), "B", "The horizontal guide prevents joint C from translating horizontally. Individual members can still extend or shorten.", "Compatibility describes permitted displacement, not force balance."),
        ),
    ),
    LessonModule(
        id="indeterminate-triangle", title="Indeterminate triangle: redundant reaction", subtitle="Equilibrium first, compatibility next",
        purpose="Reduce a first-degree indeterminate triangle to one redundant and solve it using the supplied compatibility equation.", level="ADVANCED", minutes=12,
        objectives=("Identify the extra support reaction and the degree of indeterminacy.", "Express member forces in terms of the redundant reaction R.", "Explain how area enters compatibility through EA/L."),
        diagram_id="indeterminate_triangle", experiment_id="indeterminate_triangle",
        free_body_ids=("loaded_truss_fbd", "joint_c_loaded_fbd"),
        sections=(
            P("The 3–4–5 truss has a horizontal guide at C. The loads at C are 20 kN right and 20 kN down; R = Cₓ is the redundant reaction."),
            FORMULA("Degree of indeterminacy", r"D_s=3+4-2(3)=1"),
            FORMULA("Write member forces using R", r"F_{AB}=20+R,\quad F_{AC}=0.75R-5,\quad F_{BC}=-1.25(20+R)"),
            FORMULA("Compatibility at the restrained joint", r"u_C=\sum_i\frac{F_i n_i L_i}{EA_i}=0", "The displacement at C must be zero horizontally. Each term represents one member's contribution."),
            CALLOUT("The supplied notes report R ≈ −16.667 kN for equal 1000 mm² areas, and R ≈ −15.309 kN when only A₃ = A_BC increases to 2000 mm². The negative sign means opposite to the assumed positive direction.", "info", "Values reported in the notes"),
        ),
        quiz=(
            Q("it1", "For this triangle, m = 3, r = 4 and j = 3. What degree of indeterminacy is indicated by the count?", ("0", "1", "2", "3"), "B", "Dₛ = m + r − 2j = 3 + 4 − 6 = 1, assuming stable geometry and independent constraints.", "Substitute the number of members, reactions and joints into the count."),
            Q("it2", "Which redundant is selected in the supplied triangle example?", ("Aₓ", "Bᵧ", "R = Cₓ", "F_AB"), "C", "The horizontal guide at C provides the extra reaction R = Cₓ, and the source notes select it as the redundant.", "Inspect the support added at joint C."),
            Q("it3", "Why is a compatibility equation required after equilibrium expresses all three member forces using R?", ("Equilibrium already fixes every member force", "Area must be removed from all equations", "The redundant reaction must satisfy the restrained displacement condition", "It replaces the external loading"), "C", "The horizontal guide requires u_C = 0. Compatibility and member flexibilities L/(EA) supply the relationship needed to solve the redundant.", "Connect the extra reaction to the movement restrained by the guide."),
        ),
    ),
    LessonModule(
        id="force-method", title="Internal redundancy: force method", subtitle="Choose a redundant and inspect the compatibility chain",
        purpose="Understand the primary structure, virtual member forces and force recovery for a first-degree internal redundant.", level="ADVANCED", minutes=12,
        objectives=("Count the redundancy in a rectangular truss with both diagonals.", "Describe how removing BD forms the primary structure.", "Use the force-method equations critically and verify arithmetic."),
        diagram_id="rectangular_redundant", experiment_id="force_method_audit",
        free_body_ids=("released_rectangular_fbd",),
        sections=(
            P("The rectangular truss is 4 m × 3 m, with both diagonals. The count gives one internal redundant."),
            FORMULA("Count", r"D_s=6+3-2(4)=1"),
            STEPS("Choose diagonal BD as X = F_BD.", "Remove BD to form the primary truss.", "Solve the primary truss and a unit-load case.", "Use compatibility to find X, then recover F_i = F_i^(0) + X n_i.", heading="Force method"),
            FORMULA("Compatibility for restored BD", r"\Delta_{BD}^{(0)}+\Delta_{BD}^{(X)}=\delta_{BD}=\frac{XL_{BD}}{EA_{BD}}", "The relative movement of B and D along BD must equal the bar's own signed axial deformation."),
            FORMULA("Axial deformation", r"\delta=\frac{FL}{EA}", "F = signed member force; L = length; E = Young's modulus; A = area."),
            CALLOUT("The displayed PDF terms add to **12,280 mm**, not **13,400 mm**. The note's reported X = −1.3433 kN is not verified. **Verify both formulation and arithmetic** before using it as an answer.", "danger", "Source discrepancy"),
        ),
        quiz=(
            Q("fm1", "Which member is selected as the internal redundant in the supplied rectangular-truss notes?", ("AB", "AC", "BD", "CD"), "C", "The source chooses diagonal BD as X = F_BD and removes it to form the primary structure.", "Find the diagonal explicitly identified as X in the method steps."),
            Q("fm2", "After selecting BD as the redundant, what is the primary structure?", ("The original truss with BD made rigid", "The truss with BD temporarily removed", "Only the diagonal BD", "The whole truss without supports"), "B", "The primary determinate structure is formed by removing BD temporarily while retaining AB, BC, CD, DA and AC.", "Recall what is done to the chosen redundant before solving the primary structure."),
            Q("fm3", "The listed denominator terms in the provided PDF sum to 12,280 mm. What should students do with its stated 13,400 mm denominator and reported redundant force?", ("Accept them without checking", "Replace all forces with zero", "Treat them as verified because the PDF prints them", "Flag the mismatch and verify the compatibility calculation"), "D", "The displayed terms sum to 12,280 mm, so the conflicting denominator and result need checking before being treated as final.", "The displayed arithmetic is part of the evidence; compare the term-by-term sum with the printed total."),
        ),
    ),
    LessonModule(
        id="optimization", title="Truss optimization: make it a glass box", subtitle="Connect design variables to structural response",
        purpose="Formulate a simple minimum-material objective and interpret stress and displacement constraints.", level="DESIGN", minutes=10,
        objectives=("Write the material-volume or constant-density weight objective.", "Distinguish stress and displacement constraints.", "Explain why area can change force distribution in an indeterminate truss."),
        diagram_id="optimization_chain", experiment_id="optimization_sandbox",
        sections=(
            FORMULA("Objective: use less material", r"\min_{\mathbf A}V=\sum_i A_iL_i"),
            FORMULA("Keep stress within its limit", r"\left|\frac{F_i(\mathbf A)}{A_i}\right|\leq \sigma_{\mathrm{allow}}"),
            FORMULA("Keep displacement within its limit", r"|\delta_j(\mathbf A)|\leq\delta_{\mathrm{allow}}"),
            TABLE("Why area matters", ("Determinate truss", "Indeterminate truss"), (("Area usually changes stress and displacement—not the ideal member forces.", "Area changes stiffness and can redistribute member forces."),)),
            CALLOUT("This is a teaching sandbox, not a code-compliant design tool. Buckling, connections and load combinations are not checked.", "warning", "Scope"),
        ),
        quiz=(
            Q("o1", "For constant material density, which expression is proportional to truss self-weight?", ("Σ Aᵢ/Lᵢ", "Σ AᵢLᵢ", "Σ Lᵢ/Aᵢ", "Σ 1/(AᵢLᵢ)"), "B", "With constant density and gravity, weight is proportional to material volume, Σ AᵢLᵢ.", "Weight depends on how much material occupies the member lengths."),
            Q("o2", "In the usual ideal determinate truss under prescribed static loads, what does changing member area normally affect?", ("The equilibrium member-force distribution only", "Stress and displacement, while ideal member forces stay fixed", "Only the number of joints", "Only the support type"), "B", "Equilibrium fixes the ideal determinate member-force distribution for the same geometry and external loads. Area affects stress and stiffness/displacement.", "Keep the model assumptions in mind and separate force from stress and deformation."),
            Q("o3", "What is the most accurate statement about adding a redundant member?", ("It always makes the optimum weight smaller", "It removes all displacement constraints", "It adds a load path but does not guarantee a lighter optimum", "It makes stiffness independent of area"), "C", "Redundancy can improve stiffness and allow redistribution, but the extra member also consumes material; the optimum depends on constraints and loading.", "Compare the potential stiffness benefit with the material that is added."),
        ),
    ),
)


def get_modules() -> tuple[LessonModule, ...]:
    """Return the immutable lesson catalog."""
    return MODULES


def get_module(module_id: str) -> LessonModule:
    for module in MODULES:
        if module.id == module_id:
            return module
    raise KeyError(f"Unknown lesson module: {module_id}")
