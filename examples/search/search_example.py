"""
Example demonstrating how to use the search functionality in splore_sdk.
"""

import os
from dotenv import load_dotenv
import time
from splore_sdk import SploreSDK

# Load environment variables from .env file (if it exists)
load_dotenv()

# Get necessary environment variables
API_KEY = os.getenv("SPLORE_API_KEY")
BASE_ID = os.getenv("SPLORE_BASE_ID")
AGENT_ID = os.getenv("SPLORE_AGENT_ID")

def main():
    # Initialize the SDK
    sdk = SploreSDK(api_key=API_KEY, base_id=BASE_ID)
    
    # Initialize an agent
    agent_sdk = sdk.init_agent(agent_id=AGENT_ID)
    
    # Perform a search query
    print(f"Performing search query for agent {AGENT_ID}...")
    search_results = agent_sdk.search_query(
        query="What is machine learning?",
        count=5,  # Return 5 results
        engine="google"  # Use Google search engine
    )
    
    print("\nSearch Results:")
    print("--------------------")
    for i, result in enumerate(search_results.get("results", []), 1):
        print(f"{i}. {result.get('title')}")
        print(f"   URL: {result.get('link')}")
        print(f"   Snippet: {result.get('snippet')[:100]}...")
        print()
    
    # Wait a moment before getting search history
    time.sleep(2)
    
    # Get search history
    print("\nRetrieving search history...")
    history = agent_sdk.get_search_history(page=0, size=10)
    
    print("\nSearch History:")
    print("--------------------")
    for i, item in enumerate(history.get("items", []), 1):
        print(f"{i}. Query: {item.get('query')}")
        print(f"   Date: {item.get('createdAt')}")
        print()

if __name__ == "__main__":
    main()
