import json
from typing import List, Dict, Any

class Constraint:
    """Comprehensive LTLf and Target-Branched Declare templates supported by Declare4Py."""

    
    EVENTUALLY_A = "eventually_a"
    NEXT_A = "next_a"
    EVENTUALLY_A_AND_EVENTUALLY_B = "eventually_a_and_eventually_b"
    EVENTUALLY_A_THEN_B = "eventually_a_then_b"
    EVENTUALLY_A_OR_B = "eventually_a_or_b"
    EVENTUALLY_A_NEXT_B = "eventually_a_next_b"
    EVENTUALLY_A_THEN_B_THEN_C = "eventually_a_then_b_then_c"
    EVENTUALLY_A_NEXT_B_NEXT_C = "eventually_a_next_b_next_c"

    IS_FIRST_STATE_A = "is_first_state_a"
    IS_SECOND_STATE_A = "is_second_state_a"
    IS_THIRD_STATE_A = "is_third_state_a"
    LAST = "last"
    SECOND_LAST = "second_last"
    THIRD_LAST = "third_last"
    IS_LAST_STATE_A = "is_last_state_a"
    IS_SECOND_LAST_STATE_A = "is_second_last_state_a"
    IS_THIRD_LAST_STATE_A = "is_third_last_state_a"

    P_DOES_A = "p_does_a"
    A_IS_DONE_BY_P_AND_Q = "a_is_done_by_p_and_q"
    P_DOES_A_AND_B = "p_does_a_and_b"
    P_DOES_A_AND_THEN_B = "p_does_a_and_then_b"
    P_DOES_A_AND_EVENTUALLY_B = "p_does_a_and_eventually_b"
    P_DOES_A_A_NOT_B = "p_does_a_a_not_b"
    A_DONE_BY_P_P_NOT_Q = "a_done_by_p_p_not_q"

    PRECEDENCE = "precedence"
    CHAIN_PRECEDENCE = "chain_precedence"
    RESPONDED_EXISTENCE = "responded_existence"
    CHAIN_RESPONSE = "chain_response"
    NOT_CHAIN_PRECEDENCE = "not_chain_precedence"
    NOT_CHAIN_RESPONSE = "not_chain_response"
    RESPONSE = "response"
    NOT_PRECEDENCE = "not_precedence"
    NOT_RESPONSE = "not_response"
    NOT_RESPONDED_EXISTENCE = "not_responded_existence"
    ALTERNATE_RESPONSE = "alternate_response"
    ALTERNATE_PRECEDENCE = "alternate_precedence"

    ABSENCE2 = "absence2"
    NEG_SUCCESSION = "neg_succession"
    NOT_COEXISTENCE = "not_coexistence"
    SUCCESSION = "succession"  
    EXISTENCE = "existence"    

    @classmethod
    def all(cls):
        """Return all available constraint template names."""
        return [
            getattr(cls, attr)
            for attr in dir(cls)
            if attr.isupper() and not attr.startswith("__")
        ]

class CoDeclareModel:
    """
    A class representing a coDECLARE model with typed constraint templates.
    """

    def __init__(self):
        self.environment: List[str] = []
        self.system: List[str] = []
        self.assumptions: List[Dict[str, Any]] = []
        self.guarantees: List[Dict[str, Any]] = []

   
    def add_environment_activity(self, name: str):
        if name not in self.environment:
            self.environment.append(name)

    def add_system_activity(self, name: str):
        if name not in self.system:
            self.system.append(name)

  
    def _validate_template(self, template: str):
        if template not in Constraint.all():
            raise ValueError(
                f"Invalid constraint '{template}'.\n"
                f"Available templates: {', '.join(Constraint.all())}"
            )

    def add_assumption(self, template: str, activities: List[str]):
        self._validate_template(template)
        self.assumptions.append({
            "template": template,
            "activities": activities
        })

    def add_guarantee(self, template: str, activities: List[str]):
        self._validate_template(template)
        self.guarantees.append({
            "template": template,
            "activities": activities
        })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "environment": self.environment,
            "system": self.system,
            "assumptions": self.assumptions,
            "guarantees": self.guarantees
        }

    def to_json(self, path: str):
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f" Model saved to {path}")

 
    # Load from JSON
    @classmethod
    def from_json(cls, path: str) -> "CoDeclareModel":
        with open(path) as f:
            data = json.load(f)

        model = cls()
        model.environment = data.get("environment", [])
        model.system = data.get("system", [])
        model.assumptions = data.get("assumptions", [])
        model.guarantees = data.get("guarantees", [])
        return 
    
