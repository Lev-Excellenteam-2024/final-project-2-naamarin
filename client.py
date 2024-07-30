import requests
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Status:
    status: str
    filename: str
    timestamp: datetime
    explanation: str

    def is_done(self) -> bool:
        return self.status == 'done'

    def __str__(self) -> str:
        return f"Status: {self.status}, Filename: {self.filename}, Timestamp: {self.timestamp}, Explanation: {self.explanation}"


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def upload(self, file_path: str) -> str:
        with open(file_path, 'rb') as file:
            response = requests.post(f"{self.base_url}/upload", files={'file': file})

        if response.status_code == 200:
            data = response.json()
            return data.get('uid')
        else:
            response.raise_for_status()

    def status(self, uid: str) -> Status:
        response = requests.get(f"{self.base_url}/status", params={'UID': uid})

        if response.status_code == 200:
            data = response.json()
            return Status(
                status=data['status'],
                filename=data['filename'],
                timestamp=datetime.fromtimestamp(float(data['timestamp'])),
                explanation=data['explanation']
            )
        else:
            response.raise_for_status()


# Example usage
if __name__ == "__main__":
    client = Client(base_url="http://127.0.0.1:5000")

    try:
        while True:
            choise = input("Press 1 to upload file, 2 to check status and 3 for quit: ")
            if choise == '1':
                file_path = input("Enter a file path:\n")
                print( "The unique identifier is: " + client.upload(file_path))

            elif choise == '2':
                uid = input("Enter the unique identifier:\n")
                status = client.status(uid)
                print(status)
            else:
                break

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
