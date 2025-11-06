#!/usr/bin/env python3
import yaml
import os

# --- HTML TEMPLATE ---
TEMPLATE_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Core System Environments</title>
<style>
body {background:#eef2f5;font-family:"Segoe UI",Arial,sans-serif;margin:0;}
header {
  position: relative;
  background: linear-gradient(90deg, #1b5e20, #388e3c, #2e7d32);
  color: #fff;
  text-align: center;
  padding: 26px;
  font-size: 30px;
  font-weight: 600;
  letter-spacing: 0.8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border-bottom: 3px solid #a5d6a7;
}

.container{display:flex;flex-direction:column;align-items:center;gap:40px;padding:30px;}

.card{
  background:white;
  border-radius:12px;
  padding:24px 32px;
  border-top:5px solid #bbb;
  width:90%;
  max-width:1500px;
  box-shadow:0 6px 12px rgba(0,0,0,0.08);
  transition:0.3s ease;
  cursor:pointer;
  overflow:hidden;
}
.card h3{margin:0;font-size:22px;}
.card-content{
  max-height:0;
  overflow:hidden;
  transition:max-height 0.5s ease;
}
.card:hover .card-content{max-height:3000px;}
.card:hover{transform:translateY(-4px);box-shadow:0 10px 18px rgba(0,0,0,0.15);}

.prod {border-top: 4px solid #388E3C;background: linear-gradient(to bottom right, #F1F8E9, #E8F5E9);}
.preprod {border-top: 4px solid #8BC34A;background: linear-gradient(to bottom right, #F9FBE7, #F1F8E9);}
.develop {border-top: 4px solid #1565C0;background: linear-gradient(to bottom right, #E3F2FD, #E8EAF6);}

ul{list-style:none;margin:0;padding:0;}
li{border-top:1px solid #eee;padding:10px 0;}
li:first-child{border-top:none;}

.sub-env {margin-top:14px;padding:14px 18px;border-left:4px solid #ccc;border-radius:8px;width:calc(100% - 10px);}
.sub-env h4{margin:4px 0 8px 0;color:#333;}

.link-wrapper{position:relative;display:inline-block;}
.link-wrapper a{color:#1e88e5;font-weight:600;text-decoration:none;}
.link-wrapper a:hover{text-decoration:underline;}

.copy-icon{opacity:0;position:absolute;right:-32px;top:50%;transform:translateY(-50%);
  width:26px;height:26px;border:1px solid #ccc;border-radius:6px;background:#f8f9fa;
  background-image:url('data:image/svg+xml;utf8,<svg fill="none" stroke="%23000" stroke-width="2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>');
  background-repeat:no-repeat;background-position:center;cursor:pointer;transition:opacity 0.2s ease;}
.link-wrapper:hover .copy-icon{opacity:1;}
.copy-icon:hover{background-color:#e8eaf0;}

.copied{display:none;position:absolute;right:-75px;top:48%;transform:translateY(-50%);background:#4CAF50;color:white;padding:3px 8px;border-radius:6px;font-size:13px;}
</style>
</head>
<body>
<header>
  <a href="http://your-domain/index.html" class="home-button" style="position:absolute;left:30px;top:50%;transform:translateY(-50%);color:white;text-decoration:none;">🏠 Back</a>
  <h1>Core System Environments URLs</h1>
</header>
<div class="container">
"""

TEMPLATE_FOOTER = """
</div>
<footer style="text-align:center;color:#555;font-size:14px;margin-top:40px;">
© 2025 Core System Environment Dashboard | Open Source Edition
</footer>
</body>
</html>
"""

# --- FUNCTIONS ---

def build_link(url):
    return f'''
    <li>
      <div class="link-wrapper">
        <a href="{url}" target="_blank">{url}</a>
        <span class="copy-icon" onclick="navigator.clipboard.writeText('{url}')"></span>
        <span class="copied">✔ Copied</span>
      </div>
    </li>
    '''

def build_card(env, urls):
    color_class = {"prod": "prod", "preprod": "preprod", "develop": "develop"}.get(env, "")
    html = f'<div class="card {color_class}">\n  <h3>{env.capitalize()}</h3>\n  <div class="card-content">\n'

    if isinstance(urls, dict):
        for ns, ns_urls in urls.items():
            html += f'  <div class="sub-env {ns}">\n    <h4>{ns.capitalize()}</h4>\n    <ul>\n'
            for u in ns_urls:
                html += build_link(u)
            html += "    </ul>\n  </div>\n"
    else:
        html += "  <ul>\n"
        for u in urls:
            html += build_link(u)
        html += "  </ul>\n"

    html += "  </div>\n</div>\n"
    return html

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir))
    core_dir = os.path.join(root_dir, "..", "core-system")

    cards = ""

    for f in ["prod.yaml", "preprod.yaml", "develop.yaml"]:
        path = os.path.join(core_dir, f)
        if os.path.exists(path):
            with open(path) as y:
                data = yaml.safe_load(y)
                if data:
                    env = list(data.keys())[0]
                    urls = data[env]
                    cards += build_card(env, urls)

    output_path = os.path.join(root_dir, "core-index.html")
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(TEMPLATE_HEADER + cards + TEMPLATE_FOOTER)

    print(f"✅ {output_path} updated!")
