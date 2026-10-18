"""Reusable Plotly diagrams for each lesson."""
from __future__ import annotations

from typing import Mapping
import plotly.graph_objects as go

Point = tuple[float, float]


class DiagramFactory:
    """Create consistent, labelled engineering schematics."""

    INK = "#243e50"
    TEAL = "#0d9488"
    BLUE = "#2878b5"
    AMBER = "#d18b14"
    RED = "#c43c4b"
    GREEN = "#16845a"
    SLATE = "#7b8d99"

    @classmethod
    def build(cls, diagram_id: str) -> go.Figure:
        methods = {
            "basic_truss": cls.basic_truss,
            "truss_types": cls.truss_types,
            "determinacy": cls.determinacy,
            "method_joints": cls.method_joints,
            "method_sections": cls.method_sections,
            "determinate_example": cls.determinate_example,
            "truss_compatibility": cls.truss_compatibility,
            "indeterminate_triangle": cls.indeterminate_triangle,
            "rectangular_redundant": cls.rectangular_redundant,
            "optimization_chain": cls.optimization_chain,
        }
        try:
            return methods[diagram_id]()
        except KeyError as exc:
            raise ValueError(f"Unknown diagram id: {diagram_id}") from exc

    @classmethod
    def _member(cls, fig: go.Figure, nodes: Mapping[str, Point], a: str, b: str,
                label: str, color: str | None = None, width: float = 3.3,
                dash: str = "solid") -> None:
        x1, y1 = nodes[a]
        x2, y2 = nodes[b]
        fig.add_trace(go.Scatter(
            x=[x1, x2], y=[y1, y2], mode="lines",
            line={"color": color or cls.INK, "width": width, "dash": dash},
            name=label, showlegend=False,
            customdata=[[label, a, b], [label, a, b]],
            hovertemplate="<b>%{customdata[0]}</b><br>Joints %{customdata[1]}–%{customdata[2]}<extra></extra>",
        ))

    @classmethod
    def _nodes(cls, fig: go.Figure, nodes: Mapping[str, Point], highlight: str | None = None) -> None:
        names = list(nodes)
        fig.add_trace(go.Scatter(
            x=[nodes[n][0] for n in names], y=[nodes[n][1] for n in names],
            mode="markers+text", text=names, textposition="top center",
            textfont={"size": 12, "color": "#173042"},
            marker={"size": [14 if n == highlight else 10 for n in names],
                    "color": [cls.AMBER if n == highlight else cls.TEAL for n in names],
                    "line": {"color": "#ffffff", "width": 1.5}},
            customdata=[[n, nodes[n][0], nodes[n][1]] for n in names],
            hovertemplate="<b>Joint %{customdata[0]}</b><br>x = %{customdata[1]:.2f} m<br>y = %{customdata[2]:.2f} m<extra></extra>",
            name="Joints", showlegend=False,
        ))

    @classmethod
    def _supports(cls, fig: go.Figure, nodes: Mapping[str, Point], names: tuple[str, ...]) -> None:
        for name in names:
            x, y = nodes[name]
            fig.add_trace(go.Scatter(
                x=[x, x - .22, x + .22, x], y=[y - .05, y - .34, y - .34, y - .05],
                mode="lines", fill="toself", fillcolor="#dce5eb",
                line={"color": "#718390", "width": 1.3},
                hovertemplate=f"<b>Support at {name}</b><extra></extra>",
                name=f"Support {name}", showlegend=False,
            ))
            gy = y - .36
            fig.add_shape(type="line", x0=x - .31, x1=x + .31, y0=gy, y1=gy,
                          line={"color": "#718390", "width": 1.5})
            for i in range(5):
                xx = x - .23 + i * .115
                fig.add_shape(type="line", x0=xx, x1=xx - .08, y0=gy, y1=gy - .08,
                              line={"color": "#9caeb9", "width": 1})

    @classmethod
    def _arrow(cls, fig: go.Figure, start: Point, end: Point, label: str,
               color: str | None = None, label_pos: Point | None = None) -> None:
        c = color or cls.AMBER
        fig.add_annotation(x=end[0], y=end[1], ax=start[0], ay=start[1],
                           xref="x", yref="y", axref="x", ayref="y",
                           text="", showarrow=True, arrowhead=3, arrowsize=1.1,
                           arrowwidth=2.2, arrowcolor=c)
        if label:
            x, y = label_pos or ((start[0] + end[0]) / 2 + .1, (start[1] + end[1]) / 2 + .1)
            fig.add_annotation(x=x, y=y, text=f"<b>{label}</b>", showarrow=False,
                               font={"size": 11, "color": c},
                               bgcolor="rgba(255,255,255,0.93)", borderpad=2)

    @classmethod
    def _base(cls, fig: go.Figure, title: str, height: int = 360,
              x_range: tuple[float, float] | None = None,
              y_range: tuple[float, float] | None = None,
              equal_scale: bool = True) -> go.Figure:
        fig.update_layout(
            title={"text": f"<b>{title}</b>", "x": .02, "xanchor": "left",
                   "font": {"size": 15, "color": "#152535"}},
            height=height, autosize=True,
            margin={"l": 8, "r": 8, "t": 53, "b": 8},
            paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
            font={"family": "DM Sans, Segoe UI, sans-serif", "size": 12, "color": "#314758"},
            hoverlabel={"bgcolor": "#ffffff", "font_size": 13}, showlegend=False,
        )
        fig.update_xaxes(visible=False, range=list(x_range) if x_range else None,
                         showgrid=False, zeroline=False, fixedrange=True)
        fig.update_yaxes(visible=False, range=list(y_range) if y_range else None,
                         showgrid=False, zeroline=False, fixedrange=True)
        if equal_scale:
            fig.update_yaxes(scaleanchor="x", scaleratio=1)
        return fig

    @classmethod
    def basic_truss(cls) -> go.Figure:
        nodes = {"A": (0.0, 0.0), "B": (4.0, 0.0), "C": (2.0, 2.4)}
        fig = go.Figure()
        for a, b, label in (("A", "B", "Bottom chord AB"), ("A", "C", "Rafter AC"), ("C", "B", "Rafter CB")):
            cls._member(fig, nodes, a, b, label, width=4)
        cls._supports(fig, nodes, ("A", "B"))
        cls._nodes(fig, nodes)
        cls._arrow(fig, (2, 3.1), (2, 2.52), "Load P", label_pos=(2.38, 2.94))
        fig.add_annotation(x=2, y=-.70, text="4 m span", showarrow=False,
                           font={"color": "#617586", "size": 10})
        return cls._base(fig, "Explore the parts of a triangular truss", 390,
                         (-.7, 4.7), (-1.0, 3.35))

    @classmethod
    def truss_types(cls) -> go.Figure:
        fig = go.Figure()
        panels = (("Pratt", 0.0), ("Warren", 4.3), ("Howe", 8.6))
        for title, offset in panels:
            bottom = [(offset + i, 0.0) for i in range(4)]
            if title == "Warren":
                top = [(offset + .5, .75), (offset + 1.5, .75), (offset + 2.5, .75)]
                nodes = {**{n: p for n, p in zip("ABCD", bottom)}, **{n: p for n, p in zip("EFG", top)}}
                members = [(a, b, "Chord") for a, b in zip("ABC", "BCD")] + [(a, b, "Diagonal") for a, b in (("A", "E"), ("E", "B"), ("B", "F"), ("F", "C"), ("C", "G"), ("G", "D"))]
            else:
                top = [(offset + i, .75) for i in range(4)]
                nodes = {**{n: p for n, p in zip("ABCD", bottom)}, **{n: p for n, p in zip("EFGH", top)}}
                members = [(a, b, "Chord") for a, b in zip("ABC", "BCD")] + [(a, b, "Chord") for a, b in zip("EFG", "FGH")]
                members += [(a, b, "Vertical") for a, b in zip("ABCD", "EFGH")]
                if title == "Pratt":
                    members += [("E", "B", "Diagonal"), ("F", "C", "Diagonal"), ("G", "D", "Diagonal")]
                else:
                    members += [("A", "F", "Diagonal"), ("B", "G", "Diagonal"), ("C", "H", "Diagonal")]
            for a, b, typ in members:
                color = cls.GREEN if title == "Pratt" and typ == "Diagonal" else cls.AMBER if title == "Warren" and typ == "Diagonal" else cls.RED if title == "Howe" and typ == "Diagonal" else cls.SLATE if typ == "Vertical" else cls.INK
                cls._member(fig, nodes, a, b, f"{title} {typ.lower()} {a}{b}", color, 2.8 if typ != "Vertical" else 2.1)
            cls._nodes(fig, nodes)
            cls._supports(fig, nodes, ("A", "D"))
            fig.add_annotation(x=offset + 1.5, y=1.2, text=f"<b>{title} truss</b>", showarrow=False,
                               font={"size": 13, "color": cls.TEAL})
        fig.add_annotation(x=1.5, y=-.62, text="Green diagonals", showarrow=False, font={"size": 9, "color": cls.GREEN})
        fig.add_annotation(x=5.8, y=-.62, text="Alternating web", showarrow=False, font={"size": 9, "color": cls.AMBER})
        fig.add_annotation(x=10.1, y=-.62, text="Opposite diagonal pattern", showarrow=False, font={"size": 9, "color": cls.RED})
        return cls._base(fig, "Compare common planar truss configurations", 340,
                         (-.55, 12.7), (-.9, 1.45), equal_scale=False)

    @classmethod
    def determinacy(cls) -> go.Figure:
        fig = go.Figure()
        cases = ((0, "Determinate by count", cls.GREEN, True, False),
                 (3.2, "Redundant by count", cls.AMBER, True, True),
                 (6.4, "Untriangulated", cls.RED, False, False))
        for offset, title, color, diagonal_a, diagonal_b in cases:
            nodes = {"A": (offset, 0), "B": (offset + 2, 0), "C": (offset + 2, 1), "D": (offset, 1)}
            for a, b, label in (("A", "B", "Bottom chord"), ("B", "C", "Vertical"), ("C", "D", "Top chord"), ("D", "A", "Vertical")):
                cls._member(fig, nodes, a, b, f"{label} {a}{b}", cls.SLATE if label == "Vertical" else cls.INK, 2.4)
            if diagonal_a:
                cls._member(fig, nodes, "A", "C", "Diagonal AC", color, 3.2)
            if diagonal_b:
                cls._member(fig, nodes, "B", "D", "Additional diagonal BD", cls.AMBER, 3.2)
            cls._nodes(fig, nodes)
            cls._supports(fig, nodes, ("A", "B"))
            fig.add_annotation(x=offset + 1, y=1.5, text=f"<b>{title}</b>", showarrow=False,
                               font={"size": 11, "color": color})
        return cls._base(fig, "A count is a first check — inspect geometry too", 340,
                         (-.5, 8.8), (-.7, 1.8), equal_scale=False)

    @classmethod
    def method_joints(cls) -> go.Figure:
        nodes = {"A": (0, 0), "B": (4, 0), "C": (0, 3)}
        fig = go.Figure()
        for a, b, label in (("A", "B", "AB bottom chord"), ("A", "C", "AC vertical member"), ("B", "C", "BC diagonal")):
            cls._member(fig, nodes, a, b, label, cls.AMBER if "A" in (a, b) else cls.INK, 4)
        cls._supports(fig, nodes, ("A", "B"))
        cls._nodes(fig, nodes, "A")
        cls._arrow(fig, (0, 0), (.75, 0), "F_AB assumed tension", cls.GREEN, (.42, .28))
        cls._arrow(fig, (0, 0), (0, .8), "F_AC assumed tension", cls.GREEN, (.5, .62))
        fig.add_annotation(x=2.0, y=1.65, text="Start at a joint with ≤ 2 unknowns", showarrow=False,
                           font={"size": 10, "color": "#744900"}, bgcolor="#fff5d8", borderpad=4)
        return cls._base(fig, "Method of joints — isolate a manageable joint", 370,
                         (-.9, 5.1), (-.8, 4.1), equal_scale=False)

    @classmethod
    def method_sections(cls) -> go.Figure:
        nodes = {"A": (0, 0), "B": (1, 0), "C": (2, 0), "D": (3, 0), "E": (4, 0),
                 "F": (0, 1.0), "G": (1, 1.0), "H": (2, 1.0), "I": (3, 1.0), "J": (4, 1.0)}
        fig = go.Figure()
        members = []
        members += [(a, b, "Bottom chord") for a, b in zip("ABCD", "BCDE")]
        members += [(a, b, "Top chord") for a, b in zip("FGHI", "GHIJ")]
        members += [(a, b, "Vertical") for a, b in (("A", "F"), ("B", "G"), ("C", "H"), ("D", "I"), ("E", "J"))]
        members += [(a, b, "Diagonal") for a, b in (("A", "G"), ("B", "H"), ("C", "I"), ("D", "J"))]
        cut = {("B", "C"), ("G", "H"), ("B", "H")}
        for a, b, typ in members:
            is_cut = (a, b) in cut
            right = nodes[a][0] > 1.5 and nodes[b][0] > 1.5
            color = cls.RED if is_cut else "#ccd7dd" if right else cls.SLATE if typ == "Vertical" else cls.INK
            cls._member(fig, nodes, a, b, f"{typ} {a}{b}" + (" — cut member" if is_cut else ""), color, 4 if is_cut else 2.25, "solid")
        cls._nodes(fig, nodes)
        fig.add_shape(type="line", x0=1.5, x1=1.5, y0=-.2, y1=1.3,
                      line={"color": cls.RED, "width": 2, "dash": "dash"})
        fig.add_annotation(x=1.5, y=1.48, text="Section cut", showarrow=False,
                           font={"size": 11, "color": cls.RED})
        for x, y, label in ((1.5, .92, "F₁"), (1.7, .42, "F₂"), (1.5, -.23, "F₃")):
            fig.add_annotation(x=x, y=y, text=f"<b>{label}</b>", showarrow=False,
                               font={"size": 10, "color": cls.RED}, bgcolor="#fff", borderpad=1)
        return cls._base(fig, "Cut through selected members and isolate one side", 360,
                         (-.5, 4.6), (-.6, 1.85), equal_scale=False)

    @classmethod
    def determinate_example(cls) -> go.Figure:
        nodes = {"A": (0, 0), "B": (4, 0), "C": (0, 3)}
        fig = go.Figure()
        for a, b, label, color in (("A", "B", "AB — 20 kN tension", cls.GREEN),
                                   ("A", "C", "AC — 5 kN compression", cls.RED),
                                   ("B", "C", "BC — 25 kN compression", cls.RED)):
            cls._member(fig, nodes, a, b, label, color, 4)
        cls._supports(fig, nodes, ("A", "B"))
        cls._nodes(fig, nodes)
        cls._arrow(fig, (-.85, 3), (0, 3), "Pₓ = 20 kN", label_pos=(-.38, 3.25))
        cls._arrow(fig, (.42, 4.05), (.42, 3.1), "Pᵧ = 20 kN", label_pos=(.95, 3.8))
        cls._arrow(fig, (0, 0), (-.82, 0), "Aₓ = −20", cls.BLUE, (-.53, .24))
        cls._arrow(fig, (0, 0), (0, .63), "Aᵧ = 5", cls.BLUE, (.38, .40))
        cls._arrow(fig, (4, 0), (4, .63), "Bᵧ = 15", cls.BLUE, (4.55, .38))
        return cls._base(fig, "Worked source example: 3–4–5 truss", 390,
                         (-1.45, 5.1), (-.8, 4.55), equal_scale=False)

    @classmethod
    def truss_compatibility(cls) -> go.Figure:
        """A three-member pin-jointed truss with a horizontal redundant at C."""
        nodes = {"A": (0, 0), "B": (4, 0), "C": (0, 3)}
        fig = go.Figure()
        for a, b, label in (("A", "B", "AB · 4 m"), ("A", "C", "AC · 3 m"), ("B", "C", "BC · 5 m")):
            cls._member(fig, nodes, a, b, label, width=4)
        cls._supports(fig, nodes, ("A",))
        # Vertical roller at B: three rollers below the truss support a small plate.
        fig.add_shape(type="line", x0=3.60, x1=4.40, y0=-0.10, y1=-0.10,
                      line={"color": cls.SLATE, "width": 2})
        for xx in (3.78, 4.00, 4.22):
            fig.add_shape(type="circle", x0=xx - 0.07, x1=xx + 0.07, y0=-0.28, y1=-0.14,
                          line={"color": cls.SLATE, "width": 1.2}, fillcolor="#dce5eb")
        fig.add_shape(type="line", x0=3.55, x1=4.45, y0=-0.31, y1=-0.31,
                      line={"color": cls.SLATE, "width": 1.4})
        for xx in (3.63, 3.83, 4.03, 4.23, 4.43):
            fig.add_shape(type="line", x0=xx, x1=xx - 0.08, y0=-0.32, y1=-0.41,
                          line={"color": "#9caeb9", "width": 1})
        # A vertical guide with rollers at C restrains horizontal translation while
        # permitting vertical movement. It is a support at the truss joint C.
        fig.add_shape(type="line", x0=-0.66, x1=-0.66, y0=2.25, y1=3.75,
                      line={"color": cls.SLATE, "width": 3})
        for yy in (2.56, 3.15):
            fig.add_shape(type="circle", x0=-0.48, x1=-0.34, y0=yy - 0.07, y1=yy + 0.07,
                          line={"color": cls.SLATE, "width": 1.5}, fillcolor="#dce5eb")
        fig.add_trace(go.Scatter(x=[-0.34, 0], y=[3, 3], mode="lines",
                                 line={"color": cls.SLATE, "width": 2},
                                 hoverinfo="skip", showlegend=False, name="Horizontal guide connection"))
        cls._nodes(fig, nodes, highlight="C")
        cls._arrow(fig, (0.0, 4.05), (0.0, 3.0), "P = 10 kN ↓", cls.AMBER, (0.70, 3.83))
        cls._arrow(fig, (-0.90, 2.70), (-0.02, 2.70), "R = Cₓ", cls.BLUE, (-0.48, 2.98))
        fig.add_annotation(x=2.1, y=1.45, text="3 members · 3 joints<br><b>one redundant reaction</b>",
                           showarrow=False, bgcolor="#fff5d8", bordercolor="#f3c969", borderpad=6,
                           font={"size": 11, "color": "#744900"})
        fig.add_annotation(x=1.95, y=-0.67, text="Ideal truss: point load is applied at joint C",
                           showarrow=False, font={"size": 10, "color": cls.TEAL},
                           bgcolor="rgba(255,255,255,0.93)")
        return cls._base(fig, "Pin-jointed truss with a redundant horizontal support", 410,
                         (-1.35, 5.0), (-1.0, 4.45), equal_scale=False)

    @classmethod
    def indeterminate_triangle(cls) -> go.Figure:
        nodes = {"A": (0, 0), "B": (4, 0), "C": (0, 3)}
        fig = go.Figure()
        for a, b, label in (("A", "B", "AB — 4 m"), ("A", "C", "AC — 3 m"), ("B", "C", "BC — 5 m")):
            cls._member(fig, nodes, a, b, label, width=4)
        cls._supports(fig, nodes, ("A", "B"))
        cls._nodes(fig, nodes)
        fig.add_shape(type="line", x0=-.35, x1=-.35, y0=2.35, y1=3.65,
                      line={"color": cls.SLATE, "width": 3})
        for yy in (2.62, 3.05):
            fig.add_shape(type="circle", x0=-.27, x1=-.12, y0=yy-.07, y1=yy+.07,
                          line={"color": cls.SLATE, "width": 1.5}, fillcolor="#dce5eb")
        cls._arrow(fig, (.1, 3.25), (.85, 3.25), "Pₓ = 20", label_pos=(.50, 3.5))
        cls._arrow(fig, (.35, 4.02), (.35, 3.16), "Pᵧ = 20", label_pos=(.75, 3.85))
        cls._arrow(fig, (0, 2.72), (-.78, 2.72), "R = Cₓ", cls.BLUE, (-.45, 2.95))
        fig.add_annotation(x=2.3, y=1.0, text="m=3, r=4, j=3<br><b>Dₛ = 1</b>",
                           showarrow=False, bgcolor="#fff5d8", bordercolor="#f3c969", borderpad=6,
                           font={"size": 12, "color": "#744900"})
        return cls._base(fig, "One additional horizontal reaction", 390,
                         (-1.2, 5.0), (-.8, 4.5), equal_scale=False)

    @classmethod
    def rectangular_redundant(cls) -> go.Figure:
        nodes = {"A": (0, 0), "B": (4, 0), "C": (4, 3), "D": (0, 3)}
        fig = go.Figure()
        members = (("A", "B", "AB bottom chord"), ("B", "C", "BC right vertical"),
                   ("C", "D", "CD top chord"), ("D", "A", "DA left vertical"),
                   ("A", "C", "AC retained diagonal"), ("B", "D", "BD selected redundant"))
        for a, b, label in members:
            redundant = (a, b) == ("B", "D")
            cls._member(fig, nodes, a, b, label, cls.RED if redundant else cls.INK,
                        4.5 if redundant else 3, "dash" if redundant else "solid")
        cls._supports(fig, nodes, ("A", "B"))
        cls._nodes(fig, nodes)
        cls._arrow(fig, (4.0, 4.0), (4.0, 3.13), "P = 10 kN", label_pos=(4.55, 3.65))
        fig.add_annotation(x=2.0, y=1.7, text="BD is temporarily removed<br>to form the primary structure",
                           showarrow=False, bgcolor="#fff0f0", bordercolor="#edb5bc", borderpad=4,
                           font={"size": 10, "color": cls.RED})
        fig.add_annotation(x=2.05, y=2.6, text="AC remains", showarrow=False,
                           bgcolor="#edf4ff", font={"size": 9, "color": cls.BLUE}, borderpad=2)
        return cls._base(fig, "Rectangular truss with both diagonals", 390,
                         (-.8, 5.0), (-.9, 4.45), equal_scale=False)

    @classmethod
    def optimization_chain(cls) -> go.Figure:
        fig = go.Figure()
        labels = ["Area A", "Stiffness K", "Displacement U", "Member forces F", "Stress σ", "Constraints"]
        xs = [0.8, 2.6, 4.4, 6.2, 8.0, 9.8]
        colors = [cls.BLUE, cls.TEAL, cls.AMBER, cls.RED, cls.BLUE, cls.GREEN]
        for i, (label, x, color) in enumerate(zip(labels, xs, colors)):
            fig.add_shape(type="rect", x0=x-.65, x1=x+.65, y0=.45, y1=1.45,
                          line={"color": color, "width": 2}, fillcolor="#ffffff")
            fig.add_annotation(x=x, y=.95, text=f"<b>{label}</b>", showarrow=False,
                               font={"size": 10, "color": color})
            if i < len(labels) - 1:
                fig.add_annotation(x=xs[i+1]-.7, y=.95, ax=x+.67, ay=.95,
                                   xref="x", yref="y", axref="x", ayref="y",
                                   text="", showarrow=True, arrowhead=2,
                                   arrowwidth=1.7, arrowcolor=cls.SLATE)
        fig.add_annotation(x=5.3, y=2.0, text="<b>Glass-box design loop</b>", showarrow=False,
                           font={"size": 14, "color": cls.INK})
        fig.add_annotation(x=5.3, y=-.05, text="Minimise material volume subject to stress and displacement limits",
                           showarrow=False, font={"size": 10, "color": "#526878"})
        return cls._base(fig, "Make the design decisions and consequences visible", 290,
                         (-.1, 10.7), (-.35, 2.35), equal_scale=False)
