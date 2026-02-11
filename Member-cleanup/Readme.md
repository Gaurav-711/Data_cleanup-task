What logic did you apply?

I fixed the CSV data from the Excel file, standardized all signup dates to YYYY-MM-DD format, cleaned and normalized names and emails (including handling Gmail aliases), and identified low-quality leads such as test entries or invalid domains.I removed the invalid records into a separate "Extra" file. I then removed duplicate users at the file, retained only the most recent signup per user, and added an "is_multi_plan" flag for users who signed up for more than one unique plan. The Final result is a clean Golden Record CSV suitable for CRM usage.



2. What was the most frustrating part, and why were 20% of leads deleted?

For me the most frustrating part was that the different types of errors that i found in the file. Some rows contained commas inside names (for example, “Doe, John”), which broke normal CSV rules and required reconstructing rows logically instead of relying on simple splitting. Additionally, email variations represented the same person, making deduplication challenging. Then the .Lang email with the Alice Wonderland name , J4ne Smith , and so many other errors.These kinds of error required special changes in the code which was a good learning experience. 

To a non-technical manager, I would say :" the removed leads were test data, duplicates, invalid emails, or structurally corrupted records. Keeping them would inflate metrics and reduce CRM data quality. Removing them ensures accurate reporting and better business decisions."
