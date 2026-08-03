import time
import logging
from Eng_Console import cycle_ecs
from GM_Algorithm import main as open_OSTest, run_scan, click_button, debug_setup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# freq = [25, 37, 50, 67, 75, 95, 100, 125, 150, 175, 200, 212, 225, 237, 250, 275, 300]
# angle = [70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5]
# ✅ define inputs
freq = "125"
angle = "55"

freq = [25, 37, 50, 67, 75, 95, 100, 125, 150, 175, 200, 212, 225, 237, 250, 275, 300]
angle = [70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5]



galvo = "H_Galvo"
Scan = "H Scan"


galvo = "2D_Galvo"
Scan = "2D Scan"

freq = [125]
angle = [55, 40, 10, 50]

freq = [str(f) for f in freq]
angle = [str(a) for a in angle]


def main():
    # ✅ Step 1: Launch & configure FPGA tool
    time.sleep(3)
    open_OSTest()
    app, window = debug_setup()

    for f in freq:
        for a in angle:
            pm1, pm2 = run_scan(f, a, galvo, Scan)

            pm1_val = float(pm1)
            pm2_val = float(pm2)

            if pm1_val < 1 or pm2_val < 1:
                click_button(window, "Close")
                time.sleep(3)
                cycle_ecs()
                time.sleep(3)
                open_OSTest()

        logger.info("Testing Complete.")



scan_cases = [
    (50, [16, 14.845]),
    (125, [10, 7.07]),
    (200, [10, 7.07]),
    (237, [13, 11.31]),
]

def Safety_Checks():
    time.sleep(3)

    open_OSTest()
    app, window = debug_setup()

    for freq, angles in scan_cases:
        for angle in angles:

            # convert to string for your UI functions
            f = str(freq)
            a = str(angle)

            pm1, pm2 = run_scan(f, a, galvo, Scan)

            pm1_val = float(pm1)
            pm2_val = float(pm2)

            if pm1_val < 1 or pm2_val < 1:
                click_button(window, "Close")
                time.sleep(3)

                cycle_ecs()
                time.sleep(3)

                open_OSTest()
                app, window = debug_setup()   # ✅ IMPORTANT (reconnect)

    logger.info("Testing Complete.")


if __name__ == "__main__":
    main()
    Safety_Checks()

# cd desktop
# cd Desktop\AutomatedTesting
# python -i Run_GM.py

# python -i Eng_Console.py


# Note, with bypass ECS cycle not required.
