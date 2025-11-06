#!/usr/bin/env python3
import yaml
import os

# --- HTML TEMPLATE ---
TEMPLATE_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Client Portal Environments</title>
<style>
body {background:#f4f6f8;font-family:"Segoe UI",Arial,sans-serif;margin:0;}
header {
  position: relative;
  background: linear-gradient(90deg, #00796B, #009688, #26A69A);
  color: #fff;
  text-align: center;
  padding: 26px;
  font-size: 26px;
  font-weight: 600;
  letter-spacing: 0.8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  border-bottom: 3px solid #80CBC4;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
  padding: 30px;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 24px 32px;
  border-top: 5px solid #bbb;
  width: 90%;
  max-width: 1200px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
  transition: 0.3s ease;
  cursor: pointer;
  overflow: hidden;
}

.card h3 {
  margin: 0;
  font-size: 22px;
  color: #004D40;
}

.card-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.5s ease;
}
.card:hover .card-content { max-height: 2000px; }
.card:hover { transform: translateY(-4px); box-shadow: 0 10px 18px rgba(0,0,0,0.15); }

.prod {border-top: 4px solid #2E7D32;background:linear-gradient(to bottom right,#f7fbf7,#edf7ed);}
.preprod {border-top: 4px solid #F9A825;background:linear-gradient(to bottom right,#fffdf3,#fff8e1);}
.develop {border-top: 4px solid #1565C0;background:linear-gradient(to bottom right,#f5f8fc,#e9f1fb);}

ul {list-style:none;margin:0;padding:0;}
li {border-top:1px solid #eee;padding:10px 0;}
li:first-child {border-top:none;}

.link-wrapper {position:relative;display:inline-block;}
.link-wrapper a {color:#1e88e5;font-weight:600;text-decoration:none;}
.link-wrapper a:hover {text-decoration:underline;}

.copy-icon {
  opacity:0;
  position:absolute;
  right:-32px;
  top:50%;
  transform:translateY(-50%);
  width:26px;
  height:26px;
  border:1px solid #ccc;
  border-radius:6px;
  background:#f8f9fa;
  background-image:url('data:image/svg+xml;utf8,<svg fill="none" stroke="%23000" stroke-width="2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>');
  background-repeat:no-repeat;
  background-position:center;
  cursor:pointer;
  transition:opacity 0.2s ease;
}
.link-wrapper:hover .copy-icon {opacity:1;}
.copy-icon:hover {background-color:#e8eaf0;}

.copied {
  display:none;
  position:absolute;
  right:-75px;
  top:48%;
  transform:translateY(-50%);
  background:#4CAF50;
  color:white;
  padding:3px 8px;
  border-radius:6px;
  font-size:13px;
}

.home-button {
  position: absolute;
  left: 30px;
  top: 50%;
  transform: translateY(-55%);
  display: inline-flex;
  align-items: center;
  background-color: #ffffff22;
  border: 1px solid #ffffff44;
  color: white;
  padding: 8px 14px;
  border-radius: 8px;
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
  transition: 0.25s ease;
}

.home-button:hover {
  background-color: #ffffff33;
  transform: translateY(-55%) scale(1.05);
}
</style>
</head>
<body>
<header>
  <a href="http://your-domain/index.html" class="home-button">
    <span style="margin-right:6px;">🏠</span> Back to Home
  </a>
  <h1>Client Portal Environments URLs</h1>
</header>
<div class="container">
"""

TEMPLATE_FOOTER = """
</div>
<footer style="text-align:center;color:#555;font-size:14px;margin-top:40px;">
© 2025 Client Portal Environment Dashboard | Open Source Edition
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
    html = f'<div class="card {color_class}">\n  <h3>{env.capitalize()}</h3>\n  <div class="card-content">\n  <ul>\n'
    for u in urls:
        html += build_link(u)
    html += "  </ul>\n  </div>\n</div>\n"
    return html


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir))
    portal_dir = os.path.join(root_dir, "..", "client-portal")

    cards = ""

    for f in ["prod.yaml", "preprod.yaml", "develop.yaml"]:
        path = os.path.join(portal_dir, f)
        if os.path.exists(path):
            with open(path) as y:
                data = yaml.safe_load(y)
                if data:
                    env = list(data.keys())[0]
                    urls = data[env]
                    cards += build_card(env, urls)

    output_path = os.path.join(root_dir, "portal-index.html")
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(TEMPLATE_HEADER + cards + TEMPLATE_FOOTER)

    print(f"✅ {output_path} updated!")
