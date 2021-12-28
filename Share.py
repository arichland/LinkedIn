_author_ = 'arichland'

import requests
import SelectContent
import Credentials

class ShareContent:
    def __init__(self):
        self.token = Credentials.token
        self.url = 'https://api.linkedin.com/v2/'
        self.urn = Credentials.member_id
        self.content = SelectContent.main()

    def share(self):
        content = self.content
        title = content[0][0]
        link = content[0][1]
        descr = content[0][2]
        author = f"urn:li:person:{self.urn}"
        headers = {'X-Restli-Protocol-Version': '2.0.0',
                   'Content-Type': 'application/json',
                   'Authorization': f'Bearer {self.token}'}
        api_url = f'{self.url}shares'
        post_data = {
            "content": {
                "contentEntities": [
                    {
                        "entityLocation": link,
                        "thumbnails": [
                            {
                                "resolvedUrl": ""
                            }
                        ]
                    }
                ],
                "title": descr
            },
            "distribution": {
                "linkedInDistributionTarget": {}
            },
            "owner": author,
            "subject": title,
            "text": {
                "text": title
            }
        }
        response = requests.post(api_url, headers=headers, json=post_data)
        if response.status_code == 201:
            print("Success")
            print(response.content)
        else:
            print(response.content)
            print(api_url)


def main():
    go = ShareContent()
    go.share()

if __name__ == "__main__":
    main()