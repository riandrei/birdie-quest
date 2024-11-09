import pygame
import configs
import assets
from objects.background import Background
from objects.floor import Floor
from objects.obstacle import Obstacle
from objects.bird import Bird
import cv2 as cv
import mediapipe as mp
import threading
import queue
import time

pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT)) 
clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameover = False

assets.load_sprites()

sprites = pygame.sprite.LayeredUpdates()

Background(0, sprites)
Background(1, sprites)

Floor(0, sprites)
Floor(1, sprites)

bird = Bird(sprites)

pygame.time.set_timer(column_create_event, 2500)

# Initialize OpenCV and MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
VID_CAP = cv.VideoCapture(0)
VID_CAP.set(cv.CAP_PROP_FPS, 15)  # Limit webcam to 15 FPS

# Queue for face mesh results
face_data_queue = queue.Queue()

def process_face_mesh():
    with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7) as face_mesh:
        
        while running:
            # Capture frame
            ret, frame = VID_CAP.read()
            if not ret:
                continue

            # Resize and process frame
            frame = cv.resize(frame, (320, 240))
            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)

            # Get nose position if face is detected
            if results.multi_face_landmarks:
                nose_y = results.multi_face_landmarks[0].landmark[94].y
                face_data_queue.put(nose_y)

# Start face mesh processing in a separate thread
threading.Thread(target=process_face_mesh, daemon=True).start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == column_create_event:
            Obstacle(sprites)

    # Update bird position based on the latest nose position in the queue
    if not face_data_queue.empty():
        nose_y = face_data_queue.get()
        bird.update_marker_position(nose_y)

    sprites.draw(screen)

    if not gameover:
        sprites.update()

    if bird.check_collision(sprites):
        gameover = True

    # Update display
    pygame.display.flip()
    clock.tick(configs.FPS)

# Release resources
VID_CAP.release()
cv.destroyAllWindows()
pygame.quit()
