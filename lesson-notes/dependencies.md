# Managing Dependencies with pip-tools

Using `pip-tools` keeps your top-level packages in `requirements.in` and automatically generates a locked `requirements.txt`.

## 1. Initial Setup
Run these commands once to install the tool and create your input file:
```bash
pip install pip-tools
touch requirements.in
```

## 2. The 3-Step Workflow
Every time you want to install a new dependency, run this sequence:

```bash
# 1. Add the package to your tracking file
echo "requests" >> requirements.in

# 2. Automatically update requirements.txt with pinned dependencies
pip-compile --upgrade requirements.in

# 3. Install the package into your local environment
pip-sync
```
*(Note: `pip-sync` will install new packages and uninstall anything not listed in your files to keep your virtual environment clean).*