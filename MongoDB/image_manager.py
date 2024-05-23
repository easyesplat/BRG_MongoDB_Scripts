from get_database import get_database
from gridfs import GridFS
from PIL import Image
import io

# Global variables 
db = get_database("hazards")
fs = GridFS(db)

def upload_image(steer_photo_id):
    # Read the image file
    try:
        with open('/Volumes/LaCie/STEER/Photos/' + steer_photo_id + '.jpg', 'rb') as f:
            image_data = f.read()
    except:
        print("\033[91mCouldn't read .jpg\033[0m")
        try:
            with open('/Volumes/LaCie/STEER/Photos/' + steer_photo_id + '.png', 'rb') as f:
                image_data = f.read()
        except:
            print("\033[91mCouldn't read .png\033[0m")

    # Store the image in MongoDB
    image_id = fs.put(image_data, filename=steer_photo_id)

    print(f"Image uploaded with id: {image_id}")
    return image_id

def print_image(image_id):
    # Retrieving the image
    out = fs.get(image_id)
    image = Image.open(io.BytesIO(out.read()))
    image.show()
    return image

if __name__ == "__main__":
    image_id = upload_image("test")
    print_image(image_id)
