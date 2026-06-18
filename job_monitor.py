from dotenv import load_dotenv
load_dotenv()

import os
import json
import requests
import feedparser
from database import init_db, job_exists, save_job
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Your profile
name = "Hunter Russo"
location = "Austin, TX"
my_skills = ["systems engineer", "network engineer", "electrical engineer",
             "hardware engineer", "devops", "embedded", "infrastructure",
             "technical", "software engineer"]

def score_job(job_title, company, tags):
    prompt = f"""
    I am a candidate with the following background:
    - Electrical Engineering degree from Texas State University, GPA 3.51
    - Systems Engineer internship at Poly (Austin)
    - Network Engineer internship at Nextlink
    - Skills: Python, C, networking (TCP/IP, VPN, DHCP), hardware, embedded systems, MATLAB
    
    Rate this job on a scale of 1-10 for how well it fits my background.
    Job Title: {job_title}
    Company: {company}
    Tags: {tags}
    
    Respond with only a JSON object like this:
    {{"score": 7, "reason": "one sentence reason"}}
    """
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        result = json.loads(message.content[0].text)
        return result['score'], result['reason']
    except:
        return 0, "Could not parse response"

def process_job(title, company, tags, url, date_posted=None):
    title_lower = title.lower()
    url_lower = url.lower()
    is_relevant = any(skill in title_lower for skill in my_skills)

    if is_relevant and not job_exists(url_lower):
        score, reason = score_job(title_lower, company, tags)
        if score >= 6:
            print(f"\n  ✓ {title} at {company}")
            print(f"    Score: {score}/10 — {reason}")
            print(f"    Link: {url}")
            if date_posted:
                print(f"    Posted: {date_posted}")
            save_job(title, company, score, reason, url_lower, date_posted)
            return 1
    return 0

def fetch_remoteok():
    print("\n[RemoteOK] Searching...")
    search_terms = ["engineer", "embedded", "hardware", "networking", "systems"]
    total = 0

    for term in search_terms:
        url = f"https://remoteok.com/api?tag={term.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                jobs = response.json()
                for job in jobs[1:]:
                    title = job.get('position', '')
                    company = job.get('company', '')
                    tags = job.get('tags', [])
                    job_url = job.get('url', '')
                    date_posted = job.get('date', '')[:10]
                    if title and job_url:
                        total += process_job(title, company, tags, job_url, date_posted)
        except Exception as e:
            print(f"  RemoteOK error: {e}")

    print(f"[RemoteOK] Done — {total} new matches")

def fetch_arbeitnow():
    print("\n[Arbeitnow] Searching...")
    search_terms = ["electrical engineer", "systems engineer",
                    "network engineer", "hardware engineer"]
    total = 0

    for term in search_terms:
        url = f"https://www.arbeitnow.com/api/job-board-api?search={term.replace(' ', '+')}&location=Austin"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('data', [])
                for job in jobs:
                    title = job.get('title', '')
                    company = job.get('company_name', '')
                    tags = job.get('tags', [])
                    job_url = job.get('url', '')
                    date_posted = str(job.get('created_at', ''))[:10]
                    if title and job_url:
                        total += process_job(title, company, tags, job_url, date_posted)
        except Exception as e:
            print(f"  Arbeitnow error: {e}")

    print(f"[Arbeitnow] Done — {total} new matches")

def fetch_adzuna():
    print("\n[Adzuna] Searching...")
    search_terms = ["electrical engineer", "systems engineer",
                    "network engineer", "hardware engineer"]
    total = 0

    app_id = os.environ.get("ADZUNA_APP_ID")
    api_key = os.environ.get("ADZUNA_API_KEY")

    for term in search_terms:
        url = f"https://api.adzuna.com/v1/api/jobs/us/search/1?app_id={app_id}&app_key={api_key}&what={term.replace(' ', '+')}&where=Austin+TX&results_per_page=20"
        try:
            response = requests.get(url, timeout=10)
            print(f"  Adzuna status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('results', [])
                print(f"  Jobs returned: {len(jobs)}")
                for job in jobs:
                    title = job.get('title', '')
                    company = job.get('company', {}).get('display_name', 'Unknown')
                    job_url = job.get('redirect_url', '')
                    date_posted = job.get('created', '')[:10]
                    if title and job_url:
                        total += process_job(title, company, [], job_url, date_posted)
        except Exception as e:
            print(f"  Adzuna error: {e}")

    print(f"[Adzuna] Done — {total} new matches")

def fetch_usajobs():
    print("\n[USAJobs] Searching...")
    search_terms = ["electrical engineer", "systems engineer",
                    "network engineer", "hardware engineer"]
    total = 0

    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": "hrusso222@yahoo.com",
        "Authorization-Key": os.environ.get("USAJOBS_API_KEY")
    }

    for term in search_terms:
        url = f"https://data.usajobs.gov/api/search?Keyword={term.replace(' ', '+')}&LocationName=Austin,+TX&ResultsPerPage=25"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"  USAJobs status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('SearchResult', {}).get('SearchResultItems', [])
                print(f"  Jobs returned: {len(jobs)}")
                for job in jobs:
                    inner = job.get('MatchedObjectDescriptor', {})
                    title = inner.get('PositionTitle', '')
                    company = inner.get('OrganizationName', '')
                    job_url = inner.get('PositionURI', '')
                    date_posted = inner.get('PublicationStartDate', '')[:10]
                    if title and job_url:
                        total += process_job(title, company, [], job_url, date_posted)
        except Exception as e:
            print(f"  USAJobs error: {e}")

    print(f"[USAJobs] Done — {total} new matches")

# --- MAIN ---
print(f"\nJob monitor starting for {name} in {location}")
print("=" * 50)
init_db()

fetch_remoteok()
fetch_arbeitnow()
fetch_adzuna()
fetch_usajobs()

print("\n" + "=" * 50)
print("All sources checked.")