import socket
import pygame
import sys

# Initialize Pygame
pygame.init()

# Initialize the joystick module
pygame.joystick.init()

# Check if there's at least one joystick connected
if pygame.joystick.get_count() == 0:
    print("No joystick detected.")
    pygame.quit()
    sys.exit()

# Get the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()


class RuidaController:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(5) 
    
    def send(self, data):
        try:
            self.sock.sendto(data, (self.host, self.port))
        except Exception as e:
            print(f"Error sending data: {e}")

    def receive(self):
        try:
            data, addr = self.sock.recvfrom(1024) 
            return data
        except socket.timeout:
            print("Timeout occurred")
        except Exception as e:
            print(f"Error receiving data: {e}")

    def close(self):
        self.sock.close()


def sendCommand(command):
     controller.send(bytes.fromhex(command))
     controller.send(bytes.fromhex('cc'))


def main():
    controller_ip = "192.168.68.163"  
    controller_port = 50207          

    global controller
    controller = RuidaController(controller_ip, controller_port)
    controller.send(bytes.fromhex('cc'))

    try:
      while True:
          # Handle events
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()

          # X axis controll
          if (joystick.get_axis(0) > 0.4):
            sendCommand("a55002")
          elif (joystick.get_axis(0) < -0.4):
            sendCommand("a55001")
          elif (joystick.get_axis(0) < 0.2 and joystick.get_axis(0) > -0.8):
            sendCommand("a55102")

          # Y axis controll
          if (joystick.get_axis(1) > 0.4):
            sendCommand("a55004")
          elif (joystick.get_axis(1) < -0.4):
            sendCommand("a55003")
          elif (joystick.get_axis(1) < 0.2 and joystick.get_axis(0) > -0.8):
            sendCommand("a55103")

          # Z axis controll
          if (joystick.get_axis(3) > 0.4):
            sendCommand("a5500b")
          elif (joystick.get_axis(3) < -0.4):
            sendCommand("a5500a")
          elif (joystick.get_axis(3) < 0.2 and joystick.get_axis(0) > -0.8):
            sendCommand("a5510a")

          # A button, pulse laser
          if (joystick.get_button(0)):
            sendCommand("a55005")      
          else:
            sendCommand("a55105")

          pygame.time.delay(100)

    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
        controller.close()


if __name__ == "__main__":
    main()


