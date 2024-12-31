# Face Morph
![Screenshot 2024-12-30 181916](https://github.com/user-attachments/assets/e86f2dff-5169-4821-b1ef-d4c15f11edd3)

It allows users to upload an image, which the program processes to align the face. Then, it averages the face with its flipped version and displays the result.

# The workflow is carried out as:
## 1. Aligning 
Firstly, we use [dlib's frontal_face_detector](http://dlib.net/python/index.html#dlib_pybind11.get_frontal_face_detector) to detect a face. For a detected face, [dlib's shape predictor](http://dlib.net/python/index.html#dlib_pybind11.shape_predictor)
identifies 68 facial landmarks. We use it to extract the Center of the Face (Nose) and Rotation (Left Eye and Right Eye).

To align, we calculate the angle between two eyes using [arctan2](https://numpy.org/doc/2.1/reference/generated/numpy.arctan2.html), construct a rotation matrix centered at the nose point to rotate the image so that the eyes align horizontally using [affine transformation](https://docs.opencv.org/3.4/d4/d61/tutorial_warp_affine.html).

## 2. Averaging
We use [numpy's mean function](https://numpy.org/doc/2.1/reference/generated/numpy.mean.html) to calculate the mean value of the corresponding pixels of both the original aligned image and its flipped version. Then we convert the result back to image format.

