# -*- coding: utf-8 -*-

import shutil
import time
from tkinter import Tk
from tkinter.filedialog import askdirectory

import speech_recognition as sr
from moviepy.editor import *
from pydub import AudioSegment
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from google_trans_new import google_translator

def cropAudio(total):
    translator = google_translator()
    r = sr.Recognizer()

    segundos = 0

    h = 0
    m = 0
    s = 0
    i = 0

    os.mkdir('./extract')
    repeticoes = total / 5

    print('Foram encontrados ', repeticoes, ' linhas de legenda!\n')

    corDaFonte = input(
        "Você quer a fonte branca ou amarela?\n1- Branco\n2- Amarelo\n")

    opt = int(input("Você quer traduzir o texto?\n1-Sim\n2-Não\n"))

    print('\n')
    while i <= repeticoes:
        i = i + 1
        print('Estamos na linha ', i)

        if s == 60:
            m = m + 1
            s = 0
        if m == 60:
            m = 0
            h = h + 1

        if segundos + 5 < total:
            segundoInicial = segundos * 1000
            segundoFinal = (segundos + 5) * 1000
        else:
            segundoInicial = segundos * 1000
            segundoFinal = total * 1000

        song = AudioSegment.from_wav('./download/audioparalegendar.wav')

        extract = song[segundoInicial:segundoFinal]

        extract.export('./extract/audioextract.wav', format="wav")

        try:
            with sr.AudioFile('./extract/audioextract.wav') as source:
                f = open("./data/subtitle.srt", "a")
                audio_data = r.record(source)

                traducao = r.recognize_google(audio_data)

                if opt == 1:
                    traducao = translator.translate(traducao, lang_tgt='pt')

                f.write(str(i) + '\n')
                inicio = time.strftime('%H:%M:%S',
                                       time.gmtime(segundoInicial / 1000))
                final = time.strftime('%H:%M:%S',
                                      time.gmtime(segundoFinal / 1000))
                f.write(inicio + ',000 --> ' + final + ',000\n')
                if corDaFonte == '1' or corDaFonte != '2':
                    f.write(traducao + '\n' + '\n')
                else:
                    f.write('<font color="#ffff54">' + traducao + '</font>' +
                            '\n' + '\n')
                f.close()

        except:
            os.remove('./extract/audioextract.wav')
            s = s + 5
            segundos = segundos + 5
            continue

        os.remove('./extract/audioextract.wav')

        s = s + 5
        segundos = segundos + 5

    shutil.rmtree('./extract')
    shutil.rmtree('./download')
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n')
    return print("Legenda criada com sucesso!\n")


def createAudio(video, segundos):
    os.mkdir('./download')
    os.mkdir('./data')
    os.rename(video.download(), './download/videoparalegendar.mp4')

    videoconversor = VideoFileClip('./download/videoparalegendar.mp4')
    audioconvertido = videoconversor.audio

    audioconvertido.write_audiofile('./download/audioparalegendar.wav')

    videoconversor.close()
    audioconvertido.close()

    os.system('cls' if os.name == 'nt' else 'clear')
    return cropAudio(segundos)


def getPath():
    root = Tk()
    path = askdirectory(title="Selecione a pasta")
    if os.path.exists(path):
        root.destroy()
        return path
    return getPath()


def getLink():
    link = input('Digite o link do vídeo: ')
    print('\n')
    try:
        yt = YouTube(link)
        print("Vídeo encontrado: ", yt.title)
        createAudio(yt.streams.get_lowest_resolution(), yt.length)
        print("Selecione onde deseja salvar a legenda e o vídeo")
        path = getPath()
        print("Aguarde enquanto fazemos o download do seu vídeo!")
        yt.streams.filter(
            progressive=True).get_highest_resolution().download(path)
        shutil.move("./data/subtitle.srt", path)
        shutil.rmtree('./data')

    except VideoUnavailable:
        print(" ")
        print('::: Este vídeo está privado! :::')
        getLink()


getLink()
