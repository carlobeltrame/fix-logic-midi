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
            prev = out[-1]
            # swap times saved on messages
            msg.time, prev.time = prev.time, msg.time
            # insert current before previous in list
            out[-1] = msg
            out.append(prev)
        # replace fixed track
        mid.tracks[t] = MidiTrack(out)

mid = MidiFile('input.mid')
fix_zero_length_notes(mid, 0)
mid.save('output.mid')
