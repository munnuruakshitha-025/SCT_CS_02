# PixelShield - Image Encryption Tool

A GUI-based image encryption and decryption application developed using Python and Tkinter. The application performs pixel manipulation using a user-defined key to demonstrate a simple image encryption technique.

## Task

SkillCraft Technology Internship - Cyber Security Task 02

## Objective

Develop a simple image encryption tool using pixel manipulation by applying a basic mathematical operation to the pixel values of an image.

## Features

- Select PNG, JPG, JPEG, and BMP images
- Encrypt images using pixel manipulation
- Decrypt encrypted images
- User-defined encryption key
- Preview original and processed images
- Save processed images
- Clear and reset the application
- User-friendly graphical interface

## Technologies Used

- Python 3
- Tkinter
- Pillow (PIL)
- Pixel Manipulation
- Basic Mathematical Operations

## How It Works

The application reads the RGB values of every pixel in the selected image.

### Encryption

For each pixel, the selected key is added to the Red, Green, and Blue values.

```text
Encrypted Pixel = (Original Pixel + Key) % 256
