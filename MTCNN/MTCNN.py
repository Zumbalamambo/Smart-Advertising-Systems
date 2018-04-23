from MTCNN import detect_face
import cv2
import tensorflow as tf


class MTCNN():

    def __init__(self, mtcnn_model_dir):
        # mtcnn parameters
        self._minsize = 10                      # minimum size of face
        self._threshold = [0.4, 0.5, 0.6]       # three steps's threshold
        self._factor = 0.8                      # scale factor
        self._sess = tf.Session()
        self._pnet, self._rnet, self._onet = detect_face.create_mtcnn(self._sess, mtcnn_model_dir)


    def __crop_image__(self, img, bounding_box):
        # Expanding face
        x1 = bounding_box[1] 
        x2 = bounding_box[3]
        
        y1 = bounding_box[0]
        y2 = bounding_box[2]

        offset = int(0.2*(y2 - y1)) 
        x1 = (x1 - offset) if (x1 - offset) > 0 else 0 
        y1 = (y1 - offset) if (y1 - offset) > 0 else 0
        y2 = (y2 + offset) if (y2 + offset) < img.shape[1] else img.shape[1]
        x2 = x2 + offset if (x2 + offset) < img.shape[0] else img.shape[0]
        crop_im = img[x1:x2, y1:y2, :]
        return crop_im


    def __landmark_detect__(self, image):
        with tf.Graph().as_default():
            bounding_boxes, points = detect_face.detect_face(image, 
                                                        self._minsize, 
                                                        self._pnet, 
                                                        self._rnet, 
                                                        self._onet, 
                                                        self._threshold, 
                                                        self._factor)

            nrof_faces = bounding_boxes.shape[0]    # number of faces
            # print('Number of faces: {}'.format(nrof_faces))
            
            if nrof_faces == 0:
                return False, _, _

        return [True, bounding_boxes, points]
        
        
    def single_face_crop(self, image):
        with tf.Graph().as_default():
            bounding_boxes, _ = detect_face.detect_face(image, 
                                                        self._minsize, 
                                                        self._pnet, 
                                                        self._rnet, 
                                                        self._onet, 
                                                        self._threshold, 
                                                        self._factor)

            nrof_faces = bounding_boxes.shape[0]    # number of faces
            # print('Number of faces: {}'.format(nrof_faces))
            
            if nrof_faces == 0:
                return _, False

            for face_position in bounding_boxes:    
                face_position = face_position.astype(int)
                # cv2.rectangle(frame, (face_position[0],face_position[1]),(face_position[2],face_position[3]),(0,255,0),2)
                # Get crop image from bounding box

                img_crop = self.__crop_image__(image, face_position)
                # Create crop image
                img_crop = cv2.cvtColor(img_crop, cv2.COLOR_BGR2RGB)

        return [img_crop, True]


    def multi_face_crop(self, image):
        crop_arr = []
        bounding_boxes = []

        with tf.Graph().as_default():
            bounding_boxes, _ = detect_face.detect_face(image, 
                                                        self._minsize, 
                                                        self._pnet, 
                                                        self._rnet, 
                                                        self._onet, 
                                                        self._threshold, 
                                                        self._factor)

            nrof_faces = bounding_boxes.shape[0]    # number of faces
            # print('Number of faces: {}'.format(nrof_faces))
            
            if nrof_faces == 0:
                return [crop_arr, bounding_boxes, False]

            for face_position in bounding_boxes:    
                face_position = face_position.astype(int)
                # cv2.rectangle(frame, (face_position[0],face_position[1]),(face_position[2],face_position[3]),(0,255,0),2)
                # Get crop image from bounding box

                crop = self.__crop_image__(image, face_position)
                # Create crop image
                crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
                # crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
                crop_arr.append(crop)
                
        return [crop_arr, bounding_boxes, True]