from midiutil import MIDIFile

def create_midi_from_data(track_data, tempo, output_file):
    midi = MIDIFile(numTracks=len(track_data), ticks_per_quarternote=480)
    for i, (notes, total_duration) in enumerate(track_data):
        track = i
        time = 0
        channel = i  # Assigning each track to a different channel
        midi.addTrackName(track, time, f"Track {i+1}")
        midi.addTempo(track, time, tempo)
        for pitch_set, dur in notes:
            for pitch in pitch_set:
                midi.addNote(track, channel, pitch, time, dur, 100)
                time += int(dur * midi.ticks_per_quarternote)
        time = total_duration * midi.ticks_per_quarternote

    with open(output_file, "wb") as f:
        midi.writeFile(f)

def generate_chords(chord_sequence, duration):
    chords = []
    for chord in chord_sequence:
        chords.append((chord, duration))
    return chords

def scale_notes(notes):
    e_minor_scale = [64, 66, 67, 69, 71, 72, 74, 76]
    scaled_notes = []
    for note in notes:
        scaled_note = note % 12
        if scaled_note not in e_minor_scale:
            closest_note = min(e_minor_scale, key=lambda x: abs(x - scaled_note))
            scaled_notes.append(note - scaled_note + closest_note)
        else:
            scaled_notes.append(note)
    return scaled_notes

def get_chord_progression(key):
    chord_progression = {
        'I': scale_notes([64, 67, 71]),   # E minor chord
        'V': scale_notes([71, 74, 79]),   # B major chord
        'vi': scale_notes([69, 72, 76]),  # C major chord
        'IV': scale_notes([64, 67, 71])   # A minor chord
    }
    return chord_progression[key]

def generate_dubstep_song(tempo=140, output_file="dubstep_song.mid"):
    chord_progression = [
        generate_chords(get_chord_progression('I'), 4),
        generate_chords(get_chord_progression('V'), 4),
        generate_chords(get_chord_progression('vi'), 4),
        generate_chords(get_chord_progression('IV'), 4)
    ]
    
    chords_track = [(note, duration) for chord in chord_progression for note, duration in chord]
    melody_track = [
        (scale_notes([64, 67, 71]), 0.25),
        (scale_notes([66, 69, 72]), 0.25),
        (scale_notes([67, 71, 74]), 0.25),
        (scale_notes([69, 72, 76]), 0.25),
        (scale_notes([71, 74, 79]), 0.5),
        (scale_notes([69, 72, 76]), 0.25),
        (scale_notes([67, 71, 74]), 0.25),
        (scale_notes([66, 69, 72]), 0.25),
    ]
    bass_track = [(note, duration) for note, duration in chords_track]  # Corrected line
    
    full_song = [
        (melody_track, 4),
        (chords_track, 4),
        (bass_track, 4)
    ]
    
    create_midi_from_data(full_song, tempo=tempo, output_file=output_file)

generate_dubstep_song()
