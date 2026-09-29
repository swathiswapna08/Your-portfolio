import sqlite3
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# DEFAULT SOFT PASTEL AESTHETIC PORTRAIT
PASTEL_PORTRAIT = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=800"

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            bio TEXT,
            about_text TEXT,
            skills TEXT,
            project_title TEXT,
            project_desc TEXT,
            email TEXT,
            phone TEXT,
            location TEXT,
            image_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# COMMON CSS STYLES (Lavender & White Theme)
COMMON_STYLE = '''
<style>
  :root {
    --lavender-bg: #f4effc;
    --lavender-card: #ffffff;
    --lavender-pill: #ece5ff;
    --lavender-primary: #9b7be8;
    --lavender-dark: #7a51dd;
    --text-main: #2d2640;
    --text-sub: #6c6382;
    --text-heading: #241a3a;
    --radius-card: 24px;
    --radius-pill: 999px;
    --shadow-soft: 0 12px 30px rgba(122, 81, 221, 0.08);
    --shadow-hover: 0 18px 40px rgba(122, 81, 221, 0.15);
  }

  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
  body { background-color: var(--lavender-bg); color: var(--text-main); padding-bottom: 60px; position: relative; overflow-x: hidden; }

  /* FLORAL ACCENTS */
  .floral-bg { position: absolute; z-index: 0; pointer-events: none; opacity: 0.85; }
  .floral-top-left { top: -10px; left: -10px; width: 240px; }
  .floral-bottom-right { bottom: 20px; right: -10px; width: 260px; }

  /* NAVBAR */
  .navbar { display: flex; justify-content: flex-start; align-items: center; gap: 40px; padding: 22px 8%; background: rgba(244, 239, 252, 0.9); backdrop-filter: blur(10px); position: sticky; top: 0; z-index: 100; }
  .brand { display: flex; align-items: center; gap: 10px; font-family: 'Caveat', cursive; font-size: 2.3rem; color: var(--text-heading); font-weight: 700; white-space: nowrap; }
  .brand-icon { color: var(--lavender-primary); font-size: 1.8rem; }
  .nav-links { display: flex; list-style: none; gap: 28px; align-items: center; margin-right: auto; }
  .nav-links a { text-decoration: none; color: var(--text-sub); font-weight: 600; font-size: 0.95rem; }
  .nav-links a:hover { color: var(--lavender-dark); }

  .btn { padding: 10px 24px; border-radius: var(--radius-pill); font-size: 0.9rem; font-weight: 600; text-decoration: none; display: inline-flex; align-items: center; gap: 8px; cursor: pointer; border: none; transition: all 0.25s ease; }
  .btn-primary { background: var(--lavender-primary); color: #ffffff; box-shadow: 0 4px 14px rgba(155, 123, 232, 0.4); }
  .btn-primary:hover { background: var(--lavender-dark); transform: translateY(-2px); }
  .btn-outline { background: #ffffff; color: var(--text-main); border: 1px solid #dcd4fa; }

  /* HERO & GRID */
  .hero-wrapper { display: grid; grid-template-columns: 1fr 1fr; align-items: center; gap: 40px; padding: 60px 8% 40px; }
  .greeting { font-family: 'Caveat', cursive; font-size: 2.2rem; color: var(--lavender-dark); }
  .main-title { font-family: 'Caveat', cursive; font-size: 4.5rem; color: var(--text-heading); line-height: 1.1; margin: 10px 0; }
  .hero-bio { font-size: 1.05rem; color: var(--text-sub); line-height: 1.6; margin-bottom: 30px; }

  .preview-card { background: var(--lavender-card); border-radius: var(--radius-card); padding: 20px; box-shadow: var(--shadow-hover); text-align: center; }
  .preview-img { width: 100%; height: 280px; object-fit: cover; border-radius: 16px; margin-bottom: 15px; }

  .grid-cards-container { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; padding: 20px 8% 40px; }
  .info-card { background: var(--lavender-card); border-radius: var(--radius-card); padding: 28px 24px; box-shadow: var(--shadow-soft); display: flex; flex-direction: column; justify-content: space-between; }
  .card-title { font-family: 'Caveat', cursive; font-size: 1.9rem; color: var(--text-heading); margin-bottom: 10px; }
  .card-text { font-size: 0.9rem; color: var(--text-sub); line-height: 1.6; }

  /* FORM STYLES */
  .form-container { max-width: 650px; margin: 40px auto; background: #ffffff; padding: 40px; border-radius: var(--radius-card); box-shadow: var(--shadow-soft); }
  .form-container h2 { font-family: 'Caveat', cursive; font-size: 2.8rem; color: var(--text-heading); margin-bottom: 4px; }
  .form-subtext { font-size: 0.9rem; color: var(--text-sub); margin-bottom: 28px; }
  .form-group { margin-bottom: 20px; display: flex; flex-direction: column; gap: 6px; }
  .form-group label { font-weight: 600; font-size: 0.88rem; color: var(--text-heading); }
  .form-group input, .form-group textarea { width: 100%; padding: 12px 16px; border: 1px solid #dcd4fa; border-radius: 12px; font-size: 0.92rem; background: #faf8ff; outline: none; }

  /* PORTFOLIO DISPLAY */
  .hero-container { display: grid; grid-template-columns: 1.1fr 0.9fr; padding: 40px 10% 60px; align-items: center; gap: 60px; }
  .photo-blob-wrapper { position: relative; width: 320px; height: 380px; margin: 0 auto; }
  .purple-blob { position: absolute; width: 100%; height: 100%; background: #d8c7ff; border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%; }
  .profile-img { position: absolute; width: 100%; height: 100%; object-fit: cover; border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%; }
  .skills-pills { display: flex; flex-wrap: wrap; gap: 8px; }
  .pill { background: var(--lavender-pill); color: var(--text-main); font-size: 0.78rem; font-weight: 600; padding: 6px 14px; border-radius: var(--radius-pill); }
  .footer-tagline { text-align: center; margin-top: 50px; font-size: 0.78rem; letter-spacing: 2px; color: var(--text-sub); font-weight: 600; }
</style>
'''

