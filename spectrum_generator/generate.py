from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
import youtube_dl

import spectrogen

FILENAME = 'fantano.wav'
YT_URL = 'https://www.youtube.com/watch?v=yAF9XlluONA'

def finish_hook(data):
    global FILENAME
    if data['status'] == 'finished':
        print('Downloaded video {0}'.format(data['filename']))
        FILENAME = data['filename'][:data['filename'].rindex('.')] + '.mp3'


def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320'
        }],
        'progress_hooks': [finish_hook]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main():
    download_audio(YT_URL)

    sound = AudioSegment.from_file(FILENAME)
    mono_sound = sound.split_to_mono()[0]

    samples = np.array(mono_sound.get_array_of_samples())
    freq = mono_sound.frame_rate

    print("Frequency: {0}".format(freq))

    fig, ax = plt.subplots(1)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.axis('off')

    plt.specgram(samples, Fs=freq, pad_to=pow(2, 16),
                 NFFT=pow(2, 10), noverlap=pow(2, 2))
    plt.yscale('log')
    plt.ylim((100, 21000))

    ax.axis('off')
    fig.set_size_inches(30, 12, forward=True)
    fig.savefig('spectrum.png', dpi=100, facecolor=None, transparent=True)


if __name__ == '__main__':
    # main()
    print('Filename: {0}'.format(spectrogen.download_audio(YT_URL)))
