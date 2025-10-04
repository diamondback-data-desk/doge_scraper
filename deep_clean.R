# Script to clean raw DOGE data to the University of Maryland

# library
library(tidyverse)

# Reading in raw DOGE data
doge_data <- read_csv("data/doge_data.csv")

# Cleaning the data
clean_doge_data <- doge_data |>
  filter(type != "lease") |>
  mutate(
    savings = str_extract(details, "\\$?[0-9,\\.]+(?=\\s+[Ss]avings)"),
    contract_total = str_extract(details, "\\$?[0-9,\\.]+(?=\\s+[Tt]otal)"),
    contract_description = str_extract(details, "(?i)Total Contract\\s+.*") |> 
      str_remove("(?i)Total Contract\\s+"),
    grant_description = str_extract(details, "(?i)Total Grant\\s+.*") |> 
      str_remove("(?i)Total Grant\\s+"),
    providing_agency = str_extract(details, "(?i)Agency:\\s*[^$]+") |>
      str_remove("(?i)Agency:\\s*"),
    vendor = str_extract(details, "^(.*?)\\s*[Aa]gency:") |>
      str_remove("\\s*[Aa]gency:")
  )

clean_doge_data <- clean_doge_data |>
  mutate(
    vendor_lower = str_to_lower(vendor),
    details_lower = str_to_lower(details)
  )

# Making one data frame with all the cuts related to the University of Maryland
# includes non-College Park related campuses
umd_doge_cuts <- clean_doge_data |>
  mutate(
    vendor = str_to_lower(vendor),
    details = str_to_lower(details)# making Vendor and Recipient strings lower
  ) |>
  filter(
    str_detect(vendor, "university of maryland") | 
    str_detect(vendor, " university of maryland ") |
    str_detect(vendor, "university of maryland ") |
    str_detect(vendor, " university of maryland") |
    str_detect(vendor, "university of maryland, college park") | 
    str_detect(vendor, " university of maryland, college park  ") |
    str_detect(vendor, "university of maryland, college park ") |
    str_detect(vendor, " university of maryland, college park") |
    str_detect(details, "university of maryland") | 
    str_detect(details, " university of maryland ") |
    str_detect(details, "university of maryland ") |
    str_detect(details, " university of maryland") |
    str_detect(details, "university of maryland, college park") | 
    str_detect(details, " university of maryland, college park  ") |
    str_detect(details, "university of maryland, college park ") |
    str_detect(details, " university of maryland, college park")
) |>
  select(-details)


# Filtering out cuts that include "baltimore", "es", or "Eastern Shore"
umd_doge_cuts_unrelated <- umd_doge_cuts |>
  filter(
    str_detect(Vendor, "baltimore") | 
    str_detect(Recipient, "baltimore") |
    str_detect(Vendor, "university of maryland es") |
    str_detect(Recipient, "university of maryland es") |
    str_detect(Vendor, "eastern shore") |
    str_detect(Recipient, "eastern shore") 
  )

# Creating data frame with only cuts related to the university of maryland
# or university of maryland, college park
umd_doge_cuts_related <- anti_join(umd_doge_cuts, umd_doge_cuts_unrelated)

# writing to the csv
write_csv(umd_doge_cuts_related, "data/umd_cuts.csv")
