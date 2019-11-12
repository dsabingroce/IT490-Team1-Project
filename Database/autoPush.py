import os

os.system("git add --all")
os.system("git commit -m 'Auto-Updated Script'")
os.system("git pull origin staging")
os.system("git push origin development:staging")
