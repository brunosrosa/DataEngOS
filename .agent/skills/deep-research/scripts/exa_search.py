import argparse
import json
import os
import sys
import urllib.request
import urllib.error

# Hardcoded key from setup for ease of use in this environment, 
# or preferably read from env/args. Let's use env var or fall back to the one provided.
DEFAULT_EXA_KEY = "7a9a3e73-bd92-43b0-9e4e-5d718e22aea0"

def exa_search(query, num_results=5, use_autoprompt=True):
    url = "https://api.exa.ai/search"
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": os.environ.get("EXA_API_KEY", DEFAULT_EXA_KEY)
    }
    
    payload = {
        "query": query,
        "numResults": num_results,
        "useAutoprompt": use_autoprompt,
        "contents": {
            "text": True  # Retrieve text content for RAG
        }
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except urllib.error.HTTPError as e:
        print(f"Error calling Exa API: {e.code} - {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="Search using Exa AI")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--num", type=int, default=3, help="Number of results")
    
    args = parser.parse_args()
    
    print(f"Searching Exa for: {args.query}...", file=sys.stderr)
    result = exa_search(args.query, args.num)
    
    if result and 'results' in result:
        print(f"Found {len(result['results'])} results.\n")
        for res in result['results']:
            print(f"--- SOURCE: {res.get('title', 'No Title')} ---")
            print(f"URL: {res.get('url', 'No URL')}")
            # Truncate content for display
            content = res.get('text', '')[:500].replace('\n', ' ')
            print(f"CONTENT: {content}...\n")
    else:
        print("No results found or error occurred.")

if __name__ == "__main__":
    main()
