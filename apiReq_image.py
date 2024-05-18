from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

# Initialize the OpenAI client
client = OpenAI()

# Generate images using the OpenAI client
response = client.images.generate(
    prompt="A cute baby sea otter",
    n=2,
    size="1024x1024"
)

# Extract URLs of the generated images from the response
image_urls = []
for image_data in response.data:
    image_urls.append(image_data.url)

# Download and display the images
for url in image_urls:
    # Download the image from the URL
    response = requests.get(url)

    # Open the image using PIL
    image = Image.open(BytesIO(response.content))

    # Display the image using the default image viewer
    image.show()