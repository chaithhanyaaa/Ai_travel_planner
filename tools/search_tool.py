from langchain_tavily import TavilySearch

from config import (
    TAVILY_API_KEY,
    TAVILY_MAX_RESULTS,
)

search_tool = TavilySearch(
    api_key=TAVILY_API_KEY,
    max_results=TAVILY_MAX_RESULTS,
)