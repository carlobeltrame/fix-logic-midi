from mido import MidiFile, Message, MidiTrack, MetaMessage

def fix_zero_length_notes(mid, maxmsg=10):
    for t, track in enumerate(mid.tracks):
        out = []
        first_msg = True
        num = 0
        for i, msg in enumerate(track):
            num += 1
            if num > maxmsg and maxmsg > 0:
                break
            if isinstance(msg, MetaMessage):
                first_msg = True
                out.append(msg)
                continue
            if first_msg:
                first_msg = False
                out.append(msg)
                continue
            if not(msg.type == 'note_off' and msg.time == 0):
                out.append(msg)
                continue
            #print('-----')
            prev = out[-1]
            #print(prev)
            #print(msg)
            #print('swap')
            # swap times
            msg.time, prev.time = prev.time, msg.time
            # insert before previous
            out[-1] = msg
            out.append(prev)
            #print(msg)
            #print(prev)
        # replace fixed track
        mid.tracks[t] = MidiTrack(out)

def print_midi_file(mid, maxmsg=10):
    for track in mid.tracks:
        num = 0
        for msg in track:
            num += 1
            if num > maxmsg and maxmsg > 0:
                break
            print(msg)

mid = MidiFile('input.mid')
fix_zero_length_notes(mid, 0)
mid.save('output.mid')
