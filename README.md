# FACE人脸检测
## 一、说明:
施工中..
```text
face
├─ DataUI.py
├─ DataUI.ui
├─ MainUI.py
├─ MainUI.ui
├─ README.md
├─ backend
│    ├─ db.py
│    └─ models.py
├─ main.py
├─ recognition
│    ├─ Recognizer.py
│    ├─ align
│    │    ├─ MtcnnDetector.py
│    │    ├─ align_mtcnn.py
│    │    ├─ config.py
│    │    ├─ detector.py
│    │    ├─ fcn_detector.py
│    │    ├─ model
│    │    │    ├─ ONet
│    │    │    ├─ PNet
│    │    │    └─ RNet
│    │    ├─ model.py
│    │    └─ utils.py
│    ├─ data  # 该目录被加入到.gitignore中，但程序运行时需要此数据
│    │    ├─ dataSet
│    │    │    └─ CASIA-WebFace
│    │    ├─ graph
│    │    │    ├─ train
│    │    │    └─ val
│    │    ├─ model
│    │    │    ├─ checkpoint
│    │    │    ├─ model.ckpt-101.data-00000-of-00001
│    │    │    ├─ model.ckpt-101.index
│    │    │    └─ model.ckpt-101.meta
│    │    ├─ model_origin
│    │    │    ├─ checkpoint
│    │    │    ├─ model.ckpt-76031.data-00000-of-00001
│    │    │    ├─ model.ckpt-76031.index
│    │    │    └─ model.ckpt-76031.meta
│    │    ├─ output
│    │    │    └─ out.mp4
│    │    └─ pictures
│    │           ├─ BXD.jpg
│    │           ├─ CH.jpg
│    │           └─ embeddings.h5
│    ├─ run
│    │    ├─ embeddings.py
│    │    └─ test.py
│    └─ train
│           ├─ config.py
│           ├─ inception_resnet_v1.py
│           └─ train.py
└─ sql
       └─ comprehensive_design_3.sql
```
## 二、功能:
### 1、录入&检测&考勤打卡
![avatar](./pic/rt.jpg)
### 2、检索
![avatar](./pic/log.jpg)
