#6. Write a try/except block that gracefully handles at least three different exception types (ValueError, ZeroDivisionError, FileNotFoundError).

def process_file_data(filename):
    print(f"Attempting to process: {filename}")
    
    try:
        with open(filename, 'r') as file:
            content = file.read()
        
        divisor = int(content)
        
        result = 100 / divisor
        
        print(f"Success! 100 divided by your number is: {result}")

    except FileNotFoundError:
        print("Error: That file doesn't exist. Please check the path.")
        
    except ValueError:
        print("Error: The file does not contain a valid integer.")
        
    except ZeroDivisionError:
        print("Error: The file contains a '0'. Math cannot divide by zero.")
        
    except Exception as e:
        print(f"System Alert: An unexpected error occurred -> {e}")
