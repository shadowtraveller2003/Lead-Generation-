import pandas as pd
import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from urllib.parse import quote_plus

#change the directory to where you want all the results to be saved at.
output_dir = r'Lead-Generation-main'
os.makedirs(output_dir, exist_ok=True)

def login_to_linkedin(page, username, password):
    page.goto("https://www.linkedin.com/login")
    page.fill("input[name='session_key']", username)
    page.fill("input[name='session_password']", password)
    page.click("button[type='submit']")
    page.wait_for_selector("input[placeholder='Search']")

def extract_people_info(page):
    people_info = []
    people_list = page.query_selector_all("li.reusable-search__result-container")
    for person in people_list:
        try:
            name = person.query_selector("span.entity-result__title-text > a").inner_text()
            title = person.query_selector("div.entity-result__primary-subtitle").inner_text()
            location = person.query_selector("div.entity-result__secondary-subtitle").inner_text()
            people_info.append({
                "Name": name,
                "Title": title,
                "Location": location
            })
        except Exception as e:
            print(f"Error extracting person details: {e}")
    
    return people_info

def create_linkedin_search_url(company_name):
    base_url = "https://www.linkedin.com/search/results/people/"
    query = f"?keywords={quote_plus(company_name)}&origin=SWITCH_SEARCH_VERTICAL"
    return base_url + query

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
      #enter your linkedin username and password
        username = 'xyz@gmail.com'
        password = 'xyz'
        
        try:
            print("Logging in to LinkedIn...")
            login_to_linkedin(page, username, password)
            print("Logged in successfully.")
          #code in the same directory as the google_maps_leads to get the same results as mine.
            csv_file_path = os.path.join(output_dir, 'google_maps_leads.csv')
            companies = pd.read_csv(csv_file_path)['Title'].tolist()
            
            for company_name in companies:
                search_url = create_linkedin_search_url(company_name)
                print(f"Navigating to search URL for company: {company_name}")
                page.goto(search_url)
                for _ in range(3):
                    try:
                        page.wait_for_selector("li.reusable-search__result-container, h2.artdeco-empty-state__headline", timeout=60000)  # Wait up to 60 seconds
                        print(f"Search results loaded for company: {company_name}")
                        break
                    except PlaywrightTimeoutError:
                        print(f"Retrying... Search results not loaded yet for company: {company_name}")
                else:
                    print(f"Failed to load search results for company: {company_name}")
                    continue
                if page.query_selector("h2.artdeco-empty-state__headline"):
                    print(f"No results found for company: {company_name}")
                    continue

                all_people_info = []

                for _ in range(5):
                    try:
                        people_info = extract_people_info(page)
                        all_people_info.extend(people_info)
                        next_button = page.query_selector("button.artdeco-pagination__button--next")
                        if next_button and not next_button.is_disabled():
                            next_button.click()
                            page.wait_for_selector("li.reusable-search__result-container", timeout=60000)  # Wait up to 60 seconds
                            print("Navigating to the next page...")
                        else:
                            print("No more pages or next button disabled.")
                            break
                    except PlaywrightTimeoutError as e:
                        print(f"Timeout error on page navigation for company {company_name}: {e}")
                        break
                    except Exception as e:
                        print(f"Error navigating to the next page for company {company_name}: {e}")
                        break
                
                if all_people_info:
                    df = pd.DataFrame(all_people_info)
                    company_safe_name = "".join(c if c.isalnum() else "_" for c in company_name)
                    output_file = os.path.join(output_dir, f"{company_safe_name}_linkedin_people_info.csv")
                    df.to_csv(output_file, index=False)
                    print(f"Saved data to {output_file}")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            browser.close()

    print("LinkedIn people information retrieval complete.")

if __name__ == "__main__":
    main()
