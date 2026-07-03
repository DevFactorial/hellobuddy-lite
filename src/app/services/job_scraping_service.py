import os
import serpapi
import json
import os
import markdown
from config.config import get_value_from_config

def search_jobs_with_sdk(query: str, location: str, num_pages: int = 1, date_posted: str = "today",
                         country: str = "IN") -> list:
    print(f"--- Fetching Jobs via SerpApi SDK for: '{query}' in '{location}' ---")
    
    # Initialize client (It automatically picks up SERPAPI_KEY from env variables if not passed)
    #api_key = os.getenv("SERPAPI_KEY", "")
    api_key = get_value_from_config("API_KEYS", "SERPAPI_KEY")

    client = serpapi.Client(api_key=api_key)
    
    # Configure parameters explicitly for Google Jobs engine
    # 1. Inject the "remote" constraint explicitly into the keyword query
    params = {
        "engine": "google_jobs",
        "q": query, # Added remote here
        "location": location,                  # Use a valid geographic region
        "chips": f"date_posted:{date_posted}",            # Use the date_posted parameter
        "hl": "en",
        "gl": country
    }
    if date_posted == "all":
        params.pop("chips")  # Remove the date_posted filter if "all" is specified
    print(params)
    
    try:
        all_results = []
        total_desired = num_pages * 10
        results = client.search(params)
        for page in results.yield_pages(max_pages = num_pages):
            organic_results = page.get("jobs_results", [])
            all_results.extend(organic_results)
            
            if len(all_results) >= total_desired:
                break
        
        if not all_results:
            print("No jobs found matching criteria.")
            return []
            
        print(f"Found {len(all_results)} jobs successfully.\n")
        
        extracted_jobs = []
        for index, job in enumerate(all_results, 1):
            job_data = {
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": job.get("location"),
                # This full description text is exactly what you pass to LangChain for skill parsing:
                "description": job.get("description"), 
                "via": job.get("via"), # e.g. "via LinkedIn", "via Indeed"
                "apply_link": job.get("share_link") # Share/Apply redirect link
            }
            # Look inside SerpApi's parsed response for the item loop:
            apply_options = job.get("apply_options", [])
            direct_apply_link = "";
            if apply_options:
                # Option A: Grab the absolute first apply link available
                direct_apply_link = apply_options[0].get("link")
                
                # Option B: Or loop through them to find an explicit target (like LinkedIn)
                for option in apply_options:
                    if "linkedin" in option.get("title", "").lower():
                        direct_apply_link = option.get("link")
                        break
            else:
                # Fallback to the share link if no deep apply array metadata was exposed
                direct_apply_link = job.get("share_link")
            
            job_data['apply_link'] = direct_apply_link
            extracted_jobs.append(job_data)
            
            # Print quick console preview summary
            print(f"[{index}] {job_data['title']} at {job_data['company']} ({job_data['via']})")
            print(f"    Snippet: {job_data['description'][:120]}...\n")
            
        return extracted_jobs

    except serpapi.HTTPError as e:
        print(f"SerpApi HTTP Error occurred: {e.status_code} - {e.error}")
    except Exception as e:
        print(f"Unexpected error: {e}")



# --- Advanced Version: Handling a LIST of multiple jobs ---
def save_job_list_to_markdown(jobs_list: list, filepath: str = "all_job_matches.md"):
    """
    Takes a list of job dictionaries and creates a comprehensive report
    complete with a summary overview table at the top.
    """
    if not jobs_list:
        print("No jobs provided to save.")
        return

    # Create the top summary table header
    md_content = "# 🚀 Hellobuddy Job Match Report\n\n"
    md_content += "| Position | Company | Location | Platform |\n"
    md_content += "| :--- | :--- | :--- | :--- |\n"
    
    # Populate the summary table rows
    for job in jobs_list:
        title = job.get('title', 'N/A')
        company = job.get('company', 'N/A')
        location = job.get('location', 'N/A')
        via = job.get('via', 'Link')
        apply = job.get('apply_link', '#')
        
        md_content += f"| [{title}]({apply}) | **{company}** | {location} | *{via}* |\n"
        
    md_content += "\n\n---\n\n"
    
    # Append the detailed descriptions below the table
    for idx, job in enumerate(jobs_list, 1):
        md_content += f"## {idx}. {job.get('title')} at {job.get('company')}\n"
        md_content += f"> 📍 **Location:** {job.get('location')} | 🌐 **Source:** {job.get('via')} | 🔗 [Apply Direct]({job.get('apply_link', '#')})\n\n"
        md_content += f"### Description\n{job.get('description')}\n\n"
        md_content += "...\n\n"

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(md_content)
    print(f"Full report with {len(jobs_list)} jobs compiled at {filepath}")
    return md_content


def convert_md_file_to_html_body(md_content: str) -> str:
    """Converts markdown content to converted HTML into a responsive styling wrapper."""
        
    # Convert native markdown syntax to HTML string layout
    html_content = markdown.markdown(md_content, extensions=['tables'])
    
    # Wrap the raw HTML inside a clean, modern responsive email wrapper
    styled_email_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333333; max-width: 600px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #1e293b; font-size: 24px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }}
            h2 {{ color: #334155; font-size: 20px; margin-top: 24px; }}
            h3 {{ color: #475569; font-size: 16px; }}
            a {{ color: #2563eb; text-decoration: none; font-weight: bold; }}
            a:hover {{ text-decoration: underline; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }}
            th, td {{ border: 1px solid #cbd5e1; padding: 10px; text-align: left; }}
            th {{ background-color: #f8fafc; font-weight: 600; color: #1e293b; }}
            blockquote {{ margin: 16px 0; padding: 4px 16px; border-left: 4px solid #3b82f6; background-color: #f0fdf4; color: #1e293b; font-style: italic; }}
            hr {{ border: 0; height: 1px; background: #e2e8f0; margin: 24px 0; }}
        </style>
    </head>
    <body>
        {html_content}
        <hr />
        <p style="font-size: 12px; color: #64748b; text-align: center;">Sent automatically by your Hellobuddy AI Agent.</p>
    </body>
    </html>
    """
    return styled_email_html

if __name__ == "__main__":
    # Test execution mock payload
    extracted_jobs = search_jobs_with_sdk(
        query="AI Jobs", 
        location="Bangalore, Karnataka, India"
    )
    save_job_list_to_markdown(extracted_jobs, "all_jobs.md")
