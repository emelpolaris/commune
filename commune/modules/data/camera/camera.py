import cv2
import threading
from threading import Thread, Event
import time
from datetime import datetime
import os
import gradio as gr
import commune as c


class Camera(c.Module):
    def __init__(self):
        self.rtsp_streams = self.get_cameras()
        self.event = Event()
        self.frame_buffer = [None]
        self.flag_capture = False
    def set_config(self, rtsp_stream):
        self.rtsp_stream = rtsp_stream
        self.cap = cv2.VideoCapture(self.rtsp_stream)        
        self.capture_thread = threading.Thread(target=self.capture_frames, args=(self.event, self.cap))
        
    def get_cameras(self, filename: str="cameralist.txt"):
        if not os.path.exists(filename):
            return []
        camerafile = open(filename, "r")
        cameralist = camerafile.readlines()
        cameralist = [camera[:-1] for camera in cameralist]
        camerafile.close()
        return cameralist
    def capture_frames(self, event: Event, cap):
        # Video reader        
        while True:
            ret, frame = cap.read()
            if not ret:
                print(f"Error reading frame from camera. Attempting to reconnect...")
                time.sleep(3)
                continue
            
            self.flag_capture = True
            self.frame_buffer = frame            
            
            if event.is_set():
                print('The thread was stopped prematurely.')
                break
            
    # Function to save screenshot when 's' key is pressed
    def save_screenshot(self, event: Event, folder_name: str="Image", ):
        while True:            
            if self.flag_capture == False:                
                continue
            screenshot = cv2.resize(self.frame_buffer, (800, 600))            
            cv2.imshow("Frame", screenshot)
            if cv2.waitKey(1) & 0xFF == ord('s'):                
                if screenshot is not None:
                    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    screenshot_name = os.path.join(folder_name, f"screenshot_{current_time}.png")
                    cv2.imwrite(screenshot_name, screenshot)
                    print(f"Screenshot saved: {screenshot_name}")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                event.set()
            if event.is_set():
                print('The thread was stopped prematurely.')
                break
    def gradio(self):
        with gr.Blocks(title="Stable Diffusion", css="#vertical_center_align_markdown { position:absolute; top:30%;background-color:white;} .white_background {background-color: #ffffff} .none_border {border: none;border-collapse:collapse;}") as demo:
            with gr.Column():
                with gr.Group():
                    gr.Markdown("## &nbsp;1. Configure camera")
                    with gr.Row():
                        camera_ip = gr.Dropdown(self.rtsp_streams, value=self.rtsp_streams[0], label="Select Camera", info="Choose IP addresses",)
                        folder_name_textbox = gr.Textbox(value="Frames", label="Saving Folder", visible=True, interactive=True, type="text")
                    with gr.Row():
                        username_textbox = gr.Textbox(value="", label="User", visible=True, interactive=True, type="text")
                        password_textbox = gr.Textbox(value="", label="Password", visible=True, interactive=True, type="password")
                        
                with gr.Group():
                    gr.Markdown("## &nbsp;2. Capture Frames")
                    with gr.Column():
                        with gr.Column():
                            output_img = gr.Image(label="Frame", visible=True, interactive=True)
                        with gr.Column():
                            with gr.Row():                                                         
                                start_btn = gr.Button(value="Start Capturing", scale=1, interactive=True)
                                                                
                                quit_btn = gr.Button(value="Quit", scale=1, interactive=True)
                            with gr.Row():
                                save_btn = gr.Button(value="Save", scale=1, interactive=False)
                                show_btn = gr.Button(value="Show", scale=1, interactive=False)
            ### Actions
                        
            def capture_frame(camera_ip, username_textbox, password_textbox):
                self.event = Event()
                rtsp_stream = f"rtsp://{username_textbox}:{password_textbox}@{camera_ip}"
                print(f"**************{rtsp_stream}***************")
                self.set_config(rtsp_stream,)
                self.capture_thread.start()
                while True:
                    if self.flag_capture == True:
                        break
                return gr.update(interactive=False), gr.update(interactive=True), gr.update(interactive=True)
               
            def frame_show():
                while True:
                    if self.flag_capture == True:
                        break               
                return gr.update(value=self.frame_buffer)
            
            def save_frame(folder_name_textbox):
                if not os.path.exists(folder_name_textbox):
                    os.mkdir(folder_name_textbox)               
                screenshot = cv2.resize(self.frame_buffer, (800, 600))                                          
                if screenshot is not None:
                    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    base_path = os.getcwd()
                    screenshot_name = os.path.join(base_path, folder_name_textbox, f"screenshot_{current_time}.png")
                    cv2.imwrite(screenshot_name, screenshot)
                    print(f"Screenshot saved: {screenshot_name}")
                    
            def quit_capture():
                self.event.set()
                return gr.update(interactive=True)            
            
            def select_camera():
                self.event.set()
                return gr.update(interactive=True), gr.update(interactive=False), gr.update(interactive=False)
            
            ### Add functions to component            
            camera_ip.change(select_camera, outputs=[start_btn, save_btn, show_btn,], queue=False,)
            start_btn.click(capture_frame, inputs=[camera_ip, username_textbox, password_textbox], outputs=[start_btn, save_btn, show_btn], queue=False,)
            save_btn.click(save_frame, inputs=[folder_name_textbox], queue=False,)
            quit_btn.click(quit_capture, outputs=[start_btn], queue=False)
            show_btn.click(frame_show, outputs=[output_img], queue=False)            
            
        demo.launch(share=True)
