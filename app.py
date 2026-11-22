from flask import Flask, request, render_template_string
app = Flask(__name__)

SCHEMES = [
    {"name": "🎓 PM Scholarship - For Students", "for_who": "student", "min_age": 17, "max_age": 25, "max_income": 300000, "why": "Age is okay, Income is okay, You are a student", "docs": "Aadhaar, Income Certificate, Marksheet", "last_date": "31 Dec 2026", "link": "https://scholarships.gov.in", "source": "scholarships.gov.in - Checked on 22 Nov 2026"},
    {"name": "🌾 PM Fasal Bima - Crop Insurance", "for_who": "farmer", "min_age": 18, "max_age": 100, "max_income": 1000000, "why": "Age is okay, You are a farmer", "docs": "Aadhaar, Land Papers, Bank Passbook", "last_date": "15 Jan 2027", "link": "https://pmfby.gov.in", "source": "pmfby.gov.in - Checked on 22 Nov 2026"},
    {"name": "👧 Sukanya Samriddhi - For Girl Child", "for_who": "girl", "min_age": 0, "max_age": 10, "max_income": 1000000, "why": "Age is okay, For girl child", "docs": "Aadhaar, Birth Certificate", "last_date": "Anytime - Post Office", "link": "https://www.nsiindia.gov.in", "source": "nsiindia.gov.in - Checked on 22 Nov 2026"},
    {"name": "🏥 Ayushman Health Card", "for_who": "all", "min_age": 0, "max_age": 100, "max_income": 300000, "why": "Income is okay, For all families", "docs": "Aadhaar, Ration Card", "last_date": "Anytime", "link": "https://pmjay.gov.in", "source": "pmjay.gov.in - Checked on 22 Nov 2026"},
]

HTML = """
<link rel="manifest" href="/manifest.json">
<style>
body{font-family:Arial; background:#f0f4ff; margin:0; padding:15px}
.card{background:white; border-radius:15px; padding:18px; max-width:450px; margin:auto; box-shadow:0 4px 12px #ccc}
h1{color:#1a3c9e; text-align:center; font-size:24px}
input,select{width:100%; padding:12px; margin:8px 0; border-radius:10px; border:1px solid #ccc; font-size:16px}
button{width:100%; padding:14px; background:#1a3c9e; color:white; border:none; border-radius:12px; font-size:18px}
.result{background:#e8f5e9; border-radius:12px; padding:12px; margin:12px 0; border-left:5px solid green}
a{color:#1a3c9e; word-break:break-all}
</style>
<div class="card">
<h1>🇮🇳 Claim What's Yours</h1>
<p style="text-align:center">Find Govt Schemes you deserve.<br>In simple language.</p>
<form method="POST">
<label>Your Age</label><input name="age" type="number" placeholder="Example: 19" required>
<label>I am a</label><select name="who"><option>student</option><option>farmer</option><option>girl</option><option>other</option></select>
<label>Family Income per Year (₹)</label><input name="income" type="number" placeholder="Example: 200000" required>
<button>🔍 Check My Schemes</button>
</form>
{% if results is not none %}
<h2>Result for You:</h2>
{% if results %}
{% for s in results %}
<div class="result"><b>{{ s.name }}</b><br><br>
✅ <b>Status:</b> You are <b>LIKELY eligible</b> (Not 100% guarantee)<br>
💡 <b>Why:</b> {{ s.why }}<br>
📄 <b>Documents:</b> {{ s.docs }}<br>
📅 <b>Last Date:</b> {{ s.last_date }}<br>
🔗 <b>Apply:</b> <a href="{{ s.link }}">{{ s.link }}</a><br>
📌 <b>Source:</b> {{ s.source }}
</div>
{% endfor %}
{% else %}<p>No scheme found. Try again.</p>{% endif %}
{% endif %}
<p style="font-size:12px; color:grey; text-align:center">Note: This is only guidance. Please check official website.</p>
</div>
"""
@app.route("/manifest.json")
def manifest():
    return {
        "name": "Claim What's Yours",
        "short_name": "Claim App",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#2563eb",
        "icons": [{"src": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png", "sizes": "512x512", "type": "image/png"}]
    }

@app.route("/", methods=["GET", "POST"])
def home():
    results = None
    if request.method == "POST":
        age = int(request.form["age"]); who = request.form["who"]; income = int(request.form["income"])
        results = []
        for s in SCHEMES:
            if s["min_age"] <= age <= s["max_age"] and income <= s["max_income"]:
                if s["for_who"] == "all" or s["for_who"] == who or (who=="student" and s["for_who"]=="student"):
                    results.append(s)
                elif who=="other" and s["for_who"]=="all":
                    results.append(s)
    return render_template_string(HTML, results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
