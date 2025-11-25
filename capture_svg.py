#!/usr/bin/env python3
"""
SVG to GIF Converter
Creates a professional typing animation with blinking cursor
"""

import os
from PIL import Image, ImageDraw, ImageFont


def create_typing_gif():
    """Create professional typing animation GIF with blinking cursor"""

    # Create assets directory
    if not os.path.exists('assets'):
        os.makedirs('assets')

    # Text content (clean, professional, no emoji)
    text_lines = [
        "Hey, I'm Biaoo",
        "AI Engineer | Sustainability Enthusiast"
    ]

    # Image parameters
    width, height = 600, 80
    background_color = (255, 255, 255, 0)  # Transparent
    text_color = (99, 102, 241)  # #6366F1 Indigo
    cursor_color = (99, 102, 241)

    # Load font
    font_size = 28
    font = None

    font_paths = [
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/Monaco.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/Library/Fonts/SF-Mono-Regular.otf",
        "/System/Library/Fonts/Supplemental/Menlo.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
    ]

    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, font_size)
            print(f"Using font: {font_path}")
            break
        except Exception:
            continue

    if font is None:
        print("Warning: Using default font")
        font = ImageFont.load_default()

    images = []
    cursor_width = 2
    cursor_height = 30

    def create_frame(text, show_cursor=True):
        """Create a single frame with optional cursor"""
        img = Image.new('RGBA', (width, height), color=background_color)
        draw = ImageDraw.Draw(img)

        # Calculate text position (centered)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        # Draw text
        draw.text((x, y), text, fill=text_color, font=font)

        # Draw cursor
        if show_cursor and text:
            cursor_x = x + text_width + 3
            cursor_y = (height - cursor_height) // 2
            draw.rectangle(
                [cursor_x, cursor_y, cursor_x + cursor_width, cursor_y + cursor_height],
                fill=cursor_color
            )

        return img

    def add_typing_frames(text, frame_list):
        """Add typing animation frames for a text"""
        current_text = ""
        for i, char in enumerate(text):
            current_text += char
            # Add frame with cursor
            frame_list.append(create_frame(current_text, show_cursor=True))
            # Add frame without cursor (blink effect every 3 chars)
            if i % 3 == 0:
                frame_list.append(create_frame(current_text, show_cursor=False))

    def add_pause_frames(text, frame_list, count=10):
        """Add pause frames with blinking cursor"""
        for i in range(count):
            show_cursor = i % 2 == 0  # Blink cursor
            frame_list.append(create_frame(text, show_cursor=show_cursor))

    def add_erase_frames(text, frame_list):
        """Add erasing animation frames"""
        for i in range(len(text), 0, -2):  # Erase 2 chars at a time (faster)
            current_text = text[:i]
            frame_list.append(create_frame(current_text, show_cursor=True))

    # Line 1: Type, pause, erase
    print(f"Creating frames for: {text_lines[0]}")
    add_typing_frames(text_lines[0], images)
    add_pause_frames(text_lines[0], images, count=16)  # Longer pause
    add_erase_frames(text_lines[0], images)

    # Small gap between lines
    for _ in range(4):
        images.append(create_frame("", show_cursor=True))
        images.append(create_frame("", show_cursor=False))

    # Line 2: Type, pause, erase
    print(f"Creating frames for: {text_lines[1]}")
    add_typing_frames(text_lines[1], images)
    add_pause_frames(text_lines[1], images, count=20)  # Even longer pause for second line
    add_erase_frames(text_lines[1], images)

    # Final pause before loop
    for _ in range(6):
        images.append(create_frame("", show_cursor=True))
        images.append(create_frame("", show_cursor=False))

    # Save GIF
    if images:
        print(f"Saving {len(images)} frames to GIF...")

        try:
            images[0].save(
                'assets/typing.gif',
                format='GIF',
                save_all=True,
                append_images=images[1:],
                duration=80,  # 80ms per frame for smooth animation
                loop=0,
                disposal=2,
                transparency=0,
                optimize=True
            )
            print("Saved: assets/typing.gif")
            print(f"Total frames: {len(images)}")
        except Exception as e:
            print(f"Error saving GIF: {e}")
            # Fallback method
            images[0].save(
                'assets/typing.gif',
                save_all=True,
                append_images=images[1:],
                duration=80,
                loop=0
            )
            print("Saved using fallback method")
    else:
        print("Error: No frames created")


if __name__ == "__main__":
    print("Creating professional typing animation...")
    print("=" * 50)
    create_typing_gif()
    print("=" * 50)
    print("Done!")
