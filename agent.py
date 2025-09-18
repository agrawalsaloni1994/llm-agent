import ollama
import subprocess

class SimpleLLMAgent:
    def __init__(self, model_name="llama2"):
        """
        Initializes the agent with a specified Ollama model.
        Ensure Ollama is running and the model is downloaded.
        """
        self.model_name = model_name

    def generate_response(self, prompt):
        """
        Generates a text response from the LLM based on the given prompt.
        """
        try:
            response = ollama.chat(model=self.model_name, messages=[
                {'role': 'user', 'content': prompt},
            ])
            return response['message']['content']
        except Exception as e:
            return f"Error communicating with Ollama: {e}"

    def execute_command(self, command):
        """
        Executes a shell command and returns its output.
        """
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Command execution failed: {e.stderr.strip()}"
        except FileNotFoundError:
            return f"Command not found: {command.split(' ')[0]}"

    def run_agent(self, user_input):
        """
        Processes user input, generates a response, and potentially executes commands.
        """
        # Example: Simple logic to detect if a command should be executed
        if user_input.lower().startswith("execute:"):
            command_to_execute = user_input[len("execute:"):].strip()
            print(f"Executing command: {command_to_execute}")
            return self.execute_command(command_to_execute)
        else:
            print(f"Generating response for: {user_input}")
            return self.generate_response(user_input)

if __name__ == "__main__":
    agent = SimpleLLMAgent()
    
    print("Simple LLM Agent. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        response = agent.run_agent(user_input)
        print(f"Agent: {response}")
