
import asyncio
import queue  # Use standard thread-safe queue
import threading
from concurrent.futures import ThreadPoolExecutor
from speech_transcription.main import transcribe_audio_object, record_audio, reset
from gpt.prompter import Prompter

import openai

with open('API_key.txt', 'r') as file:
    # Read the content and strip any whitespace/newline characters
    openai.api_key = file.readline().strip()

# Function to run the transcribe_batch in a loop

# Function to run the transcribe_batch in a loop
async def run_batch_transcription():
    with ThreadPoolExecutor() as executor:
        while True:
            result = await async_transcribe_batch(executor, {'batch_duration':10})
            print(f"Transcription result: {result}")
            await asyncio.sleep(10)  # Interval between batch transcriptions (e.g., 10 seconds)

async def async_transcribe_batch(executor, q, prompter):
    loop = asyncio.get_event_loop()
    
    while True:
        # Transcribe the audio clip in a separate thread
        transcript = await loop.run_in_executor(executor, transcribe_audio_object, q.get())
        print(f"Transcript: {transcript}")

        # Process the transcription with Prompter
        if transcript:
            highlight = prompter.append(transcript)  # Append the result to the prompter for further GPT interaction
            print(f"GPT Highlight: {highlight}")

        

def record_audio_wrapper(q, batch_len, sample_rate):
    while True:
        q.put(record_audio(batch_len, sample_rate))


async def handle_user_prompts(prompter):
    loop = asyncio.get_event_loop()

    while True:
        # read and reset user input
        print("checked for uin")
        user_input = ''
        with open('userin.txt', 'r') as stdin:
            content = stdin.read()  # Read the entire file content
        if content.strip():  # `.strip()` removes any leading/trailing whitespace or newlines
            user_input = content
            with open('userin.txt', 'w'):
                pass  # resets the file

        
            # then prompt the model.
            response = prompter.ask(user_input)
            print(f"User Input: {user_input}")
            print(f"GPT Response: {response}")

        # Add a small sleep to prevent constant, tight-loop polling
        await asyncio.sleep(1)

async def main():
    prompter = Prompter()
    q = queue.Queue()
    reset()
    batch_len = 10
    sample_rate = 16000

    # record. generate batch_len length clips. add audio to queue. 
    recording_thread = threading.Thread(target=record_audio_wrapper, args=(q,batch_len, sample_rate), daemon=True)
    recording_thread.start()
    # pool threads for concurrency
    with ThreadPoolExecutor() as executor:
        # Continuously transcribe batches of audio clips stored in queue.
        #await async_transcribe_batch(executor, q, prompter)
        
        await asyncio.gather(
            async_transcribe_batch(executor, q, prompter),  # Handle transcription
            handle_user_prompts(prompter)  # Handle user inputs
        )
        





# Run the main async loop
if __name__ == "__main__":
    asyncio.run(main())