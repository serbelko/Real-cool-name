from PIL import Image

# Load the sprite sheet
sprite_sheet = Image.open("sprites\walk.png")

# Define sprite properties
frame_width = 48
frame_height = 64
columns = 8  # Number of sprites per row in original sheet
rows = 6  # Total number of rows
total_frames = columns * rows

# New image dimensions
new_width = frame_width * columns * rows  # All rows concatenated horizontally
new_height = frame_height  # Single row height

# Create a new blank image
new_image = Image.new("RGBA", (new_width, new_height))

# Process each row and place it in the new image
for row in range(rows):
    for col in range(columns):
        sprite_x = col * frame_width
        sprite_y = row * frame_height
        frame = sprite_sheet.crop((sprite_x, sprite_y, sprite_x + frame_width, sprite_y + frame_height))

        # New X position in the final sprite strip
        new_x = (row * columns + col) * frame_width
        new_image.paste(frame, (new_x, 0))

# Save the new sprite sheet
new_image.save("walk1.png")

print("Sprite strip saved as sprite_strip.png")
