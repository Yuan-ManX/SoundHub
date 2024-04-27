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
import os

def retrieve_audio(query_text, audio_folder, top_n=5):
    """
    Retrieves the top_n audio files most similar to the query text.

    Parameters:
    query_text (str): The query text to compare against.
    audio_folder (str): The path to the folder containing audio files.
    top_n (int): The number of top similar audio files to retrieve, default is 5.

    Returns:
    list: A list of the top_n most similar audio file names.
    """
    # Load the CLAP model
    clap_model = CLAP(version='2023', use_cuda=False)

    # Get a list of audio file paths
    audio_files = [os.path.join(audio_folder, f) for f in os.listdir(audio_folder) if f.endswith('.wav')]

    # Extract embeddings for the query text
    text_embeddings = clap_model.get_text_embeddings([query_text])

    # Initialize a list to store similarities
    similarities = []

    # Calculate similarity for each audio file
    for audio_file in audio_files:
        audio_embeddings = clap_model.get_audio_embeddings([audio_file])
        similarity = clap_model.compute_similarity(audio_embeddings, text_embeddings)
        similarities.append((audio_file, similarity))

    # Sort the audio files by similarity in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)

    # Get the top_n most similar audio files
    top_similar_audio_files = [audio_file for audio_file, _ in similarities[:top_n]]

    return top_similar_audio_files
