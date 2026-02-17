# Complete Terminal Workflow for Assignment 2 (DVC + Git)

## Initial Setup
```bash
# 1. Create folder structure
mkdir -p data/raw data/processed notebooks src
mv raw_data.csv data/raw/raw_data.csv
mv prepare.ipynb notebooks/
```

## DVC + Git Version 1 (seed=42)
```bash
# 2. Initialize repo
git init
dvc init

# 3. Track raw data
dvc add data/raw/raw_data.csv
git add data/raw/.gitignore data/raw/raw_data.csv.dvc
git commit -m "v1: Add raw data"

# 4. Run notebook (seed=42) → creates splits
cd notebooks && jupyter notebook prepare.ipynb  # Cells 2-6
cd ..

# 5. Track splits
dvc add data/processed/train.csv data/processed/validation.csv data/processed/test.csv
git add data/processed/.gitignore data/processed/*.csv.dvc
git commit -m "v1: Add processed splits (seed=42)"
```

## DVC Version 2 (seed=28)
```bash
# 6. Create v2 splits
# Edit notebooks/prepare.ipynb: SPLIT_RANDOM_STATE = 28
# Rerun Cells 2-6

# 7. Track v2
dvc add data/processed/*.csv
git add data/processed/*.csv.dvc data/processed/.gitignore
git commit -m "v2: Updated splits (seed=123)"
```

## Push to GitHub
```bash
# 8. Upload (after removing .git clash)
mv .git .git-backup
cd ..
```
