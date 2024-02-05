#!/bin/bash
# # This code create and press profiles database

#Create Profile DB
# parent_directory="/groups/itay_mayrose/danielz/gene_fams/ProfilesUpdated/updProfiles/"
parent_directory=$1
output_file="$parent_directory/data_base_profile.hmm"

# Change to the parent directory
cd "$parent_directory" || exit
# Create an empty profileDB.hmm file
touch "$output_file"
# Iterate through each subdirectory
for subdirectory in */; do
    subdirectory_path="${parent_directory}${subdirectory}"
    # Change to the subdirectory
    cd "$subdirectory_path" || exit
    # Concatenate all .hmm files in the subdirectory into profileDB.hmm
    cat *.hmm >> "$output_file"
    # Optionally, you can print a message for each subdirectory processed
    echo "Concatenated .hmm files in $subdirectory to $output_file"
    # Move back to the parent directory
    cd "$parent_directory" || exit
done
hmmpress $output_file
