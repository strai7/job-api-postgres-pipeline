from extract import fetch_all_jobs
from database import create_table
from load import load_raw_pages

def main():
    create_table()
    pages = fetch_all_jobs()
    load_raw_pages(pages)

if __name__ == "__main__":
    main()
