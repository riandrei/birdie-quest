import pygame
import configs
import assets
import cv2 as cv
import mediapipe as mp
import threading
import queue
import time
import json

from objects.background import Background
from objects.floor import Floor
from objects.obstacle import Obstacle
from objects.bird import Bird
from objects.score import Score
from objects.menu import Menu
from objects.game_over import GameOver
from objects.scores import Scores, get_scores_file_path

pygame.init()
pygame.display.set_caption('Flight Frenzy')

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT)) 
clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameover = False
gamestarted = False

assets.load_sprites()

pygame.display.set_icon(assets.get_sprite('blue_lost'))

sprites = pygame.sprite.LayeredUpdates()

def create_sprites():
    Background(0, sprites)
    Background(1, sprites)

    Floor(0, sprites)
    Floor(1, sprites)

    return Bird(sprites), Score(sprites), Menu(sprites), GameOver(sprites), Scores(sprites)

bird, score, menu, game_over_object, scores = create_sprites()


# Initialize OpenCV and MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
VID_CAP = cv.VideoCapture(0)
VID_CAP.set(cv.CAP_PROP_FPS, 15)  # Limit webcam to 15 FPS

# Queue for face mesh results
face_data_queue_y = queue.Queue()
face_data_queue_x = queue.Queue()

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
                nose_x = results.multi_face_landmarks[0].landmark[94].x
                face_data_queue_y.put(nose_y)
                face_data_queue_x.put(nose_x)


# Start face mesh processing in a separate thread
threading.Thread(target=process_face_mesh, daemon=True).start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == column_create_event:
            Obstacle(sprites)
        if scores.show_scores:
            scores_action = scores.handle_event(event)

            if scores_action is not None:   
                if scores_action == 0:
                    menu.show_menu = True
                    scores.clear()
                    sprites.empty()
                    bird, score, menu, game_over_object, scores = create_sprites()
                    pass
        elif menu.show_menu:
            action = menu.handle_event(event)
            if action is not None:
                if action == 0:
                    menu.show_menu = False
                    clear = menu.clear()
                    gamestarted = True
                    pygame.time.set_timer(column_create_event, 2500)
                    pass
                elif action == 1:
                    menu.show_menu = False
                    clear = menu.clear()
                    scores = Scores(sprites)
                    scores.show_scores = True
                    sprites.draw(screen)
                    pygame.display.flip()   
                    pass
                elif action == 2:
                    running = False
                    pass
        if gameover:
            action = game_over_object.handle_event(event)
            if action is not None:
                if action == 0:
                    gameover = False
                    sprites.empty()
                    bird, score, menu, game_over_object, scores = create_sprites()
                    gamestarted = True
                    menu.show_menu = False
                    menu.clear()
                    game_over_object.clear()
                    scores.clear()
                elif action == 1:
                    gameover = False
                    sprites.empty()
                    bird, score, menu, game_over_object, scores = create_sprites()
                    gamestarted = False
                    game_over_object.clear()
                    scores.clear()

    if menu.show_menu:
        sprites.draw(screen)
        menu.update()
        pygame.display.flip()
        game_over_object.clear()
        scores.clear()
    
    if gameover:
        sprites.draw(screen)
        game_over_object.update()
        pygame.display.flip()

    if scores.show_scores:
        sprites.draw(screen)
        scores.update()
        pygame.display.flip()

    if gamestarted:
        # Update bird position based on the latest nose position in the queue
        if not face_data_queue_x.empty() and not face_data_queue_y.empty():
            nose_y = face_data_queue_y.get()
            nose_x = face_data_queue_x.get()
            
            bird.update_marker_position(nose_x, nose_y)

        screen.fill((255, 255, 255))
        sprites.draw(screen)

        if not gameover:
            sprites.update()

        if bird.check_collision(sprites) and not gameover:
            gameover = True
            game_over_object = GameOver(sprites, score.value)

            scores_file_path = get_scores_file_path()
            scores_data = Scores.load_scores(Scores)
            if score.value > 0:
                if len(scores_data) < 10:
                    scores_data.append((score.value, time.strftime("%m-%d-%y")))
                    with open(scores_file_path, 'w') as file:
                        json.dump(scores_data, file)
                else:
                    scores_data[-1] = (score.value, time.strftime("%m-%d-%y"))
                    with open(scores_file_path, 'w') as file:
                        json.dump(scores_data, file)

        for sprite in sprites:
            if type(sprite) is Obstacle and sprite.is_passed(bird.rect.x):
                score.value += 1

        # Update display
        pygame.display.flip()
        clock.tick(configs.FPS)

# Release resources
VID_CAP.release()
cv.destroyAllWindows()
pygame.quit()
