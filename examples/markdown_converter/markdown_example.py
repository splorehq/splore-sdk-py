"""
Example demonstrating how to use the Markdown to HTML converter in splore_sdk.

This example shows various ways to convert markdown content to HTML, including:
1. Basic conversion using md_to_html
2. Advanced conversion with custom extensions
3. Integration with agent responses
4. Real-world examples of markdown content
"""

import os
from dotenv import load_dotenv

# Import the utility functions
from splore_sdk.utils import md_to_html
from splore_sdk import SploreSDK

# Load environment variables from .env file (if it exists)
load_dotenv()

# Example markdown content
EXAMPLE_MARKDOWN = """
# Markdown to HTML Converter

This is a demonstration of the Markdown to HTML converter utility in the Splore SDK.

## Features

* Converts headings
* Handles **bold** and *italic* text
* Supports `inline code` and code blocks
* Creates [links](https://splore.com)
* And more!

```python
# Example code block
def hello_world():
    print("Hello from Splore SDK!")
```

1. Numbered lists work too
2. Just like this
3. It's very convenient

> Blockquotes are also supported
"""


# Example markdown with tables and images
TABLE_MARKDOWN = """
# Data Analysis Report

## Summary

| Metric | Value | Status |
|--------|-------|--------|
| Revenue | $10,000 | 
| Expenses | $5,000 | 
| Profit | $5,000 | 

![](https://example.com/analysis-chart.png)
"""


def simple_conversion_example():
    """Demonstrate the basic usage of the md_to_html function."""
    print("\n=== Basic Markdown to HTML Conversion ===\n")
    
    # Convert markdown to HTML using the utility function
    html = md_to_html(EXAMPLE_MARKDOWN)
    
    # Print the result
    print(html)
    
    # You can also save the HTML to a file
    with open("output.html", "w") as f:
        f.write(html)
    print("\nHTML output saved to output.html")


def table_conversion_example():
    """Demonstrate conversion of markdown tables and images."""
    print("\n=== Table and Image Conversion ===\n")
    
    # Convert markdown with tables to HTML
    html = md_to_html(TABLE_MARKDOWN)
    
    # Print the result
    print(html)
    
    # Save to a separate file
    with open("table_output.html", "w") as f:
        f.write(html)


def format_extracted_response_example():
    """
    Demonstrate how to format extracted response data using markdown.
    
    This example shows how to take raw extracted data and format it
    into a well-structured markdown document that can be converted to HTML.
    """
    print("\n=== Formatting Extracted Response ===\n")
    
    # Example of raw extracted data (simulated)
    extracted_data = {
        "title": "Financial Report",
        "date": "2025-04-09",
        "metrics": {
            "revenue": 10000,
            "expenses": 5000,
            "profit": 5000
        },
        "summary": "The company has shown strong growth in Q1",
        "key_points": [
            "Revenue increased by 20%",
            "Cost optimization measures were successful",
            "New product launch contributed to growth"
        ]
    }
    
    # Format the data as markdown
    markdown_content = f"""
# {extracted_data['title']}

Date: {extracted_data['date']}

## Summary

{extracted_data['summary']}

## Key Metrics

| Metric | Value |
|--------|-------|
| Revenue | ${extracted_data['metrics']['revenue']:,} |
| Expenses | ${extracted_data['metrics']['expenses']:,} |
| Profit | ${extracted_data['metrics']['profit']:,} |

## Key Points

{chr(10).join(f"* {point}" for point in extracted_data['key_points'])}
    """
    
    # Convert to HTML
    html = md_to_html(markdown_content)
    
    # Save to file
    with open("formatted_extract.html", "w") as f:
        f.write(html)
    
    print("\nFormatted extracted data saved to formatted_extract.html")
    print("\nExample of formatted markdown:")
    print(markdown_content)


def integration_with_agent_example():
    """
    Demonstrate how to use the Markdown converter with agent responses.
    
    This example shows how you might process markdown content returned 
    from an agent's response before displaying it to users.
    """
    # Get API credentials
    API_KEY = os.getenv("SPLORE_API_KEY", "your_api_key")
    BASE_ID = os.getenv("SPLORE_BASE_ID", "your_base_id")
    AGENT_ID = os.getenv("SPLORE_AGENT_ID", "your_agent_id")
    
    print("\n=== Integration with Agent Example ===\n")
    
    # Skip the actual API call if credentials aren't provided
    if API_KEY == "your_api_key" or BASE_ID == "your_base_id" or AGENT_ID == "your_agent_id":
        print("Skipping API call (credentials not provided)")
        
        # Simulate agent response with markdown
        mock_agent_response = {
            "response": EXAMPLE_MARKDOWN,
            "sources": []
        }
        
        # Convert the markdown response to HTML
        formatted_response = md_to_html(mock_agent_response["response"])
        
        print("\nConverted agent response (simulated):")
        print(f"{formatted_response[:300]}...\n")
        print("(Output truncated for brevity)")
        return
    
    try:
        # Initialize the SDK
        sdk = SploreSDK(api_key=API_KEY, base_id=BASE_ID)
        
        # Initialize an agent
        agent = sdk.init_agent(agent_id=AGENT_ID)
        
        # In a real application, you might search or extract information
        # Example: search_results = agent.search.search(query="What is Splore?")
        
        # Then convert any markdown response to HTML for display
        # formatted_html = md_to_html(search_results.get("response", ""))
        
        print("Agent initialized successfully")
        print("In a real application, you would make API calls here")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Run the examples
    simple_conversion_example()
    table_conversion_example()
    format_extracted_response_example()
    integration_with_agent_example()
    
    print("\nDone!")
