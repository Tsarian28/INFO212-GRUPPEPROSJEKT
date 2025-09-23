# INFO212-GRUPPEPROSJEKT
Semesterprosjekt høst 2025 info 212

# 👩‍💻 Team GitHub Workflow Guide

This is how we will collaborate on this project. Please **follow these steps every time** you work on the code to keep `main` clean and avoid conflicts.

---

## ✅ Step-by-step Checklist

### 1. Before starting work
- [ ] Make sure you are up to date:
  ```bash
  git pull origin main
2. Create a new branch for your task
 Never work directly on main

 Create a branch named after your task/feature:

git checkout -b feature-name
3. Do your work and commit
 Make small commits with clear messages:

git add .
git commit -m "Describe what you changed"
4. Push your branch to GitHub
 Upload your branch:


git push origin feature-name
5. Open a Pull Request (PR)
 Go to GitHub and open a PR from your branch → main

 Ask a teammate to review it

6. Review and merge
 Teammate reviews the PR

 Fix issues if needed

 Merge into main only when approved and tested

7. Clean up (optional, but recommended)
 Delete your branch after merge:

git branch -d feature-name        # delete locally
git push origin --delete feature-name   # delete on GitHub


🚦 Golden Rule
NEVER code directly on main.
Always: branch → commit → push → pull request → review → merge.