# 1. HOME PAGE
INDEX_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><title>Your Portfolio - Builder</title>
  <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  ''' + COMMON_STYLE + '''
</head>
<body>
  <nav class="navbar">
    <div class="brand"><i class="fa-solid fa-butterfly brand-icon"></i><span>Your Portfolio</span> ♡</div>
    <ul class="nav-links">
      <li><a href="/">Home</a></li>
      <li><a href="/form" class="btn btn-primary"><i class="fa-solid fa-pen-to-square"></i> Edit Portfolio</a></li>
    </ul>
  </nav>

  <section class="hero-wrapper">
    <div>
      <span class="greeting">Create & Showcase in Minutes ♡</span>
      <h1 class="main-title">Build Your Aesthetic Portfolio</h1>
      <p class="hero-bio">Easily structure your bio, academic credentials, projects, and contact info in soft lavender styling.</p>
      <a href="/form" class="btn btn-primary" style="padding: 16px 36px; font-size: 1.1rem;">Start Building Now &rarr;</a>
    </div>

    <div class="preview-card">
      <img src="''' + PASTEL_PORTRAIT + '''" class="preview-img" alt="Soft Pastel Portrait">
      <div class="preview-caption"><i class="fa-solid fa-wand-magic-sparkles"></i> Soft Pastel Aesthetic Preview</div>
    </div>
  </section>

  <section class="grid-cards-container">
    <div class="info-card"><h3 class="card-title">Personal Profile</h3><p class="card-text">Customize name, role, and intro bio.</p></div>
    <div class="info-card"><h3 class="card-title">Featured Projects</h3><p class="card-text">Highlight web development apps and stack details.</p></div>
    <div class="info-card"><h3 class="card-title">Key Tech Skills</h3><p class="card-text">Display technical skills using lavender pill badges.</p></div>
    <div class="info-card"><h3 class="card-title">Contact Options</h3><p class="card-text">Add direct phone, email, and location info.</p></div>
  </section>
  <footer class="footer-tagline">YOUR PORTFOLIO BUILDER &nbsp; ♡ &nbsp; ALL RIGHTS RESERVED</footer>
