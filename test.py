import os 
import requests

if __name__ == "__main__":
    resp = requests.get('http://www.baidu.com')
    print(resp.text)