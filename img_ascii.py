from PIL import Image
import streamlit as st

# ASCII characters used to represent different color brightness in the ASCII art
ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

def resize_image(image, new_width=100):
    # Calculate the new height of the image maintaining the aspect ratio
    width, height = image.size
    new_height = int(new_width * (height / width))
    # Resize the image to the new dimensions
    return image.resize((new_width, new_height))

def grayify(image):
    # Convert the image to grayscale
    return image.convert("L")

def pixels_to_ascii(image):
    # Convert the pixels of the image to ASCII characters based on their brightness
    pixels = image.getdata()
    ascii_str = "".join(ASCII_CHARS[pixel // 25] for pixel in pixels)
    return ascii_str

def img_to_ascii(image, new_width):
    # Convert an image to ASCII art with a specified width
    resized_gray_image = grayify(resize_image(image, new_width))
    ascii_characters = pixels_to_ascii(resized_gray_image)
    ascii_img = ""
    # Break the ASCII string into lines to form the ASCII art
    for i in range(0, len(ascii_characters), new_width):
        line = ascii_characters[i:i + new_width]
        ascii_img += line + "\n"
    return ascii_img

def ascii_to_html(ascii_img, color="#FFFFFF"):
    # Format the ASCII art as HTML for display, with a specified text color
    html_img = f"<pre style='color: {color}; font-family: monospace; line-height: 10px;'>{ascii_img}</pre>"
    return html_img

def save_file(file_name, content, mode='w'):
    with open(file_name, mode) as f:
        f.write(content)

def create_download_button(file_name, label, file_type):
    with open(file_name, 'rb') as f:
        st.download_button(label=label, data=f, file_name=f'{file_name}.{file_type}')

def main(new_width=100):
    # Streamlit application main function
    st.title('Image to ASCII Converter')
    # File uploader for the image
    file_input = st.file_uploader('Upload your image here:')
    # Color picker for the ASCII text color
    color = st.color_picker('Choose your text color', '#000000')

    if file_input:
        try:
            # Process the uploaded image and convert it to ASCII art
            image = Image.open(file_input)
            ascii_image = img_to_ascii(image, new_width)
            html_image = ascii_to_html(ascii_image, color)
        
            # Save and allow downloading of the ASCII art as an HTML file
            with open("ascii_image.html", "w") as f:
                f.write(html_image)
            # Save and allow downloading of the ASCII art as an text file
            with open("ascii_image.txt", 'w') as f:
                f.write(ascii_image)
            #Download the html file 
            with open('ascii_image.html', 'rb') as f:
                st.download_button(label='Download ASCII Image as HTML', data=f, file_name='ascii_image.html')
            #Download the text file 
            with open('ascii_image.txt', 'rb') as f:
                st.download_button(label='Download ASCII Image as Text File', data=f, file_name='ascii_image.txt')

        except OSError:
            # Handle invalid file format error
            st.write('Invalid file format. Please upload a valid image (png/jpg/jpeg).')

if __name__ == '__main__':
    #Please run the program using "streamlit run img_ascii.py"
    main()