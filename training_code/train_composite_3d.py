# -*- coding: utf-8 -*-
"""Composite.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZbZTYlm1d1MaSyXt0ywCt4MCbnV12C3G
"""

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv3D,ConvLSTM2D,Input,Concatenate
import numpy as np 
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

encoder_input=Input((None,404,404,1),name="encoder_input")
decoder_input=Input((None,404,404,1),name="decoder_input")
forecaster_input=Input((None,404,404,1),name="forecaster_input")

encoder_1=ConvLSTM2D(16,(3,3),padding="same",
        input_shape=(None,404,404,1),
        activation='linear',
        return_sequences=True,return_state=True,
        kernel_initializer='he_normal',name="encoder_1")

encoder_2=ConvLSTM2D(16,(3,3),padding="same",
        return_sequences=True,return_state=True,
        activation='linear',
        kernel_initializer='he_normal',name="encoder_2")

decoder_1=ConvLSTM2D(16,(3,3),padding="same",
        return_sequences=True,return_state=True,
        activation='linear',
        # kernel_regularizer="l1_l2",
        kernel_initializer='he_normal',name="decoder_1")

decoder_2=ConvLSTM2D(16,(3,3),padding="same",
        return_sequences=True,return_state=True,
        activation='linear',
        # kernel_regularizer="l1_l2",
        kernel_initializer='he_normal',name="decoder_2")

forecaster_1=ConvLSTM2D(16,(3,3),padding="same",
        return_sequences=True,return_state=True,
        activation='linear',kernel_regularizer="l1_l2",
        recurrent_initializer="he_normal",
        kernel_initializer='he_normal',name="forecaster_1")

forecaster_2=ConvLSTM2D(16,(3,3),padding="same",
        return_sequences=True,return_state=True,
        activation='linear',kernel_regularizer="l1_l2",
        recurrent_initializer="he_normal",
        kernel_initializer='he_normal',name="forecaster_2")

# concat_layer = Concatenate(name="Concatenate")


decoder_conv=Conv3D(filters=1, kernel_size=(3,3,3),
        activation='sigmoid',kernel_initializer='he_normal',
        padding='same', data_format='channels_last',
        
        name="decoder_Conv_layer")

forecaster_conv=Conv3D(filters=1, kernel_size=(3,3,3),
        activation='sigmoid',kernel_initializer='he_normal',
        padding='same', data_format='channels_last',
        name="forecaster_Conv_layer")

encoder_1_outputs=encoder_1(encoder_input)
encoder_1_output=encoder_1_outputs[0]
encoder_1_state=encoder_1_outputs[1:]

encoder_2_outputs=encoder_2(encoder_1_output)
encoder_2_output=encoder_2_outputs[0]
encoder_2_state=encoder_2_outputs[1:]


decoder_1_outputs=decoder_1(inputs=decoder_input,
                            initial_state=encoder_2_state)
decoder_1_output=decoder_1_outputs[0]
decoder_1_state=decoder_1_outputs[1:]

decoder_2_outputs=decoder_2(inputs=decoder_1_output,
                            initial_state=encoder_2_state)
decoder_2_output=decoder_2_outputs[0]
decoder_2_state=decoder_2_outputs[1:]
decoder_2_output=decoder_conv(decoder_2_output)

forecaster_1_outputs=forecaster_1(inputs=forecaster_input,
                                  initial_state=encoder_2_state)

forecaster_1_output=forecaster_1_outputs[0]
forecaster_1_state=forecaster_1_outputs[1:]

forecaster_2_outputs=forecaster_2(inputs=forecaster_1_output,
                                  initial_state=encoder_2_state)
forecaster_2_output=forecaster_2_outputs[0]
forecaster_2_state=forecaster_2_outputs[1:]

# output_from_forecaster = concat_layer([forecaster_1_output,
#                                      forecaster_2_output])
forecaster_2_output=forecaster_conv(forecaster_2_output)

composite_model = Model([encoder_input, decoder_input,forecaster_input], [decoder_2_output,forecaster_2_output],name="Composite")

composite_model.summary()

from tensorflow.keras.utils import plot_model
plot_model(model=composite_model,show_shapes=True,)

