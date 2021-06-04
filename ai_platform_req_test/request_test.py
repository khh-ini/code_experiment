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
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config['GCP']['GOOGLE_APPLICATION_CREDENTIALS']

project = config['GCP']['PROJECT_ID']
region = config['GCP']['REGION']
model = config['GCP']['MODEL_NAME']
version = config['GCP']['MODEL_VERSION']

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

    category_index = {1: {'id': 1, 'name': 'D00'}, 2: {'id': 2, 'name': 'D01'},3: {'id': 3, 'name': 'D02'}, 4: {'id': 4, 'name': 'D03'}}
    class_name = ["D00","D01","D02","D03"]
    img = tf.io.read_file(image)
    img = tf.io.decode_image(img)
    img = tf.image.resize(img, [img_shape, img_shape])

    img = tf.cast(tf.expand_dims(img, axis=0), tf.int16)

    instances_list = img.numpy().tolist()

    result = predict_json(project, region, model, instances_list, version)[0]

    
    test = np.array(result['detection_classes']).astype(np.int64)
    pred_class = category_index[tf.argmax(result)]

    print(pred_class)

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
