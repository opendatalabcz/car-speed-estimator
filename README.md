# Car speed estimator
Car speed estimating from single camera using YoloV3 and Optical Flow

## Setup
Download the trained weights of the models and configurations:
- [yoloV3.weights](https://pjreddie.com/media/files/yolov3.weights)
- [YoloV3.cfg](https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg)
- [coco.names](https://github.com/pjreddie/darknet/blob/master/data/coco.names)

Put them inside src file

### Install the requirements

Run:
```
pip install -r requirements.txt
```

## Usage
Run:
```
python run.py
```

This will start Gui which will help you put video file and setup measuring parametes

For getting my test data you may use this link:
[Test data](https://www.dropbox.com/sh/e7p0bx68zmq24tf/AAARDee2y2o7i1615U7_kpRma?dl=0)
Paramaters of measuring area are:
Starting line:
X: 560 Y: 450  
X: 560 Y: 300
Ending line:
X: 810 Y: 450
X: 810 Y: 300
Length: 8
