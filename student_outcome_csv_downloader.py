from playwright.sync_api import sync_playwright
import os

# Academic Year term starts with Fall 2014 to Spring 2020 for 2014-2020 (EXCLUDES Summer)
# Academic Year term starts with Fall 2020 to Spring 2024 for 2020-2024 (EXCLUDES Summer)

def download_course_success_csv(start_year_label, filename):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("🔍 Navigating to Credit Course Retention/Success Rate Report page...")
        page.goto("https://datamart.cccco.edu/Outcomes/Course_Ret_Success.aspx", timeout=180000)

        print("\n🕒 Please manually select the following filters in the browser:")
        print(f"  • Select State-District-College: Collegewide Search")
        print(f"  • Select District-College: Select ALL colleges")
        print(f"  • Select Term-Annual Option: Term Search")
        print(f"  • IMPORTANT: Only select Fall, Winter, and Spring terms for academic years starting {start_year_label}")
        print(f"    (⚠️ Do NOT select Summer terms — EOPS annual year excludes summer)")
        print(f"  • Select Program Type: All")
        print(f"  • Select Instruction Method: All")
        print(f"  • Click Update Report")
        print(f"  • Once the table loads, click Export To ➝ CSV")

        print("\n📥 Waiting for CSV file to download...")

        try:
            with page.expect_download(timeout=360000) as download_info:
                print("👉 Waiting for 'Export ➝ CSV' to be clicked...")
                pass  # Wait manually
            download = download_info.value
            save_path = os.path.join(os.getcwd(), filename)
            download.save_as(save_path)
            print(f"✅ CSV file saved to: {save_path}")
        except Exception as e:
            print(f"❌ Download failed: {e}")

        browser.close()

if __name__ == "__main__":
    # Download for 2014–2020 (Fall 2014 - Spring 2020, excluding Summers)
    download_course_success_csv("Fall 2014 to Spring 2020", "Course_Success_Data_2014_2020.csv")

    # Download for 2020–2024 (Fall 2020 - Spring 2024, excluding Summers)
    download_course_success_csv("Fall 2020 to Spring 2024", "Course_Success_Data_2020_2024.csv")
