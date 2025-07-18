import os
import requests
from rich import print

EVENT_INFORMATION = "https://pretalx.com/api/events/"
SPEAKER_INFORMATION = "https://pretalx.com/api/events/{event}/speaker-information/"

class PretalxClient:
    """ A simple client for interacting with Pretalx REST API """
    def __init__(self, base_url=None, default_headers=None, timeout=10):
        token = os.getenv('PRETALX_API_TOKEN')
        if not token:
            raise ValueError("Please provide an environment Variable named 'PRETALX_API_TOKEN'")
        else:
            self.token = token
        
        self.session = requests.Session()

        self.base_url = base_url.rstrip('/') if base_url else None
        self.timeout = timeout

        self.default_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Python PretalxClient/1.0'
        }

        if default_headers:
            self.default_headers.update(default_headers)

        self.session.headers.update(self.default_headers)
        
    
    def auth(self):
        """ Add Authentication parameters to the Pretalx Client Request """
        self.session.headers.update({"Authorization": f"Token {self.token}"})

    def _build_url(self, endpoint: str) ->str:
        url = f"{self.base_url}/{endpoint.lstrip('/')}" if self.base_url else endpoint
        return url

    def get_events(self, event_name: str):
        """ Get a list of events by name search """
        url = self._build_url("/events")
        query = {
                # "q": event_name
                # "is_public": True
        }
        resp = self.session.get(url, params=query)
        print(resp)
        return resp.text

    def get_event(self, event_slug: str):
        url = self._build_url(f"/events/{event_slug}")
        resp = self.session.get(url)
        print(resp)
        return resp.json()

    def get_speaker_information(self, event_slug: str):
        url = self._build_url(f"/events/{event_slug}/speakers")
        print(self.session.headers)
        resp = self.session.get(url)
        print(resp)
        return resp.text
    


def main():
    print("Hello from pretalx-api!")
    client = PretalxClient(base_url="https://pretalx.org/api")
    client.auth()
    # print(client.get_events("")[0])
    # print(client.get_event("open-source-experience-2025"))
    print(client.get_speaker_information("mayatest1-2025"))


if __name__ == "__main__":
    main()
