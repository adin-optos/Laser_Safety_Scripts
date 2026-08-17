# Automated Testing

This repository contains automation scripts for Systems and LSDV testing.

## Main Script

### Run_GM.py

`Run_GM.py` automates the Galvo Monitor algorithm trip test using OSTest.

All other scripts and utilities should be used as indicated by their filenames and inline code comments.

---

# Getting Started

Follow the steps below to set up and run the scripts.

## 1. Download the Repository

### Option 1: Clone the Repository

```cmd
git clone <repository_url>
```

### Option 2: Download ZIP

Download and extract the repository ZIP file to a suitable location.

---

## 2. Verify Python Installation

Open **Command Prompt** and check whether Python is installed:

```cmd
python --version
```

Expected output:

```text
Python 3.x.x
```

If Python is not found, search for an existing installation:

```cmd
where /r C:\ python.exe
```

If Python is not installed, download and install it from:

https://www.python.org/downloads/

When installing Python, ensure that **Add Python to PATH** is selected.

Verify Python and pip are accessible:

```cmd
python --version
python -m pip --version
```

---


## 3. Configure the PATH Environment Variable

Ensure the following directories are included in the **System PATH** environment variable:

```text
C:\Users\ServiceAdmin\AppData\Local\Programs\Python\Python312
```

```text
C:\Users\ServiceAdmin\AppData\Local\Programs\Python\Python312\Scripts
```

Verify that Python and pip are accessible:

```cmd
python --version
```

```cmd
python -m pip --version
```

Expected output:

```text
Python 3.x.x
```

```text
pip xx.x
```

---

## 4. Create a Virtual Environment

Navigate to the repository's `AutomatedTesting` directory:

```cmd
cd Desktop
cd Laser_Safety_Scripts-main
cd Laser_Safety_Scripts-main
cd AutomatedTesting
```

Create a virtual environment:

```cmd
python -m venv .venv
```

Activate the virtual environment:

```cmd
.venv\Scripts\activate
```

The command prompt should now display:

```text
(.venv)
```

at the beginning of the prompt.

---

## 5. Install Required Packages

With the virtual environment activated, install the required packages:

```cmd
python -m pip install -r req.txt
```

Wait for the installation to complete.

---

## 6. Install Additional Software

Some scripts require Digilent WaveForms hardware support libraries.

Install Digilent WaveForms if prompted by missing `dwf.dll` or `pydwf` errors:

https://digilent.com/shop/waveforms/

After installation, restart Command Prompt and reactivate the virtual environment before running the scripts.

---

## 7. Navigate to the Test Directory

```cmd
cd GM_Algorithm_Test
```

---

## 8. Run the Galvo Monitor Test

Run:

```cmd
python -i Run_GM.py
```

The test will start automatically.

---

## Notes

- The `-i` option keeps the Python interpreter open after the script completes.
- Always activate the virtual environment before running any scripts:
  ```cmd
  .venv\Scripts\activate
  ```
- If package installation fails, verify that internet access is available.
- If multiple Python versions are installed, ensure Python 3.x is being used.
- Additional scripts and utilities can be run in the same manner as required.
- To leave the virtual environment, run:
  ```cmd
  deactivate
  ```
