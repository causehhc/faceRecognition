import tensorflow as tf
import numpy as np
import os
from recognition.run.embeddings import load_model
from recognition.align.MtcnnDetector import MtcnnDetector
from recognition.align.detector import Detector
from recognition.align.fcn_detector import FcnDetector
from recognition.align.model import P_Net, R_Net, O_Net
import recognition.align.config as config
import cv2
import h5py


def load_align(path_root):
    thresh = config.thresh
    min_face_size = config.min_face
    stride = config.stride
    test_mode = config.test_mode
    detectors = [None, None, None]
    # 模型放置位置
    model_path = [
        '{}/PNet/'.format(path_root),
        '{}/RNet/'.format(path_root),
        '{}/ONet'.format(path_root)
    ]
    batch_size = config.batches
    PNet = FcnDetector(P_Net, model_path[0])
    detectors[0] = PNet

    if test_mode in ["RNet", "ONet"]:
        RNet = Detector(R_Net, 24, batch_size[1], model_path[1])
        detectors[1] = RNet

    if test_mode == "ONet":
        ONet = Detector(O_Net, 48, batch_size[2], model_path[2])
        detectors[2] = ONet

    mtcnn_detector = MtcnnDetector(detectors=detectors, min_face_size=min_face_size,
                                   stride=stride, threshold=thresh)
    return mtcnn_detector


def align_face(img, mtcnn_detector):
    try:
        boxes_c, _ = mtcnn_detector.detect(img)
    except:
        print('找不到脸')
        return None, None, None
    # 人脸框数量
    num_box = boxes_c.shape[0]
    bb_arr = []
    scaled_arr = []
    if num_box > 0:
        det = boxes_c[:, :4]
        det_arr = []
        img_size = np.asarray(img.shape)[:2]
        for i in range(num_box):
            det_arr.append(np.squeeze(det[i]))

        for i, det in enumerate(det_arr):
            det = np.squeeze(det)
            bb = [int(max(det[0], 0)), int(max(det[1], 0)), int(min(det[2], img_size[1])),
                  int(min(det[3], img_size[0]))]
            cv2.rectangle(img, (bb[0], bb[1]), (bb[2], bb[3]), (0, 255, 0), 2)
            bb_arr.append([bb[0], bb[1]])
            cropped = img[bb[1]:bb[3], bb[0]:bb[2], :]
            scaled = cv2.resize(cropped, (160, 160), interpolation=cv2.INTER_LINEAR)
            # TODO
            scaled = cv2.cvtColor(scaled, cv2.COLOR_BGR2RGB) - 127.5 / 128.0
            # scaled = (cv2.cvtColor(scaled, cv2.COLOR_BGR2RGB) - 127.5) / 128.0  # 需要重新训练

            scaled_arr.append(scaled)
        scaled_arr = np.array(scaled_arr)
        return img, scaled_arr, bb_arr
    else:
        print('找不到脸 ')
        return None, None, None


class FaceRecognizer:
    def __init__(self, path_pictures, path_root, path_model):
        self.threshold = 0.002  # 识别人脸阈值

        self.path_pictures = path_pictures
        self.path_h5 = "{}/embeddings.h5".format(self.path_pictures)
        if os.path.exists(self.path_h5):
            f = h5py.File(self.path_h5, 'r')
            class_arr = f['class_name'][:]
            self.class_arr = [k.decode() for k in class_arr]
            self.emb_arr = f['embeddings'][:]
            f.close()
        else:
            self.class_arr = []
            self.emb_arr = None

        self.cap = cv2.VideoCapture(0)
        self.mtcnn_detector = load_align(path_root)

        tf.Graph().as_default()
        self.sess = tf.Session()
        load_model('{}/'.format(path_model), sess=self.sess)
        self.images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        self.embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        self.phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
        self.keep_probability_placeholder = tf.get_default_graph().get_tensor_by_name('keep_probability:0')

        self.commitFlag = False

    def get_one_shot(self, detectFlag, imgID=None, delete=False):
        face_class_res = None
        ret, frame = self.cap.read()
        if not detectFlag:
            return ret, frame, face_class_res
        t1 = cv2.getTickCount()
        img, scaled_arr, bb_arr = align_face(frame, self.mtcnn_detector)
        if scaled_arr is not None:
            feed_dict = {
                self.images_placeholder: scaled_arr,
                self.phase_train_placeholder: False,
                self.keep_probability_placeholder: 1.0
            }
            embs = self.sess.run(self.embeddings, feed_dict=feed_dict)
            face_num = embs.shape[0]
            face_class = ['Others'] * face_num

            for i in range(face_num):
                if self.emb_arr is not None:
                    diff = np.mean(np.square(embs[i] - self.emb_arr), axis=1)
                    min_diff = min(diff)
                    # print(min_diff)
                    if min_diff < self.threshold:
                        index = np.argmin(diff)
                        face_class[i] = self.class_arr[index]
                        face_class_res = self.class_arr[index]
                if imgID is not None:
                    if delete is False:
                        self.class_arr.append(imgID)
                    if self.emb_arr is None:  # 初始无数据
                        face_class_res = imgID
                        self.emb_arr = np.array(embs, copy=True)
                    else:
                        if face_class_res is not None:  # 数据更新
                            index = self.class_arr.index(face_class_res)
                            self.class_arr.remove(face_class_res)
                            if self.emb_arr.shape[0] == 1:
                                self.emb_arr = None
                            else:
                                self.emb_arr = np.delete(self.emb_arr, index, axis=0)
                        if delete is False:
                            self.emb_arr = np.concatenate((self.emb_arr, [embs[i]]))  # 先将p_变成list形式进行拼接，注意输入为一个tuple
                    self.commitFlag = True
                    # cv2.imwrite('{}/{}.jpg'.format(self.path_pictures, imgID), frame)

            t2 = cv2.getTickCount()
            t = (t2 - t1) / cv2.getTickFrequency()
            fps = 1.0 / t
            for i in range(face_num):
                bbox = bb_arr[i]

                cv2.putText(img, '{}'.format(face_class[i]),
                            (bbox[0], bbox[1] - 2),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)

                # 画fps值
                cv2.putText(img, '{:.4f}'.format(t) + " " + '{:.3f}'.format(fps), (10, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        else:
            img = frame
        return ret, img, face_class_res

    def save_embedding(self):
        if self.emb_arr is not None:
            f = h5py.File(self.path_h5, 'w')
            class_arr = [i.encode() for i in self.class_arr]
            f.create_dataset('class_name', data=class_arr)
            f.create_dataset('embeddings', data=self.emb_arr)
            f.close()


def main(output=False):
    path_h5 = '../data/pictures'
    path_root = '../align/model'
    path_model = '../data/model_origin'
    recognizer = FaceRecognizer(path_h5, path_root, path_model)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    path = '../data/output'
    if not os.path.exists(path):
        os.mkdir(path)
    out = cv2.VideoWriter(path + '/out.mp4', fourcc, 10, (640, 480))
    while True:
        ret, img = recognizer.get_one_shot(True)
        if ret:
            if output:
                out.write(img)
            cv2.imshow("result", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    recognizer.cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
