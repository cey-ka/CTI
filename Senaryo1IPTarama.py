import requests
import json
import os
import time

API_KEY = "kullanilan_api_key"
INPUT_FILE = "ips.txt"
MALICIOUS_FILE = "malicious_ips.txt"
NOT_FOUND_FILE = "not_found_ips.txt"
RESPONSES_DIR = "responses"


VT_URL = "https://www.virustotal.com/api/v3/ip_addresses/{}"
HEADERS = {
    "x-apikey": API_KEY
}


os.makedirs(RESPONSES_DIR, exist_ok=True)


with open(INPUT_FILE, "r") as ip_file, \
     open(MALICIOUS_FILE, "w") as mal_file, \
     open(NOT_FOUND_FILE, "w") as nf_file:

    for line in ip_file:
        ip = line.strip()
        if not ip:
            continue

        url = VT_URL.format(ip)
        try:
            response = requests.get(url, headers=HEADERS)
            if response.status_code == 200:
                data = response.json()


                with open(f"{RESPONSES_DIR}/{ip}.json", "w") as out_json:
                    json.dump(data, out_json, indent=4)

                stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                malicious = stats.get("malicious", 0)
                suspicious = stats.get("suspicious", 0)

                if malicious > 0 or suspicious > 0:
                    mal_file.write(f"{ip}\n")

            elif response.status_code == 404:
                nf_file.write(f"{ip}\n")
            else:
                print(f"[!] API Error {response.status_code} for IP: {ip}")
        except Exception as e:
            print(f"[!] Exception for IP {ip}: {e}")

        time.sleep(15)

print("IP tarama tamamlandı.")
