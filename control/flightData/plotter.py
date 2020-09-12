import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse

def General(df, fileName, saveFlag):
    # Find autonomous sections
    df['modeSwitch'] =  df['Mode'] == 'GUIDED_NOGPS'

    idx = [0]
    for ii in range(df.shape[0]-1):
        if (df['modeSwitch'][ii+1] == df['modeSwitch'][ii]):
            pass
        else:
            idx.append(ii)

    # Master
    fig = plt.figure(figsize=(11, 7), dpi=100)

    # Roll and Pitch
    plt.subplot(2, 2, 1)
    ax0 = plt.gca()

    df.plot(kind='line', x='Time', y='Roll-UAV',  color='#FB8604', alpha=0.5, style='-', ax=ax0)
    df.plot(kind='line', x='Time', y='Pitch-UAV', color='#700CBC', alpha=0.5, style='-', ax=ax0)

    df.plot(kind='line', x='Time', y='Roll-Control',  color='#FB8604', style='-', ax=ax0)
    df.plot(kind='line', x='Time', y='Pitch-Control', color='#700CBC', style='-', ax=ax0)

    ax0.set_title('Roll & Pitch Control', fontsize=14, fontweight='bold')
    ax0.set_xlabel('')
    ax0.set_ylabel('Angle [deg]', fontweight='bold')

    for ii in range(0,len(idx),2):
        plt.axvspan(df['Time'][idx[ii]], df['Time'][idx[ii+1]], color='gray', alpha=0.2)

    # Yaw
    plt.subplot(2, 2, 2)
    ax1 = plt.gca()

    df.plot(kind='line', x='Time', y='Yaw-Ang', color='tab:blue', style='-', ax=ax1)
    df.plot(kind='line', x='Time', y='Yaw-Control', color='tab:blue', style='--', ax=ax1)

    ax1.set_title('Yaw Control', fontsize=14, fontweight='bold')
    ax1.set_xlabel('')
    ax1.set_ylabel('Angle [Deg or Deg/s]', fontweight='bold')

    for ii in range(0,len(idx),2):
        plt.axvspan(df['Time'][idx[ii]], df['Time'][idx[ii+1]], color='gray', alpha=0.2)
    
    # North East
    plt.subplot(2, 2, 3)
    ax3 = plt.gca()

    df.plot(kind='line', x='Time', y='North-Pos', color='#700CBC', style='-',  ax=ax3)
    df.plot(kind='line', x='Time', y='East-Pos',  color='#FB8604', style='-',  ax=ax3)
    df.plot(kind='line', x='Time', y='Down-Pos',  color='#7FBD32', style='-',  ax=ax3)

    df.plot(kind='line', x='Time', y='North-Desired', color='#700CBC', style='--',  ax=ax3)
    df.plot(kind='line', x='Time', y='East-Desired',  color='#FB8604', style='--',  ax=ax3)
    df.plot(kind='line', x='Time', y='Down-Desired',  color='#7FBD32',  style='--', ax=ax3)

    ax3.set_title('NED Position', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Time [s]', fontweight='bold')
    ax3.set_ylabel('Position [cm]', fontweight='bold')

    ax3.legend(['N', 'E', 'D'])

    for ii in range(0,len(idx),2):
        plt.axvspan(df['Time'][idx[ii]], df['Time'][idx[ii+1]], color='gray', alpha=0.2)
    
    # Thrust
    plt.subplot(2, 2, 4)
    ax4 = plt.gca()

    df.plot(kind='line', x='Time', y='Thrust-Control', color='#7FBD32', style='-', ax=ax4)

    ax4.set_title('Thrust Control', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Time [s]', fontweight='bold')
    ax4.set_ylabel('Normalized Thrust Command', fontweight='bold')
    ax4.get_legend().remove()

    for ii in range(0,len(idx),2):
        plt.axvspan(df['Time'][idx[ii]], df['Time'][idx[ii+1]], color='gray', alpha=0.2)
    
    # Save the figure    
    if saveFlag is True:
        fig.savefig(str(fileName).replace('.csv','')+'-GENERAL.png', dpi=fig.dpi)

def FreqSleep(df, fileName, saveFlag): 
    # Create a figure
    fig = plt.figure(figsize=(12, 6), dpi=100)

    # Create subplot: Frequency
    plt.subplot(1, 2, 1)
    ax1 = plt.gca()

    # Plot data
    df.plot(kind='line', x='Time', y='Freq',  color='k',  style='-',  ax=ax1)

    # Format figure
    title = 'Sampling Frequency\n' + '{:<4.3f} +/- {:<0.3f} '.format(df['Freq'].mean(), df['Freq'].std())
    ax1.set_title(title, fontsize=14, fontweight='bold')
    ax1.set_xlabel('Time [s]', fontweight='bold')
    ax1.set_ylabel('Frequency [Hz]', fontweight='bold')
    ax1.get_legend().remove()


    # Create subplot: Sleep request
    plt.subplot(1, 2, 2)
    ax0 = plt.gca()

    # Plot data
    df['time2delay'] = df['time2delay'] * 1000
    df['actualDelay'] = df['actualDelay'] * 1000

    df.plot(kind='line', x='time2delay', y='actualDelay',  color='r',  style='+',  ax=ax0)

    # Figure formatting
    ax0.set_title('Sleep Request', fontsize=14, fontweight='bold')
    ax0.set_xlabel('Requested Sleep Time [ms]', fontweight='bold')
    ax0.set_ylabel('Actual Sleep Time [ms]', fontweight='bold')
    ax0.get_legend().remove()

    # Add grid
    plt.grid()

    # Save the figure 
    if saveFlag is True:
        fig.savefig(str(fileName).replace('.csv','')+'-FREQ_SLEEP.png', dpi=fig.dpi)

def DiffState(df, fileName, saveFlag):
    # Master
    fig = plt.figure(figsize=(12, 6), dpi=100)

    # Create subplot: NEDY Difference 
    plt.subplot(1, 2, 1)
    ax = plt.gca()

    # Plot data
    df.plot(kind='line', x='Time', y='North-Dif', color='tab:purple', style='-', ax=ax)
    df.plot(kind='line', x='Time', y='East-Dif',  color='tab:orange', style='-', ax=ax)
    df.plot(kind='line', x='Time', y='Down-Dif',  color='tab:green',  style='-', ax=ax)
    df.plot(kind='line', x='Time', y='Yaw-Dif',   color='tab:blue',   style='-', ax=ax)

    # Format figure
    ax.set_title('Difference Comparison', fontsize=14, fontweight='bold')
    ax.set_xlabel('Time [s]', fontweight='bold')
    ax.set_ylabel('Difference [Cm]', fontweight='bold')


    # Create subplot: Land and Queue
    plt.subplot(1, 2, 2)
    ax = plt.gca()

    # Plot data
    df['Landing-State'] = (df['Landing-State'] == True).astype(int)
    df.plot(kind='line', x='Time', y='Landing-State', color='k', style='-', ax=ax)
    df.plot(kind='line', x='Time', y='Q-Size', alpha=0.3, color='r', style='-', ax=ax)

    # Format Figure
    ax.set_title('State and Queue Check', fontsize=14, fontweight='bold')
    ax.set_xlabel('Time [s]', fontweight='bold')
    ax.set_ylabel('State [ ]', fontweight='bold')

    # Save the figure 
    if saveFlag is True:
        fig.savefig(str(fileName).replace('.csv','')+'-FREQ_SLEEP.png', dpi=fig.dpi)

########################
# Argparse
# Example use: python plotter.py --input "flight1.csv"
########################
parser = argparse.ArgumentParser()
parser.add_argument("--input", help = "input filename")
args = parser.parse_args()
fileName = args.input

# Prepare CSV
try:
    df = pd.read_csv(fileName, header = 0, names = ['Mode', 'Time', 
                            'Freq', 'time2delay', 'actualDelay',
                            'North-Desired', 'East-Desired', 'Down-Desired',
                            'Roll-UAV', 'Pitch-UAV', 'Yaw-UAV',
                            'Roll-Control', 'Pitch-Control', 'Yaw-Control', 'Thrust-Control',
                            'North-Pos', 'East-Pos', 'Down-Pos', 'Yaw-Ang',
                            'North-Vel', 'East-Vel', 'Down-Vel', 'Yaw-Vel',
                            'North-Acc', 'East-Acc', 'Down-Acc', 
                            'North-Raw', 'East-Raw', 'Down-Raw', 'Yaw-Raw',
                            'North-Dif', 'East-Dif', 'Down-Dif', 'Yaw-Dif',
                            'Landing-State', 'Q-Size'])
                            
except:
    print('Error with file.')
    exit()

# Plotting options
General(df.copy(), fileName, saveFlag=False)
FreqSleep(df.copy(), fileName, saveFlag=False)
DiffState(df.copy(), fileName, saveFlag=False)
plt.show()


# kalman filter 
# velocity / accel
