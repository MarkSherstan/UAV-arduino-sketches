from threading import Thread
import cv2.aruco as aruco
from T265 import T265
import numpy as np
import math
import time
import cv2

class Vision:
    def __init__(self):
        # Performance parameters
        self.startTime = None
        self.endTime   = None
        self.counter   = 0

        # Camera calibration matrices 
        self.mtx1 = np.array([[284.65527842,  0.0,            420.10118496],
                        [0.0,           285.43891088,   403.82029423],
                        [0.0,           0.0,            1.0         ]])
        self.dist1 = np.array([[-0.01159942, 0.00393409, 0.00059457, -0.0002535, -0.0006091]])

        self.mtx2 = np.array([[287.8954394,  0.0,            418.40412543],
                        [0.0,           287.99235758,   410.12408383],
                        [0.0,           0.0,            1.0         ]])
        self.dist2 = np.array([[-0.00818909, 0.00187817, 0.00132013, -0.00018278, -0.00044735]])
        
        # Camera to body frame values in cm
        self.offset1 = [-2.3, -15.0, 0]
        self.offset2 = [4.1, -15.0, 0]
    
    def run(self, Q):
        # Start the connection to the T265
        cam = T265()

        # Start the threads
        VP1 = VisionPose(ID='1', mtx=self.mtx1, dist=self.dist1, offset=self.offset1)
        VP1.startThread(cam.Img1)
        
        VP2 = VisionPose(ID='2', mtx=self.mtx2, dist=self.dist2, offset=self.offset2)
        VP2.startThread(cam.Img2)
        
        # Start the main thread timer
        self.startTime = time.time()

        # Process data until closed
        try: 
            while(True):
                # Get data from T265
                VP1.updateImg(cam.Img1)
                VP2.updateImg(cam.Img2)
                psiRate = cam.psiRate   # Deg/s
                vN  = cam.vz * -100.0   # Cm/s
                vE  = cam.vx *  100.0   # Cm/s
                vD  = cam.vy *  100.0   # Cm/s

                # Average the results between cameras
                North = (VP1.N + VP2.N) / 2.0
                East  = (VP1.E + VP2.E) / 2.0
                Down  = (VP1.D + VP2.D) / 2.0
                Yaw   = (VP1.Y + VP2.Y) / 2.0
                
                # Add data to the queue
                Q.put([North, East, Down, vN, vE, vD, Yaw, psiRate])

                # Increment the counter 
                self.counter += 1

        except KeyboardInterrupt:
            # Prep to close
            self.endTime = time.time()
            print('Closing Vision!')
        
        finally: 
            # Close all the threads
            cam.close()
            VP1.close()
            VP2.close()
            
            # Performance of main thread
            print('Main vision thread rate: ', round(self.loopCount / (self.endTime - self.startTime),1))

