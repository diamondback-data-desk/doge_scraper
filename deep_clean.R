
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
    vendor = str_to_lower(vendor),
    full_details = str_to_lower(details)
  )

# Making one data frame with all the cuts related to the University of Maryland
# includes non-College Park related campuses
umd_doge_cuts <- clean_doge_data |>
  filter(str_detect(full_details, "university of maryland")) |>
  select(-details)

# writing to the csv
write_csv(umd_doge_cuts, "data/umd_cuts.csv")
