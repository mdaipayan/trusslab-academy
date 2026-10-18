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
            P("A truss is a framework made from straight members connected at joints. In the ideal plane-truss model, members mainly carry axial force: tension or compression."),
            BULLETS("**Joints** are the connection points, often labelled A, B, C, and so on.", "**Members** are the bars connecting joints.", "**Supports** restrain selected translations and create support reactions.", "Loads are applied at joints in the ideal model; member bending is neglected." , heading="Know the parts"),
            FORMULA("Axial stress", r"\sigma=\frac{F}{A}", "F is the signed axial member force and A is the cross-sectional area."),
            CALLOUT("A truss is not automatically stable just because it contains triangles. The member connectivity and support restraints must also prevent a mechanism.", "highlight", "Remember"),
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
            P("A truss name usually describes a characteristic arrangement of top chords, bottom chords, verticals and diagonals. Learn to identify the pattern before attempting member-force analysis."),
            TABLE("Compare the three layouts", ("Type", "Visual clue", "Typical introductory description"), (
                ("Pratt", "Panelled truss with diagonals in one direction", "Under typical downward loading, diagonals are commonly in tension and verticals in compression."),
                ("Warren", "Alternating triangular web", "Often drawn without vertical members; diagonal force signs alternate with the load pattern."),
                ("Howe", "Diagonal direction opposite a typical Pratt layout", "Under typical downward loading, diagonals are commonly in compression and verticals in tension."),
            )),
            CALLOUT("Do not memorise a force sign from the name alone. Confirm the actual loading, supports, geometry and sign convention for the truss you are analysing.", "warning", "Engineering caution"),
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
            FORMULA("Degree of static indeterminacy by count", r"D_s=m+r-2j", "m = members, r = independent support-reaction components, and j = joints."),
            TABLE("Read the count carefully", ("Count", "Interpretation"), (
                ("m + r = 2j", "Determinate by count, if the truss is stable and constraints are independent."),
                ("m + r > 2j", "Indeterminate by count; additional compatibility/stiffness relations are generally needed."),
                ("m + r < 2j", "Insufficient constraints by count; often a mechanism, but inspect geometry."),
            )),
            FORMULA("Triangular example", r"m=3,\quad r=3,\quad j=3\quad\Rightarrow\quad D_s=3+3-2(3)=0"),
            CALLOUT("The count is a screening rule, not proof of stability. A poor member layout or dependent support restraints can make a truss unstable even when m + r = 2j.", "highlight", "Key distinction"),
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
        sections=(
            P("Equilibrium means the isolated joint has no unbalanced force. In a static problem, the total force to the right must balance the total force to the left, and the total upward force must balance the total downward force."),
            FORMULA("The two joint-equilibrium equations", r"\sum F_x=0,\qquad\sum F_y=0", "Σ means ‘sum of’. Fₓ is each force's horizontal component; Fᵧ is each force's vertical component. Choose a sign convention first, for example right and up positive."),
            STEPS("Find support reactions from whole-truss equilibrium.", "Choose a joint with at most two unknown member forces.", "Draw the free-body diagram and assume unknown member forces act in tension (away from the joint).", "Resolve diagonal member forces into horizontal and vertical components, then apply both equilibrium equations.", "A negative answer means the actual force is opposite the assumed direction, i.e. compression under the tension-positive convention.", heading="A reliable workflow"),
            P("Worked example at joint C: use the 3–4–5 triangle in the next lesson. At C, the external load is 20 kN to the right and 20 kN downward. Assume F_BC and F_AC are tensile first. For member BC, the horizontal and vertical direction ratios are 4/5 and 3/5."),
            FORMULA("Horizontal balance at C", r"\sum F_x=0:\quad 20+\frac45F_{BC}=0\quad\Rightarrow\quad F_{BC}=-25\text{ kN}", "The 20 kN rightward load must be balanced by 20 kN to the left. Since a positive tensile assumption produced a negative answer, BC is in compression (25 kN)."),
            FORMULA("Vertical balance at C", r"\sum F_y=0:\quad -20-\frac35F_{BC}-F_{AC}=0\quad\Rightarrow\quad F_{AC}=-5\text{ kN}", "Substitute F_BC = −25 kN. The result F_AC = −5 kN means AC is in compression (5 kN). The negative signs indicate force direction, not a negative physical magnitude."),
            CALLOUT("For a plane truss, a single joint provides two independent force-equilibrium equations. Starting with more than two unknown member forces usually means choosing another joint first.", "highlight", "Exam tip"),
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
        sections=(
            P("A section cut is an imaginary slice through the truss. Keep one side of the cut, replace each severed member with its unknown axial force, and balance the forces and moments on that free body."),
            FORMULA("Equilibrium of the isolated section", r"\sum F_x=0,\quad\sum F_y=0,\quad\sum M_O=0", "The first two equations balance horizontal and vertical forces. ΣM_O = 0 means the sum of moments about a chosen point O is zero. For a force, moment = force × perpendicular distance to its line of action."),
            P("Quick strategy example: suppose a cut exposes three unknown member forces. Take moments about the intersection of the lines of action of two unknowns. Those two forces have zero moment about that point, so the moment equation can solve the third force directly. Then use ΣFₓ = 0 and ΣFᵧ = 0 for the remaining two, provided the equations are independent."),
            STEPS("Determine whole-truss support reactions.", "Pass an imaginary cut through the member(s) whose forces are sought; for the usual plane-truss section method, keep the number of unknown cut forces to at most three.", "Choose one side of the cut and draw its free-body diagram.", "Apply ΣFₓ = 0, ΣFᵧ = 0 and ΣM = 0.", "Take moments about the intersection of two unknown cut forces where possible, so those two forces make no moment about that point.", heading="Steps for a section cut"),
            CALLOUT("Use the method of joints when you need the whole force state progressively; use a section when only a few selected member forces are needed quickly.", "success", "When is this method useful?"),
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
        sections=(
            P("The uploaded study notes use A = (0, 0), B = (4, 0), C = (0, 3) m. Members are AB = 4 m, AC = 3 m and BC = 5 m. A is pinned; B is a vertical roller. Joint C carries Pₓ = 20 kN to the right and Pᵧ = 20 kN downward."),
            FORMULA("Whole-truss equilibrium", r"\sum M_A=0:\quad 4B_y-20(3)=0\Rightarrow B_y=15\text{ kN}", "The 20 kN horizontal force at C has a 3 m perpendicular lever arm about A. The 20 kN vertical force passes through A's horizontal line and contributes no moment about A in this geometry. Lengths are in metres, so moments are in kN·m."),
            FORMULA("Vertical and horizontal force balance", r"\sum F_y=0:\ A_y+B_y-20=0\Rightarrow A_y=5\text{ kN};\qquad \sum F_x=0:\ A_x+20=0\Rightarrow A_x=-20\text{ kN}", "The vertical reactions add to 20 kN upward. Ax is −20 kN under the convention right positive, so the actual reaction is 20 kN to the left."),
            P("Now isolate joint C and assume F_AC and F_BC are tensile (forces pointing away from C). Since BC is a 3–4–5 member, its direction components are 4/5 horizontally and 3/5 vertically."),
            FORMULA("Joint C: find BC then AC", r"20+\frac45F_{BC}=0\Rightarrow F_{BC}=-25\text{ kN};\qquad -20-\frac35F_{BC}-F_{AC}=0\Rightarrow F_{AC}=-5\text{ kN}", "Both answers are negative under the initial tension-positive assumption, so BC = 25 kN compression and AC = 5 kN compression."),
            TABLE("Reactions reported in the notes", ("Reaction", "Value", "Direction"), (("Aₓ", "−20 kN", "Left"), ("Aᵧ", "5 kN", "Up"), ("Bᵧ", "15 kN", "Up"))),
            TABLE("Member-force result", ("Member", "Length", "Signed member force", "Nature"), (("AB", "4 m", "F_AB = +20 kN", "Tension"), ("AC", "3 m", "F_AC = −5 kN", "Compression"), ("BC", "5 m", "F_BC = −25 kN", "Compression"))),
            FORMULA("Normal stress", r"\sigma=\frac{F}{A}", "Use N in newtons and A in mm² to obtain stress in MPa because 1 N/mm² = 1 MPa."),
            CALLOUT("For the stated ideal determinate problem, reducing A_AB from 1000 mm² to 500 mm² keeps F_AB = 20 kN but doubles σ_AB from 20 MPa to 40 MPa. Area still affects stiffness and displacement.", "highlight", "Main takeaway"),
            CALLOUT("The source notes also give δ_Cv = 75/A_AC mm when A_AC is in mm² for the stated unit-load example. This is a source-specific educational result under the stated assumptions, not a complete design check.", "info", "Displacement result from the notes"),
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
        sections=(
            P("This is a pin-jointed triangular truss—not a beam, rigid frame or parallel-bar analogy. The joints are A = (0, 0), B = (4, 0) and C = (0, 3) m. Members AB = 4 m, AC = 3 m and BC = 5 m. A is a pin, B is a vertical roller, and C is a roller against a vertical guide that restrains horizontal movement. A downward point load P = 10 kN acts directly at joint C. All applied loading is at a truss joint."),
            FORMULA("1 · Count the indeterminacy", r"D_s=m+r-2j=3+4-2(3)=1", "There are m = 3 members, r = 4 reaction components (two at A, one at B, and the horizontal reaction at C), and j = 3 joints. The count identifies one redundant reaction, assuming the geometry and restraints are stable."),
            P("Use a tension-positive sign convention: a positive member force means tension; a negative force means compression. The horizontal reaction at C is the redundant R. To determine it, temporarily release the horizontal restraint at C and analyse the resulting determinate primary truss."),
            FORMULA("2 · Solve the released primary truss", r"F_{AB}^{(0)}=0,\qquad F_{AC}^{(0)}=-10\text{ kN},\qquad F_{BC}^{(0)}=0", "With the 10 kN downward load at C and only A-pin/B-vertical-roller supports, the vertical member AC carries 10 kN compression. AB and BC are zero-force members for this primary-load case. The superscript (0) means force before adding the redundant reaction."),
            FORMULA("3 · Apply a unit horizontal load at C", r"n_{AB}=1,\qquad n_{AC}=0.75,\qquad n_{BC}=-1.25", "These are the member forces caused by a unit horizontal load acting to the right at C on the released primary truss. Lower-case n denotes the unit-load member force; the negative value for BC means compression under the stated tension-positive sign convention."),
            FORMULA("4 · Compatibility: joint C cannot move horizontally", r"u_C=\sum_i\frac{F_i^{(0)}n_iL_i}{EA_i}+R\sum_i\frac{n_i^2L_i}{EA_i}=0", "Because the horizontal guide remains in the real structure, the final horizontal displacement at C must be zero. The first sum is the displacement caused by the applied vertical load in the released truss; the second term is the displacement contribution from the redundant R. This is a deformation condition, not another force-equilibrium equation."),
            CALLOUT("The compatibility condition is u_C = 0—not that every member has zero extension. Individual members may extend or shorten; their signed contributions must combine to give zero horizontal movement at the restrained joint.", "highlight", "Meaning of compatibility"),
            FORMULA("5 · Worked solution when every member has the same E and A", r"R=-\frac{(-10)(0.75)(3)}{(1)^2(4)+(0.75)^2(3)+(-1.25)^2(5)}=\frac{22.5}{13.5}=1.667\text{ kN}", "Lengths are in metres and forces in kN; E and common A cancel from the ratio. The numerator terms are ΣF⁽⁰⁾nL = −22.5 kN·m. The flexibility-coefficient sum is Σn²L = 4 + 1.6875 + 7.8125 = 13.5 m."),
            FORMULA("Recover the actual member forces", r"F_{AB}=R=1.667\text{ kN};\quad F_{AC}=-10+0.75R=-8.750\text{ kN};\quad F_{BC}=-1.25R=-2.083\text{ kN}", "AB is in tension; AC and BC are in compression. This superposition uses Fᵢ = Fᵢ⁽⁰⁾ + Rnᵢ."),
            CALLOUT("Check the result at joint C: the 1.667 kN rightward support reaction balances the diagonal's 2.083 kN compression component of 1.667 kN to the left. Vertically, AC contributes 8.750 kN upward and BC contributes 1.250 kN upward, balancing the 10 kN downward joint load.", "info", "Equilibrium check"),
            CALLOUT("This example is an ideal truss because the members meet at pin joints and the applied point load acts at joint C. The extra horizontal support makes it indeterminate; compatibility is what determines its redundant reaction.", "highlight", "Keep the model straight"),
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
        sections=(
            P("The source model has A = (0, 0), B = (4, 0), C = (0, 3) m; AB = 4 m, AC = 3 m and BC = 5 m. A is pinned, B is a vertical roller, and C has a horizontal guide that supplies R = Cₓ. At C, Pₓ = 20 kN acts right and Pᵧ = 20 kN acts downward."),
            FORMULA("Degree of indeterminacy by count", r"D_s=m+r-2j=3+4-2(3)=1"),
            FORMULA("Member forces as functions of R", r"F_{AB}=20+R,\quad F_{AC}=0.75R-5,\quad F_{BC}=-1.25(20+R)"),
            P("Why equilibrium alone is not enough: the extra horizontal support reaction R adds an unknown. Force equilibrium lets the member forces be written in terms of R, but a second kind of condition is needed to determine R. The horizontal guide prevents joint C from moving horizontally, so the final horizontal displacement must be zero."),
            FORMULA("Compatibility relation from virtual work", r"u_C=\sum_i\frac{F_i n_i L_i}{E A_i}=0", "u_C is the horizontal displacement at C. Fᵢ is the actual axial force in member i under the real loads and chosen redundant; nᵢ is the axial force caused by a unit horizontal load at C on the primary structure; Lᵢ is member length; E is Young's modulus; Aᵢ is area. Use a consistent unit system. Each term is one member's contribution to the displacement in the unit-load direction."),
            P("Interpretation: calculate the displacement that the real loads would produce at C on the released primary structure, calculate how the redundant reaction changes that displacement, and choose R so the two effects cancel exactly. The support condition is u_C = 0, not ‘every member has zero extension’. Individual members can extend or shorten while their total horizontal contribution at C sums to zero."),
            FORMULA("Redundant reaction from the source note", r"R=-\frac{80000/A_1-11250/A_2+156250/A_3}{4000/A_1+1687.5/A_2+7812.5/A_3}", "A₁ = A_AB, A₂ = A_AC and A₃ = A_BC in mm²; the source equation gives R in kN."),
            CALLOUT("The source reports R ≈ −16.667 kN for equal areas of 1000 mm² and R ≈ −15.309 kN when only A₃ is raised to 2000 mm². The sign means the actual reaction is opposite the chosen positive horizontal direction.", "highlight", "Numbers from the supplied notes"),
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
        sections=(
            P("The supplied notes use a 4 m × 3 m rectangle: AB = CD = 4 m, BC = DA = 3 m and diagonals AC = BD = 5 m. A is pinned, B is a vertical roller, and a 10 kN downward load acts at C. There are six members, three support reactions and four joints."),
            FORMULA("Degree of internal indeterminacy", r"D_s=m+r-2j=6+3-2(4)=1"),
            STEPS("Select diagonal BD and define X = F_BD.", "Remove BD temporarily to create the primary determinate structure with AB, BC, CD, DA and AC.", "Solve the primary structure for the actual loading, then apply a unit load in the redundant direction to obtain virtual member forces nᵢ.", "Use compatibility to find X, then recover each primary member force from Fᵢ = Fᵢ⁽⁰⁾ + X nᵢ.", heading="Force method overview"),
            P("Compatibility meaning in the force method: removing an internal redundant bar creates a released primary structure. When bar BD is restored, the relative movement of joints B and D along the bar's axis must match BD's own axial extension or shortening. It is not generally correct to say that the relative movement is zero for a finite-stiffness redundant member."),
            FORMULA("Compatibility for the restored redundant bar", r"\Delta_{BD}^{(0)}+\Delta_{BD}^{(X)}=\delta_{BD}=\frac{X L_{BD}}{E A_{BD}}", "Δ⁽⁰⁾ is the signed relative displacement along BD caused by external loading on the released primary structure. Δ⁽ˣ⁾ is the signed additional relative displacement of those joints caused by applying the redundant force X to the primary structure. δ_BD is the redundant bar's own signed axial deformation; use one consistent sign convention throughout."),
            FORMULA("Axial flexibility of a uniform bar", r"\delta=\frac{F L}{E A},\qquad f=\frac{L}{E A}", "F is the signed axial member force, L is member length, E is Young's modulus and A is cross-sectional area. For a uniform axial member, flexibility increases with length and decreases when E or A increases."),
            FORMULA("Force recovery in the primary members", r"F_i=F_i^{(0)}+Xn_i", "Fᵢ⁽⁰⁾ is the force in member i from the real load on the primary structure, and nᵢ is the member force from the chosen unit-load system. Restore the redundant's effect after solving X."),
            CALLOUT("Arithmetic and modelling audit: the displayed virtual-force terms add to 12,280 mm, not the PDF's stated 13,400 mm. The note also needs a clearly stated compatibility convention for the finite-stiffness redundant BD and its own deformation before the reported X = −1.3433 kN can be accepted. Verify both formulation and arithmetic; do not use the printed result as a validated answer.", "danger", "Source discrepancy — verify before grading"),
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
            FORMULA("Material volume objective", r"\min_{\mathbf A} V(\mathbf A)=\sum_{i=1}^{m}A_iL_i"),
            FORMULA("Stress constraint", r"|\sigma_i(\mathbf A)|=\left|\frac{F_i(\mathbf A)}{A_i}\right|\leq\sigma_{\mathrm{allow}}"),
            FORMULA("Displacement constraint", r"|\delta_j(\mathbf A)|\leq\delta_{\mathrm{allow}}"),
            TABLE("Structural behaviour comparison", ("Ideal determinate truss", "Indeterminate truss"), (("Equilibrium generally fixes F for prescribed loading and geometry.", "F depends on equilibrium plus compatibility and stiffness."), ("Changing A normally changes stress and displacement, not F.", "Changing A can redistribute F through stiffness EA/L."))),
            P("A glass-box learning system should reveal the geometry, reactions, member-force signs, areas, stresses, displacements, constraint utilisation, objective value and optimisation history. Students should be able to answer: why did the design change this area, and what structural consequence followed?"),
            CALLOUT("This starter's sandbox is a single-member sizing illustration, not a certified truss optimizer. It does not check buckling, connections, fatigue, fabrication, load combinations or design-code compliance.", "warning", "Scope of the demo"),
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
