from filter import MovingAverage
import pandas as pd
import datetime
import time
import math

class Controller:
    def __init__(self, vehicle):
        # Vehicle class
        self.UAV = vehicle

        # Maximum controller output constraints
        self.rollConstrain  = [-4, 4]               # Deg
        self.pitchConstrain = self.rollConstrain    # Deg
        self.thrustConstrain = [-0.5, 0.5]	        # Normalized
        self.yawRateConstrain = [-10, 10]           # Deg / s
        self.derivativeGainConstrain = [-125, 125]  # [ ]

        # PID Gains: NORTH (pitch)
        self.kp_NORTH = 0.17
        self.ki_NORTH = 0.015   # Max 3 deg with 200 bounds
        self.kd_NORTH = 0.08

        # PID Gains: EAST (roll)
        self.kp_EAST = 0.16
        self.ki_EAST = 0.015    # Max 3 deg with 200 bounds
        self.kd_EAST = 0.11

        # PID Gains: DOWN (thrust)
        self.kp_DOWN = 0.002
        self.ki_DOWN = 0.00008   # Max 0.04 with 500 bounds
        self.kd_DOWN = 0

        # PID Gains: YAW (yaw rate)
        self.kp_YAW = 0.20
        self.ki_YAW = 0.02
        self.kd_YAW = 0.00

        # Cutoff height
        self.gainHeight = 25.0
        
        # Landing check 
        self.landErrorNE = 5.0
        self.landErrorD  = 10.0
        self.landHeight  = 15.0
        self.landCount   = 0 
        self.landCountRequired = 45

        # Previous errors
        self.northPrevError = 0
        self.eastPrevError = 0
        self.downPrevError = 0
        self.yawPrevError = 0

        # Integral tracking
        self.northI = 0
        self.eastI = 0
        self.downI = 0
        self.yawI = 0

        # Integral term constraints
        self.northIcontstrain = [-200, 200]
        self.eastIcontstrain  = self.northIcontstrain
        self.downIcontstrain  = [-500, 500]
        self.yawIcontstrain   = [-500, 500]

        # Timing
        self.timer = None

        # Data logging
        self.tempData = []
        self.data = []
        
        # Low pass filter for D term
        self.nAvg = MovingAverage(5)
        self.eAvg = MovingAverage(5)
        self.dAvg = MovingAverage(5)
        self.yAvg = MovingAverage(5)
        
    def startController(self):
        self.resetController()
        self.sendAttitudeTarget(0, 0, 0, 0.5)
        self.timer = time.time()
        self.startTime = time.time()

    def resetController(self):
        # Reset integral terms
        self.northI = 0
        self.eastI = 0
        self.downI = 0
        self.yawI = 0
        
        # Reset landing counter 
        self.landCount = 0
        
        # Reset timer 
        self.timer = time.time()

    def euler2quaternion(self, roll, pitch, yaw):
        # Convert degrees to radians 
        roll = math.radians(roll)
        pitch = math.radians(pitch)
        yaw = math.radians(yaw)
        
        # Euler angles (rad) to quaternion
        yc = math.cos(yaw * 0.5)
        ys = math.sin(yaw * 0.5)
        rc = math.cos(roll * 0.5)
        rs = math.sin(roll * 0.5)
        pc = math.cos(pitch * 0.5)
        ps = math.sin(pitch * 0.5)

        q0 = yc * rc * pc + ys * rs * ps
        q1 = yc * rs * pc - ys * rc * ps
        q2 = yc * rc * ps + ys * rs * pc
        q3 = ys * rc * pc - yc * rs * ps

        return [q0, q1, q2, q3]

    def sendAttitudeTarget(self, roll, pitch, yawRate, thrustRate):
        # Convert from degrees to radians
        yawRate = math.radians(yawRate)

        # https://mavlink.io/en/messages/common.html#SET_ATTITUDE_TARGET
        # https://ardupilot.org/dev/docs/copter-commands-in-guided-mode.html#copter-commands-in-guided-mode-set-attitude-target
        msg = self.UAV.message_factory.set_attitude_target_encode(
            0, # time_boot_ms
            0, # Target system
            0, # Target component
            0b00000000, # If bit is set corresponding input ignored (mappings)
            self.euler2quaternion(roll, pitch, 0), # Quaternion
            0, # Body roll rate in radian
            0, # Body pitch rate in radian
            yawRate,   # Body yaw rate in rad/s
            thrustRate # Thrust
        )
        
        # Send the constructed message
        self.UAV.send_mavlink(msg)

    def getVehicleAttitude(self):
        # Actual vehicle attitude
        roll  = math.degrees(self.UAV.attitude.roll)
        pitch = math.degrees(self.UAV.attitude.pitch)
        yaw   = math.degrees(self.UAV.attitude.yaw)
        return roll, pitch, yaw
       
    def constrain(self, val, minVal, maxVal):
        return max(min(maxVal, val), minVal)

    def PID(self, error, errorPrev, I, dt, kp, ki, kd, filt, debug=False):
        # Run the PID controller
        P = error
        I = I + error * dt
        D = filt.update(self.constrain((error - errorPrev) / dt, self.derivativeGainConstrain[0], self.derivativeGainConstrain[1]))
        PID = (kp * P) + (ki * I) + (kd * D)

        # Logging
        self.tempData.extend([kp, ki, kd, I, P*kp, I*ki, D*kd, (PID)])
        
        # Debugging
        if debug is True:
            print('{:<8.0f} {:<8.0f} {:<8.0f} {:<8.2f} {:<8.2f} {:<8.2f} {:<8.2f}'.format(error, 1/dt, I, P*kp, I*ki, D*kd, (PID)))
        
        # Return values 
        return PID, I

    def positionControl(self, actual, desired):
        # Error calculations
        errorNorth = desired[0] - actual[0]
        errorEast  = desired[1] - actual[1]
        errorDown  = desired[2] - actual[2]
        errorYaw   = desired[3] - actual[3]

        # Get time delta
        dt = time.time() - self.timer
        self.timer = time.time()
            
        # Run the remainder of the control
        rollControl, self.eastI   = self.PID(errorEast, self.eastPrevError, self.eastI, dt, self.kp_EAST, self.ki_EAST, self.kd_EAST, self.eAvg)
        pitchControl, self.northI = self.PID(errorNorth, self.northPrevError, self.northI, dt, self.kp_NORTH, self.ki_NORTH, self.kd_NORTH, self.nAvg)
        thrustControl, self.downI = self.PID(errorDown, self.downPrevError, self.downI, dt, self.kp_DOWN, self.ki_DOWN, self.kd_DOWN, self.dAvg)
        yawControl, self.yawI     = self.PID(errorYaw, self.yawPrevError, self.yawI, dt, self.kp_YAW, self.ki_YAW, self.kd_YAW, self.yAvg)
        
        # Constrain I terms to prevent integral windup
        self.northI = self.constrain(self.northI, self.northIcontstrain[0], self.northIcontstrain[1])
        self.eastI  = self.constrain(self.eastI, self.eastIcontstrain[0], self.eastIcontstrain[1]) 
        self.downI  = self.constrain(self.downI, self.downIcontstrain[0], self.downIcontstrain[1])
        self.yawI   = self.constrain(self.yawI, self.yawIcontstrain[0], self.yawIcontstrain[1])

        # Update previous error
        self.northPrevError = errorNorth
        self.eastPrevError  = errorEast
        self.downPrevError  = errorDown
        self.yawPrevError   = errorYaw

        # Constrain the controller values
        rollAngle  = self.constrain(rollControl, self.rollConstrain[0], self.rollConstrain[1])
        pitchAngle = self.constrain(pitchControl, self.pitchConstrain[0], self.pitchConstrain[1])
        thrust     = self.constrain(thrustControl, self.thrustConstrain[0], self.thrustConstrain[1])
        yawRate    = self.constrain(yawControl, self.yawRateConstrain[0], self.yawRateConstrain[1])

        # Inverse direction of controller if required
        rollAngle  = rollAngle
        pitchAngle = -pitchAngle
        thrust     = thrust + 0.5
        yawRate    = -yawRate

        # Mixer -> Psi: SITL (+), actual (-)
        psi = -math.radians(actual[3])
        pitchAngleTemp = pitchAngle*math.cos(psi) - rollAngle*math.sin(psi)
        rollAngleTemp = pitchAngle*math.sin(psi) + rollAngle*math.cos(psi)
        pitchAngle = pitchAngleTemp
        rollAngle = rollAngleTemp

        # Check if UAV has landed
        if ((abs(errorNorth) < self.landErrorNE) and (abs(errorEast) < self.landErrorNE) and 
                (actual[2] < self.landHeight) and (self.landCount >= self.landCountRequired) and 
                (abs(errorDown) < self.landErrorD)):
            landState = True
        elif ((abs(errorNorth) < self.landErrorNE) and (abs(errorEast) < self.landErrorNE) and 
                (actual[2] < self.landHeight) and (abs(errorDown) < self.landErrorD)):
            self.landCount += 1
            landState = False
        else:
            landState = False

        # Hard set gain schedule
        if (actual[2] < self.gainHeight) and (errorDown < 0):
            thrust = 0.4
        
        # Log temp data
        self.tempData.extend([errorNorth, desired[0], actual[0],
                              errorEast , desired[1], actual[1],
                              errorDown , desired[2], actual[2],
                              errorYaw  , desired[3], actual[3],
                              rollAngle, pitchAngle, yawRate, thrust, dt, time.time()-self.startTime, self.UAV.mode.name])

        # Save data and reset temp 
        self.data.append(self.tempData)
        self.tempData = []
        
        # Return the values
        return rollAngle, pitchAngle, yawRate, thrust, landState

    def logData(self, now):
        # Write data to a data frame
        df = pd.DataFrame(self.data, columns=['E-kp', 'E-ki', 'E-kd', 'E-I-Tot', 'E-P', 'E-I', 'E-D', 'E-PID',
                                              'N-kp', 'N-ki', 'N-kd', 'N-I-Tot', 'N-P', 'N-I', 'N-D', 'N-PID',
                                              'D-kp', 'D-ki', 'D-kd', 'D-I-Tot', 'D-P', 'D-I', 'D-D', 'D-PID',
                                              'Y-kp', 'Y-ki', 'Y-kd', 'Y-I-Tot', 'Y-P', 'Y-I', 'Y-D', 'Y-PID',
                                              'errorN', 'desiredN', 'actualN',
                                              'errorE', 'desiredE', 'actualE',
                                              'errorD', 'desiredD', 'actualD',
                                              'errorY', 'desiredY', 'actualY',
                                              'roll', 'pitch', 'yaw-rate', 'thrust', 'dt', 'Time', 'Mode'])

        # Save data to CSV
        fileName = 'flightData/' + now.strftime('%Y-%m-%d__%H-%M-%S--CONTROL') + '.csv'
        df.to_csv(fileName, index=None, header=True)
        print('Control log saved to: ' + fileName)
