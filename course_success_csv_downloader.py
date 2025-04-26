from playwright.sync_api import sync_playwright
import os

def download_course_success_csv():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("🔍 Navigating to Credit Course Retention/Success Rate Report page...")
        page.goto("https://datamart.cccco.edu/Outcomes/Course_Ret_Success.aspx", timeout=180000)

        print("\n🕒 Please manually select the following filters in the browser:")
        print("  • Select State-District-College: Collegewide Search")
        print("  • Select District-College: Select ALL colleges")
        print("  • Select Term-Annual Option: Term Search")
        print("  • Select ALL Terms")
        print("  • Select Program Type: All")
        print("  • Select Instruction Method: All")
        print("  • Click Update Report")
        print("  • Once the table loads, click Export To ➝ CSV")
        
        print("\n📥 Waiting for CSV file to download...")

        try:
            with page.expect_download(timeout=360000) as download_info:
                print("👉 Waiting for 'Export ➝ CSV' to be clicked...")
                pass  # Manually triggered
            download = download_info.value
            save_path = os.path.join(os.getcwd(), download.suggested_filename)
            download.save_as(save_path)
            print(f"✅ CSV file saved to: {save_path}")
        except Exception as e:
            print(f"❌ Download failed: {e}")

        browser.close()

if __name__ == "__main__":
    download_course_success_csv()
