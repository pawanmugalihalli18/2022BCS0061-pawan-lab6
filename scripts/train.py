import json
import os
import random

os.makedirs("app/artifacts", exist_ok=True)

# fake training accuracy
accuracy = round(random.uniform(0.7, 0.99), 4)

metrics = {
    "accuracy": accuracy
}

with open("app/artifacts/metrics.json", "w") as f:
    json.dump(metrics, f)

print(f"Training done. Accuracy: {accuracy}")