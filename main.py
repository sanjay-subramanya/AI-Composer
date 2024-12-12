import os
from dotenv import load_dotenv
from src.core.workflow import create_workflow
from src.utils.midi import play_midi

def main():
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    app = create_workflow(api_key)
    
    inputs = {
        "musician_input": "Create a mysterious and thrilling piece in C minor",
        "style": "mysterious and thrilling",
        "tempo": 90,     # Beats per minute (60=slow, 90=moderate, 120=fast)
        "duration": 32  # In beats (16=4 bars, 32=8 bars)
    }
    
    result = app.invoke(inputs)
    print(f"Composition created. MIDI file saved at: {result['midi_file']}")
    play_midi(result['midi_file'])

if __name__ == "__main__":
    main() 