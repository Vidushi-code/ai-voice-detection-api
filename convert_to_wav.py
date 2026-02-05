from pydub import AudioSegment
import os

folders = ["data/human", "data/ai"]

for folder in folders:
    for file in os.listdir(folder):
        if file.endswith(".mp3"):
            mp3_path = os.path.join(folder, file)
            wav_path = os.path.join(folder, file.replace(".mp3", ".wav"))

            audio = AudioSegment.from_mp3(mp3_path)
            audio = audio.set_frame_rate(16000).set_channels(1)
            audio.export(wav_path, format="wav")

            print("Converted:", file)