</body>
</html>
'''

# 2. FORM PAGE
FORM_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><title>Edit Profile - Your Portfolio</title>
  <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  ''' + COMMON_STYLE + '''
</head>
<body>
  <nav class="navbar">
    <div class="brand">Your Portfolio ♡</div>
    <a href="/" class="btn btn-outline">Back to Home</a>
  </nav>

  <div class="form-container">
    <h2>Edit Portfolio Details</h2>
    <p class="form-subtext">Fill in your details below to dynamically update your website.</p>
    
    <form action="/form" method="POST">
      <div class="form-group"><label>Full Name</label><input type="text" name="name" placeholder="e.g. Sneha" value="{{ data.name if data and data.name else '' }}" required /></div>
      <div class="form-group"><label>Role & Qualifications</label><input type="text" name="role" placeholder="e.g. Web Developer | Designer" value="{{ data.role if data and data.role else '' }}" required /></div>
      <div class="form-group"><label>Profile Image URL (Optional)</label><input type="url" name="image_url" placeholder="Paste URL or leave blank for default pastel photo" value="{{ data.image_url if data and data.image_url else '' }}" /></div>
      <div class="form-group"><label>Hero Intro Bio</label><textarea name="bio" rows="3" required>{{ data.bio if data and data.bio else '' }}</textarea></div>
      <div class="form-group"><label>About Me Details</label><textarea name="about_text" rows="3" required>{{ data.about_text if data and data.about_text else '' }}</textarea></div>
      <div class="form-group"><label>Skills (Comma separated)</label><input type="text" name="skills" placeholder="HTML, CSS, JavaScript, Python, MySQL" value="{{ data.skills if data and data.skills else '' }}" required /></div>
      <div class="form-group"><label>Featured Project Title</label><input type="text" name="project_title" placeholder="e.g. Personal Portfolio Website" value="{{ data.project_title if data and data.project_title else '' }}" required /></div>
      <div class="form-group"><label>Project Description</label><input type="text" name="project_desc" placeholder="e.g. Flask • SQLite • HTML • CSS" value="{{ data.project_desc if data and data.project_desc else '' }}" required /></div>
      <div class="form-group"><label>Email Address</label><input type="email" name="email" value="{{ data.email if data and data.email else '' }}" required /></div>
      <div class="form-group"><label>Phone Number</label><input type="tel" name="phone" value="{{ data.phone if data and data.phone else '' }}" required /></div>
      <div class="form-group"><label>Location</label><input type="text" name="location" value="{{ data.location if data and data.location else '' }}" required /></div>
      <button type="submit" class="btn btn-primary" style="width:100%; justify-content:center; padding:14px;">Generate Portfolio &rarr;</button>
    </form>
  </div>
</body>
</html>
'''

# 3. GENERATED PORTFOLIO PAGE
PORTFOLIO_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><title>{{ data.name }} - Portfolio</title>
  <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  ''' + COMMON_STYLE + '''
