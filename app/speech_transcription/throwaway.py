import sounddevice as sd
import numpy as np

def list_devices():
    print("Available audio devices:")
    devices = sd.query_devices()
    valid_input_devices = []
    for idx, device in enumerate(devices):
        input_channels = device['max_input_channels']
        if input_channels > 0:
            print(f"{idx}: {device['name']} - {input_channels} input channels")
            valid_input_devices.append(idx)
    return valid_input_devices

def test_record(duration, samplerate, device=None):
    try:
        if device is not None:
            print(f"Using device index: {device}")
        else:
            print("Using default input device.")
        print(f"Recording for {duration} seconds...")
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32', device=device)
        sd.wait()
        print("Recording finished.")
        return audio_data
    except Exception as e:
        print(f"An error occurred during recording: {e}")
        return None

if __name__ == "__main__":
    valid_devices = list_devices()
    if not valid_devices:
        print("No valid input devices found.")
    else:
        device_index = input("Enter the device index to use for recording (or press Enter to use default): ")
        if device_index.strip() == "":
            device_index = None
        else:
            try:
                device_index = int(device_index)
                if device_index not in valid_devices:
                    print("Invalid device index selected.")
                    device_index = None
            except ValueError:
                print("Invalid input. Using default device.")
                device_index = None

        audio = test_record(5, 16000, device=device_index)
        if audio is not None:
            print("Recording was successful.")
        else:
            print("Recording failed.")
