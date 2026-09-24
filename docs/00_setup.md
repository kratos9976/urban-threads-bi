# Step 0 — Project Setup (run on your machine)

```bash
# 1. Create repo
mkdir urban-threads-bi && cd urban-threads-bi
git init
git branch -M main

# 2. Python virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Core dependencies for Steps 0-2
pip install pandas numpy faker python-dotenv

# 4. .gitignore
cat > .gitignore << 'EOF'
venv/
__pycache__/
*.pyc
.env
data/processed/
.DS_Store
EOF

# 5. First commit
git add .
git commit -m "Step 0: project scaffolding"

# 6. Create GitHub repo (via gh CLI, or do it manually on github.com) and push
gh repo create urban-threads-bi --public --source=. --remote=origin
git push -u origin main
```

## Git workflow going forward
- `main` = always working/demo-ready
- One branch per step: `git checkout -b step-1-business-case`
- Commit at the end of each working session, even if incomplete: `git commit -m "WIP: step 2 dataset gen"`
- Merge back to `main` when a step is genuinely done: `git checkout main && git merge step-1-business-case`
