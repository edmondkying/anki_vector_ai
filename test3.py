from PIL import Image
import numpy as np
import urllib
import random
import time
import anki_vector
from anki_vector.events import Events
from anki_vector.util import degrees
from keras.applications.xception import Xception
from keras.preprocessing import image
from keras.applications.xception import preprocess_input, decode_predictions


model = Xception(weights='imagenet')

jokes = []
content=urllib.request.urlopen("http://www.textfiles.com/humor/COMPUTER/computer.say") 
for line in content:
    line = line.decode("utf-8")
    jokes.append(line.rstrip('\n'))

screen_dimensions = anki_vector.screen.SCREEN_WIDTH, anki_vector.screen.SCREEN_HEIGHT

with anki_vector.Robot(enable_face_detection=True) as robot:

    while True:

        face_name = None
        for face in robot.world.visible_faces:
            face_name = face.name
            break

        if face_name:
            greeting = "Hi " + face_name + ", let me tell you a joke"
            print(greeting)
            robot.behavior.say_text("Hi " + face_name + " let me tell you a joke")
            joke = jokes[random.randint(0,len(jokes)-1)]
            print(joke)
            robot.behavior.say_text(joke)
        else:

            #if float(str(robot.proximity.last_sensor_reading.distance).split()[1]) <= 130:
            if robot.proximity.last_sensor_reading.unobstructed == False:

                robot.behavior.set_lift_height(0.0)
                robot.behavior.set_head_angle(degrees(0.0))

                robot.camera.init_camera_feed()
                robot.vision.enable_display_camera_feed_on_face(True)
                robot.camera.latest_image.raw_image.save('./latest.jpg', 'JPEG')
                robot.camera.close_camera_feed()

                oimage = Image.open('./latest.jpg')
                print("Display image on Vector's face...")
                screen_data = anki_vector.screen.convert_image_to_screen_data(oimage.resize(screen_dimensions))
                robot.screen.set_screen_with_image_data(screen_data, 5.0, True)
                
                oimage = oimage.crop(box=(170,0,469,299))
                x = image.img_to_array(oimage)
                x = np.expand_dims(x, axis=0)
                x = preprocess_input(x)

                preds = model.predict(x)

                word = decode_predictions(preds, top=1)
                for i in (word):
                    for j in i:
                        obj = j[1]
                obj = obj.replace("_"," ")
                print('Predicted:', obj)

                if obj == "pill bottle":
                    robot.behavior.say_text('I need to take my meds!')
                    robot.anim.play_animation_trigger('GreetAfterLongTime')
                else:
                    robot.behavior.say_text('Might be {}'.format(obj))

                robot.vision.enable_display_camera_feed_on_face(False)


        battery_state = robot.get_battery_state()
        print(f"battery state: {battery_state}")
        if battery_state.battery_volts  <= 3.6:
            robot.behavior.say_text('I too hungry to work')
            robot.behavior.drive_on_charger()
            break

        robot.disconnect()
        time.sleep(20)
        robot.connect()

