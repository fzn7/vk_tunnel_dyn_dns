import os, re, time

LOG = '/shared/tunnel.log'
OUT = '/shared/current_url'

os.makedirs('/shared', exist_ok=True)
open(LOG, 'a').close()

# ловим любой https-URL на *.vk-apps.com (включая /path, если есть)
pat = re.compile(r'(https?://[A-Za-z0-9.-]+\.vk-apps\.com(?:/[^\s]*)?)')

def write(u: str):
    tmp = OUT + '.tmp'
    with open(tmp, 'w') as f:
        f.write(u.strip())
    os.replace(tmp, OUT)
    print('[watcher] upstream ->', u, flush=True)

# первичный прогон по уже накопившемуся логу
with open(LOG, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        m = pat.search(line)
        if m:
            write(m.group(1))

# follow: ждём новые строки и парсим на лету
with open(LOG, 'r', encoding='utf-8', errors='ignore') as f:
    f.seek(0, os.SEEK_END)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.5)
            continue
        m = pat.search(line)
        if m:
            write(m.group(1))
