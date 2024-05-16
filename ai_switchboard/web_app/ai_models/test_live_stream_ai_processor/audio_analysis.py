from ..media_processing_interface.live_stream_processor import LiveStreamProcessor

from pydub import AudioSegment
import os
import subprocess


def extract_audio(video_path, audio_path):
    subprocess.run(['ffmpeg', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', audio_path], check=True)


"""
According to chatGPT the average intensity of a scream is is 'anywhere from 90 to over 120 dB'. 
Also 'screams can have significant energy in both the low and high-frequency ranges, spanning 
from below 100 Hz to above 1000 Hz or even higher'. 

After running some tests with silent videos, talking clapping and shouting, I found that
we should consider the following thresholds when declaring the detection of screams and shouts:
- The minimum frequency is below -20000 Hz
- The maximum frequency is above 20000 Hz
- The maximum loudness is above 20000 dB
"""


def shout_scream_check(audio_path):
    sound = AudioSegment.from_file(audio_path)

    # Calculate the maximum and minimum frequencies
    frequencies = sound.get_array_of_samples()
    max_frequency = max(frequencies)
    min_frequency = min(frequencies)

    # Calculate the maximum loudness
    max_loud = sound.max

    return (min_frequency < -20000) and (max_frequency > 20000) and (max_loud > 20000)


class AudioAnalyser(LiveStreamProcessor):
    def get_directory(self):
        return os.path.dirname(__file__)

    def run_model(self, media):
        # extract audio from video and save it to a temporary file
        temp_file = 'temp.wav'
        extract_audio(media, temp_file)
        save_audio = shout_scream_check(temp_file)
        os.remove(temp_file)
        print("Audio analysis complete. Scream detected:", save_audio)
        return save_audio