composite_model.compile(optimizer="adam", loss='bce')

from google.colab import drive
drive.mount('/content/drive')

import xarray as xr 
xf=xr.open_dataset("/content/drive/My Drive/files.nc")

data=xf["IMG_VIS"].values
xf.close()

def scaleData(a):       
    return (a-np.nanmin(a))/(np.nanmax(a)-np.nanmin(a))

def prepare_data(data):
    tdata=[]
    tlabels=[]
    img_size=(404,404)
    print(len(data))
    
    arrdata=np.zeros((len(data)-6,6,img_size[0],img_size[1],1))
    arrlabel=np.zeros((len(data)-6,6,img_size[0],img_size[1],1))
    
    for i in range(0,len(data)-6-5,1):
        m=0
        for j in range(i,i+6,1):
            #print(j,j+6)
            arrdata[i,m,:,:,0]=data[j]
            arrlabel[i,m,:,:,0]=data[j+6]  

            m+=1
        # print(i,j,j+1,j+6)

    print(arrdata.shape)
    print(arrlabel.shape)
    return arrdata,arrlabel

new=[]
for i in data:
    value=scaleData(i)
    new.append(value)

data,label=prepare_data(new[:100])

mean=0
std=0.0

for_in=np.zeros(shape=data.shape)
for_in[:,0,:,:,0]=data[:,-1,:,:,0] + np.random.normal(mean, std, (404,404))
for_in[:,1:,:,:,0]=label[:,0:-1,:,:,0] + np.random.normal(mean, std, (404,404))
for_in = np.where(for_in>1,1,for_in)
for_in = np.where(for_in<0,0,for_in)

deco_in=np.zeros(shape=data.shape)
deco_out=np.ones(shape=data.shape)
deco_out[:,:,:,:,0]=data[:,::-1,:,:,0]

# for_in=np.zeros((44,7,404,404,1))
# for_out=np.zeros((44,7,404,404,1))

# for_in[:,1:,:,:,:]=label
# for_out[:,:-1,:,:,:]=label

fig,ax=plt.subplots(4,6,figsize=(18,12),subplot_kw={'xticks':[], 'yticks':[]})

for i in range(6):
      ax[0,i].imshow(data[3,i,:,:,0],cmap="gray",vmin=0,vmax=1)
      ax[1,i].imshow(deco_out[3,i,:,:,0],cmap="gray",vmin=0,vmax=1)
      ax[2,i].imshow(for_in[3,i,:,:,0],cmap="gray",vmin=0,vmax=1)
      ax[3,i].imshow(label[3,i,:,:,0],cmap="gray",vmin=0,vmax=1)

#[encoder_input, decoder_input,forecaster_input], [decoder_2_output,forecaster_2_output]
input_=[data,deco_in,for_in]
label_=[deco_out,label]

from tensorflow.keras.callbacks import EarlyStopping

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1,patience=5)

composite_model.fit(input_,label_, batch_size =1, epochs=50, validation_split=0.2,callbacks=[es],verbose=1)

import pandas as pd 

df= pd.DataFrame(composite_model.history.history)
df.plot()
df.to_csv("IMG_VIS.csv")

Encoder_model = Model(encoder_input, encoder_2_state)
Encoder_model.compile(optimizer="adam", loss='bce')

decoder_state_input_h = Input(shape=encoder_2_state[0].shape[1:],name="decoder_input_h")
decoder_state_input_c = Input(shape=encoder_2_state[1].shape[1:],name="decoder_input_c")


decoder_input_1=Input((None,404,404,1),name="decoder_input_1")


decoder_11_outputs=decoder_1(inputs=decoder_input_1,initial_state=[decoder_state_input_h,decoder_state_input_c])
decoder_11_output=decoder_11_outputs[0]
decoder_11_state=decoder_11_outputs[1:]

decoder_22_outputs=decoder_2(inputs=decoder_11_output,initial_state=[decoder_state_input_h,decoder_state_input_c])
decoder_22_output=decoder_22_outputs[0]
decoder_22_state=decoder_22_outputs[1:]
decoder_22_output=decoder_conv(decoder_22_output)

