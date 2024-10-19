import socket
import time
import datetime
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Configuration
UDP_IP: str = "192.168.0.119"  # IP address of Darkbeam.
UDP_PORT: int = 5008  # Port number for UDP communication.
FRAME_WIDTH: int = 128  # Width of the display frame in pixels.
FRAME_HEIGHT: int = 64  # Height of the display frame in pixels.
BYTEARRAY_LENGTH: int = (FRAME_WIDTH * FRAME_HEIGHT) // 8  # Length of bytearray to hold the frame data.

# Create a UDP socket for network communication.
sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Font setup (use a default PIL font or specify a path to a .ttf file)
font_path: str = "arial.ttf"  # Path to font file.
font1: ImageFont.FreeTypeFont = ImageFont.truetype(font_path, 22)  # Small font for date.
font2: ImageFont.FreeTypeFont = ImageFont.truetype(font_path, 44)  # Larger font for time.

def create_frame() -> Image:
    """Creates an image frame with the current date and time displayed."""
    image: Image = Image.new('1', (FRAME_WIDTH, FRAME_HEIGHT), 0)  # Create a blank image.
    draw: ImageDraw.Draw = ImageDraw.Draw(image)  # Drawing context for the image.
    now: datetime.datetime = datetime.datetime.now()  # Current date and time.
    date_str: str = now.strftime("%a, %d.%m.")  # Format the date as 'Day, dd.mm.'
    time_str: str = now.strftime("%H:%M")  # Format the time as 'HH:MM'.

    draw.text((5, 0), date_str, font=font1, fill=1)  # Draw the date on the first line.
    draw.text((4, 22), time_str, font=font2, fill=1)  # Draw the time on the second line.
    return image

def image_to_bytearray(image: Image) -> bytearray:
    """Converts an image to a bytearray suitable for LED matrix display."""
    image_array: Image.Image = image.convert("1")  # Ensure image is in binary format.
    byte_array: bytearray = bytearray(BYTEARRAY_LENGTH + 1)  # Initialize bytearray.
    
    byte_array[0] = 1  # brightness

    for x in range(FRAME_WIDTH):
        for y in range(FRAME_HEIGHT):
            page: int = y // 8
            byte_index: int = x + (page * FRAME_WIDTH)
            bit_index: int = y % 8
            if image_array.getpixel((x, y)):
                byte_array[byte_index + 1] |= (1 << bit_index)    
    
    return byte_array

def send_frame(byte_array: bytearray) -> None:
    """Sends a frame over UDP to the configured IP and port."""
    sock.sendto(byte_array, (UDP_IP, UDP_PORT))

def main() -> None:
    """Main loop to continuously send frames every 5 seconds."""
    while True:
        frame: Image = create_frame()
        frame = frame.rotate(180)  # Rotate frame for correct orientation.
        byte_array: bytearray = image_to_bytearray(frame)
        send_frame(byte_array)
        time.sleep(5)  # Wait for 5 seconds before sending the next frame.

if __name__ == "__main__":
    main()
