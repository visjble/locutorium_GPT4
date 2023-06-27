import tkinter as tk
import openai, time

file = open("/PATH/TO/key.txt", "r") # EDIT HERE THE PATH TO YOUR KEY

# Read the contents of the file into a string variable
string = file.read().rstrip()

# Close the file
file.close()

openai.api_key = string

model_id = 'gpt-4'

STOP_WORD = 'vale' # keyword for quitting the chat

def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation,
        max_tokens=1000
    )
    api_usage = response['usage']
    print('Total token consumed: {0}'.format(api_usage['total_tokens']))

    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})

    return conversation

def send_message(event=None):
    global conversation
    # Get the user's message from the input box
    user_message = user_input.get()
    
    # Check if the user's message is 'vale'
    if user_message.lower() == STOP_WORD:
        quit_chat()
        return

    # Clear the input box
    user_input.delete(0, tk.END)

    # Append the user's message to the conversation
    conversation.append({'role': 'user', 'content': user_message})

    # Get the chatbot's response and append it to the conversation
    conversation = ChatGPT_conversation(conversation)

    # Display the chatbot's response in the chat window
    chat_window.configure(state=tk.NORMAL)
    chat_window.insert(tk.END, 'Suasor: ' + conversation[-1]['content'].strip() + '\n\n')
    chat_window.configure(state=tk.DISABLED)
    chat_window.yview(tk.END)

def quit_chat(event=None):
    global conversation
    # Prepare the goodbye message and append it to the conversation
    goodbye_message = {'role': 'system', 'content': 'vale'}  
    conversation.append(goodbye_message)

    # Get the chatbot's response and append it to the conversation
    conversation = ChatGPT_conversation(conversation)

    # Display the chatbot's response in the chat window
    chat_window.configure(state=tk.NORMAL)
    chat_window.insert(tk.END, 'Suasor: ' + conversation[-1]['content'].strip() + '\n\n')
    chat_window.configure(state=tk.DISABLED)
    chat_window.yview(tk.END)

    # Pause the script for 3 seconds before quitting
    time.sleep(2)

    # Exit the application
    root.destroy()



# Create a new tkinter window
root = tk.Tk()
root.title('Chatbot')

# Create the chat window
chat_window = tk.Text(root, state=tk.DISABLED)
chat_window.grid(row=0, column=0, padx=10, pady=10)

# Create the input box and the send button
user_input = tk.Entry(root)
user_input.bind('<Return>', send_message)
user_input.grid(row=1, column=0, padx=10, pady=10, sticky='WE')

send_button = tk.Button(root, text='Send', command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Create the Quit button
quit_button = tk.Button(root, text='Quit', command=quit_chat)
quit_button.grid(row=1, column=2, padx=10, pady=10)

# Bind the Quit button to the quit_chat function
root.protocol('WM_DELETE_WINDOW', quit_chat)

# Create the conversation list
conversation = []
conversation.append({'role': 'system', 'content': 'Salve amice!'})
conversation = ChatGPT_conversation(conversation)

# Display the chatbot's greeting in the chat window
chat_window.configure(state=tk.NORMAL)
chat_window.insert(tk.END, 'Suasor: ' + conversation[-1]['content'].strip() + '\n\n')
chat_window.configure(state=tk.DISABLED)

# Set the focus to the input box
user_input.focus()

# Start the main event loop
root.mainloop()
