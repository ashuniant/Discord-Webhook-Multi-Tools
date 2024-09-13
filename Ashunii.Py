import os
import sys
import requests
import shutil
import ctypes
import time  # Import time module for sleep

# ANSI escape codes for text colors
RESET = '\033[0m'  # Reset to default color
GREEN = '\033[32m'  # Green color
RED = '\033[31m'
CYAN = '\033[36m'
WHITE = '\033[37m'

# Dictionary to map color names to hex values
COLOR_MAP = {
    "red": 0xFF0000,
    "green": 0x00FF00,
    "blue": 0x0000FF,
    "yellow": 0xFFFF00,
    "purple": 0x800080,
    "orange": 0xFFA500,
    "pink": 0xFFC0CB,
    "cyan": 0x00FFFF,
    "white": 0xFFFFFF,
    "black": 0x000000
}

def set_console_title(title):
    if sys.platform == 'win32':
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        print(f"\033]0;{title}\007", end='')

def clear_screen():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

def print_centered(text, width):
    lines = text.split('\n')
    centered_lines = [line.center(width) for line in lines]
    return '\n'.join(centered_lines)

def print_big_text():
    big_text = [
        "     /$$$$$$$$$$\   $$$$$$$$$$   $$      $$  $$      $$  $$$$$$          $$   $$ \ ",
        "    | $$      $$|   $$|          $$      $$  $$      $$  $$    $$        $$      | ",
        "    | $$      $$|   $$|          $$      $$  $$      $$  $$      $$      $$   $$ | ",
        "    | $$$$$$$$$$|   $$$$$$$$$$   $$$$$$$$$$  $$      $$  $$        $$    $$   $$ | ",
        "    | $$      $$|           $$   $$      $$  $$      $$  $$          $$  $$   $$ | ",
        "    | $$/    \$$|           $$   $$      $$  $$      $$  $$            $$$$   $$ | ",
        "    | $$|    |$$|  $$$$$$$$$$$   $$      $$  $$$$$$$$$$  $$              $$   $$ | ",
        "    |____________________________________________________________________________/"
    ]
    
    console_width = shutil.get_terminal_size().columns
    gradient_colors = [
        '\033[38;5;22m',  # Darker green
        '\033[38;5;28m',  # Dark green
        '\033[38;5;34m',  # Green
        '\033[38;5;40m',  # Light green
        '\033[38;5;46m'   # Lighter green
    ]
    
    for i, line in enumerate(big_text):
        color = gradient_colors[i % len(gradient_colors)]
        print(color + print_centered(line, console_width) + RESET)  # Set color and center text

def print_menu():
    menu = """
[1] Send Message To Webhook   [2] Send Embed To Webhook   [3] Webhook Spammer   [4] Send File/Image To Webhook
[5] Delete Webhook Message    [6] Webhook Configuration   [7] Message Editor    [8] Webhook Information
"""
    console_width = shutil.get_terminal_size().columns
    print(print_centered(menu, console_width))  # Center menu options

def print_small_text():
    small_text = "discord: ashunii   "
    console_width = shutil.get_terminal_size().columns
    print(print_centered(CYAN + small_text + RESET, console_width))  # Center small text

def pause_before_clear():
    input("\nPress Enter to continue...")

def replace_everyone(message):
    return message.replace("#everyone", "@everyone")

def send_message_to_webhook(webhook_url, message):
    try:
        message = replace_everyone(message)
        data = {'content': message}
        response = requests.post(webhook_url, json=data)
        
        if response.status_code == 204:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
    except Exception as e:
        print(f"An error occurred while sending the message: {e}")

