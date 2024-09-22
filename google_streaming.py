import os
import pyaudio
import time
import threading
from google.cloud import speech_v1 as speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/sushilkumarbarai/workspace/stream_bot/gtts.json"

class UserAudioStream:
    def __init__(self, user_id, rate=8000, chunk=1024):
        self.user_id = user_id
        self.rate = rate
        self.chunk = chunk
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)
        self.running = False
        self.thread = None
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.rate,
            language_code="en-US",
            max_alternatives=1
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config, interim_results=True
        )
        self.transcriptions = []
        self.chunk_counter = 0  # Counter for the number of chunks passed for transcription

    def start(self):
        """Start capturing audio and transcription for a specific user."""
        print(f"User {self.user_id} microphone listening...")
        self.running = True
        self.thread = threading.Thread(target=self._capture)
        self.thread.start()

    def stop(self):
        """Stop capturing audio for the specific user."""
        self.running = False
        self.thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        print(f"User {self.user_id} microphone not listening")

    def _capture(self):
        """Capture audio from the microphone and process it for a specific user."""
        audio_stream = self._generate_audio_stream()
        self.transcribe_stream_data(audio_stream)

    def _generate_audio_stream(self):
        """Generate audio chunks from the microphone."""
        while self.running:
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            self.chunk_counter += 1  # Increment chunk counter
            yield data

    def transcribe_stream_data(self, audio_stream):
        """Transcribe the audio stream data using Google Cloud Speech-to-Text API."""
        requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in audio_stream)
        responses = self.client.streaming_recognize(self.streaming_config, requests)

        for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            if result.is_final:
                # Capture the start time just before the transcription is printed (i.e., the transcription process)
                start_time = time.time()

                # Transcription finalized, print the result
                print(f"User {self.user_id} Transcribed Text: {transcript}")

                # Calculate the transcription time
                end_time = time.time()
                transcription_time = end_time - start_time
                print(f"User {self.user_id} Transcription took {transcription_time} seconds.")

                self.transcriptions.append(transcript)

                # Calculate microphone listening time and reset chunk counter
                listening_time_minutes = self.chunk_counter * 0.128
                print(f"User {self.user_id} total number of chunks: {self.chunk_counter} (microphone listened for {listening_time_minutes:.2f} minutes)")

                # Reset chunk counter for the next transcription
                self.chunk_counter = 0


class MultiUserAudioTranscriber:
    def __init__(self):
        self.user_streams = {}

    def add_user(self, user_id):
        """Add a new user and start their audio stream."""
        if user_id in self.user_streams:
            print(f"User {user_id} is already active.")
        else:
            user_stream = UserAudioStream(user_id)
            self.user_streams[user_id] = user_stream
            user_stream.start()

    def remove_user(self, user_id):
        """Stop and remove a user's audio stream."""
        if user_id in self.user_streams:
            self.user_streams[user_id].stop()
            del self.user_streams[user_id]
            print(f"User {user_id} has been removed.")
        else:
            print(f"User {user_id} not found.")

    def list_active_users(self):
        """List all active users."""
        active_users = list(self.user_streams.keys())
        if active_users:
            print(f"Active users: {', '.join(active_users)}")
        else:
            print("No active users.")


if __name__ == "__main__":
    transcriber = MultiUserAudioTranscriber()

    # Example usage:
    transcriber.add_user("user_1")  # Start audio capture for user 1
  #  transcriber.add_user("user_2")  # Start audio capture for user 2

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive for users
    except KeyboardInterrupt:
        print("Stopping...")
        transcriber.remove_user("user_1")
     #   transcriber.remove_user("user_2")
