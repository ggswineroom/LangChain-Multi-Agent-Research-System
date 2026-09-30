from src.tools.tools import scrape_url, web_search

# calling the functions that returns the results.

# output = web_search("Latest news about AI")
# print(output)

# scrappedText = scrape_url("https://www.artificialintelligence-news.com")
# print("The Scrapped Texts is: **************************** \n" + scrappedText)

# Invoking the tools that is decorated as a tool with langchain tool importer.

r_websearch = web_search.invoke("What is the latest research on using AI for climate change mitigation?")
print (r_websearch)
