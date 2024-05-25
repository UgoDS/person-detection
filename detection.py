# import required libraries
import cv2
import glob
import numpy as np

# initialize the HOG descriptor
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Load YOLO model
net = cv2.dnn.readNet("models/yolov3.weights", "models/yolov3.cfg")


def detect_humans_opencv(img_path):
    image = cv2.imread(img_path)

    # detect humans in input image
    (humans, _) = hog.detectMultiScale(
        image, winStride=(10, 10), padding=(32, 32), scale=1.1
    )

    # loop over all detected humans
    for x, y, w, h in humans:
        pad_w, pad_h = int(0.15 * w), int(0.01 * h)
        cv2.rectangle(
            image,
            (x + pad_w, y + pad_h),
            (x + w - pad_w, y + h - pad_h),
            (0, 255, 0),
            2,
        )

    # display the output image
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detect_humans_yolov3(img_path):
    # Define input image
    image = cv2.imread(img_path)

    # Get image dimensions
    (height, width) = image.shape[:2]

    # Define the neural network input
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Perform forward propagation
    output_layer_name = net.getUnconnectedOutLayersNames()
    output_layers = net.forward(output_layer_name)

    # Initialize list of detected people
    people = []

    # Loop over the output layers
    for output in output_layers:
        # Loop over the detections
        for detection in output:
            # Extract the class ID and confidence of the current detection
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Only keep detections with a high confidence
            if class_id == 0 and confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Add the detection to the list of people
                people.append((x, y, w, h))

    # Draw bounding boxes around the people
    for x, y, w, h in people:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    output_path = f"screenshots/persons/{img_path.split('/')[-1]}"
    if len(people) > 0:
        cv2.imwrite(output_path, image)
    return output_path


if __name__ == "__main__":
    list_images = glob.glob("screenshots/raw/*.jpeg")
    for img in list_images:
        # detect_humans_opencv(img)
        detect_humans_yolov3(img)
