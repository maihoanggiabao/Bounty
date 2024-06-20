import requests
import time
import json
import random
import brotli
import schedule
import time
import urllib.parse

# Function to read proxies from file
def get_proxies():
    with open('proxy.txt', 'r') as file:
        proxies = file.read().splitlines()
    return proxies

# Function to select a random proxy
def get_random_proxy(proxies):
    proxy = random.choice(proxies)
    user_pass, ip_port = proxy.split('@')
    type, user, password = user_pass.split(':')
    user = user.replace("//", "")
    return {
        f"{type}": f"{type}://{user}:{password}@{ip_port}",
        "ip": ip_port.split(':')[0]
    }

proxies = get_proxies()
# Function to send HTTP request
def send_request(url, headers, payload, method='GET', params=None, proxy=None):
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params, proxies=proxy)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=payload, proxies=proxy)
        else:
            raise ValueError("Unsupported HTTP method")

        if response.status_code == 200:
            return response.json()
        else:
            return response.text
    except Exception as e:
        print(f"Error during request: {e}")
        return None

# Main function
def main():
    run_once = True
    # Prompt user for enabling auto play and auto task completion
    while run_once:
        try:
            accounts = []
            try:
                with open('tokens_bounty.txt', 'r') as file:
                    for line in file:
                        accounts.append({'auth': line})
            except:
                print(f"Error in here")
            for account in accounts:
                cookie = account['auth'].replace('\n', '')
                proxy = get_random_proxy(proxies)
                headers = {
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'cookie' : f"{cookie}",
                    'priority': 'u=1, i',
                    'referer': 'https://recent-deals.vercel.app/',
                    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
                }

                startFarm_url = 'https://recent-deals.vercel.app/api/trpc/userExp.startFarm?batch=1'
                claim_url = 'https://recent-deals.vercel.app/api/trpc/userExp.harvestFarm?batch=1'
                # Define the URL
                url = "https://recent-deals.vercel.app/api/trpc/userExp.getUserExp,userExp.getRecentExpHistory,userExp.getFarmRemainTime,userExp.getFarmBonus,userExp.getFarmTime,friendBoost.hasEvmWallet,friendBoost.hasTonWallet"

                # Parameters as given in the query string
                params = {
                    'batch': '1',
                    'input': '{"0":{"json":null,"meta":{"values":["undefined"]}},"1":{"json":null,"meta":{"values":["undefined"]}},"2":{"json":null,"meta":{"values":["undefined"]}},"3":{"json":null,"meta":{"values":["undefined"]}},"4":{"json":null,"meta":{"values":["undefined"]}},"5":{"json":null,"meta":{"values":["undefined"]}},"6":{"json":null,"meta":{"values":["undefined"]}}}'
                }
                for i in range (2):
                    claimXurl = 'https://recent-deals.vercel.app/api/trpc/friendBoost.verifyFollowingBbyTwitter,friendBoost.verifyFollowingBbyTwitter?batch=1'
                    data = {
                            "0": {"json": None, "meta": {"values": ["undefined"]}},
                            "1": {"json": None, "meta": {"values": ["undefined"]}},
                        }

                    requests.post(claimXurl, headers=headers, json=data)

                #claim                                      
                try: 
                    try:
                        balance = requests.get(url, params=params, headers=headers, proxies=proxy)
                        json_data = json.loads(balance.text)
                        print(f"Balance: {json_data[0]['result']['data']['json']} Bounty")
                        claimBounty = send_request(claim_url, headers=headers, payload = {"0":{"json": "null","meta":{"values":["undefined"]}}}, method='POST', proxy=proxy)
                        if (claimBounty[0]['result']['data']['json'] == False):
                            print("Chưa đến thời gian Claim, vui lòng quay lại sau !!!")
                        else:
                            balance = requests.get(url, params=params, headers=headers, proxies=proxy)
                            json_data = json.loads(balance.text)
                            print(f"Chúc mừng bạn đã Claim thành công !!! Balance: {json_data[0]['result']['data']['json']} Bounty")
                        # Restart Farming    
                        send_request(startFarm_url, headers=headers, payload = {"0":{"json": "null","meta":{"values":["undefined"]}}}, method='POST', proxy=proxy)
                    except:
                        send_request(startFarm_url, headers=headers, payload = {"0":{"json": "null","meta":{"values":["undefined"]}}}, method='POST', proxy=proxy)
                except Exception as e:
                    print(f"Error: {e}")
                print('-' * 50)
            print('=' * 50)

        except Exception as e:
            print(f"Error: {e}")

        run_once = False 

def run_main():
    main()
    print("Waiting for the next run...")
    

if __name__ == "__main__":
    # Run main immediately
    while True:
        run_main()
        #Claim after 4 hours
        time.sleep(15000)