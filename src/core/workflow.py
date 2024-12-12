from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from .state import MusicState
from ..generators import melody, harmony
from ..utils.midi import midi_converter

def create_workflow(api_key: str):
    """Create and configure the music generation workflow."""
    llm = ChatOpenAI(api_key=api_key, model="gpt-4o-mini")
    
    workflow = StateGraph(MusicState)
    
    # Add nodes 
    workflow.add_node("melody_generator", melody.generate)
    workflow.add_node("harmony_creator", harmony.create)
    workflow.add_node("midi_converter", midi_converter)
    
    # Set entry point and edges
    workflow.set_entry_point("melody_generator")
    workflow.add_edge("melody_generator", "harmony_creator")
    workflow.add_edge("harmony_creator", "midi_converter")
    workflow.add_edge("midi_converter", END)
    
    return workflow.compile() 