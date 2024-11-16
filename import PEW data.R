
# Subset PEW data

rm(list=ls())

# Install and load necessary packages
library(haven)
library(dplyr)

# Read the mapping CSV file
mapping <- read.csv("variable_mapping.csv")

# Function to read and rename variables based on the mapping
read_and_rename <- function(file_path, mapping, year) {
  # Filter the mapping for the given year
  year_mapping <- mapping %>% filter(source_file == year)
  
  # Read only the variables needed
  cols_to_read <- year_mapping$question_number
  data <- read_sav(file_path, col_select = all_of(cols_to_read))
  
  # Rename the variables
  for (i in 1:nrow(year_mapping)) {
    old_name <- year_mapping$question_number[i]
    new_name <- year_mapping$combine_into[i]
    if (old_name %in% names(data)) {
      names(data)[names(data) == old_name] <- new_name
    }
  }
  
  # Add a column for the year
  data$year <- year
  
  # Create a unique ID for all records
  data$id <- 1:nrow(data)
  
  return(data)
}

# Years to process
years <- 2006:2023
years <- setdiff(years, 2010)
data_list <- list()

# Loop through each year, read data, and rename variables
for (year in years) {
  file_path <- paste0(year, ".sav")
  renamed_data <- read_and_rename(file_path, mapping, year)
  data_list[[paste0("pew", as.character(year))]] <- renamed_data
}

# Function to clear value labels for a single data frame before merge
clear_labels <- function(df) {
  for (col in colnames(df)) {
    attr(df[[col]], "labels") <- NULL
  }
  return(df)
}

# Apply the function to all data frames in the list
data_list <- lapply(data_list, clear_labels)
combined_data <- bind_rows(data_list)

# Load country_recode mapping file
country_recode <- read.csv("country_recode.csv", stringsAsFactors = FALSE)
merged_data <- merge(combined_data, country_recode, by.x = c("year", "country"), by.y = c("year", "country"), all.x = TRUE)

# Export combined file
write_sav(merged_data, "exported_file.sav")


               

