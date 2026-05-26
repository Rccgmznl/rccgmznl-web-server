# Git Workflow

## Branch Structure

```text
main -> stable production-ready branch
dev  -> integration/testing branch
feat/* -> feature branches
````

---

## Sync Latest Changes

Always sync with `dev` before starting work:

```bash
git checkout dev
git pull origin dev
```

---

## Create Feature Branch

Create a new feature branch from `dev`:

```bash
git checkout -b feat/your-feature-name
```

Example:

```bash
git checkout -b feat/auth-system
```

---

## Work Normally

Commit frequently:

```bash
git add .
git commit -m "feat(auth): add login validation"
```

---

## Push Feature Branch

```bash
git push origin feat/your-feature-name
```

---

## Create Pull Request

Create a PR targeting `dev`:

```bash
gh pr create
```

---

## Before Opening a PR

Ensure:

```text
- latest dev branch is pulled
- tests pass
- project runs correctly
- merge conflicts are resolved
```

---

## Merge Flow

```text
feature branch
    ↓
pull request → dev
    ↓
integration/testing
    ↓
dev → main
```

---

## Notes

* Pull frequently to reduce conflicts
* Keep commits focused and readable
* Commit history may be squashed during merge
* Do not commit secrets or `.env` files
