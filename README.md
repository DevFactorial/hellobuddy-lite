
# HelloBuddy Lite 🚀

**HelloBuddy Lite** is a lightweight, command-line automation tool designed to run seamlessly in the background. It monitors your target job markets using SerpApi, curates the latest relevant job listings, and compiles them into a beautifully structured report delivered straight to your email inbox on a schedule.

---

# 🔑 Credentials Setup Guide

Follow these steps to create your free accounts, get your API tokens, and configure your `config.ini` file.

---

## 🔍 Part 1: Setting up SerpApi (For Job Scraping)

### Step 1: Create an Account
1. Go to the [SerpApi Signup Page](https://serpapi.com/users/sign_up).
2. Register instantly using your **Google** or **GitHub** account, or sign up manually with your email.

### Step 2: Get Your API Key
1. Once logged in, you will be taken directly to your **Dashboard**.
2. Look at the top center of the dashboard for your **Private API Key**. 
3. Click the **Copy** button. 
4. Paste this string straight into your `config.ini` file under:
   ```[API_KEYS]
   SERPAPI_KEY = YOUR_SERPAPI_API_KEY


# 📧 Mailtrap Account Setup & SMTP Guide

Follow these steps to create your free Mailtrap account and capture your SMTP configuration parameters.

---

## 🛠️ Step 1: Create Your Account
1. Navigate to the official [Mailtrap Sign Up Page](https://mailtrap.io/register/signup?ref=header).
2. Choose your preferred registration pathway:
   * **Social Sign-On:** Authenticate instantly using your **Google**, **GitHub**, or **Office 365** credentials.
   * **Traditional Email:** Supply your email address and create a strong, secure password.
3. If prompted via a verification banner, check your registration inbox and confirm your email link to unlock your full dashboard dashboard workspace.

---

## 🔑 Step 2: Extract Your API Key
Mailtrap defaults new accounts into an **Email Sandbox environment**—this allows your background Python daemon to safely test HTML email layouts without accidentally sending broken formatting to a live public inbox.

1. Locate the navigation tree in the left sidebar menu.
2. Click on **Sandboxes** header.
3. Click on **"My Sandbox"**.
4. Select the **API Tokens** menu option.
5. Click on **Add Token**. Provide a name and click on **Save**
6. Copy the API Token generated.

---

## 🛠️ Installation & Setup

Follow these quick steps to get your local environment up and running from the project root folder.

### 1. Create and Activate a Virtual Environment
It is highly recommended to use an isolated virtual environment to avoid version conflicts with other Python packages on your system.

* **On macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate

  ```

* **On Windows (Command Prompt):**
  ```cmd
    python -m venv venv
    call venv\Scripts\activate
 
  ```


* **On Windows (PowerShell):**
  ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1

  ```



### 2. Install Dependencies

Once your virtual environment is active (you should see `(venv)` at the beginning of your terminal line), install the required packages from the project root:

```bash
pip install -r requirements.txt

```

---

## ⚙️ Configuration (`config.ini`)

Before running the application, you need to configure your settings. Update the file named `config.ini` in your **project root folder** and fill in your specific details:

```ini
[STORAGE]
# Absolute path to the directory where you want the store the reports.
JOB_REPORT_OUTPUT_PATH = <ABSOLUTE_PATH_TO_OUTPUT_DIRECTORY>

[EMAIL]
# Email address to which the report will be sent.
RECIPIENT = 

[SCHEDULER]
# The time of day you want the report generated and emailed (24-hour format HH:MM)
JOB_TIME = 13:54

[API_KEYS]
# Your official SerpApi API Key (Keep this secret!)
SERPAPI_KEY = <YOUR_SERPAPI_KEY>
# Your official Mail Trap API Key (Keep this secret!)
MAILTRAP_API_TOKEN = < YOUR_MAILTRAP_API_TOKEN>

[SEARCH_SETTINGS]
NUM_PAGES = 2
# The target job role (e.g., AI Architect, Python Developer)
SEARCH_QUERY = <YOUR_JOB_SEARCH_QUERY>
# A valid geographic region or country matching the target market
SEARCH_LOCATION = <YOUR_JOB_SEARCH_LOCATION> # e.g., "New York, NY", "San Francisco, CA", etc.
# The two-letter country code matching your target market (e.g., in, us, uk)
SEARCH_COUNTRY = <YOUR_JOB_SEARCH_COUNTRY CODE>  # e.g., "us" for United States, "in" for India, etc.

```

---

## 🏃 Running the Application

With your virtual environment active and your `config.ini` completely filled out, kickstart the background worker by running the following command from the project root folder:

```bash
python app/main.py

```

> **💡 Run in Background:** If you are running this on a remote server or want to close your terminal without killing the app, you can use background utilities like `nohup` or `tmux` on Linux/macOS:
> ```bash
> nohup python app/main.py > output.log 2>&1 &
> 
> ```
> 
> 

---

## 🤝 Happy Job Hunting!

Sit back, relax, and let **HelloBuddy Lite** keep its eyes on the market for you. If you need to stop the scheduler at any time, simply press `CTRL + C` in your active terminal session.

```

```
