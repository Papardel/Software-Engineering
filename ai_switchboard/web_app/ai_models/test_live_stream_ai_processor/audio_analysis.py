from ..live_processing_interface.stream_processing_interface import stream_processor
import ffmpeg
from pydub import AudioSegment
import io


def extract_audio(video):
    return ffmpeg.input(video).audio.output('-', format='wav').overwrite_output().run(capture_stdout=True)


"""
According to chatGPT the average intensity of a scream is is 'anywhere from 90 to over 120 dB'. 
Also 'screams can have significant energy in both the low and high-frequency ranges, spanning 
from below 100 Hz to above 1000 Hz or even higher'
"""


def shout_scream_check(audio_stream):
    # Load audio stream into AudioSegment
    audio = AudioSegment.from_wav(io.BytesIO(audio_stream))

    # Find the loudest part of the audio in dB
    loudest_dB = audio.dBFS

    # Find the highest and lowest frequencies
    highest_freq = audio.max_freq
    lowest_freq = audio.min_freq

    return (highest_freq < 100) or (lowest_freq > 1000) or (loudest_dB > 90)


class audio_analyser(stream_processor):
    def run_model(self, video):
        # extract audio from .ts video file using ffmpeg
        audio = extract_audio(video)

        # process audio in some way
        return shout_scream_check(audio)
