import requests
import json

def test_qwen():
    text = "I am incredibly bullish on Palantir today. PLTR is going to the moon. However, I am going to short Disney because DIS is looking terrible."
    
    prompt = f"""
    You are a quantitative data extraction engine. Read the following Reddit text.
    1. Identify any publicly traded companies mentioned.
    2. Resolve the company to its official US stock ticker.
    3. Determine the sentiment strictly toward that company (POSITIVE, NEGATIVE, NEUTRAL).
    
    Text: "{text}"
    
    CRITICAL INSTRUCTIONS:
    - Output ONLY a JSON array of objects. Do not include markdown formatting.
    - Format exactly like this: [{{"ticker": "PLTR", "sentiment": "POSITIVE"}}]
    - If no companies are discussed, output an empty array: []
    """

    print("Sending text to Qwen 2.5 (14B)...")
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:14b",
                "prompt": prompt,
                "stream": False,
                "format": "json", 
                "options": {"temperature": 0.0}
            }
        )
        
        raw_output = response.json()['response']
        print("\n--- RAW OUTPUT FROM LLM ---")
        print(raw_output)
        print("---------------------------\n")
        
        # Test if Python can actually read it
        parsed_data = json.loads(raw_output)
        print("SUCCESS! Python parsed the JSON:")
        print(parsed_data)
        
    except Exception as e:
        print(f"\nFATAL ERROR: Python could not parse the output. Error: {e}")

if __name__ == "__main__":
    test_qwen()