Decoder_model = Model([decoder_input_1] + [decoder_state_input_h,decoder_state_input_c], [decoder_22_output] +decoder_22_state)
Decoder_model.compile(optimizer="adam", loss='bce')

forecaster_state_input_h = Input(shape=encoder_2_state[0].shape[1:],name="forecaster_input_h")
forecaster_state_input_c = Input(shape=encoder_2_state[1].shape[1:],name="forecaster_input_c")


forecaster_input_1=Input((None,404,404,1),name="forecaster_input_1")


forecaster_11_outputs=forecaster_1(inputs=forecaster_input_1,initial_state=[forecaster_state_input_h,forecaster_state_input_c])
forecaster_11_output=forecaster_11_outputs[0]
forecaster_11_state=forecaster_11_outputs[1:]

forecaster_22_outputs=forecaster_2(inputs=forecaster_11_output,initial_state=[forecaster_state_input_h,forecaster_state_input_c])
forecaster_22_output=forecaster_22_outputs[0]
forecaster_22_state=forecaster_22_outputs[1:]

# output_from__forecaster = concat_layer([forecaster_11_output,forecaster_22_output])
forecaster_22_output=forecaster_conv(forecaster_22_output)


Forecaster_model = Model([forecaster_input_1] + [forecaster_state_input_h,forecaster_state_input_c], [forecaster_22_output] +forecaster_22_state)

Forecaster_model.compile(optimizer="adam", loss='bce')

def predict_(x, encoder_predict_model, decoder_predict_model, num_steps_to_predict):
  
    y_predicted = []
    
    state_h,state_c = encoder_predict_model.predict(x)
    states=[state_h,state_c]    
    decoder_input = np.zeros((1,1,404,404,1))
    # decoder_input[0,0,:,:,0]=x[0,-1,:,:,0]
    
    for _ in range(num_steps_to_predict):
        outputs_and_states = decoder_predict_model.predict([decoder_input] + states)
      
        output = outputs_and_states[0]
      
        states= outputs_and_states[1:]
       
        # add predicted value
        output=scaleData(output)
        decoder_input=output

        y_predicted.append(output)
    return np.concatenate(y_predicted, axis=1)

def predict(x, encoder_predict_model, decoder_predict_model, num_steps_to_predict):
  
    y_predicted = []
    
    state_h,state_c = encoder_predict_model.predict(x)
    states=[state_h,state_c]    
    decoder_input = np.zeros((1,1,404,404,1))
    decoder_input[0,0,:,:,0]=x[0,-1,:,:,0]
    
    for _ in range(num_steps_to_predict):
        outputs_and_states = decoder_predict_model.predict([decoder_input] + states)
      
        output = outputs_and_states[0]
      
        states= outputs_and_states[1:]
       

        # add predicted value
        output=scaleData(output)
        decoder_input=output

        y_predicted.append(output)
    return np.concatenate(y_predicted, axis=1)

ans1= predict_( data[51:52], Encoder_model, Decoder_model, 6)
ans1[:,:,:,:,:]=ans1[:,::-1,:,:,:]

ans= predict( data[51:52], Encoder_model, Forecaster_model, 6)

print(ans1.shape)
print(ans.shape)

fig,ax=plt.subplots(4,6,figsize=(18,12),subplot_kw={'xticks':[], 'yticks':[]})

for i in range(6):
      ax[0,i].imshow(data[51,i,:,:,0],cmap="gray",vmin=0,vmax=1)
      ax[1,i].imshow(ans1[0,i,:,:,0],cmap="gray",vmin=0,vmax=1)
      ax[2,i].imshow(label[51,i,:,:,0],cmap="gray",vmin=0,vmax=1)
      ax[3,i].imshow(ans[0,i,:,:,0],cmap="gray",vmin=0,vmax=1)

Encoder_model.save("Encoder_VIS.h5")
Decoder_model.save("Decoder_VIS.h5")
Forecaster_model.save("Forecaster_VIS.h5")

for i in range(6):
  plt.imshow(ans[0,i,:,:,0],cmap="gray")
  plt.colorbar()
  plt.show()



