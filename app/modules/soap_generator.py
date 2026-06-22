from modules.transcriber import transcribe_audio

text = transcribe_audio("data/sample.wav")

print("\nTranscript:\n")
print(text)