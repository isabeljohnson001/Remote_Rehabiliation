import cv2
import numpy as np
from scipy.special import expit
import time
import aidlite_gpu
import android
from upload_imgs import upload_images
from send_messages import send_mags

# Initialize the AI model on GPU
aidlite = aidlite_gpu.aidlite(1)

def resize_pad(img):
    """Resize and pad the image for input to the detector.
    This adjusts images to the dimensions required by the face and palm detectors.
    Returns resized and padded images along with the scale and padding details.
    """
    size0 = img.shape
    if size0[0] >= size0[1]:
        h1 = 256
        w1 = 256 * size0[1] // size0[0]
        padh = 0
        padw = 256 - w1
    else:
        h1 = 256 * size0[0] // size0[1]
        w1 = 256
        padh = 256 - h1
        padw = 0
    scale = size0[1] / w1 if size0[0] >= size0[1] else size0[0] / h1
    padh1, padh2 = padh // 2, padh // 2 + padh % 2
    padw1, padw2 = padw // 2, padw // 2 + padw % 2
    img1 = cv2.resize(img, (w1, h1))
    img1 = np.pad(img1, ((padh1, padh2), (padw1, padw2), (0, 0)), 'constant', constant_values=0)
    img2 = cv2.resize(img1, (128, 128))
    return img1, img2, scale, (int(padh1 * scale), int(padw1 * scale))

def denormalize_detections(detections, scale, pad):
    """Convert normalized detection coordinates back to the original image coordinates."""
    for i in range(0, len(detections), 2):
        detections[:, i] = detections[:, i] * scale * 256 - pad[0]  # x coordinates
        detections[:, i+1] = detections[:, i+1] * scale * 256 - pad[1]  # y coordinates
    return detections

def process_detections(frame):
    """Process frame for detections and perform non-max suppression."""
    img1, img2, scale, pad = resize_pad(frame)
    img2 = img2.astype(np.float32) / 255.0
    aidlite.setTensor_Fp32(img2, 128, 128)
    aidlite.invoke()
    bboxes = aidlite.getTensor_Fp32(0).reshape(896, -1)
    scores = aidlite.getTensor_Fp32(1)
    detections = _tensors_to_detections(bboxes, scores, anchors)
    filtered_detections = py_cpu_nms(detections, 0.3)
    return denormalize_detections(filtered_detections, scale, pad)

def main_loop():
    """Main processing loop."""
    cap = cv2.VideoCapture(0)  # Use the primary camera
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        processed_detections = process_detections(frame)
        for detection in processed_detections:
            cv2.rectangle(frame, (int(detection[1]), int(detection[0])), (int(detection[3]), int(detection[2])), (0, 255, 0), 2)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main_loop()
