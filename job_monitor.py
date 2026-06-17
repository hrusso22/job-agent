from dotenv import load_dotenv
load_dotenv()

import datetime
import os
import json
import requests
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


def save_match(job_title, company, score, reason, url):
    with open("matches.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"\n[{timestamp}] {score}/10 — {job_title} at {company}\n")
        f.write(f"Reason: {reason}\n")
        f.write(f"Link: {url}\n")
        f.write("-" * 50 + "\n")

def search_jobs(job_title, seen_jobs):
    print("\nSearching for", job_title, "jobs...")
    
    url = f"https://remoteok.com/api?tag={job_title.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        jobs = response.json()
        if len(jobs) > 1:
            print("\n--- Relevant Jobs ---")
            matches = 0
            for job in jobs[1:]:
                title = job.get('position', '').lower()
                tags = job.get('tags', [])
                is_relevant = any(skill in title for skill in my_skills)
                if is_relevant:
                    job_url = job.get('url', '')
                if is_relevant and job_url not in seen_jobs:
                    seen_jobs.add(job_url)
                    score, reason = score_job(title, job.get('company', ''), tags)
                    if score >= 6:
                        matches += 1
                        print(f"\n{matches}. {job.get('position')} at {job.get('company')}")
                        print(f"   Score: {score}/10 — {reason}")
                        print(f"   Link: {job.get('url', 'No link')}")
                        save_match(job.get('position'), job.get('company'), score, reason, job.get('url', ''))
            print(f"\nTotal strong matches: {matches}")

print("Job monitor starting for", name, "in", location)

search_terms = ["systems engineer", "network engineer", "electrical engineer", "hardware engineer"]

search_terms = ["engineer", "embedded", "hardware", "networking", "systems"]

seen_jobs = set()
for term in search_terms:
    search_jobs(term, seen_jobs)
    