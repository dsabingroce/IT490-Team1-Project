import os

os.system("git add --all")
os.system("git commit -m 'Auto-Updated Script'")
os.system("git push origin staging")
os.system("git pull origin master")
os.system("git push origin staging:master")
