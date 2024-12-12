from typing import Dict
from ..music.scales import SCALES
import music21
import random

def parse_scale_from_input(user_input: str) -> str:
    """Determine scale from user input."""
    if 'minor' in user_input.lower():
        return 'C minor'
    elif 'major' in user_input.lower():
        return 'C major'
    else:
        return random.choice(list(SCALES.keys()))

def generate(state: Dict) -> Dict:
    """Generate a melody based on the user's input."""
    scale_name = parse_scale_from_input(state['musician_input'])
    duration = state.get('duration', 16)  # Default to 16 if not specified
    melody = create_melody(scale_name, duration)
    return {"melody": melody}

def create_melody(scale_name: str, duration: int) -> music21.stream.Part:
    """Create a melody based on a given scale."""
    melody = music21.stream.Part()
    
    # Set the instrument for melody
    melody_instrument = music21.instrument.AcousticGuitar()
    melody.insert(0, melody_instrument)
    
    scale = SCALES[scale_name]
    remaining_duration = duration
    
    # Hybrid duration settings - mix of fast and slow notes
    durations = {
        0.25: 15,   # sixteenth note (reduced for less frantic feel)
        0.5: 35,    # eighth note (main rhythmic element)
        1.0: 35,    # quarter note (balanced with eighth notes)
        1.5: 10,    # dotted quarter (added for variety)
        2.0: 5      # half note (occasional longer notes)
    }
    
    # Keep track of previous notes to create more musical patterns
    previous_notes = []
    previous_indices = []
    current_position = 0
    
    # Define strong scale degrees (1, 3, 5, 8)
    strong_degrees = [0, 2, 4, 6]
    
    # Track phrase position to control note durations
    phrase_position = 0
    
    while remaining_duration > 0:
        # Adjust available durations based on phrase position
        if phrase_position % 4 < 3:  # First 3 beats of phrase
            current_durations = {k: v for k, v in durations.items() if k <= 1.0}
        else:  # Last beat of phrase - allow longer notes
            current_durations = {k: v for k, v in durations.items()}
        
        possible_durations = [d for d in current_durations.keys() if d <= remaining_duration]
        if not possible_durations:
            break
        
        weights = [current_durations[d] for d in possible_durations]
        note_duration = random.choices(possible_durations, weights=weights)[0]
        
        # Improved note selection logic
        if len(previous_notes) < 2:
            # Start with strong scale degrees
            note_idx = random.choice(strong_degrees)
            note_name = scale[note_idx]
        else:
            last_idx = previous_indices[-1]
            
            # On strong beats, prefer strong scale degrees
            if current_position % 1 == 0:
                if random.random() < 0.7:  # 70% chance to hit strong scale degree
                    note_idx = random.choice(strong_degrees)
                else:
                    # Stepwise motion to nearby note
                    step = random.choice([-1, 1])
                    note_idx = (last_idx + step) % len(scale)
            else:
                # For off-beats, allow more movement but control the range
                if random.random() < 0.8:  # 80% chance for stepwise motion
                    step = random.choice([-1, 1])
                    note_idx = (last_idx + step) % len(scale)
                else:
                    # Controlled leaps that stay within the scale
                    intervals = [-3, -2, 2, 3]  # Thirds and fourths
                    step = random.choice(intervals)
                    note_idx = (last_idx + step) % len(scale)
            
            note_name = scale[note_idx]
        
        # More conservative octave selection
        if previous_notes:
            current_octave = int(previous_notes[-1][-1])
            # Only change octave if moving to a note that would sound too distant
            if abs(note_idx - previous_indices[-1]) > 3:
                if note_idx < previous_indices[-1]:
                    octave = str(current_octave + 1)
                else:
                    octave = str(current_octave - 1)
            else:
                octave = str(current_octave)
        else:
            octave = '4'
        
        note = music21.note.Note(note_name + octave)
        
        # Add articulations based on beat position
        if current_position % 1 == 0:  # Strong beats
            if random.random() < 0.3:
                note.articulations.append(music21.articulations.Accent())
        
        note.quarterLength = note_duration
        melody.append(note)
        
        previous_notes.append(note_name + octave)
        previous_indices.append(note_idx)
        if len(previous_notes) > 4:  # Increased memory for better patterns
            previous_notes.pop(0)
            previous_indices.pop(0)
        
        phrase_position = (phrase_position + note_duration) % 4
        remaining_duration -= note_duration
        current_position += note_duration
    
    return melody