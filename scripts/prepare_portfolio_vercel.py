import os

PORTFOLIO_DIR = r"C:\Users\KIIT\OneDrive\Documents\Karan-Portfolio"

def update_gitignore():
    gitignore_path = os.path.join(PORTFOLIO_DIR, ".gitignore")
    with open(gitignore_path, "r", encoding="utf-8") as f:
        content = f.read()
    if "scratch/" not in content:
        with open(gitignore_path, "a", encoding="utf-8") as f:
            f.write("\n# Scratch and local test scripts\nscratch/\n")
        print("Updated .gitignore with scratch/")
    else:
        print(".gitignore already contains scratch/")

def create_vercel_json():
    vercel_path = os.path.join(PORTFOLIO_DIR, "vercel.json")
    content = """{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "cleanUrls": true,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        }
      ]
    }
  ]
}
"""
    with open(vercel_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Created vercel.json in portfolio root")

def create_vercel_deployment_doc():
    docs_dir = os.path.join(PORTFOLIO_DIR, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    doc_path = os.path.join(docs_dir, "VERCEL_DEPLOYMENT.md")
    content = """# Vercel Deployment Guide — Personal Portfolio

**Project:** Priyanshu Karan — Personal Portfolio Website  
**Repository:** [https://github.com/karan-rajput872/Portfolio](https://github.com/karan-rajput872/Portfolio)  
**Production Branch:** `main`  
**Architecture:** Static HTML/CSS/JavaScript with Node.js Serverless Function (`api/contact.js`)

---

## 1. Architecture & Vercel Detection Overview

The portfolio is structured as a high-performance, responsive static website with zero heavyweight runtime dependencies:
* **Entry Point:** `index.html` (Main portfolio landing page)
* **Dedicated Case Study:** `planet-hunters.html` (Planet Hunters ML engineering deep dive)
* **Styling:** `style.css` (Curated dark mode, glassmorphism, responsive CSS grid/flexbox)
* **Client Logic:** `script.js` (Dynamic project rendering, modal management, filtering, resume viewer)
* **Metadata Source of Truth:** `developer.json` (Profile information)
* **Serverless Contact API:** `api/contact.js` (Serverless endpoint integrating Resend for contact inquiries)
* **Configuration:** `vercel.json` (Enables clean URLs and production security headers)

Because the project does not require a bundler (Webpack, Vite, Next.js), Vercel deploys the static files directly to its global Edge CDN and compiles `api/contact.js` as an AWS Lambda / Vercel Serverless Function.

---

## 2. Vercel Project Setup Instructions

### Step 1: Import Repository
1. Log in to [Vercel Dashboard](https://vercel.com/dashboard).
2. Click **"Add New..."** → **"Project"**.
3. Select your GitHub provider and search for: `karan-rajput872/Portfolio`.
4. Click **"Import"**.

### Step 2: Configure Project Settings
In the **Configure Project** screen, set the exact parameters below:

| Configuration Setting | Required Value | Notes |
|---|---|---|
| **Project Name** | `portfolio` or `priyanshu-karan-portfolio` | Subdomain on `.vercel.app` |
| **Framework Preset** | **`Other`** | Do NOT select Next.js, Vite, or Create React App |
| **Root Directory** | **`./`** (Root of repository) | Default root folder |
| **Build Command** | *Leave empty / Override disabled* | No build step required |
| **Output Directory** | *Leave empty / Override disabled* | Root directory is served directly |
| **Install Command** | *Leave empty / Override disabled* | No npm install required for static serving |

### Step 3: Environment Variables (Optional for Contact Form)
If you wish to enable the contact form via Resend:
* `RESEND_API_KEY`: Your Resend API key (e.g., `re_123456789...`)
* `CONTACT_RECIPIENT_EMAIL`: `priyanshukaran25@gmail.com` (Destination inbox)
* `RESEND_FROM_EMAIL`: `Portfolio Contact <onboarding@resend.dev>` (or your verified domain sender)

> **Note:** If `RESEND_API_KEY` is not provided, the contact form gracefully displays a configuration message without crashing the website.

### Step 4: Click Deploy
Click **"Deploy"**. Vercel will complete the deployment in under 15 seconds.

---

## 3. Local Preview Workflow

You can preview the portfolio locally before committing changes to GitHub using either of the following commands:

### Method A: Static Python HTTP Server (Recommended for Fast Preview)
Run from the `Karan-Portfolio` directory:
```bash
python -m http.server 5500
```
Open your browser at:
```
http://localhost:5500
```
* Main Portfolio: `http://localhost:5500/` or `http://localhost:5500/index.html`
* Planet Hunters Case Study: `http://localhost:5500/planet-hunters.html`

*(If Python is in a virtual environment, run with the full python path, e.g., `path\\to\\.venv\\Scripts\\python.exe -m http.server 5500`)*

### Method B: Node.js Local Server (Includes Local Contact API)
Run from the `Karan-Portfolio` directory:
```bash
node server.js
# Or using npm
npm start
```
Open your browser at:
```
http://localhost:3000
```
This local server serves static files and routes `/api/contact` requests to `api/contact.js`.

---

## 4. Git Branching & Continuous Deployment Workflow

* **Production Deployments:**
  Every push to the `main` branch automatically triggers an instant production deployment on Vercel.
  ```bash
  git checkout main
  git add .
  git commit -m "feat: your update description"
  git push origin main
  ```
* **Preview Deployments:**
  When making experimental updates, create a feature branch:
  ```bash
  git checkout -b feature/new-update
  git commit -am "experiment: testing new layout"
  git push origin feature/new-update
  ```
  Vercel automatically creates a unique Preview URL for testing before merging to `main`.

---

## 5. Clean URLs & Routing

Thanks to `vercel.json` with `"cleanUrls": true`, both route formats are supported seamlessly:
* `https://your-domain.vercel.app/` → Serves `index.html`
* `https://your-domain.vercel.app/planet-hunters` → Serves `planet-hunters.html`
* `https://your-domain.vercel.app/planet-hunters.html` → Serves `planet-hunters.html`
* `https://your-domain.vercel.app/api/contact` → Executes serverless function `api/contact.js`

---

## 6. Common Deployment Issues & Solutions

1. **404 on Assets / Images:**
   * Cause: Absolute paths like `C:\\Users\\...` or missing files.
   * Verification: All paths in `index.html` and `planet-hunters.html` use relative paths (`assets/images/...`, `assets/certificates/...`, `assets/resume/...`).
   * Fix: Verified on disk; all assets exist and are committed to GitHub.

2. **Vercel Build Failure ("No Output Directory"):**
   * Cause: Selecting a framework preset like Next.js that expects an `out` or `.next` folder.
   * Fix: Ensure **Framework Preset** is set to **`Other`** with **Build Command** left empty.

3. **Contact Form 503 Service Unavailable:**
   * Cause: Missing `RESEND_API_KEY` in Vercel project environment variables.
   * Fix: Add `RESEND_API_KEY` in Vercel Dashboard → Settings → Environment Variables, then redeploy.
"""
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Created docs/VERCEL_DEPLOYMENT.md in portfolio")

if __name__ == "__main__":
    update_gitignore()
    create_vercel_json()
    create_vercel_deployment_doc()
    print("Portfolio preparation for Vercel completed successfully.")
