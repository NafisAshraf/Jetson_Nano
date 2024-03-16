import asyncio
import pygame
import serial
import time

async def main():
    arduino_port = 'COM3'
    arduino = serial.Serial(arduino_port, 9600, timeout=1)
    await asyncio.sleep(2)

    # Initialize Pygame
    pygame.init()

    # Set up the Xbox controller
    controller = pygame.joystick.Joystick(0)
    controller.init()

    # Get the number of buttons on the controller
    num_buttons = controller.get_numbuttons()
    print(f"Number of buttons on controller: {num_buttons}")

    # Get the number of axes on the controller
    num_axes = controller.get_numaxes()
    print(f"Number of axes on controller: {num_axes}")

    # Define a rounding function
    def round_to_nearest(value):
        return round(value, 1)

    # Define the button map
    button_map = {1: "A", 2: "B", 0: "X", 3: "Y", 4: "LB", 5: "RB", 6: "LT", 7: "RT", 8: "Left Stick", 9: "Right Stick"}
    serial_message_ON = {"LT": ("2-ON\n", "4-ON\n", "6-ON\n"), "RT": ("3-ON\n", "5-ON\n", "7-ON\n"), "X": ("4-ON\n",), "Y": ("5-ON\n",)}
    serial_message_OFF = {"LT": ("2-OFF\n", "4-OFF\n", "6-OFF\n"), "RT": ("3-OFF\n", "5-OFF\n", "7-OFF\n"), "X": ("4-OFF\n",), "Y": ("5-OFF\n",)}
    


    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 0:
                        print(f"Left joystick X-axis value: {round_to_nearest(event.value)}")
                    elif event.axis == 1:
                        print(f"Left joystick Y-axis value: {-1 * round_to_nearest(event.value)}")
                    elif event.axis == 2:
                        print(f"Right joystick X-axis value: {round_to_nearest(event.value)}")
                    elif event.axis == 3:
                        print(f"Right joystick Y-axis value: {-1 * round_to_nearest(event.value)}")

                    # RT LT
                    elif event.axis == 4:
                        print(f"LT: {round_to_nearest(event.value)}")
                    elif event.axis == 5:
                        print(f"RT: {round_to_nearest(event.value)}")

                elif event.type == pygame.JOYBUTTONDOWN:
                    # Handle button presses
                    button_index = event.button
                    if button_index in button_map:
                        button_name = button_map[button_index]
                        print(f"{button_name, button_index} button pressed")
                        if button_name in serial_message_OFF.keys():
                            for msg in serial_message_OFF[button_name]:
                                arduino.write(msg.encode())
                                print(f"Sent message to arduino - {msg}")
                        

                elif event.type == pygame.JOYBUTTONUP:
                    # Handle button releases
                    button_index = event.button
                    if button_index in button_map:
                        button_name = button_map[button_index]
                        print(f"{button_name} button released")
                        if button_name in serial_message_ON.keys():
                            for msg in serial_message_ON[button_name]:
                                arduino.write(msg.encode())
                                print(f"Sent message to arduino - {msg}")

            await asyncio.sleep(0.1)

    finally:
        pygame.quit()
        arduino.close()



if __name__ == "__main__":
    loop = asyncio.new_event_loop()  # Create a new event loop
    asyncio.run(main())  # Run the main coroutine with the new loop
    loop.close()  # Close the loop after execution

