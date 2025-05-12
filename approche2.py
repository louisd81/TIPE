import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt

lower_bound = np.array([0, 100, 100])
upper_bound = np.array([10, 255, 255])

targetDirectory = "C:/Users/louis/OneDrive/Documents/TIPE"
mp4files = glob.glob(targetDirectory + '/*.mp4')

def position():
    x = []
    y = []
    for videofile in mp4files:
    cap = cv2.VideoCapture(videofile)

    while True:
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 10:
                M = cv2.moments(contour)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                x.append(cx)
                y.append(cy)
                print(f"Red object at ({cx}, {cy})")

        scale_percent = 50  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return x,y 

def calcul():
    # Calculate potential energy using the y positions
    g = 9.81  # acceleration due to gravity
    y_min = np.min(y)  # assume ground level
    potential_energy = 0.1 * g * (y - y_min)

    # Calculate kinetic energy using the constant velocity
    velocity = 1  # m/s
    kinetic_energy = 0.5 * 0.1 * velocity**2

# Calculate mechanical energy
    mechanical_energy = potential_energy + kinetic_energy

    # Plot the energies
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Frame')
    ax1.set_ylabel('Potential Energy (J)', color=color)
    ax1.plot(potential_energy, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Kinetic Energy (J)', color=color)  # we already handled the x-label with ax1
    ax2.plot(kinetic_energy, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    # Plot mechanical energy
    ax3 = ax1.twinx()  # instantiate a third axes that shares the same x-axis
    ax3.spines["right"].set_position(("axes", 1.2))

    color = 'tab:green'
    ax3.set_ylabel('Mechanical Energy (J)', color=color)  # we already handled the x-label with ax1
    ax3.plot(mechanical_energy, color=color)
    ax3.tick_params(axis='y', labelcolor=color)

    plt.show()

calcul()
