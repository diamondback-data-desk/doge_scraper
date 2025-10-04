from selenium import webdriver # allows dynamic scraping
from selenium.webdriver.common.by import By # imports function to search HTML later
from selenium.webdriver.support.ui import WebDriverWait # allows for pauses in script until condition is me 
from selenium.webdriver.support import expected_conditions as EC # used with above import; gives predefined conditions
from threading import Thread # allows multiple functions to be run at once. Enables me to scrape DOGE faster.
import pandas as pd # gets tables from HTML and allows joining of data frames
import time # enables the scraper to not get flagged for bot behavior

# note: this scraper will use the Chrome browser

# opens three separate selenium webdrivers
# one to scrape the contracts table
# another for grants and one for leases
print("Opening Chrome drivers . . . ")
contract_driver = webdriver.Chrome()
grant_driver = webdriver.Chrome()
leases_driver = webdriver.Chrome()

# minimizing the windows so it does not show up on screen
contract_driver.minimize_window()
grant_driver.minimize_window()
leases_driver.minimize_window()

# gives a pause for everything to load just in case
time.sleep(1)

# opening DOGE site on each driver
print("Opening DOGE sites . . . ")
contract_driver.get("https://doge.gov/savings")
grant_driver.get("https://doge.gov/savings")
leases_driver.get("https://doge.gov/savings")

# setting empty lists for the data to be put into
# this is needed as we need to combine each list later
# so that it can be transformed into a csv file
contracts_table = []
grants_table = []
leases_table = []

