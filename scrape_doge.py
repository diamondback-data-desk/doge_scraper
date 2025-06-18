from selenium import webdriver # allows dynamic scraping
from selenium.webdriver.common.by import By # imports function to search HTML later
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
contract_driver.get("https://www.doge.gov/savings")
grant_driver.get("https://www.doge.gov/savings")
leases_driver.get("https://www.doge.gov/savings")

# setting empty lists for the data to be put into
# this is needed as we need to combine each list later
# so that it can be transformed into a csv file
contracts_table = []
grants_table = []
leases_table = []

# scrape function for contracts
def scrape_contracts():
    # finding the by contract value button to arrange the table by value
    # this was the only way to get the value of the contracts and other categories
    contracts_total_value = contract_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[5]/div[1]/div[1]/div[2]/button[2]')

    # clicking the by total value button to arrange it
    contracts_total_value.click()
    
    # contracts while loop
    # while the following can be done 
    while True:    
        # getting the html
        contract_html = contract_driver.page_source
        # getting the tables from html
        contract_tables = pd.read_html(contract_html)

        # adding the correct numbered table (0) for the contract table
        contracts_table.append(contract_tables[0])
        print("Contract table collected ")
      
        # trying to find the button to get the next contract table
        try:
            # finding the next button element
            next = contract_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[5]/div[1]/div[3]/div[2]/button[8]')

            # asks whether or not the next button is enabled
            # if the button is not enabled, then break the function
            # this ends the function after there are no more tables to collect
            if not next.is_enabled():
                break
                
            # if next passed the if not statement above it clicks the button
            # then sleeps for two seconds waiting to run everything else
            # after the page loads
            if next:
                next.click()
                time.sleep(2)
    
        except:
            break

# grant scraper function
def scrape_grants():
    time.sleep(2)

    grants_total_value = grant_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[5]/div[2]/div[1]/div[2]/button[2]')

    grants_total_value.click()
    
    # grants loop
    while True:
    
        grant_html = grant_driver.page_source
        grant_tables = pd.read_html(grant_html)
    
        grants_table.append(grant_tables[1])
        print("Grants table collected")
    
        try:
        
            next = grant_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[5]/div[2]/div[3]/div[2]/button[8]')
    
            if not next.is_enabled():
                break
    
            if next:
                next.click()
                time.sleep(2)
    
        except:
            break 

# function to scrape leases table
def scrape_leases():
    time.sleep(2)

    # the same notes that applied to the function scrape_grants() 
    # apply to scrape_leases() as like the contracts function,
    # their structures are extremely similar

    leases_by_date = leases_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[5]/div[3]/div[1]/div[2]/button[3]')
    leases_by_date.click()

    leases_total_value = leases_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[5]/div[3]/div[1]/div[2]/button[2]')
    leases_total_value.click()

    # leases while loop
    while True:
        
        lease_html = leases_driver.page_source
        lease_tables = pd.read_html(lease_html)

        leases_table.append(lease_tables[2])
        print("Leases table collected")

        try:
            
            next = leases_driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div/div[5]/div[3]/div[3]/div[2]/button[8]')
            
            if not next.is_enabled():
                break

            if next:
                next.click()
                time.sleep(2)
        
        except:
            break

# a function to add a new 'type' column and
# combine the separate table lists into one data frame
# then exporting to a csv file
def clean_and_csv():

    # takes all the contracts_table list of data frames 
    # and combines them into one sigular data frame
    contracts_df = pd.concat(contracts_table)
    # adds a new column named type and labels all rows contract
    # to specify that all of the collected data rows are 
    # in fact contracts
    contracts_df['type'] = 'contract'

    # the same thing as above but for grants
    grants_df = pd.concat(grants_table)
    grants_df['type'] = 'grant'

    # for leases
    leases_df = pd.concat(leases_table)
    leases_df['type'] = 'lease'

    # combining data frames into one data frame
    combined_doge_data = pd.concat([contracts_df, grants_df, leases_df])

    # making that data frame into a csv
    combined_doge_data.to_csv('data/doge_data.csv')

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
