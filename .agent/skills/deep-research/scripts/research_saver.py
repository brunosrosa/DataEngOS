import argparse
import os
import re
import sys
from datetime import datetime

def sanitize_filename(title):
    """
    Sanitizes the title to be safe for filenames.
    Converts to snake_case and removes non-alphanumeric characters.
    """
    # Lowercase
    s = title.lower()
    # Replace spaces with underscores
    s = s.replace(' ', '_')
    # Remove non-alphanumeric characters (except underscores and hyphens)
    s = re.sub(r'[^\w\-]', '', s)
    # Remove multiple underscores
    s = re.sub(r'_+', '_', s)
    return s.strip('_')

def save_research(title, content, tags):
    """
    Saves the research content to a file in docs/researchs/.
    """
    try:
        # Define output directory relative to workspace root (assuming script runs from root or we resolve relative to it)
        output_dir = "docs/researchs"

        # Ensure directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%Y-%m-%d")
        safe_title = sanitize_filename(title)
        filename = f"{timestamp}_{safe_title}.md"
        filepath = os.path.join(output_dir, filename)

        # Prepare file content
        final_content = content
        
        # Add metadata header if tags are present or just to format nicely
        meta_header = f"---\ntitle: {title}\ndate: {timestamp}\ntags: {tags}\n---\n\n"
        if not content.startswith("---"):
             final_content = meta_header + content

        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        print(f"SUCCESS: Research saved to {filepath}")
        return 0

    except PermissionError:
        print(f"ERROR: Permission denied when writing to {output_dir}. Please check file permissions or trusted folders.", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"ERROR: OS Error occurred: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}", file=sys.stderr)
        return 1

def main():
    parser = argparse.ArgumentParser(description="Save research reports to docs/researchs/")
    parser.add_argument("--title", required=True, help="Title of the research topic")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--content", help="Markdown content of the report (deprecated for large content)")
    group.add_argument("--file", help="Path to a file containing the markdown content")
    
    parser.add_argument("--tags", default="research", help="Comma-separated tags")

    args = parser.parse_args()

    content = args.content
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
            # Clean up the temporary file if it's in a temp location or scratch
            # For now, we leave retention policy to the caller, but usually we might want to delete it.
            # Let's simple read it.
        except Exception as e:
            print(f"ERROR: Could not read input file {args.file}: {e}", file=sys.stderr)
            sys.exit(1)

    sys.exit(save_research(args.title, content, args.tags))

if __name__ == "__main__":
    main()
