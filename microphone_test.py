import time

import matplotlib.pyplot as plt
import numpy as np
import pyaudio

# AUDIO INPUT
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "output.wav"

audio = pyaudio.PyAudio()
audio_data = []


def callback(input_data, frame_count, time_info, flags):
    signal = np.frombuffer(input_data, dtype=np.int16)
    audio_data.append(signal)  # Pass audio data to the queue
    return input_data, pyaudio.paContinue


stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    stream_callback=callback,
    frames_per_buffer=CHUNK,
)

# Start the stream
stream.start_stream()

start = time.time()
print(type(start))

# Main thread processes data and creates plots
all_data = []
while (time.time() - start) < RECORD_SECONDS:
    while len(audio_data):
        signal = audio_data.pop(0)
        all_data.append(signal)

stream.stop_stream()
stream.close()
audio.terminate()

# Combine all audio chunks for visualization
if all_data:
    full_signal = np.concatenate(all_data)

    # Plot the waveform
    plt.figure(figsize=(10, 4))
    plt.plot(full_signal)
    plt.title("Audio Waveform")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")

    # Save the figure
    plt.savefig("audio_waveform.png", dpi=300)
    plt.close()

print("Waveform saved as audio_waveform.png")
