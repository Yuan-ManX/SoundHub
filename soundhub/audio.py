# MIT License

# Copyright (c) 2024 Yuan-Man

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from pydub import AudioSegment

def trim(audio_path, output_path, trim_length=None, start_time=0, end_time=None):
    """
    Trim an audio file to a specified length or between specified start and end times.

    Parameters:
    - audio_path (str): The path to the audio file to be trimmed.
    - output_path (str): The path where the trimmed audio file will be saved.
    - trim_length (int, optional): The length in milliseconds to trim the audio. If specified, overrides start_time and end_time.
    - start_time (int, optional): The start time in milliseconds from where to start trimming. Default is 0.
    - end_time (int, optional): The end time in milliseconds where to end trimming. If not specified, it will be calculated based on trim_length or the duration of the audio.

    Returns:
    - None: The trimmed audio is saved to the specified output path.
    """
    audio = AudioSegment.from_file(audio_path)
    
    # If trim_length is specified, use it to calculate end_time
    if trim_length is not None:
        end_time = start_time + trim_length
    
    # If end_time is not specified, use the duration of the audio
    if end_time is None:
        end_time = len(audio)
    
    # Ensure end_time does not exceed the duration of the audio
    end_time = min(end_time, len(audio))
    
    # Trim the audio and export it to the specified output path
    trimmed_audio = audio[start_time:end_time]
    trimmed_audio.export(output_path, format="wav")


def concat(audio_paths, output_path):
    """
    Concatenate multiple audio files into a single audio file.

    Parameters:
    - audio_paths (list of str): A list of paths to the audio files to be concatenated.
    - output_path (str): The path where the concatenated audio file will be saved.

    Returns:
    - None: The concatenated audio is saved to the specified output path.
    """
    # Load each audio file into an AudioSegment object
    audio_segments = [AudioSegment.from_file(path) for path in audio_paths]
    
    # Concatenate all audio segments into a single AudioSegment object
    concatenated_audio = sum(audio_segments)
    
    # Export the concatenated audio to the specified output path
    concatenated_audio.export(output_path, format="wav")


def fade(audio_path, output_path, fade_in_duration=0, fade_out_duration=0):
    """
    Add fade-in and fade-out effects to an audio file.

    Parameters:
    - audio_path (str): The path to the audio file to which the fade effects will be added.
    - output_path (str): The path where the audio file with fade effects will be saved.
    - fade_in_duration (int, optional): The duration of the fade-in effect in milliseconds. Default is 0.
    - fade_out_duration (int, optional): The duration of the fade-out effect in milliseconds. Default is 0.

    Returns:
    - None: The audio file with fade effects is saved to the specified output path.
    """
    # Load the audio file into an AudioSegment object
    audio = AudioSegment.from_file(audio_path)
    
    # Apply fade-in effect if fade_in_duration is greater than 0
    if fade_in_duration > 0:
        audio = audio.fade_in(fade_in_duration)
    
    # Apply fade-out effect if fade_out_duration is greater than 0
    if fade_out_duration > 0:
        audio = audio.fade_out(fade_out_duration)
    
    # Export the audio with fade effects to the specified output path
    audio.export(output_path, format="wav")


def metadata(audio_path):
    """
    Retrieve metadata from an audio file.

    Parameters:
    - audio_path (str): The path to the audio file from which metadata will be retrieved.

    Returns:
    - frame_rate (int): The sample rate of the audio in frames per second.
    - channels (int): The number of audio channels (e.g., 1 for mono, 2 for stereo).
    - duration_seconds (float): The duration of the audio in seconds.
    - bit_depth (int): The bit depth of the audio, if available.

    Raises:
    - FileNotFoundError: If the audio file does not exist at the specified path.
    - Exception: If an error occurs while reading the audio file.
    """
    try:
        # Load the audio file into an AudioSegment object
        audio = AudioSegment.from_file(audio_path)
        
        # Extract metadata
        frame_rate = audio.frame_rate
        channels = audio.channels
        duration_seconds = audio.duration_seconds
        bit_depth = audio.sample_width * 8 
        
        # Return the metadata
        return frame_rate, channels, duration_seconds, bit_depth
    except FileNotFoundError:
        raise FileNotFoundError(f"The audio file at {audio_path} does not exist.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the audio file: {e}")


