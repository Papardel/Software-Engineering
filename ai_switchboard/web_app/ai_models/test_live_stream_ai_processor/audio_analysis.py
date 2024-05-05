from ..live_processing_interface.stream_processing_interface import stream_processor

import moviepy.editor as mp
from pydub import AudioSegment
import os
import subprocess


def extract_audio(video_path, audio_path):
    subprocess.run(['ffmpeg', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', audio_path], check=True)
"""
According to chatGPT the average intensity of a scream is is 'anywhere from 90 to over 120 dB'. 
Also 'screams can have significant energy in both the low and high-frequency ranges, spanning 
from below 100 Hz to above 1000 Hz or even higher'
"""


def shout_scream_check(audio_path):
    sound = AudioSegment.from_file(audio_path)

    # Calculate the maximum and minimum frequencies
    frequencies = sound.get_array_of_samples()
    max_frequency = max(frequencies)
    min_frequency = min(frequencies)

    # Calculate the maximum loudness
    max_loud = sound.max_dBFS

    return (min_frequency < 100) or (max_frequency > 1000) or (max_loud > 90)


class audio_analyser(stream_processor):
    def run_model(self, video):
        # extract audio from video and save it to a temporary file
        temp_file = 'temp.wav'
        extract_audio(video, temp_file)
        save_audio = shout_scream_check(temp_file)
        os.remove(temp_file)
        print("Audio analysis complete. Scream detected:", save_audio)
        return save_audio
