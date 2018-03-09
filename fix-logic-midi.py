import mido

msg = mido.Message('note_on', note=60)
print(msg.note)
