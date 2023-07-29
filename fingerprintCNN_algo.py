 
from tensorflow.keras.layers import Input,Lambda,Dense,Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt 


IMAGE_SIZE = [224,224]

train_path = "images/"



from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1./255,horizontal_flip=True,zoom_range=0.2,validation_split=0.15)

training_set = train_datagen.flow_from_directory(
        train_path,target_size=(224,224), batch_size=32,class_mode='categorical',
        subset='training')

validation_set = train_datagen.flow_from_directory(
        train_path,target_size=(224,224), batch_size=32,class_mode='categorical',shuffle = True,
        subset='validation')


from tensorflow.keras.applications import VGG19
from tensorflow.keras.layers import GlobalAveragePooling2D,Dropout

## We are initialising the input shape with 3 channels rgb and weights as imagenet and include_top as False will make to use our own custom inputs

mv = VGG19(input_shape=IMAGE_SIZE+[3],weights='imagenet',include_top=False)

for layers in mv.layers:
    layers.trainable = False


# if u want to add more folders and train then change number 4 to 5 or 6 based on folders u have to train
x = Flatten()(mv.output)
prediction = Dense(5,activation='softmax')(x)

# In[7]:

model = Model(inputs=mv.input,outputs=prediction)

model.summary()


import tensorflow as tf

class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self,epoch,logs={}):
        if(logs.get('loss')<=0.05):
            print("\nEnding training")
            self.model.stop_training = True
# initiating the myCallback function
callbacks = myCallback()


## Let us compile the model with Adam optimizer and loss function categorical_crossentropy and metrics as categorical_accuracy
from tensorflow.keras.optimizers import Adam
model.compile(optimizer=Adam(lr=0.0001),loss='categorical_crossentropy',metrics=['categorical_accuracy'])

history = model.fit(training_set,
                              validation_data=validation_set,
                              epochs=50,
                              verbose=1,
                              steps_per_epoch=len(training_set),
                              validation_steps=len(validation_set),
                              callbacks = [callbacks]
                             )

acc = history.history['categorical_accuracy']
val_acc = history.history['val_categorical_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

import matplotlib.pyplot as plt
plt.plot(epochs,acc)
plt.plot(epochs,val_acc)
plt.title("Training and validation Accuracy")
plt.savefig('accuracytrain.png')

plt.plot(epochs,loss)
plt.plot(epochs,val_loss)
plt.title("Training and validation Loss")
plt.savefig('validationaccuracy.png')

model.save("fingerprint.h5")

#from tensorflow.keras.models import load_model
#from tensorflow.keras.preprocessing import image
#import numpy as np

# dimensions of our images
#img_width, img_height = 224,224

# load the model we saved
#model = load_model('content.h5')
# predicting images
#img = image.load_img('content/Train/Cars/C0.jpg', target_size=(img_width, img_height))
#x = image.img_to_array(img)
#x = np.expand_dims(x, axis=0)

#classes = model.predict(x)
#print (classes)


 