def send_embed_to_webhook(webhook_url, title, description, color):
    try:
        description = replace_everyone(description)
        embed = {
            'embeds': [{
                'title': title,
                'description': description,
                'color': COLOR_MAP.get(color.lower(), 0xFFFFFF)  # Default to white if color not found
            }]
        }
        response = requests.post(webhook_url, json=embed)
        
        if response.status_code == 204:
            print("Embed sent successfully!")
        else:
            print(f"Failed to send embed. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
    except Exception as e:
        print(f"An error occurred while sending the embed: {e}")

def send_file_to_webhook(webhook_url, text, file_path):
    try:
        text = replace_everyone(text)
        file_path = file_path.strip('"').strip("'")
        
        if not os.path.isfile(file_path):
            print(f"{RED}File not found: {file_path}{RESET}")
            return
        
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            data = {'content': text}
            response = requests.post(webhook_url, data=data, files=files)
        
        if response.status_code == 204:
            print("File sent successfully!")
        else:
            print(f"Failed to send file. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
    except Exception as e:
        print(f"An error occurred while sending the file: {e}")

def delete_webhook_message(webhook_url, message_id):
    try:
        url = f"{webhook_url}/messages/{message_id}"
        response = requests.delete(url)
        
        if response.status_code == 204:
            print("Message deleted successfully!")
        else:
            print(f"Failed to delete message. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
    except Exception as e:
        print(f"An error occurred while deleting the message: {e}")

def webhook_information(webhook_url):
    try:
        response = requests.get(webhook_url)
        
        if response.status_code == 200:
            info = response.json()
            print(f"Name: {info.get('name', 'N/A')}")
            print(f"Avatar: {info.get('avatar', 'None')}")
            print(f"Channel ID: ({info.get('channel_id', 'N/A')})")
            print(f"Guild ID: ({info.get('guild_id', 'N/A')})")
        else:
            print(f"Failed to fetch webhook information. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
    except Exception as e:
        print(f"An error occurred while fetching the webhook information: {e}")

def webhook_configuration(webhook_url):
    try:
        name = input(GREEN + "@Discord.Webhook.Name: " + RESET)
        avatar = input(GREEN + "@Discord.Webhook.Avatar.Url: " + RESET)
        
        data = {
            'name': name,
            'avatar': avatar
        }
        
        response = requests.patch(webhook_url, json=data)
        
        if response.status_code == 200:
            print("Webhook configuration updated successfully!")
        else:
            print(f"Failed to update webhook configuration. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
    except Exception as e:
        print(f"An error occurred while updating the webhook configuration: {e}")

def message_editor(webhook_url, message_id):
    try:
        new_content = input(GREEN + "@Discord.Message.NewContent: " + RESET)
        new_content = replace_everyone(new_content)
        is_embed = input(GREEN + "@Embed? (y/n): " + RESET).strip().lower() == 'y'
        
        if is_embed:
            embed = {
                'embeds': [{
                    'description': new_content
                }]
            }
            response = requests.patch(f"{webhook_url}/messages/{message_id}", json=embed)
        else:
            data = {
                'content': new_content
            }
            response = requests.patch(f"{webhook_url}/messages/{message_id}", json=data)
        
        if response.status_code == 200:
            print("Message updated successfully!")
        else:
            print(f"Failed to update message. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
    except Exception as e:
        print(f"An error occurred while updating the message: {e}")

def webhook_spammer(webhook_url, message, amount):
    try:
        if amount <= 0:
            print(f"{RED}Amount must be greater than 0.{RESET}")
            return
        
        sent_count = 0
        
        for i in range(amount):
            response = requests.post(webhook_url, json={'content': message})
            
            if response.status_code == 204:
                sent_count += 1
            
            # Clear line and update progress
            progress = f"{sent_count}/{amount} Sent! ({(sent_count / amount) * 100:.0f}%)"
            sys.stdout.write('\r' + GREEN + progress + RESET)
            sys.stdout.flush()
            
            # Pause between messages to avoid rate limits
            time.sleep(1)
        
        print()  # Move to next line after updating progress
        print(f"{GREEN}{sent_count}/{amount} Sent!{RESET}")
        print(f"{GREEN}{(sent_count / amount) * 100:.0f}% successfully sent{RESET}")
    
    except Exception as e:
        print(f"{RED}An error occurred while spamming messages: {e}{RESET}")

def main():
    set_console_title("Ashuni Webhook Multi-tool")
    
    while True:
        clear_screen()
        print_big_text()
        print_small_text()
        print_menu()
        
        selection = input(GREEN + "@ASHUNII # Selection > " + RESET).strip()
        
        if selection == '1':
            webhook_url = input(GREEN + "@Discord.Webhook.Enter: " + RESET)
            message = input(GREEN + "@Discord.Message.Enter: " + RESET)
            send_message_to_webhook(webhook_url, message)
        
        elif selection == '2':
            webhook_url = input(GREEN + "@Discord.Webhook.Enter: " + RESET)
            title = input(GREEN + "@Discord.Embed.Title: " + RESET)
            description = input(GREEN + "@Discord.Embed.Description: " + RESET)
            color = input(GREEN + "@Discord.Embed.Color: " + RESET)
            send_embed_to_webhook(webhook_url, title, description, color)
        
        elif selection == '3':
            webhook_url = input(GREEN + "@Discord.Webhook.Enter: " + RESET)
            message = input(GREEN + "@Discord.Message.Enter: " + RESET)
            try:
                amount = int(input(GREEN + "@Discord.Spammer.Amount: " + RESET))
                webhook_spammer(webhook_url, message, amount)
            except ValueError:
                print(f"{RED}Invalid amount entered. Please enter a number.{RESET}")
        
        elif selection == '4':
            webhook_url = input(GREEN + "@Discord.Webhook.Enter: " + RESET)
            text = input(GREEN + "@Discord.File.Text: " + RESET)
            file_path = input(GREEN + "@Discord.File.Path: " + RESET)
            send_file_to_webhook(webhook_url, text, file_path)
        
        elif selection == '5':
            webhook_url = input(GREEN + "@Discord.Webhook.Enter: " + RESET)
            message_id = input(GREEN + "@Discord.Message.ID: " + RESET)
            delete_webhook_message(webhook_url, message_id)
        
        elif selection == '6':
            webhook_url = input(GREEN + "@Discord.Webhook.Enter: " + RESET)
            webhook_configuration(webhook_url)
        
        elif selection == '7':
            webhook_url = input(GREEN + "@Discord.Webhook.Enter: " + RESET)
            message_id = input(GREEN + "@Discord.Message.ID: " + RESET)
            message_editor(webhook_url, message_id)
        
        elif selection == '8':
            webhook_url = input(GREEN + "@Discord.Webhook.Enter: " + RESET)
            webhook_information(webhook_url)
        
        else:
            print(f"{RED}Invalid selection!{RESET}")
        
        pause_before_clear()  # Pause and wait for Enter to be pressed before clearing

if __name__ == "__main__":
    main()
