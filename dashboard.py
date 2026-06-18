from flask import Flask, request
import sqlite3

app = Flask(__name__)

def get_matches(min_score=6, days=30):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, company, score, reason, url, date_found, date_posted
        FROM jobs
        WHERE score >= ?
        ORDER BY date_posted DESC, score DESC
    """, (min_score,))
    results = cursor.fetchall()
    conn.close()
    return results

def days_ago(date_str):
    if not date_str or date_str == 'None':
        return None
    try:
        from datetime import datetime, date
        posted = datetime.strptime(date_str[:10], "%Y-%m-%d").date()
        delta = (date.today() - posted).days
        if delta == 0:
            return "today"
        elif delta == 1:
            return "yesterday"
        else:
            return f"{delta} days ago"
    except:
        return None

@app.route('/')
def home():
    min_score = int(request.args.get('min_score', 6))
    matches = get_matches(min_score)

    html = f"""
    <html>
    <head>
        <title>Hunter's Job Agent</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 960px; margin: 40px auto; padding: 0 20px; background: #f5f5f5; }}
            h1 {{ color: #1a3a5c; margin-bottom: 4px; }}
            .subtitle {{ color: #888; font-size: 14px; margin-bottom: 20px; }}
            .controls {{ display: flex; gap: 12px; align-items: center; margin-bottom: 20px; flex-wrap: wrap; }}
            .controls a {{ padding: 6px 14px; border-radius: 20px; font-size: 13px; text-decoration: none; border: 1px solid #ccc; color: #444; background: white; }}
            .controls a.active {{ background: #1a3a5c; color: white; border-color: #1a3a5c; }}
            .stats {{ background: #1a3a5c; color: white; padding: 12px 20px; border-radius: 8px; margin-bottom: 20px; font-size: 14px; }}
            .job {{ background: white; padding: 20px; margin: 12px 0; border-radius: 8px; border-left: 4px solid #ccc; }}
            .job.score-8, .job.score-9, .job.score-10 {{ border-left-color: #27ae60; }}
            .job.score-7 {{ border-left-color: #f39c12; }}
            .job.score-6 {{ border-left-color: #95a5a6; }}
            .title {{ font-size: 17px; font-weight: bold; color: #1a3a5c; }}
            .company {{ color: #666; margin: 3px 0 8px; font-size: 14px; }}
            .meta {{ display: flex; gap: 10px; align-items: center; flex-wrap: wrap; margin-bottom: 8px; }}
            .score {{ padding: 3px 10px; border-radius: 12px; background: #1a3a5c; color: white; font-size: 12px; }}
            .fresh {{ padding: 3px 10px; border-radius: 12px; background: #27ae60; color: white; font-size: 12px; }}
            .recent {{ padding: 3px 10px; border-radius: 12px; background: #f39c12; color: white; font-size: 12px; }}
            .old {{ padding: 3px 10px; border-radius: 12px; background: #95a5a6; color: white; font-size: 12px; }}
            .reason {{ color: #444; font-style: italic; font-size: 14px; margin-bottom: 8px; }}
            .link a {{ color: #2980b9; font-size: 14px; }}
            .date {{ color: #999; font-size: 12px; margin-top: 6px; }}
        </style>
    </head>
    <body>
        <h1>Hunter's Job Agent</h1>
        <div class="subtitle">Austin, TX — AI-powered job matching</div>
        <div class="controls">
            <span style="font-size:13px;color:#666">Min score:</span>
            <a href="/?min_score=6" class="{'active' if min_score == 6 else ''}">6+</a>
            <a href="/?min_score=7" class="{'active' if min_score == 7 else ''}">7+</a>
            <a href="/?min_score=8" class="{'active' if min_score == 8 else ''}">8+</a>
        </div>
        <div class="stats">Showing {len(matches)} matches — sorted by most recently posted</div>
    """

    for title, company, score, reason, url, date_found, date_posted in matches:
        score_class = f"score-{score}"
        age = days_ago(date_posted)

        if age == "today" or age == "yesterday":
            age_badge = f'<span class="fresh">{age}</span>'
        elif age and "days ago" in age and int(age.split()[0]) <= 7:
            age_badge = f'<span class="recent">{age}</span>'
        elif age:
            age_badge = f'<span class="old">{age}</span>'
        else:
            age_badge = ''

        html += f"""
        <div class="job {score_class}">
            <div class="title">{title}</div>
            <div class="company">{company}</div>
            <div class="meta">
                <span class="score">{score}/10</span>
                {age_badge}
            </div>
            <div class="reason">{reason}</div>
            <div class="link"><a href="{url}" target="_blank">View Job →</a></div>
            <div class="date">Found by agent: {date_found}</div>
        </div>
        """

    html += "</body></html>"
    return html

if __name__ == "__main__":
    print("Dashboard running at http://127.0.0.1:5000")
    app.run(debug=True)