from typing import TypedDict

class MusicState(TypedDict):
    """Define the structure of the state for the music generation workflow."""
    musician_input: str
    melody: str
    harmony: str
    rhythm: str
    style: str
    composition: str
    midi_file: str
    duration: int    # Optional, defaults to 16 beats
    tempo: int       # Optional, defaults to 90 BPM