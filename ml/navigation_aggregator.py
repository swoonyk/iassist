import re
import time
import threading
import numpy as np
import requests
from collections import deque
from ollama import generate  # Ollama LLM API

class NavigationContextAggregator:
    def __init__(self, time_window=3.0):
        self.lock = threading.Lock()
        self.time_window = time_window
        
        # Context state
        self.message_buffer = deque()
        self.current_direction = None
        self.current_obstacle = None
        self.last_emergency = None
        
        # Emergency pattern detection
        self.emergency_pattern = re.compile(r"\b(emergency|alert|danger|stop)\b", re.IGNORECASE)
        
        # Start aggregation loop
        self.running = True
        self.aggregation_thread = threading.Thread(target=self._aggregate_loop)
        self.aggregation_thread.start()

    def add_message(self, message, priority_level):
        """Add a new message with priority to the buffer."""
        with self.lock:
            self.message_buffer.append((message, priority_level))
    
    def _call_ollama(self, messages):
        """Call Ollama LLM to aggregate the messages."""
        prompt = f"""
        You are an AI assistant helping a visually impaired user navigate safely. 
        Summarize the following alerts in short, prioritized phrases** based on urgency:
        {messages}
        
        Only include the most important insights.
        """
        try:
            response = generate(model="mistral", prompt=prompt)
            return response["response"]
        except Exception as e:
            return f"Error calling Ollama: {e}"

    def _aggregate_loop(self):
        """Aggregates messages every 3 seconds and calls the LLM."""
        while self.running:
            time.sleep(self.time_window)  # Wait for 3 seconds
            
            with self.lock:
                if not self.message_buffer:
                    continue  # Skip if no new messages
                
                # Collect and clear buffer
                messages = list(self.message_buffer)
                self.message_buffer.clear()
            
            # Format messages for LLM
            formatted_messages = "\n".join(f"{p}: {m}" for m, p in messages)
            
            # Call Ollama LLM
            summary = self._call_ollama(formatted_messages)
            
            # Process the LLM response (e.g., update navigation state)
            print(f"\n🧠 LLM Aggregated Summary:\n{summary}\n")
    
    def stop(self):
        """Stop the aggregation loop."""
        self.running = False
        self.aggregation_thread.join()