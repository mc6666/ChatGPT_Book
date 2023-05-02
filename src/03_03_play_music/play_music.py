from midiutil.MidiFile import MIDIFile

# Create the MIDIFile Object
MyMIDI = MIDIFile(1)

# Tracks are numbered from zero. Times are measured in beats.
track = 0
time = 0

# Add track name and tempo.
MyMIDI.addTrackName(track, time, "Sample Track")
MyMIDI.addTempo(track, time, 120)

# C major scale
scale = [60, 62, 64, 65, 67, 69, 71, 72]

# Add a note. addNote expects the following information:
track = 0
channel = 0
pitch = scale[0]
time = 0
duration = 1
volume = 100

# Then add the scale notes
for i, pitch in enumerate(scale):
    MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

# Write the MIDI file to disk
with open("sample.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
