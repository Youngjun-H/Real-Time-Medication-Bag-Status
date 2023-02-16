# Real-Time-Medication-Bag-Status

### Setup Raspberry pI for Tflite

```python

  # Update packages on your Raspberry Pi OS.
  sudo apt-get update

  # Check your Python version. You should have Python 3.7 or later.
  python3 --version

  # Install virtualenv and upgrade pip.
  python3 -m pip install --user --upgrade pip
  python3 -m pip install --user virtualenv

  # Create a Python virtual environment for the TFLite samples (optional but strongly recommended)
  python3 -m venv ~/tflite

  # Run this command whenever you open a new Terminal window/tab to activate the environment.
  source ~/tflite/bin/activate

  # Clone the TensorFlow example repository with the TFLite Raspberry Pi samples.
  git clone https://github.com/tensorflow/examples.git
  cd examples/lite/examples/object_detection/raspberry_pi

  # Install dependencies required by the sample
  sh setup.sh
  
```
