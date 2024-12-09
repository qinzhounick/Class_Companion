import requests

url = "https://fastapi-service-940454193602.us-central1.run.app"
url = "http://127.0.0.1:8000"
#url = "http://127.0.0.1:8080"
#url = "https://fastapi-service-940454193602.us-central1.run.app"
print("test")
# Test /process_wav_data/
current_transcript = ""
with open("obama.wav", "rb") as f:
    bytestream = f.read()

# Make the POST request
response = requests.post(
    url + "/process_wav_data/",
    data=bytestream,  # Send raw bytes as the request body
    headers={
        "Content-Type": "application/octet-stream",
        "Condensed-Transcript": current_transcript  # Include the condensed transcript in a custom header
    }
)

print("/process_wav_data/ Response:", response.json())

# Test /process_wav_file/
with open("recording.wav", "rb") as f:
    files = {"file": f}
    headers = {"Condensed-Transcript": "This is the existing condensed transcript."}  # Include the condensed transcript as a header
    response = requests.post(url + "/process_wav_file/", files=files, headers=headers)
    print("/process_wav_file/ Response:", response.json())

# Test /question/
data = {"question": "What is the meaning of life?"}
headers = {"Condensed-Transcript": "This is the existing condensed transcript."}  # Include the condensed transcript as a header
response = requests.post(url + "/question/", data=data, headers=headers)
print("/question/ Response:", response.json())
