# Planet Hunters — Vercel Web Deployment Guide

## 1. Architecture Overview

The Planet Hunters project features a dual-deployment model:

1. **Python Streamlit Intelligence Platform (Original Application):**
   - **Repository Root:** `/` (`dashboard/app.py`)
   - **Platform:** Streamlit Community Cloud
   - **Status:** Unchanged, independently active at [https://planet-hunters-round1-3bvwv7d4umhsshfcvsvc8h.streamlit.app/](https://planet-hunters-round1-3bvwv7d4umhsshfcvsvc8h.streamlit.app/)
2. **Next.js Scientific Web Application (New Frontend):**
   - **Repository Subdirectory:** `web/`
   - **Platform:** Vercel
   - **Stack:** Next.js 16 (App Router), TypeScript, Tailwind CSS, Recharts, Lucide Icons

---

## 2. Vercel Deployment Instructions

Follow these step-by-step instructions to deploy the modern web application to Vercel:

### Step 1: Connect Repository to Vercel
1. Log in to your [Vercel Dashboard](https://vercel.com/dashboard).
2. Click **"Add New..."** → **"Project"**.
3. Select your GitHub account and import the repository:
   ```
   https://github.com/karan-rajput872/Planet-Hunters-Round1
   ```

### Step 2: Configure Project Root Directory (CRITICAL)
In the Vercel project configuration modal:
1. Locate the **Root Directory** field.
2. Click **"Edit"** and select or type:
   ```text
   web
   ```
3. Click **"Continue"**.

> [!IMPORTANT]
> Setting the Root Directory to `web` ensures Vercel installs dependencies from `web/package.json` and does not attempt to build the root Python workspace or interfere with Streamlit.

### Step 3: Verify Build & Development Settings
Vercel automatically detects Next.js:
- **Framework Preset:** `Next.js`
- **Build Command:** `next build` (Default)
- **Output Directory:** `.next` (Default)
- **Install Command:** `npm install` (Default)

### Step 4: Environment Variables
No custom environment variables or API keys are required. The application serves deterministic precomputed predictions and offline validation benchmarks from typed data models.

### Step 5: Deploy
Click **"Deploy"**. Vercel will:
1. Clone the repository on branch `feature/vercel-web-rebuild` (or `main` after merge).
2. Change directory into `web/`.
3. Install frontend dependencies (`lucide-react`, `recharts`, `tailwindcss`, `next`, `react`).
4. Execute `next build` and generate static production assets.
5. Provide a live production `.vercel.app` URL.

---

## 3. Local Development & Testing

To run the Next.js web application locally on your machine:

```powershell
# Navigate into the frontend directory
cd web

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Production Build Verification Command:
```powershell
cd web
npm run build
```

### Linting Verification Command:
```powershell
cd web
npm run lint
```

---

## 4. Retaining the Original Streamlit Dashboard

- The original Streamlit dashboard is deployed from the repository root via `dashboard/app.py`.
- Because the Next.js application is strictly isolated in `web/`, the Streamlit Community Cloud deployment remains completely untouched.
- The approved submission artifact `submissions/submission_FINAL.csv` (`6A378EAE...330E`) is never modified by either application.
