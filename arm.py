# arm_module.py
# import pygame
# import socket
# import time
# from threading import Event

# class ArmController:
#     def __init__(self, jetson_ip="10.42.0.185", port=5005):
#         self.jetson_ip = jetson_ip
#         self.port = port
#         self.stop_event = Event()
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#         pygame.init()
#         pygame.joystick.init()

#         if pygame.joystick.get_count() == 0:
#             raise RuntimeError("No joystick detected.")

#         self.joystick = pygame.joystick.Joystick(0)
#         self.joystick.init()

#         joystick_name = self.joystick.get_name()
#         print(f"Detected joystick name: '{joystick_name}'")
#         if joystick_name not in ["Microsoft X-Box 360 pad", "Xbox 360 Controller", "Zikway HID gamepad"]:
#             raise RuntimeError("Xbox 360 controller not connected.")

#         self.button_command_map = {
#             0: "1c", 1: "2c", 2: "3c", 3: "4c",
#             4: "5c", 5: "5ac", 6: "startCamera", 7: "allstop"
#         }

#         self.button_states = [0] * self.joystick.get_numbuttons()
#         self.last_hat = (0, 0)

#     def run(self):
#         while not self.stop_event.is_set():
#             pygame.event.pump()

#             for btn_index, command in self.button_command_map.items():
#                 is_pressed = self.joystick.get_button(btn_index)
#                 if is_pressed and not self.button_states[btn_index]:
#                     print(f"Sending command: {command}")
#                     self.sock.sendto(command.encode(), (self.jetson_ip, self.port))
#                 self.button_states[btn_index] = is_pressed

#             hat = self.joystick.get_hat(0)
#             if hat != self.last_hat:
#                 dpad_map = {
#                     (0, 1): "4ac", (0, -1): "1ac", (-1, 0): "3ac", (1, 0): "2ac"
#                 }
#                 if hat in dpad_map:
#                     print(f"D-pad → Sending {dpad_map[hat]}")
#                     self.sock.sendto(dpad_map[hat].encode(), (self.jetson_ip, self.port))
#                 self.last_hat = hat

#             time.sleep(0.1)

#     def stop(self):
#         self.stop_event.set()
#         pygame.quit()









import pygame
import socket
import time
import sys

JETSON_IP = "10.42.0.185"  # Replace if needed
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick detected.")
    sys.exit(1)

joystick = pygame.joystick.Joystick(0)
joystick.init()
joystick_name = joystick.get_name()
print(f"✅ Connected to joystick: {joystick_name}")

# Accept only Xbox 360 controllers (partial match, case-insensitive)
valid_controller = False
name_lower = joystick_name.lower()
if "xbox" in name_lower or "x-box" in name_lower:
    valid_controller = True

if not valid_controller:
    print("❌ Unsupported controller. Please connect a Microsoft X-Box 360 pad.")
    sys.exit(1)

# Your button to command map here
button_command_map = {
    0: "1c",        # A
    1: "2c",        # B
    2: "3c",        # X
    3: "4c",        # Y
    4: "5c",        # LB
    5: "5ac",       # RB
    6: "startCamera",  # Back
    7: "allstop"       # Start
}

button_states = [0] * joystick.get_numbuttons()
last_hat = (0, 0)

try:
    while True:
        pygame.event.pump()

        for btn_index, command in button_command_map.items():
            is_pressed = joystick.get_button(btn_index)

            if is_pressed and not button_states[btn_index]:
                print(f"Sending command: {command}")
                sock.sendto(command.encode(), (JETSON_IP, PORT))

            button_states[btn_index] = is_pressed

        hat = joystick.get_hat(0)
        if hat != last_hat:
            dpad_map = {
                (0, 1): "4ac",   # Up
                (0, -1): "1ac",  # Down
                (-1, 0): "3ac",  # Left
                (1, 0): "2ac"    # Right
            }
            if hat in dpad_map:
                command = dpad_map[hat]
                print(f"D-pad {hat} → Sending {command}")
                sock.sendto(command.encode(), (JETSON_IP, PORT))
            last_hat = hat

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    pygame.quit()
