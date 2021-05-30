import cv2
import numpy as np
import base64
from request_test import predict_image


def main():
    image = 'testimage.jpeg'
    with open(image, "rb") as f:
        im_b64 = base64.b64encode(f.read())

    im_bytes = base64.b64decode(im_b64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    cv2.imwrite("tmp.jpg", img)
    
    res = predict_image("tmp.jpg")
    cv2.imwrite("output.jpg", res)

main()