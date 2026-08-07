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

## 4. Install Required Packages

Open **Command Prompt** and navigate to the `req` directory.

Install the required packages:

```cmd
python -m pip install -r req.txt
```

Wait for the installation to complete.

---

## 5. Navigate to the Test Directory

From Command Prompt:

```cmd
cd Desktop
cd Laser_Safety_Scripts-main
cd Laser_Safety_Scripts-main
cd AutomatedTesting
cd GM_Algorithm_Test
```

---

## 6. Run the Galvo Monitor Test

Run:

```cmd
python -i Run_GM.py
```

The test will start automatically.

---

## Notes

- The `-i` option keeps the Python interpreter open after the script completes.
- If package installation fails, verify that internet access is available.
- If multiple Python versions are installed, ensure Python 3.x is being used.
- Additional scripts and utilities can be run in the same manner as required.
