
from PIL import Image
import numpy as np
import anki_vector
from anki_vector.events import Events
from anki_vector.util import degrees
import time
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
model = ResNet50(weights='imagenet')


with anki_vector.Robot() as robot:

    # If necessary, move Vector's Head and Lift down
    screen_dimensions = anki_vector.screen.SCREEN_WIDTH, anki_vector.screen.SCREEN_HEIGHT

    while True:
        robot.camera.init_camera_feed()
        robot.vision.enable_display_camera_feed_on_face(True)
        
        aimage = robot.camera.latest_image.raw_image.save('./latest.jpg', 'JPEG')
        oimage = Image.open('./latest.jpg')
        print("Display image on Vector's face...")
        screen_data = anki_vector.screen.convert_image_to_screen_data(oimage.resize(screen_dimensions))
        robot.screen.set_screen_with_image_data(screen_data, 5.0, True)
        
        robot.vision.enable_display_camera_feed_on_face(False)
        robot.camera.close_camera_feed()
        
        img = image.load_img('./latest.jpg', target_size=(224,224), interpolation='nearest')
        x = image.img_to_array(img)
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


        battery_state = robot.get_battery_state()
        print(f"battery state: {battery_state}")
        if battery_state.battery_volts  <= 3.6:
            robot.behavior.say_text('I too hungry to work')
            robot.behavior.drive_on_charger()
            break

        robot.disconnect()
        time.sleep(30)
        robot.connect()
