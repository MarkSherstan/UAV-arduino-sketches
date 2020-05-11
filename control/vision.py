from threading import Thread
import numpy as np
import math
import time
import cv2
import cv2.aruco as aruco

class Vision:
    def __init__(self, desiredWidth, desiredHeight, desiredFPS, autoFocus, src=0):
        # Threading parameters
        self.isReceivingFrame = False
        self.isReceivingPose = False

        self.isRunFrame = True
        self.isRunPose = True

        self.frameThread = None
        self.poseThread = None

        # Frame
        self.frame = None
        self.frameCount = 0
        self.poseCount = 0

        # Camera config 
        self.desiredWidth  = desiredWidth
        self.desiredHeight = desiredHeight
        self.desiredFPS    = desiredFPS   
        self.autoFocus     = autoFocus    
        
        # Aruco dictionary to be used and pose processing parameters
        self.arucoDict = aruco.Dictionary_get(aruco.DICT_5X5_1000)
        self.parm = aruco.DetectorParameters_create()
        self.parm.adaptiveThreshConstant = 10

        # Calibration values
        # C270
        # self.mtx = np.array([[1.40106056e+03, 0.00000000e+00, 6.36194296e+02],
        #                      [0.00000000e+00, 1.39929991e+03, 4.73179102e+02],
        #                      [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
        # self.dist = np.array([[0.00770591, 0.24889461, 0.00463238, 0.00254009, 0.28752805]])

        # C920: 640x480
        # self.mtx = np.array([[644.64187481, 0.0000000000, 318.22631417],
        #                      [0.0000000000, 646.07966016, 253.25028334],
        #                      [0.0000000000, 0.000000e000, 1.0000000000]])
        # self.dist = np.array([[-0.08303304, 1.10723415, 0.00558508, -0.00866121, -3.0388813]])

        # C920: 1280x720
        self.mtx = np.array([[936.30697877, 0.0000000000, 630.75833619],
                             [0.0000000000, 939.68072069, 411.43910036],
                             [0.0000000000, 0.000000e000, 1.0000000000]])
        self.dist = np.array([[0.02503521, -0.237694, 0.01188617, -0.00965216, 0.23757888]])

        # Marker properties
        self.lengthMarker = 0.176
        self.markerID = 17

        # Offset values in cm
        self.offsetNorth = 0
        self.offsetEast  = 0
        self.offsetDown  = 0

        # Output values
        self.North = 0
        self.East  = 0
        self.Down  = 0
        self.Yaw   = 0
        self.isReady = False

        # Start the connection to the camera
        try:
            self.cam = cv2.VideoCapture(src)
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.desiredWidth)
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.desiredHeight)
            self.cam.set(cv2.CAP_PROP_FPS, self.desiredFPS)
            self.cam.set(cv2.CAP_PROP_AUTOFOCUS, self.autoFocus)
            print('Camera start')
        except:
            print('Camera setup failed')

    def startFrameThread(self):
        # Create a thread
        if self.frameThread == None:
            self.frameThread = Thread(target=self.acquireFrame)
            self.frameThread.start()
            print('Camera thread start')

            # Block till we start receiving values
            while self.isReceivingFrame != True:
                time.sleep(0.1)

    def acquireFrame(self):
        # Acquire until closed
        while(self.isRunFrame):
            _, self.frame = self.cam.read()
            self.frameCount += 1
            self.isReceivingFrame = True

    def startPoseThread(self):
        # Block until a frame has been acquired
        while self.frame is None:
            time.sleep(0.1)

        # Create a thread
        if self.poseThread == None:
            self.poseThread = Thread(target=self.processFrame)
            self.poseThread.start()
            print('Frame processing thread start')

            # Block till we start receiving values
            while (self.isReceivingPose != True):
                time.sleep(0.1)

    def processFrame(self):
        # Process data until closed
        while(self.isRunPose):
            self.getPose()
            self.poseCount += 1
            self.isReceivingPose = True

    def getPose(self):
        # Get frame and convert to gray
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        # lists of ids and corners belonging to each id
        corners, ids, _ = aruco.detectMarkers(gray, self.arucoDict, parameters=self.parm)

        # Only continue if a marker was found and is the correct ID
        if np.all(ids != None):
            if (len(ids) != 1):
                pass
            elif (ids[0][0] == self.markerID):
                # Estimate the pose
                rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, self.lengthMarker, self.mtx, self.dist)

                # Save the distances
                self.North = (tvec[0][0][2]*100 - self.offsetNorth)
                self.East  = (tvec[0][0][0]*100 - self.offsetEast)
                self.Down  = (tvec[0][0][1]*100 - self.offsetDown)

                # Convert to rotation matrix and extract yaw
                R, _ = cv2.Rodrigues(rvec)
                eulerAngles = self.rotationMatrixToEulerAngles(R)
                self.Yaw = eulerAngles[1]
            else:
                pass

        # Change state for controller class
        self.isReady = True

    def isRotationMatrix(self, R):
        # Checks if matrix is valid
        Rt = np.transpose(R)
        shouldBeIdentity = np.dot(Rt, R)
        I = np.identity(3, dtype = R.dtype)
        n = np.linalg.norm(I - shouldBeIdentity)
        return n < 1e-6

    def rotationMatrixToEulerAngles(self, R):
        # Check if rotation matrix is valid
        assert(self.isRotationMatrix(R))

        # Check if singular
        sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])

        if (sy < 1e-6):
            # Singular
            x = math.atan2(-R[1,2], R[1,1])
            y = math.atan2(-R[2,0], sy)
            z = 0
        else:
            # Not singular
            x = math.atan2(R[2,1] , R[2,2])
            y = math.atan2(-R[2,0], sy)
            z = math.atan2(R[1,0], R[0,0])

        # Return roll, pitch, and yaw in some order
        return np.array([x, y, z])

    def close(self):
        # Close the pose processing thread
        self.isRunPose = False
        self.poseThread.join()
        print('\nFrame processing thread closed')

        # Close the capture thread
        self.isRunFrame = False
        self.frameThread.join()
        print('Camera thread closed')

        # Rlease the camera connection
        self.cam.release()
        print('Camera closed')