</head>
<body>
  <nav class="navbar">
    <div class="brand"><i class="fa-solid fa-butterfly"></i> Your Portfolio ♡</div>
    <ul class="nav-links">
      <li><a href="/">Home</a></li>
      <li><a href="/form" class="btn btn-primary"><i class="fa-solid fa-pen"></i> Edit Profile</a></li>
    </ul>
  </nav>

  <section class="hero-container">
    <div>
      <span class="greeting">Hi, I'm ♡</span>
      <h1 class="main-title">{{ data.name }} ♡</h1>
      <h2 style="font-size:1.35rem; color:var(--text-sub); margin-bottom:20px;">{{ data.role }}</h2>
      <p class="hero-bio">{{ data.bio }}</p>
    </div>
    <div>
      <div class="photo-blob-wrapper">
        <div class="purple-blob"></div>
        <img src="{{ data.image_url }}" class="profile-img" alt="Soft Pastel Profile Photo" onerror="this.onerror=null; this.src='''' + PASTEL_PORTRAIT + '''';">
      </div>
    </div>
  </section>

  <section class="grid-cards-container">
    <div class="info-card"><h3 class="card-title">About Me</h3><p class="card-text">{{ data.about_text }}</p></div>
    <div class="info-card">
      <h3 class="card-title">Skills</h3>
      <div class="skills-pills">
        {% for skill in data.skills %}
          <span class="pill">{{ skill.strip() }}</span>
        {% endfor %}
      </div>
    </div>
    <div class="info-card"><h3 class="card-title">Featured Project</h3><div class="card-text"><strong>{{ data.project_title }}</strong><p>{{ data.project_desc }}</p></div></div>
    <div class="info-card"><h3 class="card-title">Contact Details</h3><p class="card-text"><strong>Email:</strong> {{ data.email }}<br><strong>Phone:</strong> {{ data.phone }}<br><strong>Location:</strong> {{ data.location }}</p></div>
  </section>
  <footer class="footer-tagline">SMALL STEPS &nbsp; ♡ &nbsp; BIG DREAMS</footer>
</body>
</html>
'''

# ROUTES
@app.route('/')
def index():
    return render_template_string(INDEX_TEMPLATE)

@app.route('/form', methods=['GET', 'POST'])
def form():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        role = request.form.get('role')
        bio = request.form.get('bio')
        about_text = request.form.get('about_text')
        skills = request.form.get('skills')
        project_title = request.form.get('project_title')
        project_desc = request.form.get('project_desc')
        email = request.form.get('email')
        phone = request.form.get('phone')
        location = request.form.get('location')
        image_url = request.form.get('image_url')

        cursor.execute('''
            INSERT INTO portfolios (name, role, bio, about_text, skills, project_title, project_desc, email, phone, location, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, role, bio, about_text, skills, project_title, project_desc, email, phone, location, image_url))
        conn.commit()
        conn.close()
        return redirect(url_for('portfolio'))

    cursor.execute('SELECT name, role, bio, about_text, skills, project_title, project_desc, email, phone, location, image_url FROM portfolios ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    conn.close()

    current_data = None
    if row:
        current_data = {
            'name': row[0], 'role': row[1], 'bio': row[2], 'about_text': row[3],
            'skills': row[4], 'project_title': row[5], 'project_desc': row[6],
            'email': row[7], 'phone': row[8], 'location': row[9], 'image_url': row[10]
        }

    return render_template_string(FORM_TEMPLATE, data=current_data)

@app.route('/portfolio')
def portfolio():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, role, bio, about_text, skills, project_title, project_desc, email, phone, location, image_url FROM portfolios ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    conn.close()

    if not row:
        return redirect(url_for('form'))

    # Sets image URL to user's input, or defaults to the pastel portrait
    user_img = row[10] if (row[10] and row[10].strip() != '') else PASTEL_PORTRAIT

    data = {
        'name': row[0], 'role': row[1], 'bio': row[2], 'about_text': row[3],
        'skills': row[4].split(',') if row[4] else [],
        'project_title': row[5], 'project_desc': row[6],
        'email': row[7], 'phone': row[8], 'location': row[9],
        'image_url': user_img
    }

    return render_template_string(PORTFOLIO_TEMPLATE, data=data)

if __name__ == '__main__':
    app.run(debug=True)