from services.job_scraping_service import convert_md_file_to_html_body, search_jobs_with_sdk, save_job_list_to_markdown, convert_md_file_to_html_body
from config.config import get_absolute_path_from_config, get_value_from_config
from services.email_service import background_send_email_task
from services.scheduler import setup_scheduler
from datetime import datetime
from pathlib import Path
import glob
import os

def get_job_search_chips(target_folder):
    # Check if the folder contains any markdown (.md) files
    # recursive=False looks only inside the immediate folder
    md_files = glob.glob(os.path.join(target_folder, "*.md"))
    
    if not md_files:
        print("No .md files found. Setting date filter to: PAST MONTH")
        return "all"
    else:
        print(f"Found {len(md_files)} .md file(s). Setting date filter to: TODAY")
        return "today"

def append_timestamp_to_filepath(base_directory: str, base_filename: str, extension: str) -> Path:
    """
    Appends a safe ISO-like datetime string suffix to a filename 
    and resolves it into an absolute cross-platform Path.
    """
    # 1. Generate a filename-safe timestamp (e.g., "2026-07-02_16-35-12")
    # Using underscores and hyphens ensures Windows, macOS, and Linux compatibility
    timestamp_suffix = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # 2. Combine the original filename string with the suffix
    final_filename = f"{base_filename}_{timestamp_suffix}{extension}"
    
    # 3. Use pathlib to securely anchor it to the target folder path
    absolute_path = Path(base_directory).resolve() / final_filename
    
    return absolute_path

def extract_jobs_send_email(query: str, location: str, search_country: str):
    
    report_path = get_absolute_path_from_config("JOB_REPORT_OUTPUT_PATH")
    num_pages = int(get_value_from_config("SEARCH_SETTINGS", "NUM_PAGES"))
    date_posted = get_job_search_chips(report_path)  # Determine the date filter based on existing .md files
    
    extracted_jobs = search_jobs_with_sdk(query, location, num_pages = num_pages, date_posted=date_posted,
                                          country=search_country)
    #extracted_jobs = []
    mock_job = {
        "title": "Backend Engineer (Python & FastAPI)",
        "company": "TechBuddy Solutions",
        "location": "Remote, US",
        "description": "We are seeking a Backend Engineer with deep expertise in Python, FastAPI, and building LLM pipeline configurations using tools like LangChain.",
        "via": "via LinkedIn",
        "apply_link": "https://linkedin.com/jobs/view/123456"
    }
    #extracted_jobs.append(mock_job)
    
    
    file_prefix = "job_matches"
    file_ext = ".md"
    
    # Execute the resolution
    resolved_file = append_timestamp_to_filepath(report_path, file_prefix, file_ext)
    md_content = None
    if len(extracted_jobs) > 0:
        md_content = save_job_list_to_markdown(extracted_jobs, resolved_file)
    else:
        print("No jobs found matching criteria.")
        md_content = "# No job matches found for the given criteria."
            
    html_body = convert_md_file_to_html_body(md_content)
    background_send_email_task(get_value_from_config("EMAIL", "RECIPIENT"), "Job Match Alert from Hello Buddy", html_body)


