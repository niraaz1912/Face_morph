import cv2
import dlib
import numpy as np

# Initialize dlib's face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  

def load_and_align_images(image_path):
    aligned_images = []
    # Load the original image
    img = cv2.imread(image_path)
    if img is not None:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)
            nose_point = (landmarks.part(33).x, landmarks.part(33).y)
            left_eye = (landmarks.part(36).x, landmarks.part(36).y)
            right_eye = (landmarks.part(45).x, landmarks.part(45).y)

            # Calculate angle to align images
            dx = right_eye[0] - left_eye[0]
            dy = right_eye[1] - left_eye[1]
            angle = np.degrees(np.arctan2(dy, dx)) - 180

            # Rotate image to align eyes horizontally
            M = cv2.getRotationMatrix2D(nose_point, angle, 1)
            aligned_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
            aligned_images.append(aligned_img)

            # Create flipped copy
            flipped_img = cv2.flip(aligned_img, 1)
            aligned_images.append(flipped_img)
    return aligned_images

def average_faces(images):
    if not images:
        return None
    # Calculate the average of the images
    avg_image = np.mean(images, axis=0).astype(np.uint8)
    return avg_image

def process_image(image_path):
    aligned_images = load_and_align_images(image_path)
    if aligned_images:
        average_image = average_faces(aligned_images)
        average_image = cv2.flip(average_image, 0)
        average_image = crop_black_border(average_image)
        return average_image
    return None

def crop_black_border(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find all non-black pixels
    coords = cv2.findNonZero(gray)
    # Find the bounding box of non-black pixels
    x, y, w, h = cv2.boundingRect(coords)

    cropped_image = image[y:y+h, x:x+w]
    return cropped_image


process_image('images/obama.jpg')
