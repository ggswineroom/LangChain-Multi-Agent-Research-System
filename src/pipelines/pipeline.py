from src.agents.agents import build_reader_agent, build_search_agent,Writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:
    
    state = {}
    
    # Step 1 - search agent
    
    print("\n"+"="*50)
    print("Step 1 - Search Agent is Working ...")
    print("="*50)
    
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about : {topic}")]
    })

    # print("\n===== SEARCH RESULT =====")
    # print(search_result)
    # print("=========================\n")

    state["search_results"] = search_result["messages"][-1].content
    
    print("\n search result", state['search_results'])
    
    # Step 2 - Reader Agent
    
    print("\n"+"="*50)
    print("Step 2 - Reader Agent is Working ...")
    print("="*50)
    
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    (
                        f"Based on the following search results about '{topic}', "
                        f"Pick the most relevant URL and scrap it for deeper content. \n\n"
                        f"Search Results : \n {state['search_results'][:800]}"
                    )
                )
            ]
        }
    )
    
    state ['scraped_content'] = reader_result['messages'][-1].content
    
    print("\n scraped content: \n", state["scraped_content"])
    
    # Step 3  - Writer Chain
    
    print("\n"+"="*50)
    print("Step 2 - Writer is drafting the report ...")
    print("="*50)
    
    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']}"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )
    
    state["report"] = Writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
        
    })
    
    print("\n Final Report \n ", state['report'])
    
    # Step 4 - Critic Report
    print("\n"+"="*50)
    print("Step 2 - Critic is reviewing the report ...")
    print("="*50)
    
    state['feedback'] = critic_chain.invoke({
        "Report": state['report']
    })
    
    print ("\n Critic Report: \n", state['feedback'])
    
    return state
    