import os
import datetime
import music21
import pygame
from typing import Dict
from ..core.state import MusicState

def midi_converter(state: MusicState) -> Dict:
    """Convert the composition to MIDI format and save it as a file."""
    piece = music21.stream.Score()
    
    piece.append(music21.meter.TimeSignature('4/4'))
    tempo = state.get('tempo', 90)
    piece.insert(0, music21.tempo.MetronomeMark(number=tempo))
    
    piece.append(state['melody'])
    piece.append(state['harmony'])
    
    midi_dir = "output/midi_files"
    if not os.path.exists(midi_dir):
        os.makedirs(midi_dir)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    midi_filename = os.path.join(midi_dir, f"composition_{timestamp}.mid")
    piece.write('midi', midi_filename)
    
    return {"midi_file": midi_filename}

def play_midi(midi_file_path: str) -> None:
    """Play the generated MIDI file."""
    midi_file_path = midi_file_path.replace("\\", "/")
    pygame.mixer.init()
    pygame.mixer.music.load(midi_file_path)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.quit() 