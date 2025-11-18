from typing import List, Dict, Any
from Declare4Py.ProcessModels.LTLModel import LTLTemplate
from codeclare.models.codeclare_model import Constraint

# Try different parser imports depending on pylogics version
try:
    from pylogics.parsers.ltl import parse_ltlf
except Exception:
    try:
        from pylogics.parsers.ltl import parse_ltl as parse_ltlf
    except Exception:
        try:
            from pylogics.parsers import ltlf
            parse_ltlf = ltlf.parse
        except Exception:
            print("Warning: pylogics.parse_ltlf not found; using raw string parser.")
            parse_ltlf = lambda s: s


def _clean(formula_str: str) -> str:
    # Remove Declare4Py's 'con_' prefix (added internally by templates)
    return formula_str.replace("con_", "")


class LTLfGenerator:
    """
    Converts declarative constraints into LTLf formulas and their
    corresponding pylogics object representation.
    """

    def __init__(self, constraints: List[Dict[str, Any]]):
        self.constraints = constraints

        # Build supported templates dynamically from ConstraintLibrary
        self.supported = set(t.lower() for t in Constraint.all())

        # Add manual (non-Declare4Py) templates
        self.manual_templates = {"absence2", "neg_succession", "not_coexistence", "succession", "existence"}

    # ------------------------------------------------------------------
    # Manual templates (custom LTLf definitions)
    # ------------------------------------------------------------------
    def _manual(self, name: str, acts: List[str]) -> str:
        if name == "absence2":
            a, = acts
            return f"!F({a} && X(F({a})))"
        if name == "neg_succession":
            a, b = acts
            return f"G({a} -> !F({b}))"
        if name == "not_coexistence":
            a, b = acts
            return f"!((F({a})) && (F({b})))"
        if name == "succession":
            a, b = acts
            return f"G({a} -> F({b})) && (!{b}) U {a}"

        if name == "existence":
            if len(acts) != 1:
                raise ValueError("Existence template requires exactly one activity.")
            a = acts[0]
            return f"F({a})"

        raise KeyError(name)

    def _declare4py(self, template_name: str, acts: List[str]) -> str:

        if template_name == "response":
            a = acts[0]
            b = acts[1]

            
            if isinstance(b, str) and b.startswith("[") and b.endswith("]"):
                items = [x.strip() for x in b[1:-1].split(",")]
                b_disj = " || ".join(items)  
                return f"G(({a}) -> F({b_disj}))"
    

        # Normal Declare4Py handling
        t = LTLTemplate(template_name)

        if len(acts) == 0:
            model = t.fill_template([])
        elif len(acts) == 1:
            model = t.fill_template(acts)
        elif len(acts) == 2:
            model = t.fill_template([acts[0]], [acts[1]])
        else:
            raise ValueError(
                f"Template '{template_name}' expects at most 2 activities, got {len(acts)}"
            )

        return _clean(model.formula)

    # ------------------------------------------------------------------
    # Main generator
    # ------------------------------------------------------------------
    def generate(self) -> List[Dict[str, Any]]:
        results = []

        for c in self.constraints:
            name = c["template"].lower()
            acts = c["activities"]

            # Skip unsupported constraints
            if name not in self.supported and name not in self.manual_templates:
                print(f"Skipping unknown template '{name}'")
                continue

            try:
                # Build formula string
                if name in self.manual_templates:
                    s = self._manual(name, acts)
                else:
                    s = self._declare4py(name, acts)

                # Parse to LTLf AST object
                obj = parse_ltlf(s)

                results.append({
                    "template": name,
                    "activities": acts,
                    "obj": obj,
                    "ltlf": s,
                })
            except Exception as e:
                print(f"Error in template '{name}' ({acts}): {e}")

        return results
