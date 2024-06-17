#this code is to be executed after the google_maps_leads csv has been created which separated the url's based on whether they have "google.com" in their result.This specifies that the specific tile doesnt have a website of their own and uses google search to point to.

import pandas as pd
#code it in the same directory where the google_maps_leads will be created

df = pd.read_csv('google_maps_leads.csv')
filtered_df = df[df['WebsiteURL'].str.contains('google.com', na=False)]
filtered_df.to_csv('no_company_website.csv', index=False)
updated_df = df[~df['WebsiteURL'].str.contains('google.com', na=False)]
updated_df.to_csv('google_maps_leads.csv', index=False)
print("Filtered results have been saved to no_company_website.csv and removed from google_maps_leads.csv")
