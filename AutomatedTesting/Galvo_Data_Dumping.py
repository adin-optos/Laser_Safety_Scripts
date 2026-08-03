import time

from Load_FPGA_Debug_Tool import main as run_fpga_debug_tool, data_dumping, Galvo_LUT_Change, LUT_dumping, Galvo_LUT_Swap
from Enter_Patient_Scan import main as run_scan, scan_patterns, enter_patient_name, debug_setup, finish_patient, click_button

def main():
    # ✅ Step 1: Launch & configure FPGA tool
    run_fpga_debug_tool()

    enter_patient_name()
    time.sleep(2)
    LUT_dumping()
    time.sleep(2)
    finish_patient()

    Galvo_LUT_Swap()
    time.sleep(1)
    enter_patient_name()
    time.sleep(2)
    LUT_dumping()
    time.sleep(2)
    finish_patient()

    # Galvo_LUT_Swap()
    # LUT_dumping()
    #
    # Galvo_LUT_Swap()

    # H_Galvo noise

    data_files = [
        "galvo_data_25_05_2026_12_41_20.csv",
        "galvo_data_25_05_2026_12_41_201.csv"
    ]

    for file in data_files:
        # ✅ Step 1: Apply LUT for this run
        Galvo_LUT_Change(file)

        enter_patient_name()

        # ✅ Step 2: Run scan
        run_scan(scan_patterns[2])

        # ✅ Step 3: Dump data
        data_dumping()

        # ✅ Step 4: Exit + finish
        finish_patient()



    # ✅ Step 2: Run scan selection (choose one or many)
    # run_scan(scan_patterns[2])  # example
    # data_dumping()

    # for v in scan_patterns:
    #     run_scan(v)
    #     data_dumping()

    # ✅ Step 3: Finish Patient & Change LUT
    # finish_patient()
    # Galvo_LUT_Change("galvo_data_25_05_2026_12_41_20.csv")


if __name__ == "__main__":
    main()



# we can do galvo dumping on live
# Next, dumping in capture
# Next galvo noise, moving galvo
# Exit cap-app to write galvo data, so need code to exit!


# python -i Galvo_Data_Dumping.py