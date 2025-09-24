import sys
import requests
import base64
import re
import os
import random
import json

def get_proxies_from_sub_link(sub_link):
    """
    Fetches and decodes the proxy list from a subscription link.
    Supports Vmess, Vless, Trojan, and Shadowsocks links.
    """
    proxies = []
    try:
        response = requests.get(sub_link, timeout=15)
        if response.status_code != 200:
            print(f"Error fetching subscription link: {sub_link} - Status: {response.status_code}")
            return proxies
        
        decoded_content = base64.b64decode(response.text).decode('utf-8')
        
        patterns = {
            'vless': r'vless://(?:[^@]+@)?(\d{1,3}(?:\.\d{1,3}){3}|\[[0-9a-f:]+\]):(\d+)',
            'trojan': r'trojan://(?:[^@]+@)?(\d{1,3}(?:\.\d{1,3}){3}|\[[0-9a-f:]+\]):(\d+)',
            'ss': r'ss://(?:[^@]+@)?(\d{1,3}(?:\.\d{1,3}){3}|\[[0-9a-f:]+\]):(\d+)'
        }
        
        vmess_matches = re.findall(r'vmess://(.*?)(?=\s|$)', decoded_content)
        for match in vmess_matches:
            try:
                decoded_vmess = base64.b64decode(match).decode('utf-8')
                vmess_config = json.loads(decoded_vmess)
                proxies.append(f"{vmess_config['add']}:{vmess_config['port']}")
            except Exception as e:
                print(f"Failed to decode Vmess config: {e}")

        for p_type, pattern in patterns.items():
            found_proxies = re.findall(pattern, decoded_content)
            for proxy in found_proxies:
                if isinstance(proxy, tuple):
                    proxies.append(f"{proxy[0]}:{proxy[1]}")
                else:
                    proxies.append(proxy)
        
        print(f"Found {len(proxies)} proxies from {sub_link}.")
        return proxies

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to {sub_link}: {e}")
        return proxies
    except Exception as e:
        print(f"An error occurred during decoding or parsing for {sub_link}: {e}")
        return proxies


def generate_pac_file(proxies, filename="proxy.pac"):
    """
    Generates a PAC file using a list of proxies.
    """
    if not proxies:
        print("No proxies available to generate PAC file.")
        return

    selected_proxy = random.choice(proxies)
    
    obfuscation_comment = f"// Generated at {os.environ.get('GITHUB_RUN_ID', 'N/A')}\n"
    
    filtered_domains = [
        "*.youtube.com", "*.googlevideo.com", "*.twitter.com", "*.instagram.com",
        "*.telegram.org", "*.wikipedia.org", "*.facebook.com", "*.linkedin.com",
        "*.tiktok.com"
    ]

    function_name = "findProxyForURL"
    host_param = "host_address"
    url_param = "url_address"
    
    pac_content = f"""{obfuscation_comment}
function {function_name}({url_param}, {host_param}) {{
  var myProxy = "PROXY {selected_proxy}; SOCKS5 {selected_proxy}";

  var domains_to_proxy = [
    {",\n    ".join([f'"{d}"' for d in filtered_domains])}
  ];
  
  for (var i = 0; i < domains_to_proxy.length; i++) {{
    if (shExpMatch({host_param}, domains_to_proxy[i])) {{
      return myProxy;
    }}
  }}

  return "DIRECT";
}}
"""
    with open(filename, "w") as f:
        f.write(pac_content)
    
    print(f"Successfully generated {filename}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sub_to_pac.py <subscription_links_separated_by_comma>")
        sys.exit(1)
    
    sub_links_str = sys.argv[1]
    sub_links = [link.strip() for link in sub_links_str.split('\n') if link.strip()]
    
    all_proxies = []
    for link in sub_links:
        all_proxies.extend(get_proxies_from_sub_link(link))
        
    generate_pac_file(all_proxies)
