import cv2
import mediapipe as mp
import numpy as np
import serial
import time

# Inicializamos la comunicación con el arduino a través del puerto serial
arduino = serial.Serial('COM7', 9600)
time.sleep(2)

# Inicializamos los módulos de MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Iniciamos la captura de video desde la cámara (0 = cámara por defecto)
cap = cv2.VideoCapture(0)

# Creamos un diccionario para almacenar las coordenadas de las landmarks y las distancias entre dedos y base
landmarks_dict = {}
distances_dict = {'thumb': float(), 'index': float(), 'middle': float(), 'ring': float(), 'pinky': float()}
fingers_dict = {'thumb': bool(), 'index': bool(), 'middle': bool(), 'ring': bool(), 'pinky': bool()}
max_distance = {'thumb': 0.85, 'index': 1.1, 'middle': 0.9, 'ring': 1, 'pinky': 1.3}

# Declaramos la constante del radio de los servomotores
RADIUS = 1.6  # Radio de los servomotores en cm (distancia desde el eje hasta la articulación con la cuerda)

def _finger_distances(distances, point_slope = {'thumb': (-4.156, 3.408), 'index': (-2.286, 4.114), 'middle': (-1.882, 3.765), 'ring': (-1.939, 3.685), 'pinky': (-2.667, 4.533)}):
    finger_distances = {}
    for finger in distances:
        finger_distances[finger] = distances[finger]*point_slope[finger][0] + point_slope[finger][1]
        if finger_distances[finger] < 0:
            finger_distances[finger] = 0
        if finger_distances[finger] > 3.2:
            finger_distances[finger] = 3.2
    return finger_distances

def _finger_rotations(finger_distances):
    finger_rotations = {}
    for finger in finger_distances:
        finger_rotations[finger] = round(np.degrees(np.arccos(1 - finger_distances[finger] / RADIUS)))
    return finger_rotations

def _update_distances(landmarks, distances, palm):
    wrist = landmarks[0]
    distance_depth = np.sqrt((wrist[0] - landmarks[5][0])**2 + (wrist[1] - landmarks[5][1])**2)
    estimated_depth = _calculate_depth(distance_depth)
    distance_angle = np.sqrt((landmarks[5][0] - landmarks[17][0])**2 + (landmarks[5][1] - landmarks[17][1])**2)/distance_depth
    estimated_angle, angle_correction = _calculate_angle(distance_angle)
    tips = 0
    for distance in distances:
        tips += 4
        if distance != 'thumb':
            distances[distance] = round((np.sqrt((wrist[0] - landmarks[tips][0])**2 + (wrist[1] - landmarks[tips][1])**2)/distance_depth) - angle_correction/4  , 2)
        else:
            distances[distance] = round((np.sqrt((palm[0] - landmarks[tips][0])**2 + (palm[1] - landmarks[tips][1])**2)/distance_depth) - angle_correction, 2)

    finger_distances = _finger_distances(distances)
    finger_rotations = _finger_rotations(finger_distances)
    return finger_rotations, estimated_depth, estimated_angle, angle_correction

def _calculate_depth(distance, reference_distance=0.3, reference_depth=30):
    estimated_depth = (reference_distance * reference_depth) / distance
    return estimated_depth 

def _calculate_angle(distance, reference_distance=0.6, reference_angle=90, max_correction=0.3):
    estimated_angle = (-reference_angle / reference_distance) * distance + 90 # Utilizamos el negativo del otro extremo para evitar dividir por cero
    if estimated_angle < 0:
        estimated_angle = 0

    angle_correction = (max_correction / reference_angle) * estimated_angle

    return estimated_angle, angle_correction

# Creamos el objeto de detección de manos
with mp_hands.Hands(
    static_image_mode=False,       # Para video en tiempo real
    max_num_hands=1,               # Número máximo de manos a detectar
    min_detection_confidence=0.5,  # Confianza mínima para detectar
    min_tracking_confidence=0.5    # Confianza mínima para seguir la mano
) as hands:

    while True:
        ret, frame = cap.read()  # Leemos un frame de la cámara
        if not ret:
            break  # Si no se pudo leer la imagen, salimos del bucle

        # Convertimos de BGR (formato de OpenCV) a RGB (lo que usa MediaPipe)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesamos la imagen para detectar manos
        results = hands.process(frame_rgb)

        # Si se detectan manos:
        if results.multi_hand_landmarks:
            # Recorremos cada mano detectada
            for hand_landmarks in results.multi_hand_landmarks:

                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Obtenemos las coordenadas (x, y) de cada punto
                for i, landmark in enumerate(hand_landmarks.landmark):
                    landmarks_dict[i] = (landmark.x, landmark.y)

                # Calculamos distancias y obtenemos el punto de la palma
                palm = ((landmarks_dict[0][0] + landmarks_dict[5][0] + landmarks_dict[17][0])/3, (landmarks_dict[0][1] + landmarks_dict[5][1] + landmarks_dict[17][1])/3)
                angles_dict, depth, angle, angle_correction = _update_distances(landmarks_dict, distances_dict, palm)
                #print(angles_dict)

                # Dibujamos el punto de la palma
                height, width, _ = frame.shape
                palm_x = int(palm[0] * width)
                palm_y = int(palm[1] * height)
                cv2.circle(frame, (palm_x, palm_y), 3, (0, 0, 255), -1)  # punto amarillo

                # Dibujamos líneas desde las puntas de los dedos a la muñeca
                wrist_x = int(landmarks_dict[0][0] * width)
                wrist_y = int(landmarks_dict[0][1] * height)
                for tip_id in [8, 12, 16, 20]:  # IDs de las puntas de los dedos
                    finger_x = int(landmarks_dict[tip_id][0] * width) 
                    finger_y = int(landmarks_dict[tip_id][1] * height)
                    cv2.line(frame, (finger_x, finger_y), (wrist_x, wrist_y), (0, 255, 0), 1)
                # Dibujamos la linea desde la punta del pulgar a la palma
                thumb_x = int(landmarks_dict[4][0] * width) 
                thumb_y = int(landmarks_dict[4][1] * height)
                cv2.line(frame, (thumb_x, thumb_y), (palm_x, palm_y), (0, 255, 0), 1)

                # Mostramos texto con la profundidad y el ángulo estimados
                text_depth = f"{depth:.2f}cm"
                text_angle = f"{angle:.2f}degrees (Correction: {angle_correction:.2f})"
                cv2.putText(frame, text_depth, (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)
                cv2.putText(frame, text_angle, (10, 60), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)

            # Creamos un string con los datos y se la enviamos al arduino
            data = ','.join([str(angles_dict[finger]) for finger in angles_dict])
            data += '\n'
            print(data)
            arduino.write(data.encode('utf-8'))

        # Mostramos la imagen con las landmarks
        cv2.imshow('Hand Tracking', frame)

        # Salimos si se pulsa la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Liberamos la cámara y cerramos la ventana
cap.release()
cv2.destroyAllWindows()
