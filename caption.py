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


from msclap import CLAP

def audio_caption(audio_file_path, resample=True, beam_size=5, entry_length=67, temperature=0.01):
    """
    Generate a caption for an audio file.

    Parameters:
    audio_file_path (str): The path to the audio file.
    resample (bool): Whether to resample the audio file. Default is True.
    beam_size (int): The beam size for beam search. Default is 5.
    entry_length (int): The maximum length of the caption. Default is 67.
    temperature (float): The temperature for sampling. Default is 0.01.

    Returns:
    str: The generated caption text for the audio file.
    """
    # Load the msclap model
    clap_model = CLAP(version='clapcap', use_cuda=False)

    # Generate caption
    captions = clap_model.generate_caption([audio_file_path], resample=resample, beam_size=beam_size, entry_length=entry_length, temperature=temperature)

    # If the return is a list, take the first element as the caption
    caption = captions[0] if isinstance(captions, list) else captions.get('caption', '')

    return caption
