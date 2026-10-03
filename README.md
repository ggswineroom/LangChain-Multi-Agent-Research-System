# LangChain-Multi-Agent-Research-System


conda create -n langagent python=3.11 -y

conda activate langagent

conda deactivate

cd LangChain-Multi-Agent-Research-System

python -m pip install -U python-dotenv

python -m pip install -U \
  langchain \
  langchain-core \
  langchain-community \
  langchain-openrouter \
  langchain-tavily \
  tavily-python \
  streamlit \
  beautifulsoup4 \
  readability-lxml \
  trafilatura \
  requests \
  lxml \
  python-dotenv \
  rich


python -m pip install tavily-python

python3 -m pip install -U langchain-openai

streamlit run app.py



pip install -r requirements.txt
