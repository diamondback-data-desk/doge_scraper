# Automatically Scraping DOGE Cuts to the University of Maryland
By Theodore Rose

## Reasoning
DOGE and the Trump administration have seen cuts to federal contracts, grants and leases as decreasing government waste. Institutions such as universities rely heavily on federal investment through these programs, the University of Maryland is one of these institutions. The Diamondback has relied on [self reported grant terminations](https://grant-watch.us/nsf-data.html) or this university [self reporting data](https://dbknews.com/2025/04/23/umd-research-cuts-grants-trump/) ([more data](https://president.umd.edu/articles/our-response-to-federal-changes)) to report these cuts to the public. To ensure that the paper will have updated and reliable data the need to get the data from DOGE directly became paramount.

DOGE is not expressly open with their data. They have an API, though, they do not allow access to all data types, limiting information. Thus, scraping the contracts, grants and leases table directly off the DOGE website proved to be a viable solution.

## Running
This github repository updates automatically with scraping beginning at 9:00 am, ending about an hour later, with cleaning starting at 10:30 am. There is no need to pull the repository to run the programs, though if you would like to receive updates to the data with your own local clone, you will have to pull from the repository.

## Data
Raw DOGE cuts are provided in the data/doge_cuts.csv file. DOGE cuts specific to the University of Maryland or University of Maryland, College Park are located in data/umd_cuts.csv.
