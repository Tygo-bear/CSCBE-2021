import wave
import numpy

# Read file to get buffer
ifile = wave.open('StrangeSounds.wav')
samples = ifile.getnframes()
audio = ifile.readframes(samples)

# Convert buffer to float32 using NumPy
audio_as_np_int16 = numpy.frombuffer(audio, dtype=numpy.int16)
audio_as_np_float32 = audio_as_np_int16.astype(numpy.float32)

print("file opend")
max = 0
length = 0
spacing = []
for sound in audio_as_np_int16:
    max += 1
    if max > 1000000 and False:
        break
    if -1000 < sound < 1000:
        spacing.append(length)
        length = 0
    length += 1

print(spacing)
code = []
i = 0
for spaces in spacing:
    if spaces < 50:
        i += 1
    else:
        code.append(i)
        i = 0

print(code)
buffer = bytearray()
bytestring = ""
i = 0
for co in code:
    if co > 12:
        bytestring += "1"
    else:
        bytestring += "0"

    i += 1
    if i >= 8:
        buffer.append(int(bytestring, 2))
        print(bytestring)
        bytestring = ""
        i = 0

print(buffer)
with open("test.png", 'bw') as f:
    f.write(buffer)




