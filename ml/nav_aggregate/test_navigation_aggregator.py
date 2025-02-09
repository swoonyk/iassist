import time
from ml.nav_aggregate.navigation_aggregator import NavigationContextAggregator  # Import your class

# Initialize the Navigation Aggregator
nav_aggregator = NavigationContextAggregator()

# Add test messages (simulating real-time input)
test_messages = [
    ("There's a car coming fast", 4),
    ("Gunshot heard nearby", 5),
    ("Turn left", 2),
    ("Explosion detected ahead", 5),
    ("Pedestrian walking towards you", 3),
    ("Traffic light changing to red", 3),
]

print("\n🚀 Running Navigation Context Aggregator Test...\n")

# Feed messages into the system
for message, priority in test_messages:
    print(f"📩 Adding message: '{message}' (Priority: {priority})")
    nav_aggregator.add_message(message, priority)
    time.sleep(1)  # Simulate messages arriving in real-time

# Wait for at least one aggregation cycle
time.sleep(5)

# Stop the aggregator
nav_aggregator.stop()

print("\n✅ Test completed. Check above for the LLM summary.\n")