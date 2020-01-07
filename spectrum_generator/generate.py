from pydub import AudioSegment
from scipy import signal
from scipy.fft import fftshift
import matplotlib.pyplot as plt
import numpy as np

FILENAME = 'fantano.wav'


def main():
    sound = AudioSegment.from_file(FILENAME)
    mono_sound = sound.split_to_mono()[0]

    samples = np.array(mono_sound.get_array_of_samples())
    freq = mono_sound.frame_rate

    print("Frequency: {0}".format(freq))

    # f, t, Sxx = signal.spectrogram(samples, fs=freq, nfft=pow(2, 18), scaling='spectrum', mode='magnitude')

    fig, ax = plt.subplots(1)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.axis('off')

    plt.specgram(samples, Fs=freq, pad_to=pow(2, 16), NFFT=pow(2, 10), noverlap=pow(2, 2))
    plt.yscale('log')
    plt.ylim((100, 21000))

    ax.axis('off')
    fig.set_size_inches(30, 12, forward=True)
    fig.savefig('spectrum.png', dpi=100, facecolor=None)





if __name__ == '__main__':
    main()
