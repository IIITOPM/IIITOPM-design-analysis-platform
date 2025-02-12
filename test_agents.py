import os
import sys

# Print current directory and Python path
print("Current directory:", os.getcwd())
print("Python path:", sys.path)

try:
    from agents import initialize_agents
    print("Successfully imported initialize_agents")
    
    # Try to initialize the agents
    agents = initialize_agents()
    print("Successfully initialized agents:", list(agents.keys()))
except Exception as e:
    print(f"Error: {str(e)}")
    print(f"Error type: {type(e)}")
    print(f"Error location: {e.__traceback__.tb_next.tb_frame.f_code.co_filename}:{e.__traceback__.tb_next.tb_lineno}") 