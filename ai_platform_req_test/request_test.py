import tensorflow as tf
import os
import json
import cv2
from PIL import Image
import googleapiclient.discovery
from google.api_core.client_options import ClientOptions
from object_detection.utils import visualization_utils as viz_utils
import base64

import numpy as np
from matplotlib import pyplot as plt

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "tensile-ship-312415-81a2e149e9b9.json"

project = "tensile-ship-312415"
region = "asia-southeast1"
model = "jagajalan_model"
version ="v0001"


def predict_json(project, region, model, instances, version=None):
    """Send json data to a deployed model for prediction.

    Args:
        project (str): project where the Cloud ML Engine Model is deployed.
        region (str): regional endpoint to use; set to None for ml.googleapis.com
        model (str): model name.
        instances ([Mapping[str: Any]]): Keys should be the names of Tensors
            your deployed model expects as inputs. Values should be datatypes
            convertible to Tensors, or (potentially nested) lists of datatypes
            convertible to tensors.
        version: str, version of the model to target.
    Returns:
        Mapping[str: any]: dictionary of prediction results defined by the
            model.
    """
    # Create the ML Engine service object.
    # To authenticate set the environment variable
    # GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_file>
    prefix = "{}-ml".format(region) if region else "ml"
    api_endpoint = "https://{}.googleapis.com".format(prefix)
    client_options = ClientOptions(api_endpoint=api_endpoint)
    service = googleapiclient.discovery.build(
        'ml', 'v1', client_options=client_options)
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']


def predict_image(image, img_shape=224):

    np_image = np.array(cv2.imread(image))

    category_index = {1: {'id': 1, 'name': 'D00'}, 2: {'id': 2, 'name': 'D01'},3: {'id': 3, 'name': 'D02'}, 4: {'id': 4, 'name': 'D03Al'}}

    img = tf.io.read_file(image)
    img = tf.io.decode_image(img)
    img = tf.image.resize(img, [img_shape, img_shape])

    img = tf.cast(tf.expand_dims(img, axis=0), tf.int16)

    instances_list = img.numpy().tolist()

    result = predict_json(project, region, model, instances_list, version)[0]

    test = np.array(result['detection_classes']).astype(np.int64)

    num_detections = int(result.pop('num_detections'))

    viz_utils.visualize_boxes_and_labels_on_image_array(
        np_image,
        np.array(result["detection_boxes"]),
        np.array(result["detection_classes"]).astype(np.int64),
        np.array(result["detection_scores"]),
        category_index,
        use_normalized_coordinates=True,
        max_boxes_to_draw=5,
        min_score_thresh=.3,
        agnostic_mode=False
    )

    return cv2.cvtColor(np_image, cv2.COLOR_BGR2RGB)

    
def main():
    image = 'testimage.jpeg'
    with open(image, "rb") as f:
        im_b64 = base64.b64encode(f.read())

    im_bytes = base64.b64decode(im_b64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    cv2.imwrite("tmp.jpg", img)
# print(open(image,'rb').read())
# cv2.imwrite("output.jpg", )
# print(predict_image(image))

# detections =  {key: value[:num_detections].numpy() for key, value in result.items()}

# print(result['detection_classes'].astype(np.int64))
# print(num_detections)

# with open('result.json','w') as req:
#   req.write(str(result))

# print(input_data_json)