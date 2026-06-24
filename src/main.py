from extract import fetch_all_jobs
from load import laod_raw_pages

def main():
    pages = fetch_all_jobs()
    laod_raw_pages(pages)

if __name__ == "__main__":
    main()