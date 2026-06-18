from flask import Flask
import sqlite3

app = Flask(__name__)

def get_matches():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]
    print(f"Total rows in database: {count}")
    cursor.execute("""
        SELECT title, company, score, reason, url, date_found 
        FROM jobs 
        ORDER BY score DESC, date_found DESC
    """)
    results = cursor.fetchall()
    print(f"Rows returned: {len(results)}")
    if results:
        print(f"Sample row: {results[0]}")
    conn.close()
    return results

@app.route('/')
def home():
    matches = get_matches()
    
    html = """
    <html>
    <head>
        <title>Hunter's Job Agent</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; background: #f5f5f5; }
            h1 { color: #1a3a5c; }
            .job { background: white; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #1a3a5c; }
            .title { font-size: 18px; font-weight: bold; color: #1a3a5c; }
            .company { color: #666; margin: 4px 0; }
            .score { display: inline-block; padding: 3px 10px; border-radius: 12px; background: #1a3a5c; color: white; font-size: 13px; }
            .reason { color: #444; margin: 10px 0; font-style: italic; }
            .link a { color: #2980b9; }
            .date { color: #999; font-size: 12px; }
            .stats { background: #1a3a5c; color: white; padding: 15px 20px; border-radius: 8px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <h1>Hunter's Job Agent Dashboard</h1>
    """
    
    html += f'<div class="stats">Total matches found: {len(matches)}</div>'
    
    for title, company, score, reason, url, date_found in matches:
        html += f"""
        <div class="job">
            <div class="title">{title}</div>
            <div class="company">{company}</div>
            <span class="score">{score}/10</span>
            <div class="reason">{reason}</div>
            <div class="link"><a href="{url}" target="_blank">View Job →</a></div>
            <div class="date">Found: {date_found}</div>
        </div>
        """
    
    html += "</body></html>"
    return html

if __name__ == "__main__":
    print("Dashboard running at http://localhost:5000")
    app.run(debug=True)