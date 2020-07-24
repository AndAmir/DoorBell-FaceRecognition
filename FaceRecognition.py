import cv2, datetime, face_recognition, time, os, sys
import numpy as np
import Speak, Listen, camera
import speech_recognition as sr

folderName = '/Users/Andy/PycharmProjects/FaceRecognition'
# create recognizer and mic instances
recognizer = sr.Recognizer()
microphone = sr.Microphone()
now = datetime.datetime.now()
greet = []
totalName = 4
startpoint = 78


def sayGreet(greet):
    if "unknown" in greet or "Unknown" in greet:
        pass
    elif now.hour < 12:
        Speak.morning(greet)
    elif 12 <= now.hour < 18:
        Speak.afternoon(greet)
    elif 18 <= now.hour <= 24:
        Speak.evening(greet)


def getFrame():
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    return small_frame[:, :, ::-1]


def updateFaces(name,totalName, startpoint):
    fin = open(__file__, 'r')
    code = fin.readlines()
    fin.close()

    greets = "greetCheck = ["
    for i in range(totalName):
        greets += "False,"
    code[65] = greets + "False]\n"
    totalName += 1
    startpoint += 2
    code[11] = "totalName = " + str(totalName) + "\n"

    code[12] = "startpoint = " + str(startpoint) + "\n"

    code.insert(67, name+" = face_recognition.load_image_file(\""+name+".jpg\")\n" + name + "_encoding = face_recognition.face_encodings("+name +")[0]\n")

    code.insert(startpoint, "known_face_encodings.append("+name+ "_encoding)\nknown_face_names.append(\""+name+"\")\n")

    code = "".join(code)
    fout = open(__file__, 'w')
    fout.write(code)
    fout.close()


# Get a reference to web cam #0 (the default one)
video_capture = cv2.VideoCapture(0)
# Load a sample picture and learn how to recognize it.
greetCheck = [False,False,False,False]
# Load a second sample picture and learn how to recognize it.
Diya = face_recognition.load_image_file("Diya.jpg")
Diya_encoding = face_recognition.face_encodings(Diya)[0]
AndrewNoGlasses = face_recognition.load_image_file("AndrewNoGlasses.jpg")
AndrewNoGlasses_encoding = face_recognition.face_encodings(AndrewNoGlasses)[0]
Andrew = face_recognition.load_image_file("Andrew.jpg")
Andrew_encoding = face_recognition.face_encodings(Andrew)[0]
Stephanie = face_recognition.load_image_file("Stephanie.jpg")
Stephanie_encoding = face_recognition.face_encodings(Stephanie)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [Stephanie_encoding]
known_face_names = ["Stephanie"]

# Initialize some variables
known_face_encodings.append(Diya_encoding)
known_face_names.append("Diya")
known_face_encodings.append(AndrewNoGlasses_encoding)
known_face_names.append("AndrewNoGlasses")
known_face_encodings.append(Andrew_encoding)
known_face_names.append("Andrew")

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
while True:

    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Uses the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
            if not greetCheck[best_match_index]:
                greet.append(name)
                greetCheck[best_match_index] = True

            if name == "Unknown":
                Speak.speak("I see a person that isn't known, would this person like to be known and give their name?")
                time.sleep(1)
                response = Listen.recognize_speech_from_mic(recognizer, microphone)
                print(response)
                response = input("The speech recognition is a work in progress that works half the time, please type what your \"yes\" or \"no\" answer")
                if "yes" in response or "Yes" in response:
                    Speak.speak(
                        "Ok. Please make sure that you are the only one faceing the camera")
                    time.sleep(3)

                    rgb_small_frame = getFrame()
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                    if len(face_encodings) == 1:
                        Speak.speak("Please type in your name?")
                        asdf = input("Please enter your name?")
                        updateFaces(asdf,totalName,startpoint)
                        ret, frame = video_capture.read()
                        out = cv2.imwrite(asdf+'.jpg', frame)
                        os.execl(sys.executable, sys.executable, *sys.argv)
                    elif len(face_encodings) == 0:
                        Speak.speak("There is no one faceing the camera")
                    else:
                        Speak.speak("There is more than one person facing the camera")
                elif "no" in response:
                    Speak.speak("ok")
                else:
                    Speak.speak("Please respond with a yes or no answer.")
                    time.sleep(1)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Decides how to greed person

        sayGreet(greet)
        greet = []

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the web cam
video_capture.release()
cv2.destroyAllWindows()
