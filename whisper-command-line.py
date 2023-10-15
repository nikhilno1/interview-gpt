import openai
import os
import pyaudio
import wave
import threading
import sys
import queue

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")
openai.api_key = os.getenv("OPENAI_API_KEY", "")

# Record audio
def record_audio(filename, stop_event, audio_queue):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording... Press return key to stop.")

    while not stop_event.is_set():
        data = stream.read(CHUNK)
        audio_queue.put(data)

    print("Finished recording")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(list(audio_queue.queue)))

# Transcribe audio
def transcribe_audio(filename):
    with open(filename, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]

# Main function
def main():
    audio_filename = "recorded_audio.wav"
    stop_event = threading.Event()
    audio_queue = queue.Queue()

    record_thread = threading.Thread(target=record_audio, args=(audio_filename, stop_event, audio_queue))
    record_thread.start()

    input("Press the return key to stop recording...\n")
    stop_event.set()
    record_thread.join()

    transcription = transcribe_audio(audio_filename)
    print("Transcription:", transcription)

if __name__ == "__main__":
    main()