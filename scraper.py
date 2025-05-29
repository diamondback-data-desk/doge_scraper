"""
Imports
"""
#pip3 install selenium
from selenium import webdriver #alows dynamic scraping since I could not normally call the url
from selenium.webdriver.common.by import By
from threading import Thread
import pandas as pd
import time

pd.set_option('display.max_columns', None)

# this scraper will use the Chrome browser

contract_driver = webdriver.Chrome()
grant_driver = webdriver.Chrome()
leases_driver = webdriver.Chrome()

time.sleep(1)

# opening DOGE site
contract_driver.get("https://www.doge.gov/savings")
grant_driver.get("https://www.doge.gov/savings")
leases_driver.get("https://www.doge.gov/savings")

# setting empty lists for the data to be put into
contracts_table = []
grants_table = []
leases_table = []

def scrape_contracts():
    time.sleep(2)

    # contracts arranged by date, desc
    contracts_date = contract_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[1]/div[1]/div[2]/button[3]')
    contracts_date.click()
    
    # contracts while loop
    while True:    
    
        contract_html = contract_driver.page_source
        contract_tables = pd.read_html(contract_html)
        print(contract_tables)
    
        contracts_table.append(contract_tables[0])
      
        try:
    
            next = contract_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[1]/div[3]/div[2]/button[8]')
        
            if not next.is_enabled():
                break
    
            if next:
                next.click()
                time.sleep(2)
    
        except:
            break

def scrape_grants():
    time.sleep(2)

    grants_by_date = grant_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[2]/div[1]/div[2]/button[3]')
    grants_by_date.click()
    
    # grants loop
    while True:
    
        grant_html = grant_driver.page_source
        grant_tables = pd.read_html(grant_html)
    
        grants_table.append(grant_tables[1])
    
        try:
        
            next = grant_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[2]/div[3]/div[2]/button[8]')
    
            if not next.is_enabled():
                break
    
            if next:
                next.click()
                time.sleep(2)
    
        except:
            break 

def scrape_leases():
    time.sleep(2)

    leases_by_date = leases_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[3]/div[1]/div[2]/button[3]')
    leases_by_date.click()

    # leases while loop
    while True:
        
        lease_html = leases_driver.page_source
        lease_tables = pd.read_html(lease_html)

        leases_table.append(lease_tables[2])

        try:
            
            next = leases_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[4]/div[3]/div[3]/div[2]/button[8]')
            
            if not next.is_enabled():
                break

            if next:
                next.click()
                time.sleep(2)
        
        except:
            break

def clean_and_csv():

    contracts_df = pd.concat(contracts_table)
    contracts_df['type'] = 'contract'

    grants_df = pd.concat(grants_table)
    grants_df['type'] = 'grant'

    leases_df = pd.concat(leases_table)
    leases_df['type'] = 'lease'

    # combining data frames
    combined_doge_data = pd.concat([contracts_df, grants_df, leases_df])

    combined_doge_data.to_csv('data/tester.csv')

if __name__ == '__main__':
    collect_contracts = Thread(target = scrape_contracts)
    collect_grants = Thread(target = scrape_grants)
    collect_leases = Thread(target = scrape_leases)

    collect_contracts.start()
    collect_grants.start()
    collect_leases.start()

    collect_contracts.join()
    collect_grants.join()
    collect_leases.join()

    clean_and_csv()

    #closes Chrome instance
    contract_driver.quit()
    grant_driver.quit()
    leases_driver.quit()