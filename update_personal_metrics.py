import json
import urllib.request

ORCID_ID = "0000-0001-7449-7222"
MY_EMAIL = "pranavbhaskar@live.com" 

EXPLICIT_DOIS = [
    "10.52679/tabcj.2026.71001",
    "10.52679/tabcj.2024.0008",
    "10.1007/s40495-024-00370-2",
    "10.3390/agriculture14060796",
    "10.47363/JDAT/2024(1)132",
    "10.1007/978-3-031-49112-2_11",
    "10.52679/syncytia.2023.0w8yx9",
    "10.52679/bi.e202312001",
    "10.52679/bi.e202311003",
    "10.52679/tabcj.2023.0006",
    "10.21448/ijsm.1121860",
    "10.52679/tabcj.2023.0001",
    "10.52679/978-81-952885-8-8_1",
    "10.52679/978-81-952885-8-8_5",
    "10.52679/978-81-952885-8-8_6",
    "10.52679/978-81-952885-8-8_7",
    "10.52679/978-81-952885-8-8_9",
    "10.52679/syncytia.2023.5krq7z",
    "10.52679/978-81-952885-6-4_6",
    "10.52679/978-81-952885-6-4_7",
    "10.52679/978-81-952885-6-4_8",
    "10.52679/tabcj.2021.0003",
    "10.52679/tabcj.2021.0002",
    "10.1007/s11274-020-02918-y"
]

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': f'mailto:{MY_EMAIL}'})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

try:
    author_url = f"https://api.openalex.org/authors/orcid:{ORCID_ID}"
    author_data = fetch_json(author_url)
    summary_stats = author_data.get("summary_stats", {})
    
    total_works = len(EXPLICIT_DOIS)
    h_index = summary_stats.get("h_index", 0)
    i10_index = summary_stats.get("i10_index", 0)

    total_citations = 0
    for doi in EXPLICIT_DOIS:
        try:
            clean_doi = doi.replace("https://doi.org/", "")
            doi_url = f"https://api.openalex.org/works/https://doi.org/{clean_doi}"
            doi_data = fetch_json(doi_url)
            total_citations += doi_data.get("cited_by_count", 0)
        except Exception:
            pass

    metrics = {
        "total_works": total_works,
        "total_citations": total_citations,
        "h_index": h_index,
        "i10_index": i10_index,
        "last_updated": author_data.get("updated_date", "")[:10]
    }

    with open("personal-metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
        
    print("Personal metrics updated successfully!")

except Exception as e:
    print(f"Error updating metrics: {e}")
