import cv2
import numpy as np

def create_rounded_rect_mask(width, height, radius, channels=3):
    mask = np.zeros((height, width, channels), dtype=np.uint8)
    color = (255,) * channels

    # Create a rounded rectangle
    rectangle = np.zeros((height, width), dtype=np.uint8)
    rectangle = cv2.rectangle(rectangle, (radius, 0), (width - radius, height), color, -1)
    rectangle = cv2.rectangle(rectangle, (0, radius), (width, height - radius), color, -1)
    circle = cv2.circle(np.zeros((height, width), dtype=np.uint8), (radius, radius), radius, color, -1)
    rectangle = cv2.bitwise_or(rectangle, circle)
    circle = cv2.circle(np.zeros((height, width), dtype=np.uint8), (width - radius, radius), radius, color, -1)
    rectangle = cv2.bitwise_or(rectangle, circle)
    circle = cv2.circle(np.zeros((height, width), dtype=np.uint8), (radius, height - radius), radius, color, -1)
    rectangle = cv2.bitwise_or(rectangle, circle)
    circle = cv2.circle(np.zeros((height, width), dtype=np.uint8), (width - radius, height - radius), radius, color, -1)
    rectangle = cv2.bitwise_or(rectangle, circle)

    for i in range(channels):
        mask[:, :, i] = rectangle

    return mask

def create_mask(frame, scaled_width, scaled_height, final_resolution, corner_radius, gradient_color=None):
    # Create rounded rectangle mask and apply it to the frame
    mask = create_rounded_rect_mask(scaled_width, scaled_height, corner_radius, channels=frame.shape[2])
    masked_frame = cv2.bitwise_and(frame, mask)

    # Create a black background frame with gradient effect if gradient_color is provided
    if gradient_color:
        gradient_frame = np.zeros(final_resolution + (3,), dtype=frame.dtype)
        gradient_frame = cv2.rectangle(gradient_frame, (0, 0), (final_resolution[0], final_resolution[1]), gradient_color, -1)
        black_frame = cv2.addWeighted(gradient_frame, 0.5, masked_frame, 0.5, 0)
    else:
        black_frame = np.zeros(final_resolution + (3,), dtype=frame.dtype)
        x_offset = (final_resolution[0] - scaled_width) // 2
        y_offset = (final_resolution[1] - scaled_height) // 2
        black_frame[y_offset:y_offset+scaled_height, x_offset:x_offset+scaled_width] = masked_frame

    return black_frame

def process_video(input_video_path, output_video_path, scale_factor, final_resolution, corner_radius):
    cap = cv2.VideoCapture(input_video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Print resolution of input video
    input_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    input_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Input resolution:", input_width, input_height)
    print("Scale factor:", scale_factor)

    out = cv2.VideoWriter(output_video_path, fourcc, cap.get(cv2.CAP_PROP_FPS), final_resolution)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame to the new resolution while maintaining aspect ratio
        scaled_width = int(input_width * scale_factor)
        scaled_height = int(input_height * scale_factor)
        frame = cv2.resize(frame, (scaled_width, scaled_height), interpolation=cv2.INTER_LANCZOS4)

        black_frame = create_mask(frame, scaled_width, scaled_height, final_resolution, corner_radius=10)   

        out.write(black_frame)

    cap.release()
    out.release()

input_video_path = 'recording1.mov'
output_video_path = 'output_video.mp4'
process_video(input_video_path, output_video_path, scale_factor=0.5, final_resolution=(1080, 1080), corner_radius=10)
