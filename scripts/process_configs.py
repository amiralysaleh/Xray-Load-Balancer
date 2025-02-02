import requests
import json

def get_raw_configs():
    url = "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/V2RAY_RAW.txt"
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text.strip().split('\n')
        print(f"Failed to get configs. Status code: {response.status_code}")
        return []
    except Exception as e:
        print(f"Error getting configs: {str(e)}")
        return []

def process_configs():
    configs = get_raw_configs()
    if not configs:
        print("No configs found!")
        return
    
    print(f"Found {len(configs)} configs")
    
    try:
        # Prepare the request
        url = "https://surfboardv2ray.pythonanywhere.com/convert"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Join configs with newline and encode properly
        data = {
            'configs': '\n'.join(configs)
        }
        
        # Send POST request
        response = requests.post(url, data=data, headers=headers)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            result = response.text
            print("Successfully processed configs")
            
            # Save the result
            with open('v2ray_processed.txt', 'w', encoding='utf-8') as f:
                f.write(result)
            print("Saved processed configs to file")
        else:
            print(f"Error: Server returned status code {response.status_code}")
            print(f"Response content: {response.text}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    process_configs()
