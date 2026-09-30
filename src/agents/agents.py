import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.tools.tools import scrape_url, web_search

load_dotenv()

# Model Initialization ( This is the actual if you want to use chat gpt with OpenAI key)
    #llm = ChatOpenAI(model = "gpt-4o-mini", temperature=0)

# CHANGED: Retrieve your OpenRouter API key instead of the OpenAI key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    temperature=0,
)

# 1st Agent  : Search Agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        # using default system prompt
    )

# 2nd Agent : Reader Agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        # using default system prompt
    )

# 3rd Agent : Writer Agent 
# Writer Chain:  we will utilize Modern langchain LCL chain functionality 
        # {topic}, you get it from the human input
        # {research}, you get it from the reader agent that has alredy scrapped the text from the search agent provided UrLs.
writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert research writer. Write clear, structured and insightful reports. ",
        ),
        (
            "human",
            """ Write a detailed research report on the topic below. 

Topic; {topic}. 

Research Gathered:
{research}

Structure the report as:

- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional. """,
        ),
    ]
)

# Now create the writer chain
    # parameters Writer prompt , llms and stroutput parser
    # LLM do the search on the topic using Tavily search and Scrap agent, The details will be provided to writer prompt and stroutput will 
    # prepare the output to be written.
Writer_chain = writer_prompt | llm | StrOutputParser()


# 4th Agent : Critic Chain
# 
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp constructive research critic. Be honest and specific."),
    ("human", """ Review the research report below and evaluate it strictly.
     
     Report: {Report}
     
     Respond in this exact format:
     
     Score: X/10
     
     Strengths:
     - ...
     - ...
     
     Areas to improve:
     - ...
     - ...
     
     One line verdict:
     ...
     """),
])

critic_chain = critic_prompt | llm | StrOutputParser()