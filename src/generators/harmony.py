from typing import Dict
from ..music.chords import CHORDS
from ..music.progressions import (
    C_MAJOR_PROGRESSIONS, 
    C_MINOR_PROGRESSIONS,
    D_MAJOR_PROGRESSIONS,
    D_MINOR_PROGRESSIONS
)
import music21
import random

def parse_scale_from_input(user_input: str) -> str:
    """Determine scale from user input."""
    if 'minor' in user_input.lower():
        return 'C minor'
    elif 'major' in user_input.lower():
        return 'C major'
    else:
        return random.choice(['C major', 'C minor', 'D major', 'D minor'])

def create(state: Dict) -> Dict:
    """Create harmony for the generated melody."""
    scale_name = parse_scale_from_input(state['musician_input'])
    duration = state.get('duration', 16)  # Default to 16 if not specified
    harmony = create_chord_progression(scale_name, duration)
    return {"harmony": harmony}

def create_chord_progression(scale_name: str, duration: int) -> music21.stream.Part:
    """Create a chord progression."""
    harmony = music21.stream.Part()
    
    # Set the instrument for harmony
    harmony_instrument = music21.instrument.ElectricPiano()
    harmony.insert(0, harmony_instrument)
    
    remaining_duration = duration
    
    # Adjust chord durations for hybrid feel
    chord_durations = [2.0, 1.0, 1.0, 2.0]  # Alternating long and short chords
    current_duration_index = 0
    
    # Choose progression based on key and scale
    if 'D' in scale_name:
        if 'minor' in scale_name.lower():
            progression = random.choice(D_MINOR_PROGRESSIONS)
        else:
            progression = random.choice(D_MAJOR_PROGRESSIONS)
    else:  # C key
        if 'minor' in scale_name.lower():
            progression = random.choice(C_MINOR_PROGRESSIONS)
        else:
            progression = random.choice(C_MAJOR_PROGRESSIONS)
    
    current_position = 0
    
    while remaining_duration > 0:
        # Get next chord duration from pattern
        chord_duration = min(chord_durations[current_duration_index], remaining_duration)
        current_duration_index = (current_duration_index + 1) % len(chord_durations)
        
        # Select chord from progression
        progression_index = (current_position // 2) % len(progression)
        chord_name = progression[int(progression_index)]  # Use the full chord name directly
        
        if chord_name in CHORDS:
            chord = music21.chord.Chord(CHORDS[chord_name])
            chord.quarterLength = chord_duration
            
            # Simpler dynamics
            if current_position % 4 == 0:
                chord.dynamic = random.choice(['mp', 'mf'])
            
            harmony.append(chord)
            remaining_duration -= chord_duration
            current_position += chord_duration
    
    return harmony