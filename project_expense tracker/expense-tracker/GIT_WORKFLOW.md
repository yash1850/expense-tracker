# Git workflow (do these yourself so the history is yours)

Each block = one feature branch -> commit -> push -> Pull Request on GitHub -> merge -> pull main.

## 0. Setup (once)
```
cd expense-tracker
git init
git branch -M main
git add .gitignore README.md
git commit -m "Initial commit: add gitignore and README"
git remote add origin https://github.com/<your-username>/expense-tracker.git
git push -u origin main
```

## 1. Database scripts
```
git checkout -b feature/database
git add sql/
git commit -m "Add schema, load and report SQL"
git push -u origin feature/database
```

## 2. Docker setup
```
git checkout -b feature/docker-setup
git add Dockerfile .env.example
git commit -m "Add Dockerfile and env example"
git push -u origin feature/docker-setup
```

## 3. Sample data
```
git checkout -b feature/sample-data
git add data/
git commit -m "Add sample CSV and CSV with errors"
git push -u origin feature/sample-data
```

## 4. Python validation
```
git checkout -b feature/validation
git add app/
git commit -m "Add Pydantic model and CSV validation app"
git push -u origin feature/validation
```

After each push: on GitHub click **Compare & pull request** -> **Merge pull request**, then:
```
git checkout main
git pull origin main
```

## Useful checks
```
git status
git branch
git log --oneline --graph
```
