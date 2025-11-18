from codeclare.models.codeclare_model import Constraint, CoDeclareModel
from pathlib import Path
import subprocess

# Create the coDECLARE model

model = CoDeclareModel()

# Environment and system activities
for a in ["regaddr", "pay", "reqc", "open"]:
    model.add_environment_activity(a)
for b in ["skip", "ship", "cancel", "refund"]:
    model.add_system_activity(b)

# Add assumptions using the ConstraintLibrary

model.add_assumption(Constraint.PRECEDENCE, ["regaddr", "ship"])
model.add_assumption(Constraint.RESPONSE, ["open", "regaddr"])
model.add_assumption(Constraint.ABSENCE2, ["pay"])

# Add guarantees using the ConstraintLibrary
model.add_guarantee(Constraint.NEG_SUCCESSION, ["reqc", "pay"])
model.add_guarantee(Constraint.RESPONSE,["reqc", "[cancel, refund]"])
model.add_guarantee(Constraint.SUCCESSION, ["pay", "ship"])

# Save model to input folder

Path("input").mkdir(exist_ok=True)
model_path = Path("input/order.json")
model.to_json(str(model_path))

subprocess.run(["python3", "-m", "codeclare.main", "--in", str(model_path)], check=True)
