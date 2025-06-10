import os
import re


log_folder = 'stealer_logs_test'  
password_files = []
wallet_files = []
token_dirs = []  

for root, dirs, files in os.walk(log_folder):
    for file in files:
        filepath = os.path.join(root, file)
        if 'password' in file.lower():
            password_files.append(filepath)
        elif 'wallet' in root.lower():
            wallet_files.append(filepath)
        elif 'telegram' in root.lower():
            token_dirs.append(root)
	
password_pattern = re.compile(r'password\s*[:=]\s*(\S+)', re.IGNORECASE)

for pfile in password_files:
    with open(pfile, 'r', errors='ignore') as f:
        for line in f:
            match = password_pattern.search(line)
            if match:
                print(f"[PAROLA] {pfile}: {match.group(1)}")

for wfile in wallet_files:
    print(f"[CÜZDAN DOSYASI] {wfile}")

telegram_token_pattern = re.compile(r'\d{8,10}:[A-Za-z0-9_-]{35,}', re.IGNORECASE)


for tdir in set(token_dirs):  
    for root, dirs, files in os.walk(tdir):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', errors='ignore') as f:
                    content = f.read()
                    tokens = telegram_token_pattern.findall(content)
                    if tokens:
                        print(f"[TELEGRAM TOKEN] {filepath}:")
                        for token in tokens:
                            print(f"  ➤ {token}")
            except Exception as e:
                print(f"[HATA] {filepath}: {e}")
