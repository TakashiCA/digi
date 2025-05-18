import time
import random
import os
import sys

class DigiPet:
    def __init__(self, name):
        self.name = name
        self.hunger = 50  # 0-100 (0: full, 100: starving)
        self.energy = 100  # 0-100 (0: exhausted, 100: fully rested)
        self.cleanliness = 100  # 0-100 (0: dirty, 100: clean)
        self.is_sleeping = False
        self.needs_cleaning = False
        self.last_poop_time = time.time()
        self.animation_frame = 0

    def get_sprite(self):
        # Basic ASCII art sprites for different states
        normal = [
            r"  ╭──╮  ",
            r" ╭╯^^╰╮ ",
            r" │o  o│ ",
            r" ╰────╯ "
        ]
        
        sleeping = [
            r"  ╭──╮  ",
            r" ╭╯--╰╮ ",
            r" │z  z│ ",
            r" ╰────╯ "
        ]
        
        eating = [
            r"  ╭──╮  ",
            r" ╭╯^^╰╮ ",
            r" │o  o│ ",
            r" ╰─○──╯ "
        ]
        
        dirty = [
            r"  ╭──╮ ★",
            r" ╭╯>_╰╮ ",
            r" │o  o│ ",
            r" ╰────╯ "
        ]

        if self.needs_cleaning:
            return dirty
        elif self.is_sleeping:
            return sleeping
        elif self.hunger < 30:  # Just ate
            return eating
        else:
            return normal

    def feed(self):
        if self.is_sleeping:
            return "Shh! Your pet is sleeping!"
        if self.hunger < 10:
            return f"{self.name} is too full to eat!"
        self.hunger = max(0, self.hunger - 30)
        self.energy = min(100, self.energy + 10)
        return f"{self.name} enjoys the meal!"

    def sleep(self):
        if self.is_sleeping:
            return f"{self.name} is already sleeping!"
        self.is_sleeping = True
        return f"{self.name} goes to sleep..."

    def wake(self):
        if not self.is_sleeping:
            return f"{self.name} is already awake!"
        self.is_sleeping = False
        self.energy = min(100, self.energy + 60)
        return f"{self.name} wakes up!"

    def clean(self):
        if self.is_sleeping:
            return "Shh! Your pet is sleeping!"
        if not self.needs_cleaning:
            return f"Already clean!"
        self.needs_cleaning = False
        self.cleanliness = 100
        return f"All clean now!"

    def update_status(self):
        current_time = time.time()
        
        # Decrease energy over time
        if not self.is_sleeping:
            self.energy = max(0, self.energy - 1)
        
        # Increase hunger over time
        self.hunger = min(100, self.hunger + 1)
        
        # Random pooping based on time and feeding
        if not self.needs_cleaning and current_time - self.last_poop_time > 30:
            if random.random() < 0.1:
                self.needs_cleaning = True
                self.cleanliness = max(0, self.cleanliness - 50)
                self.last_poop_time = current_time
                return f"Made a mess!"
        
        return None

    def get_status_indicators(self):
        # Create simple indicators for status
        hunger_ind = "HUNGER: " + "█" * (self.hunger // 20) + "░" * (5 - self.hunger // 20)
        energy_ind = "ENERGY: " + "█" * (self.energy // 20) + "░" * (5 - self.energy // 20)
        clean_ind = "CLEAN:  " + "█" * (self.cleanliness // 20) + "░" * (5 - self.cleanliness // 20)
        return [hunger_ind, energy_ind, clean_ind]

def draw_frame(content, width=40, height=20):
    # Create a v-pet style frame
    top = "╔" + "═" * (width-2) + "╗"
    bottom = "╚" + "═" * (width-2) + "╝"
    empty_line = "║" + " " * (width-2) + "║"
    
    # Initialize the screen with empty lines
    screen = [empty_line for _ in range(height)]
    
    # Add top and bottom borders
    screen.insert(0, top)
    screen.append(bottom)
    
    # Add content to the middle of the screen
    start_line = (height - len(content)) // 2
    for i, line in enumerate(content):
        if start_line + i < height:
            screen[start_line + i] = "║" + line.center(width-2) + "║"
    
    return screen

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("Welcome to DigiPet!")
    pet_name = input("What would you like to name your pet? ")
    pet = DigiPet(pet_name)
    
    while True:
        clear_screen()
        status_message = pet.update_status()
        
        # Prepare the display content
        display_content = []
        
        # Add pet sprite
        display_content.extend(pet.get_sprite())
        display_content.append("")  # Empty line for spacing
        
        # Add status indicators
        display_content.extend(pet.get_status_indicators())
        display_content.append("")  # Empty line for spacing
        
        # Add status message if exists
        if status_message:
            display_content.append(status_message)
            display_content.append("")
        
        # Add menu
        display_content.append("[A]Feed [B]Clean [C]Sleep [Q]Quit")
        
        # Draw the frame with all content
        screen = draw_frame(display_content)
        
        # Print the entire screen
        print("\n".join(screen))
        
        # Get user input
        choice = input("\nChoice: ").lower()
        
        message = ""
        if choice == 'a':
            message = pet.feed()
        elif choice == 'b':
            message = pet.clean()
        elif choice == 'c':
            if pet.is_sleeping:
                message = pet.wake()
            else:
                message = pet.sleep()
        elif choice == 'q':
            print(f"\nGoodbye! Thanks for taking care of {pet.name}!")
            break
        
        if message:
            print(message)
            time.sleep(1)

if __name__ == "__main__":
    main() 