class VisionPose:
    def __init__(self, ID, mtx, dist, offset, lengthMarker=6.43, spacing=3.22):        
        # ID
        self.ID = ID
        
        # Camera parameters (intrinsic and extrensic)
        self.mtx = mtx
        self.dist = dist
        self.offset = offset
        
        # Initial conditions for pose calculation 
        self.rvec = None
        self.tvec = None
        
        # Threading parameters
        self.isReceiving = False
        self.isRun = True
        self.threadX = None

        # Performance
        self.startTime = None
        self.endTime = None
        self.loopCounter = 0
        self.poseCounter = 0
        
        # Aruco dictionary and parameter to be used for pose processing
        self.arucoDict = aruco.custom_dictionary(17, 3)
        self.parm = aruco.DetectorParameters_create()
        self.parm.cornerRefinementMethod = aruco.CORNER_REFINE_SUBPIX
        self.parm.cornerRefinementWinSize = 5
        self.parm.cornerRefinementMaxIterations = 100
        self.parm.cornerRefinementMinAccuracy = 0.00001

        # Create the ArUco board
        self.board = aruco.GridBoard_create(
            markersX=4,                 # Columns
            markersY=3,                 # Rows
            markerLength=lengthMarker,  # cm
            markerSeparation=spacing,   # cm
            dictionary=self.arucoDict)

        # Output variables: Position of body frame wrt ArUco frame (observing from above)
        #   North (negative when UAV is behind the target)
        #   East  (negative when UAV is to the left of the target)
        #   Down  (negative when UAV is below the target -> always positive)
        #   Yaw   (Positive counter clockwise viewing UAV from top)
        self.N = 0
        self.E = 0
        self.D = 0
        self.Y = 0

    def startThread(self, img):
        # Initialize an image before start
        self.gray = img
        
        # Create a thread
        if self.threadX == None:
            self.threadX = Thread(target=self.run)
            self.threadX.start()
            print('Thread ' + self.ID + ' start.')

            # Block till we start receiving values
            while self.isReceiving != True:
                time.sleep(0.1)

            # Start the timer and reset counters
            self.loopCounter = 0
            self.poseCounter = 0
            self.startTime = time.time()
    
    def run(self):
        # Run until thread is closed
        while(self.isRun):
            self.getPose()
            self.loopCounter += 1
            self.isReceiving = True
        
        # Record end time 
        self.endTime = time.time()
        
    def updateImg(self, img):
        self.gray = img
        
    def getPose(self):
        # lists of ids and corners belonging to each id
        corners, ids, _ = aruco.detectMarkers(image=self.gray, dictionary=self.arucoDict, 
                                              parameters=self.parm, cameraMatrix=self.mtx, 
                                              distCoeff=self.dist)

        # Only estimate the pose if a marker was found
        if np.all(ids != None):
            _, self.rvec, self.tvec = aruco.estimatePoseBoard(corners=corners, ids=ids, board=self.board, 
                                                              cameraMatrix=self.mtx, distCoeffs=self.dist, 
                                                              rvec=self.rvec, tvec=self.tvec)
            
            # Convert from vector to rotation matrix and then transform to body frame
            R, _ = cv2.Rodrigues(self.rvec)
            R, t = self.transform2Body(R, self.tvec)

            # Get yaw
            _, _, yaw = self.rotationMatrix2EulerAngles(R)

            # Save values
            self.N = t[1] 
            self.E = t[0]
            self.D = t[2]
            self.Y = yaw
        
    def isRotationMatrix(self, R):
        # Checks if matrix is valid
        Rt = np.transpose(R)
        shouldBeIdentity = np.dot(Rt, R)
        I = np.identity(3, dtype = R.dtype)
        n = np.linalg.norm(I - shouldBeIdentity)
        return n < 1e-6

    def rotationMatrix2EulerAngles(self, R):
        try:
            # Check if rotation matrix is valid
            assert(self.isRotationMatrix(R))

            # Dont rotate more than 45 degrees in any direction and we will not get gimbal lock / singularities
            x = math.degrees(math.atan2(R[2,1], R[2,2]))
            y = math.degrees(-math.asin(R[2,0]))
            z = math.degrees(math.atan2(R[1,0], R[0,0]))
            
            # Return results
            return x, y, z
        except:
            # Return 0's upon failure
            print('Not a rotation matrix')
            return 0, 0, 0

    def transform2Body(self, R, t):
        # Original (ArUco wrt camera)
        Tca = np.append(R, t, axis=1)
        Tca = np.append(Tca, np.array([[0, 0, 0, 1]]), axis=0)

        # Transformation (camera wrt drone body frame)
        Tbc = np.array([[1,  0,  0,  self.offset[0]],
                        [0,  1,  0,  self.offset[1]],
                        [0,  0,  1,  self.offset[2]],
                        [0,  0,  0,  1]])

        # Resultant pose (ArUco wrt drone body frame)
        Tba = np.dot(Tbc, Tca)
        R = Tba[0:3,0:3]
        t = Tba[0:3,3]

        # Drone body frame wrt ArUco
        R = np.transpose(R)
        t = np.dot(-R, t)

        # Return reults 
        return R, t

    def close(self):
        # Close the thread
        self.isRun = False
        self.threadX.join()
        print('Thread ' + self.ID + ' closed.')
        
        # Print performance
        print('  Loop rate (' + self.ID + '): ', round(self.loopCounter / (self.endTime - self.startTime),1))
        print('  Pose rate (' + self.ID + '): ', round(self.poseCounter / (self.endTime - self.startTime),1))
