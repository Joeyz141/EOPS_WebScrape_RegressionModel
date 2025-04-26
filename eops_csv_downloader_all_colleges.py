from playwright.sync_api import sync_playwright
import os

def download_eops_csv_by_year_range(start_year, end_year):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print(f"🔍 Navigating to EOPS Report page for {start_year} to {end_year}...")
        page.goto("https://datamart.cccco.edu/Services/EOPS_CARE_Status.aspx", timeout=180000)

        print("🕒 Please manually select the following dropdown filters in the opened browser:")
        print(f"  • Select Terms: {start_year} to {end_year}")
        print("  • Check only EOPS Status box")
        print("  • Click Update Report and wait for table to appear")
        print("  • Then click Export To ➝ CSV")

        print("📥 Waiting for CSV file to be downloaded...")

        try:
            with page.expect_download(timeout=360000) as download_info:
                print("👉 Waiting for you to click 'Export to ➝ CSV'...")
                # Waits until download starts
                pass
            download = download_info.value
            save_path = os.path.join(os.getcwd(), f"EOPS_{start_year}_to_{end_year}.csv")
            download.save_as(save_path)
            print(f"✅ CSV file saved as: {save_path}")

        except Exception as e:
            print(f"❌ Download failed for {start_year} to {end_year}: {e}")

        browser.close()

if __name__ == "__main__":
    # Define year ranges
    year_ranges = [
        (2014, 2020),
        (2020, 2024)
    ]

    for start_year, end_year in year_ranges:
        download_eops_csv_by_year_range(start_year, end_year)