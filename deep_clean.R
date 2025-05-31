library(tidyverse)

doge_data <- read_csv("data/doge_data.csv")

umd_doge_cuts <- doge_data |>
  mutate(
    Vendor = str_to_lower(Vendor),
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

umd_doge_cuts_unrelated <- umd_doge_cuts |>
  filter(
    str_detect(Vendor, "baltimore") | 
    str_detect(Recipient, "baltimore") |
    str_detect(Vendor, "es") |
    str_detect(Recipient, "es") |
    str_detect(Vendor, "Eastern Shore") |
    str_detect(Recipient, "Eastern Shore") 
  )

umd_doge_cuts_related <- anti_join(umd_doge_cuts, umd_doge_cuts_unrelated)

write_csv(umd_doge_cuts_related, "data/umd_cuts.csv")