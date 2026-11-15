# %% [markdown]
# # Setup check
#
# Run every cell once before Day 1. It imports the libraries the labs use, reads the data files of Mashraq Municipal Permits Office and draws one seeded number. Nothing here calls or downloads a model.

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ds-205.git"
    if not Path("/content/ds-205").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ds-205"], check=True)
    os.chdir("/content/ds-205/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("mashraq.py").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import numpy as np
import pandas as pd
import mashraq as U
print("mode:", U.MODE)

# %%
import importlib

missing = []
for name in ("numpy", "pandas", "scipy", "statsmodels", "matplotlib"):
    try:
        mod = importlib.import_module(name)
        print(f"✅ {name} {mod.__version__}")
    except ImportError:
        missing.append(name)
        print(f"❌ {name} is missing")

# %%
counts = {"history days": len(U.history()), "past notices": len(U.units_notices()), "holders in the reminder test": len(U.renewal_test()),
          "rows in the platform export": len(U.notice_log()), "page views": len(U.form_pages()), "branches": len(U.branches()),
          "counter visits": len(U.counter_visits()), "studies": len(U.js("studies.json"))}
for k, v in counts.items():
    print(f"{k:<30}{v:>8,}")
ok = counts["history days"] == 182 and counts["holders in the reminder test"] == 60_000 and counts["branches"] == 24 and counts["studies"] == 6
U.check(ok, "the data files are complete: 182 days of history, 60,000 holders in the reminder test, 24 branches, 6 studies")

# %%
x = float(U.rng(1).binomial(1000, 0.62) / 1000)
print(f"a seeded draw of 1,000 holders at 62% gives {x:.1%}; your neighbour should read the same number")
h = U.history()
plt = U.plt()
plt.plot(h["notices_sent"].to_numpy())
plt.title("Notices sent per day, 182 days")
plt.xlabel("day")
plt.show()

# %%
if missing:
    print("Missing:", ", ".join(missing), "· locally run `uv sync` in labs/; in Colab rerun the first cell.")
else:
    print("Ready for Day 1.")
