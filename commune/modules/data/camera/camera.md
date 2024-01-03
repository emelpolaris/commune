# Camera Capture

This module contains Python scripts that demonstrate how to capture frames from IP cameras using Gradio and OpenCV.

## Setup

Before getting started, be sure to the IP addresses, ports, routs, and user info such as an user name and password.

To set up and run this project, follow these steps:

1. Install the required packages with `pip`:

```bash
pip install -r requirements.txt
```

2. Add accessible cameras into the cameralist.txt:

While running the module, read the camera list saved in this file and capture frames from these cameras.

```
81.149.241.74:554/Streaming/Channels/101
81.149.241.74:1054/Streaming/Channels/101
```

## How to run.

```bash
c data.camera gradio
```

### Configure the camera
- Select camera
- Type in the saving folder
- Type in the user name.
- Type in the password
### Capture frames
- start capturing
    Start the thread capturing frames from selected camera.
- show
    Show captured frame
- Save
    Save captured frame in the selected folder with a particular formated name.
## License

[MIT License](LICENSE)
