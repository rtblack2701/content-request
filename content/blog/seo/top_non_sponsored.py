from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from content.blog.seo.top_non_sponsored_seo_analysis import analyze_webpage
import os


def get_top_non_sponsored_article(keyword):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://www.google.com")

    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "q")))
        driver.execute_script("arguments[0].value = arguments[1];", search_box, keyword)
        driver.execute_script("arguments[0].form.submit();", search_box)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )

        search_results = driver.find_elements(By.XPATH, "//a/h3/ancestor::a")
        seen_urls = set()

        for result in search_results:
            is_sponsored = result.find_elements(By.XPATH, ".//span[contains(text(),'Ad')]")
            title = result.find_element(By.TAG_NAME, 'h3').text.strip()
            url = result.get_attribute('href')

            if (
                url and
                'getunleash.io' not in url and
                not is_sponsored and
                url not in seen_urls
            ):
                seen_urls.add(url)
                seo_data = analyze_webpage(url)

                if seo_data:
                    headings = seo_data.get('heading_structure', [])
                    word_count = seo_data.get('word_count', 0)

                    if headings and len(headings) >= 3:
                        log_lines = [
                            f"✅ Using SEO article: {title}",
                            f"🌐 URL: {url}",
                            f"📝 Word Count: {word_count}",
                            "🧱 Heading Structure:"
                        ] + [f"  {h['tag'].upper()}: {h['text']}" for h in headings]

                        log_content = "\n".join(log_lines)

                        # Print to terminal
                        print("\n" + log_content)

                        # Write to seo_sniping.log (overwrite each run)
                        log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../seo_sniping.log"))
                        with open(log_path, "w") as log_file:
                            log_file.write(log_content)

                        driver.quit()
                        return title, url, headings, word_count
                    else:
                        print(f"⚠️ Skipped: Not enough usable headings in article: {url}")

        driver.quit()
        return None, None, None, None

    except Exception as e:
        driver.quit()
        print(f"Error during scraping: {e}")
        return None, None, None, None