import subprocess
import time

# List of scraping scripts
scripts = [
    "indeed_jobs.py",
    "linkedin.py",
    "tmcf_jobs.py",
    "uncf.py"
]

# Run each scraping script
for script in scripts:
    print(f"Running {script}...")
    try:
        subprocess.run(["python", script], check=True)
        print(f"✅ {script} completed successfully.\n")
    except subprocess.CalledProcessError:
        print(f"❌ Error running {script}.\n")

# Wait for 10 seconds before sending email (ensuring files are updated)
time.sleep(30)

# Send the email with CSV files
print("📧 Sending email with job listings...")
try:
    subprocess.run(["python", "automate_email.py"], check=True)
    print("✅ Email sent successfully.\n")
except subprocess.CalledProcessError:
    print("❌ Error sending email.\n")

print("🎯 Daily job scraping & email automation completed!")
