
# Multi-User Audio Transcriber using Google Cloud Speech-to-Text

This Python project provides real-time audio transcription for multiple users using the Google Cloud Speech-to-Text API. Each user can start and stop their own audio stream independently, and their speech will be transcribed in real-time.

## Table of Contents

- [Installation](#installation)
- [Google Cloud Setup](#google-cloud-setup)
- [Usage](#usage)
- [Use Case](#use-case)
- [License](#license)

## Installation

Before running this project, ensure you have the necessary dependencies installed. You can install them using the following command:

```bash
pip install pyaudio google-cloud-speech
```

Additionally, you will need the `PyAudio` package. You can install it using:

- For macOS:
  ```bash
  brew install portaudio
  pip install pyaudio
  ```
- For Linux:
  ```bash
  sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
  sudo apt-get install ffmpeg libav-tools
  pip install pyaudio
  ```
- For Windows:
  Download and install the appropriate version of `PyAudio` from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).

## Google Cloud Setup

To use Google Cloud Speech-to-Text, you must set up the Google Cloud SDK and download a credentials JSON file.

### Steps:

1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Speech-to-Text API** for the project.
3. Create a service account with the required roles.
4. Download the JSON credentials file for the service account.
5. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to the path of your credentials file.

For detailed instructions, visit the [Google Cloud Text-to-Speech Client Libraries](https://cloud.google.com/text-to-speech/docs/libraries#client-libraries-usage-python) page.

Example command for setting the environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="path_to_your_service_account_key.json"
```

## Usage

### Running the Program

To run the program, execute the following command in your terminal:

```bash
python multi_user_audio_transcriber.py
```

### Adding and Removing Users

1. **Add a new user**:
   In the code, use `add_user(user_id)` to start transcription for a new user. For example:

   ```python
   transcriber.add_user("user_1")  # Starts audio capture and transcription for user 1
   ```

2. **Remove a user**:
   To stop transcription for a specific user and close their stream:

   ```python
   transcriber.remove_user("user_1")
   ```

### Stopping the Transcriber

The transcriber can be stopped by pressing `Ctrl+C` in the terminal. This will terminate the audio stream for all users.

## Use Case

This project can be used in various real-time voice transcription scenarios, such as:

- **Call Centers**: Multiple agents are speaking with customers simultaneously. Each agent’s speech can be captured and transcribed in real-time for quality control, analysis, or record-keeping.
  
- **Multi-user Voice Meetings**: A meeting where multiple users’ speech is being transcribed at the same time, making it easy to generate meeting notes for multiple participants.

- **Speech Therapy Sessions**: Therapists can track what each participant is saying in a multi-user session for better feedback and analysis.

### Example Use Case Flow:

1. An admin adds participants to a session:
   ```python
   transcriber.add_user("agent_1")
   transcriber.add_user("agent_2")
   ```

2. Both users are now speaking, and the transcription for each user is recorded and available for later analysis.

3. After the session ends, the admin can stop the streams for both users:
   ```python
   transcriber.remove_user("agent_1")
   transcriber.remove_user("agent_2")
   ```

4. The system automatically stops listening and closes all active sessions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
