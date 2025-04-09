"""
Example demonstrating how to use the Markdown to HTML converter in splore_sdk.
"""

import os
from dotenv import load_dotenv

# Import the utility functions
from splore_sdk.utils import md_to_html, MarkdownConverter
from splore_sdk import SploreSDK, AgentSDK

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


def advanced_conversion_example():
    """Demonstrate more advanced usage with custom extensions."""
    print("\n=== Advanced Markdown to HTML Conversion ===\n")
    
    # Create a converter instance
    converter = MarkdownConverter()
    
    # Convert with specific extensions
    html = converter.convert(
        EXAMPLE_MARKDOWN,
        extensions=['extra', 'codehilite', 'toc'],
        extension_configs={
            'codehilite': {
                'linenums': True,
                'css_class': 'highlight'
            }
        },
        safe_mode=True
    )
    
    # Print the result (just showing first 500 chars)
    print(f"{html[:500]}...\n")
    print("(Output truncated for brevity)")


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
    advanced_conversion_example()
    integration_with_agent_example()
    
    print("\nDone!")
