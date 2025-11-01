import sys
import re
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.juniors.ro/jobs"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

def fetch_soup(url: str) -> BeautifulSoup | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    return BeautifulSoup(r.text, "html.parser")

def parse_job_card(card) -> dict | None:
    title_tag = card.find("h3")
    if not title_tag:
        return None

    whole_text = " ".join(list(card.stripped_strings))
    if "Companie:" not in whole_text:
        return None

    job_title = title_tag.get_text(strip=True)

    location = "N/A"
    post_date = "N/A"
    strings = list(card.stripped_strings)
    try:
        t_idx = strings.index(job_title)
    except ValueError:
        t_idx = -1

    for s in strings[t_idx + 1 : t_idx + 8]:
        if "|" in s:
            parts = [p.strip() for p in s.split("|", 1)]
            if len(parts) == 2:
                location, post_date = parts
                break

    m = re.search(r"Companie:\s*([^|*]+?)(?:\s{2,}|\sSursa:|$)", whole_text)
    company = m.group(1).strip() if m else "N/A"

    technologies = []
    for a in card.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a["href"]
        if text and text not in {"Detalii", "Raportează"} and "/jobs" in href and "q=" in href:
            technologies.append(text)

    return {
        "Job title": job_title,
        "Company name": company,
        "Location": location,
        "Technologies": ", ".join(dict.fromkeys(technologies)),
        "Post date": post_date,
    }

def job_search(prog_language: str):
    url = f"{BASE_URL}?q={requests.utils.quote(prog_language)}"
    soup = fetch_soup(url)
    if soup is None:
        return None

    results = []
    seen_titles = set()

    for h3 in soup.find_all("h3"):
        container = h3
        for _ in range(4):
            container = container.parent
            if not container:
                break
            text = " ".join(container.stripped_strings)
            if "Companie:" in text and "Detalii" in text:
                job = parse_job_card(container)
                if job and job["Job title"] not in seen_titles:
                    results.append(job)
                    seen_titles.add(job["Job title"])
                break

        if len(results) >= 8:
            break

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python job_search.py <programming_language>")
        print("Example: python job_search.py Python")
        sys.exit(1)

    language_to_search = " ".join(sys.argv[1:])
    jobs = job_search(language_to_search)

    if jobs is None:
        print("\nCould not complete the search due to an error.")
    else:
        jobs_to_show = jobs[1:8] if jobs else []
        if not jobs_to_show:
            print(f"Found 0 job postings to display for '{language_to_search}'")
        else:
            for i, job in enumerate(jobs_to_show, 1):
                print(f"{i}. {job['Job title']}")
                print(f"   • Company: {job['Company name']}")
                print(f"   • Location: {job['Location']}")
                print(f"   • Technologies: {job['Technologies'] or 'N/A'}")
                print(f"   • Post date: {job['Post date']}")
                print()
                print()
