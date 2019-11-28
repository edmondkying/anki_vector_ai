# anki_vector_ai
making a few AI projects on the anki vector.  Its a great bargain at $78 at amazon.com when jetbot is $300
you need to pip install kara, tf, numpy, anki_vector_sku, and time packages


test1.py

Use ResNet50 image network to identify object while vector is walking around.
It will display the image on its screen.
it will say out loud what it is.
It will print out what it is on the console.
I tried the event driven way but the api is so buggy that once it executed, it threw future exceptions and that was the end of it.  So here I'm using a while True loop instead but I reliquish control of the robot for 15 seconds in between so vector can carry on anything else.
