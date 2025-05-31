# Script to clean raw DOGE data to the University of Maryland

# library
library(tidyverse)

# Reading in raw DOGE data
doge_data <- read_csv("data/doge_data.csv")

# Making one data frame with all the cuts related to the University of Maryland
# includes non-College Park related campuses
umd_doge_cuts <- doge_data |>
  mutate(
    Vendor = str_to_lower(Vendor), # making Vendor and Recipient strings lower
    Recipient = str_to_lower(Recipient)
  ) |>
  filter(
    str_detect(Vendor, "university of maryland") | 
    str_detect(Vendor, " university of maryland ") |
    str_detect(Vendor, "university of maryland ") |
    str_detect(Vendor, " university of maryland") |
    str_detect(Recipient, "university of maryland") | 
    str_detect(Recipient, " university of maryland ") |
    str_detect(Recipient, "university of maryland ") |
    str_detect(Recipient, " university of maryland") |
    str_detect(Recipient, "university of maryland, college park") | 
    str_detect(Recipient, " university of maryland, college park  ") |
    str_detect(Recipient, "university of maryland, college park ") |
    str_detect(Recipient, " university of maryland, college park")
)

# Filtering out cuts that include "baltimore", "es", or "Eastern Shore"
umd_doge_cuts_unrelated <- umd_doge_cuts |>
  filter(
    str_detect(Vendor, "baltimore") | 
    str_detect(Recipient, "baltimore") |
    str_detect(Vendor, "es") |
    str_detect(Recipient, "es") |
    str_detect(Vendor, "eastern shore") |
    str_detect(Recipient, "eastern shore") 
  )

# Creating data frame with only cuts related to the university of maryland
# or university of maryland, college park
umd_doge_cuts_related <- anti_join(umd_doge_cuts, umd_doge_cuts_unrelated)

# writing to the csv
write_csv(umd_doge_cuts_related, "data/umd_cuts.csv")