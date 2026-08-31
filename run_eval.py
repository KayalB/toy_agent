import shutil
from agent import run_agent
from grade import grade

TASK = "The tests in this project are failing. Find out why and fix it."
N = 1

results = []
for i in range(N):
    shutil.rmtree("workspace", ignore_errors=True)
    shutil.copytree("env_template", "workspace")

    run = run_agent(TASK, verbose=False)
    score = grade("workspace")

    results.append({**run, "passed": score["passed"]})
    print(f"run {i}: passed={score['passed']} turns={run['turns']} ~${run['cost']:.4f}")

passed = sum(r["passed"] for r in results)
print(f"\n{passed}/{N} passed")
print(f"total cost ~${sum(r['cost'] for r in results):.4f}")