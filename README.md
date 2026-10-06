# STAT 112 Quarto Site — Setup Guide

## 0. Prerequisites
- Install [Quarto](https://quarto.org/docs/get-started/) (CLI).
- Install [R](https://cran.r-project.org/) or make sure Python is available if you plan to run code chunks (not required just to render markdown pages).
- Install [Git](https://git-scm.com/) and have a GitHub account.
- (Recommended) [VS Code](https://code.visualstudio.com/) with the "Quarto" extension for live preview.

## 1. Project files (already included in this folder)
```
stat112-site/
├── _quarto.yml              # site config: navbar with Course Info / Computing dropdowns
├── index.qmd                # home page: Quarto "about" (solana) template — photo + About Me
├── course-overview.qmd      # what the course covers
├── course-syllabus.qmd      # textbook, reference books, grading policy, ground rules
├── course-team.qmd          # instructor + TA contact info, office hours
├── course-schedule.qmd      # week-by-week topic table (vizdata.org-style)
├── course-faq.qmd           # frequently asked questions (placeholders — edit freely)
├── computing-setup.qmd      # Tableau/Flourish/Python/DataCamp setup instructions
├── homeworks.qmd            # homework list (placeholder table)
├── recitations.qmd          # weekly recitation notes, one tab per week
├── styles.scss               # custom SCSS theme (note: .scss, not .css — see below)
├── images/                  # put profile.jpeg here
├── .github/workflows/publish.yml   # auto-deploy on every push (optional)
├── .gitignore
└── README.md
```

This mirrors the structure of [vizdata.org](https://vizdata.org) (Duke's STA 313
course site): a "Course Info" dropdown (Overview / Syllabus / Teaching Team /
Schedule / FAQ), a "Computing" dropdown (Setup), plus Recitations and Homeworks
as their own navbar items, and a personal "Home" page built on Quarto's
built-in `about: template: solana` layout.

**Why `.scss` and not `.css`:** when a stylesheet is listed inside `theme: [cosmo, styles.scss]`
in `_quarto.yml`, Quarto treats it as a *theme layer*, which must be valid SCSS with
`/*-- scss:defaults --*/` and `/*-- scss:rules --*/` section markers (a plain `.css`
file in that list will throw a "doesn't contain at least one layer boundary" error).
`styles.scss` in this folder already has both sections — edit the `$primary` color
near the top to change the accent color everywhere at once.

## 2. Add your photo
Put your photo in `images/profile.jpeg` (any name is fine — just update the
`image:` line in `index.qmd` to match).

## 3. Edit the placeholders
- `_quarto.yml`: replace `YOUR_REPO_NAME` in the output settings if needed, and double-check the GitHub/email links on the right of the navbar.
- `index.qmd`: fill in the "About Me" paragraphs and Education/Experience.
- `course-team.qmd`: fill in real office hours (currently "TBD").
- `course-faq.qmd`: replace the placeholder Q&A with real questions as they come up.
- `homeworks.qmd`: fill in the homework table as assignments are posted.
- `recitations.qmd`: replace each week's placeholder text with real notes, slides, code, or datasets as the semester goes on. You can add more tabs (`## Week 15`, etc.) the same way.

## 4. Preview locally
From inside the `stat112-site` folder:
```bash
quarto preview
```
This opens a live-reloading local preview in your browser. Edit any `.qmd` or `.css` file and it updates automatically.

## 5. Create the GitHub repository
```bash
cd stat112-site
git init
git add .
git commit -m "Initial Quarto site"
gh repo create YOUR_REPO_NAME --public --source=. --remote=origin
git push -u origin main
```
(If you don't have the `gh` CLI, create the repo manually on github.com, then
`git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git`
and `git push -u origin main`.)

## 6. Publish to GitHub Pages

**Option A — one-command publish (simplest, good for a first deploy):**
```bash
quarto publish gh-pages
```
This renders the site, creates/pushes a `gh-pages` branch, and prints the
live URL. Run it again any time you want to push updates manually.

**Option B — automatic publish on every push (recommended once the site is stable):**
The included `.github/workflows/publish.yml` file does this for you via
GitHub Actions. After your first push to `main`:
1. Go to your repo on GitHub → **Settings → Pages**.
2. Under "Build and deployment" → **Source**, select **Deploy from a branch**, then branch **gh-pages** (it will be created automatically after the first Action run), folder `/ (root)`.
3. From then on, every `git push` to `main` re-renders and republishes the site automatically — you don't need to run `quarto publish` yourself.

Your site will be live at:
```
https://YOUR_GITHUB_USERNAME.github.io/YOUR_REPO_NAME/
```

## 7. Adding new recitation weeks later
Just edit the `## Week N` sections in `recitations.qmd` (or add new ones),
then either run `quarto publish gh-pages` again, or simply `git push` if
you're using the GitHub Actions workflow.
