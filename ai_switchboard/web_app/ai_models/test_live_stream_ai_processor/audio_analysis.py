from ..live_processing_interface.stream_processing_interface import StreamProcessor
import ffmpeg


def extract_audio(video):
    try:
        # Input stream
        input_stream = ffmpeg.input(video)

        # Output stream
        output_stream = ffmpeg.output(input_stream, 'pipe:', format='wav')

        # Run ffmpeg command and capture output
        out, _ = ffmpeg.run(output_stream, capture_stdout=True)

        print("Audio extracted successfully!")

        return out
    except ffmpeg.Error as e:
        print(f"Error extracting audio: {e}")
        return None


class audio_analyser(StreamProcessor):
    def run_model(self, video):
        # do some audio analysis using ffmpeg
        audio = extract_audio(video)

        return