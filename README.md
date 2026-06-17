# AI Job Search Agent

A Python-based autonomous job search agent that monitors job boards, 
filters postings by relevance, and uses the Claude AI API to score 
each opportunity against my background as an Electrical Engineer.

## Why I Built This

I'm an EE graduate transitioning into the Austin tech industry. 
Instead of manually scrolling job boards, I built a tool to do it 
for me — and used it as an opportunity to refresh my Python skills 
and learn API integration.

## What It Does

- Searches multiple job boards via API across several search terms
- Filters results by job title relevance
- Sends each match to Claude AI with my resume background for intelligent scoring
- Returns only strong matches (6/10 or above) with a reason explaining the fit
- Saves all matches to a timestamped log file

## Tech Stack

- Python 3.14
- Anthropic Claude API (claude-sonnet-4-6)
- RemoteOK API
- python-dotenv for secure API key management

## How To Run

1. Clone the repo
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip3 install requests anthropic python-dotenv`
5. Add your Anthropic API key to a `.env` file: `ANTHROPIC_API_KEY=your_key`
6. Run: `python3 job_monitor.py`

## Built By

Hunter Russo — EE Graduate, Texas State University  
Austin, TX | github.com/hrusso22