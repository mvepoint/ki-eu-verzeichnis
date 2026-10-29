#!/usr/bin/env python3
"""Prüft, ob Tool-URLs und Quell-URLs erreichbar sind (HTTP 2xx/3xx nach Redirects). Schreibt data/url_check.json."""
import json, subprocess, datetime
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
d=json.load(open("data/tools.json")); out=[]; bad=0
for t in d["tools"]:
    for u in [t["url"]]+t["quellen"]:
        r=subprocess.run(["curl","-sL","-m","25","-A",UA,"-H","Accept: text/html","-H","Accept-Language: de-DE","-o","/dev/null","-w","%{http_code} %{url_effective}",u],capture_output=True,text=True).stdout.split(" ",1)
        code=r[0]; ok=code.startswith(("2","3"))
        bad+= not ok
        out.append(dict(tool=t["slug"],url=u,status=code,final=r[1] if len(r)>1 else "",ok=ok))
        print(("OK " if ok else "FAIL"),code,t["slug"],u)
json.dump(dict(geprueft=datetime.date.today().isoformat(),ergebnisse=out),open("data/url_check.json","w"),indent=2,ensure_ascii=False)
print("fehlerhaft:",bad,"von",len(out))
