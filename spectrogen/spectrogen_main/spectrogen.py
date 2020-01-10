from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
import youtube_dl as ydl
import os


def replace_extension(filename: str, new_ext: str) -> str:
    return filename[:filename.rindex('.')] + '.' + new_ext


def download_audio(url: str, output_dir: str) -> str:
    """Downloads audio from YouTube"""
    ydl_options = {
        'format': 'bestaudio',
        'outtmpl': output_dir + '/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }

    with ydl.YoutubeDL(ydl_options) as downloader:
        video_info = downloader.extract_info(url, download=True)
        filename = downloader.prepare_filename(video_info)

        return replace_extension(filename, 'mp3')


def extract_raw_audio(input_filename: str, start: int = 0, end: int = -1):
    """Extracts raw audio from MP3 file"""
    audio = AudioSegment.from_mp3(input_filename)
    first_channel = audio.split_to_mono()[0]

    final_audio = None

    if end > 0:
        final_audio = first_channel[start:end]
    else:
        final_audio = first_channel[start:]

    samples = np.array(final_audio.get_array_of_samples())
    frequency = final_audio.frame_rate

    return (samples, frequency)


def generate_spectrogram(data, frequency: int, output_filename: str) -> None:
    """Generated spectrogram from raw data"""
    figure, axis = plt.subplots(1)

    figure.subplots_adjust(left=0, right=1, bottom=0, top=1)
    axis.axis('off')

    plt.specgram(data, Fs=frequency, pad_to=pow(2, 16),
                 NFFT=pow(2, 10), noverlap=pow(2, 2))
    plt.yscale('log')
    plt.ylim((100, 20000))

    axis.axis('off')
    figure.set_size_inches(15, 8, forward=True)
    figure.savefig(output_filename, dpi=100, facecolor=None, transparent=True)


def create_spectrogram_from_video(url: str, output_dir: str, start: int = 0, end: int = -1,
                                  temp_cache_dir: str = './tempcache') -> str:
    """Creates spectrogram from YouTube video and returns it's filename"""
    audio_file = download_audio(url, temp_cache_dir)

    raw_audio, audio_frequency = extract_raw_audio(audio_file, start, end)

    spectrogram_file = output_dir + '/' + os.path.basename(replace_extension(audio_file, 'png'))

    if not os.path.exists(os.path.dirname(spectrogram_file)):
        os.mkdir(os.path.dirname(spectrogram_file))

    generate_spectrogram(raw_audio, audio_frequency, spectrogram_file)

    os.remove(audio_file)

    return spectrogram_file
