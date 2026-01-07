from scripts.rag_with_FT import generate_answer
import sys

def start_chat():
    print("\nDeepSeek NBA Analyst (RAG Powered)")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("\033[1mYou:\033[0m ") 
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            print("\033[3mThinking via DeepSeek...\033[0m") 
            response = generate_answer(user_input)
            
            print(f"\n\033[94mBot:\033[0m {response}\n") 
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    start_chat()