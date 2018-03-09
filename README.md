# fix-logic-midi

When hand-writing MIDI in a DAW, quantization often leads to some notes starting at the exact same point in time a previous note stops. If the pitches and channels of the two touching notes are the same (e.g. a C held until the end of the bar and another C starting exactly on the start of the next bar), this can lead to problems when the MIDI data is exported and re-imported in different programs (such as exporting from Logic Pro and importing in REAPER). In the MIDI file, the concurrent note_on and note_off events can be in any order, and are marked as concurrent by a time difference of zero. However, if the note_on event of the next note is stored before the note_off event of the previous note, some programs interpret this as a zero-length note when imporing the file, causing very short or even omitted notes.

### Example

The note_off event in the third line cuts off both note_on events in some programs. (Note that note_off events can have an individual velocity in MIDI, but this is often set to the default value of 64).
```
note_on channel=0 note=61 velocity=97 time=120
note_on channel=0 note=61 velocity=97 time=600
note_off channel=0 note=61 velocity=64 time=0
note_off channel=0 note=61 velocity=64 time=1200
```

This script aims to correct such MIDI files, such that in groups of concurrent messages, note_off events are always listed first.

The script corrects this sequence without changing the musical meaning. Both notes will be correctly imported in all DAWs.
```
note_on channel=0 note=61 velocity=97 time=120
note_off channel=0 note=61 velocity=64 time=600
note_on channel=0 note=61 velocity=97 time=0
note_off channel=0 note=61 velocity=64 time=1200
```

### Usage

Download the repo and go into the folder:
```bash
git clone https://github.com/carlobeltrame/fix-logic-midi.git
cd fix-logic-midi
```

Copy your MIDI file into the same folder:
```
cp <path/to/my-input.mid> .
```

Then, if you have Python3 and mido installed, run
```bash
python3 fix-logic-midi.py <my-input.mid>
```

Otherwise, if you have Docker and docker-compose installed, run
```bash
INPUT=<my-input.mid> docker-compose up
```