def rms(audio_path):
    """
    Calculate and return the Root Mean Square (RMS) value of an audio file.

    Parameters:
    - audio_path (str): The path to the audio file from which the RMS value will be calculated.

    Returns:
    - rms_value (float): The RMS value of the audio file in decibels (dBFS).

    Raises:
    - FileNotFoundError: If the audio file does not exist at the specified path.
    - Exception: If an error occurs while reading the audio file or calculating the RMS value.
    """
    try:
        # Load the audio file into an AudioSegment object
        audio = AudioSegment.from_file(audio_path)
        
        # Calculate the RMS value of the audio file
        rms_value = audio.dBFS
        
        # Return the RMS value
        return rms_value
    except FileNotFoundError:
        raise FileNotFoundError(f"The audio file at {audio_path} does not exist.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the audio file or calculating the RMS value: {e}")


def mix(audio_paths, output_path, volume=1.0):
    """
    Mix multiple audio files into a single audio file with optional volume control.

    Parameters:
    - audio_paths (list of str): A list of paths to the audio files to be mixed.
    - output_path (str): The path where the mixed audio file will be saved.
    - volume (float, optional): The volume level for the mixed audio, ranging from 0.0 (mute) to 1.0 (original volume). Default is 1.0 (no change).

    Returns:
    - None: The mixed audio is saved to the specified output path.

    Raises:
    - FileNotFoundError: If any of the audio files do not exist at the specified paths.
    - Exception: If an error occurs while reading the audio files or mixing them.
    """
    try:
        # Load each audio file into an AudioSegment object
        audio_segments = [AudioSegment.from_file(path) for path in audio_paths]
        
        # Adjust the volume of each audio segment if volume is specified
        if volume != 1.0:
            audio_segments = [segment.set_volume(volume) for segment in audio_segments]
        
        # Mix all audio segments into a single AudioSegment object
        mixed_audio = sum(audio_segments)
        
        # Export the mixed audio to the specified output path
        mixed_audio.export(output_path, format="wav")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"One or more audio files do not exist at the specified paths: {e}")
    except Exception as e:
        raise Exception(f"An error occurred while reading the audio files or mixing them: {e}")


def mix_two(audio_path1, audio_path2, output_path, volume=1.0):
    """
    Mix two audio files into a single audio file with optional volume control.

    Parameters:
    - audio_path1 (str): The path to the first audio file to be mixed.
    - audio_path2 (str): The path to the second audio file to be mixed.
    - output_path (str): The path where the mixed audio file will be saved.
    - volume (float, optional): The volume level for the mixed audio, ranging from 0.0 (mute) to 1.0 (original volume). Default is 1.0 (no change).

    Returns:
    - None: The mixed audio is saved to the specified output path.

    Raises:
    - FileNotFoundError: If any of the audio files do not exist at the specified paths.
    - Exception: If an error occurs while reading the audio files or mixing them.
    """
    try:
        # Load each audio file into an AudioSegment object
        audio_segment1 = AudioSegment.from_file(audio_path1)
        audio_segment2 = AudioSegment.from_file(audio_path2)
        
        # Adjust the volume of each audio segment if volume is specified
        if volume != 1.0:
            audio_segment1 = audio_segment1.set_volume(volume)
            audio_segment2 = audio_segment2.set_volume(volume)
        
        # Mix the two audio segments into a single AudioSegment object
        mixed_audio = audio_segment1 + audio_segment2
        
        # Export the mixed audio to the specified output path
        mixed_audio.export(output_path, format="wav")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"One or more audio files do not exist at the specified paths: {e}")
    except Exception as e:
        raise Exception(f"An error occurred while reading the audio files or mixing them: {e}")


def convert_mp3_to_wav(mp3_path, wav_output_path):
    """
    Convert an MP3 audio file to WAV format.

    Parameters:
    - mp3_path (str): The path to the MP3 audio file to be converted.
    - wav_output_path (str): The path where the converted WAV audio file will be saved.

    Returns:
    - None: The MP3 audio file is converted to WAV format and saved to the specified output path.

    Raises:
    - FileNotFoundError: If the MP3 file does not exist at the specified path.
    - Exception: If an error occurs while reading the MP3 file or converting it to WAV.
    """
    try:
        # Load the MP3 audio file into an AudioSegment object
        audio_segment = AudioSegment.from_file(mp3_path)
        
        # Export the audio segment to WAV format
        audio_segment.export(wav_output_path, format="wav")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The MP3 file at {mp3_path} does not exist: {e}")
    except Exception as e:
        raise Exception(f"An error occurred while converting the MP3 file to WAV: {e}")

