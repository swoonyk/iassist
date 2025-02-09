import numpy as np
from collections import deque
import time

navigation_data = [
    "A person is walking towards you with a briefcase",
    "There is a car approaching from your left",
    "A bicycle is parked nearby",
    "Someone is using their phone while walking",
    "A student is sitting on a bench",
    "There's a tree with low-hanging branches",
    "A group of people are talking ahead",
    "Construction work is ongoing to your right",
    "A delivery person is carrying packages",
    "Someone is walking their dog",
    "A child is playing with a ball",
    "There's a wet floor sign ahead",
    "A person with a walking stick is approaching",
    "Someone is carrying groceries",
    "A person is typing on their laptop",
    "There is a person behind you who is reading a book",
]

# 10% priority 3, 40% priority 2, 50% priority 1
priorities = np.random.choice([3, 2, 1], size=len(navigation_data), 
                            p=[0.2, 0.3, 0.5])
navigation_priorities = dict(zip(navigation_data, priorities))

class NavigationQueue:
    def __init__(self, data_dict, initial_size=3):
        self.queue = []  # Using list instead of deque for more control
        self.data = list(data_dict.items())
        self.current_index = 0  # Start from beginning
        self.interrupted_item = None
        self.interrupted = False

        # Initialize with first 3 items
        for i in range(min(initial_size, len(self.data))):
            self.add_next_item()

    def sort_queue(self):
        # Sort by priority (highest first)
        self.queue.sort(key=lambda x: x[1], reverse=True)
        # Remove priority 1 items if queue is too long
        if len(self.queue) > 3:
            self.queue = [item for item in self.queue if item[1] > 1][:3]

    def add_next_item(self):
        if self.current_index < len(self.data):
            next_item = self.data[self.current_index]
            self.current_index += 1
            if next_item[1] >= 2 or len(self.queue) < 3:
                self.insert_with_priority(next_item)
            return True
        return False

    def insert_with_priority(self, item):
        scenario, priority = item
        if priority == 3:
            # Interrupt current output and process immediately
            self.interrupted = True
            if self.interrupted_item:
                # Put the previously interrupted item back in queue
                self.queue.insert(0, self.interrupted_item)
                self.interrupted_item = None
            self.queue.insert(0, item)
        elif priority == 2:
            # Find position after priority 3s but before priority 1s
            insert_pos = 0
            while (insert_pos < len(self.queue) and 
                   self.queue[insert_pos][1] == 3):
                insert_pos += 1
            self.queue.insert(insert_pos, item)
        else:  # priority 1
            self.queue.append(item)
        self.sort_queue()

    def display_scenario(self, scenario, priority):
        """Display the scenario with proper formatting."""
        # If this is a priority 3 message, show warning first
        if priority == 3:
            print("\n⚠️  WARNING: High Priority Message Incoming!")
            time.sleep(0.5)
            print("\n🔴 Priority 3 (Urgent):", end=" ", flush=True)
        elif priority == 2:
            print("\n🟡 Priority 2 (Important):", end=" ", flush=True)
        else:
            print("\n⚪ Priority 1 (Info):", end=" ", flush=True)

        # If interrupted during this message's display, still show the full message
        if self.interrupted:
            print(scenario)
            self.interrupted = False
            return False

        # Display word by word
        words = scenario.split()
        for i, word in enumerate(words):
            print(word, end=" ", flush=True)
            if i < len(words) - 1:  # Don't sleep after the last word
                time.sleep(0.3)
        print()  # New line after scenario completes
        time.sleep(1)
        return True

    def process_queue(self):
        if not self.queue:
            return False

        # Get next item to process
        current_item = self.queue.pop(0)  # Remove from queue immediately

        # Add next item right away
        self.add_next_item()

        # Process the removed item
        if not self.display_scenario(*current_item):
            # If interrupted, save the current item
            self.interrupted_item = current_item
            return True

        return len(self.queue) > 0 or self.current_index < len(self.data)

def main():
    nav_queue = NavigationQueue(navigation_priorities)
    try:
        while True:
            if not nav_queue.process_queue():
                print("\nNo more scenarios to process")
                break
            time.sleep(0.5)  # Small pause between queue processing cycles
    except KeyboardInterrupt:
        print("\nStopped by user")

if __name__ == "__main__":
    main()