# functions scraping spcific tables
def scrape_grants():
    # finding the by grant value button to arrange the table by value
    grants_total_value = grant_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[2]/div[1]/div[2]/button[2]') # the direct xpath to the button . . . this breaks often and could be fixed (works without fix tho)
    grants_total_value.click()

    page_number = 1
    
    while True:
        
        # Wait for table rows to load
        time.sleep(1)
        tbody = grant_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[2]/div[2]/div/div/div/table/tbody') #path to table body
        rows = tbody.find_elements(By.TAG_NAME, 'tr') # Collects all rows
        
        for i, row in enumerate(rows): #for loop going through every row in the table and getting the popup info
            try:
                # Re-find the row to avoid stale element issues
                tbody = grant_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[2]/div[2]/div/div/div/table/tbody') # error handling, same as before
                current_rows = tbody.find_elements(By.TAG_NAME, 'tr')
                
                if i < len(current_rows): # if statement clicking the row, else skips
                    current_rows[i].click()
                else:
                    print(f"Row {i} no longer exists, skipping")
                    continue

                # Wait for the popup to appear
                popup = WebDriverWait(grant_driver, 10).until( # waits for the popup to appear before selecting the text area
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.w-full.flex.flex-col.items-center.overflow-y-auto")))

                # Get the content
                try:
                    content_container = popup.find_element(By.CSS_SELECTOR, "div.flex.flex-col.items-center.space-y-2.w-full.px-4") # finding the text element
                    details = content_container.text # takes all text
                except:
                    details = popup.text # else get text of entire popup

                grants_table.append(details) # adding data to table

                # Close the popup
                close_button = popup.find_element(By.XPATH, "//button[text()='Close']") # clicking close by  the name
                close_button.click()

            except Exception as e: # if something weird happens print error statement with row number for debugging
                print(f"Error on row {i}: {e}")

        # Try to go to next page
        try:
            next_button = grant_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[2]/div[3]/div[2]/button[8]') # Get next button
            if next_button.is_enabled():
                print(f"Going to page {page_number + 1}") # keeps track of page number
                next_button.click() # click next
                page_number += 1
            else:
                print("Next button not presnet. Done!")
                break
        except Exception as e:
            print(f"Scraping ended: {e}")
            break
    
    print(f"Total grants collected: {len(grants_table)}") # prints total number of rows collected

# function to scrape leases table
def scrape_leases():
    # finding the by lease value button to arrange the table by value
    leases_total_value = leases_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[3]/div[1]/div[2]/button[2]')
    leases_total_value.click()

    page_number = 1
    
    while True:
        
        # Wait for table rows to load
        time.sleep(1)
        tbody = leases_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[3]/div[2]/div/div/div/table/tbody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        
        for i, row in enumerate(rows):
            try:
                # Re-find the row to avoid stale element issues
                tbody = leases_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[3]/div[2]/div/div/div/table/tbody')
                current_rows = tbody.find_elements(By.TAG_NAME, 'tr')
                
                if i < len(current_rows):
                    current_rows[i].click()
                else:
                    print(f"Row {i} no longer exists, skipping")
                    continue

                # Wait for the popup to appear
                popup = WebDriverWait(leases_driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.w-full.flex.flex-col.items-center.overflow-y-auto")))

                # Get the content
                try:
                    content_container = popup.find_element(By.CSS_SELECTOR, "div.flex.flex-col.items-center.space-y-2.w-full.px-4")
                    details = content_container.text
                except:
                    details = popup.text

                leases_table.append(details)

                # Close the popup
                close_button = popup.find_element(By.XPATH, "//button[text()='Close']")
                close_button.click()

            except Exception as e:
                print(f"Error on row {i}: {e}")

        # Try to go to next page
        try:
            next_button = leases_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[3]/div[3]/div[2]/button[8]')
            if next_button.is_enabled():
                print(f"Going to page {page_number + 1}")
                next_button.click()
                page_number += 1
            else:
                print("Next button disabled, ending pagination")
                break
        except Exception as e:
            print(f"Pagination ended: {e}")
            break
    
    print(f"Total leases collected: {len(leases_table)}")

def scrape_contracts():
    # finding the by contract value button to arrange the table by value
    contracts_total_value = contract_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[1]/div[1]/div[2]/button[2]')
    contracts_total_value.click()

    page_number = 1
    
    while True:
        
        # Wait for table rows to load
        time.sleep(1)
        tbody = contract_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[1]/div[2]/div/div/div/table/tbody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        
        for i, row in enumerate(rows):
            try:
                # Re-find the row to avoid stale element issues
                tbody = contract_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[1]/div[2]/div/div/div/table/tbody')
                current_rows = tbody.find_elements(By.TAG_NAME, 'tr')
                
                if i < len(current_rows):
                    current_rows[i].click()
                else:
                    print(f"Row {i} no longer exists, skipping")
                    continue

                # Wait for the popup to appear
                popup = WebDriverWait(contract_driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.w-full.flex.flex-col.items-center.overflow-y-auto")))

                # Get the content
                try:
                    content_container = popup.find_element(By.CSS_SELECTOR, "div.flex.flex-col.items-center.space-y-2.w-full.px-4")
                    details = content_container.text
                except:
                    details = popup.text

                contracts_table.append(details)

                # Close the popup
                close_button = popup.find_element(By.XPATH, "//button[text()='Close']")
                close_button.click()

            except Exception as e:
                print(f"Error on row {i}: {e}")

        # Try to go to next page
        try:
            time.sleep(1)
            next_button = contract_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[1]/div[3]/div[2]/button[8]')
            if next_button.is_enabled():
                print(f"Going to page {page_number + 1}")
                next_button.click()
                page_number += 1
            else:
                print("Next button disabled, ending pagination")
                break
        except Exception as e:
            print(f"Pagination ended: {e}")
            break
    
    print(f"Total contracts collected: {len(contracts_table)}")

# a function to add a new 'type' column and
# combine the separate table lists into one data frame
# then exporting to a csv file
def clean_and_csv():

    # Create dataframes from the detail strings collected from each section
    # Each list now contains detail strings instead of dataframes
    contracts_df = pd.DataFrame(contracts_table, columns=['details'])
    contracts_df['type'] = 'contract'

    grants_df = pd.DataFrame(grants_table, columns=['details'])
    grants_df['type'] = 'grant'

    leases_df = pd.DataFrame(leases_table, columns=['details'])
    leases_df['type'] = 'lease'

    # combining data frames into one data frame
    combined_doge_data = pd.concat([contracts_df, grants_df, leases_df], ignore_index=True)

    # making that data frame into a csv
    combined_doge_data.to_csv('data/doge_data.csv', index=False)

# when the scraper.py file is called in a terminal
# the following things occur
if __name__ == '__main__':

    # adds the function to a thread to allow them to run at the same time
    # saving on run time
    collect_contracts = Thread(target = scrape_contracts)
    collect_grants = Thread(target = scrape_grants)
    collect_leases = Thread(target = scrape_leases)

    # begins each function, and allows them to run at the same time
    collect_contracts.start()
    collect_grants.start()
    collect_leases.start()

    # waiting for the other functions to end
    # ensures that all the data from all tables are collected
    # before trying to combine them with clean_and_csv()
    collect_contracts.join()
    collect_grants.join()
    collect_leases.join()

    # calls the clean_and_csv() function
    clean_and_csv()

    #closes each Chrome instance
    contract_driver.quit()
    grant_driver.quit()
    leases_driver.quit()
