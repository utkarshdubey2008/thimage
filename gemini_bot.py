import telebot
import os
import google.generativeai as genai

# Configure API keys
genai.configure(api_key="AIzaSyAGZ27K6iQzOUUGXIwQ7MZh3_Fx3LaEcA4")
bot = telebot.TeleBot("7272861624:AAEoJ5YvJChvrNXqPmT8LxtHdk1fcYqwVPs")

# Image generation function
def generate_image(prompt: str):
    imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")
    result = imagen.generate_images(
        prompt=prompt,
        number_of_images=1,
        safety_filter_level="block_only_high",
        person_generation="allow_adult",
        aspect_ratio="3:4",
        negative_prompt="Outside",
    )
    return result.images[0] if result.images else None

# Start command
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Gemini ImageGen bot! Send /generate [prompt] to create an image.")

# Generate image command
@bot.message_handler(commands=["generate"])
def generate(message):
    prompt = message.text[len("/generate "):].strip()
    if not prompt:
        bot.reply_to(message, "Please provide a prompt with /generate [prompt].")
        return

    bot.reply_to(message, "Generating your image, please wait...")
    image = generate_image(prompt)

    if image:
        image._pil_image.save("generated_image.jpg")  # Save image temporarily
        with open("generated_image.jpg", "rb") as img:
            bot.send_photo(message.chat.id, img)
    else:
        bot.reply_to(message, "Sorry, I couldn't generate an image. Try a different prompt.")

# Run the bot
bot.polling()
