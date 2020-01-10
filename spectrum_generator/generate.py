import spectrogen

YT_URL = 'https://www.youtube.com/watch?v=yAF9XlluONA'

if __name__ == '__main__':
    spectrogen.create_spectrogram_from_video(YT_URL, './generated')
