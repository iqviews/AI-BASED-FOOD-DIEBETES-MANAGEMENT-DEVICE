# Import the python file containing the ML model
from flask import Flask, request, render_template,jsonify # Import flask libraries
import pickle
import pandas as pd
import string
import cv2
import numpy as np

from keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.models import load_model
from keras.applications.inception_v3 import InceptionV3
from keras.layers import AveragePooling2D, Dropout, Dense, Flatten
from keras.models import Model
import math


import typing
import glob
from PIL import Image
from io import BytesIO
import json

from predict import predict
from food_info import fds_food_info
import matplotlib.pyplot as plt





# Initialize the flask class and specify the templates directory
app = Flask(__name__, template_folder='templates')




# Id the decision is not to eat the food
# The system will send mail to teh user

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

message = MIMEMultipart()
message["To"] = 'To line here.'
message["From"] = 'The Diabetes Management Portal'
message["Subject"] = 'Your Diabetes Wellness Alert'

title = '<b> Title line here. </b>'
messageText = MIMEText('Dear Sir/Madam, Your recent glucose levels indicate concern, please prioritize your diet and management for optimal health. Contact our Phicision at 1800 800 4025','html')
message.attach(messageText)

email = "shamsudheenmarakkar17@gmail.com"
password =  "ojduepawovrjnvph"




# Default route set as 'home'
@app.route('/')
def landing():
    return render_template('1.landing.html') # Render home.html



@app.route('/login',methods=['POST'])
def login():
	if request.method == 'POST':
		return render_template('2.login.html') # Render home.html    


@app.route('/status',methods=['POST'])
def logincheck():
	if request.method == 'POST':
		details = [x for x in request.form.values()]
		print(details)
	username = details[0]
	password = details[1]
	age = details[2]
	gender = details[3]
	glucose_level = details[4]
	blood_group = details[5]

	file = open('agecache.txt', 'w')
	file.write(age)
	file.close()

	file = open('gendercache.txt', 'w')
	file.write(gender)
	file.close()

	file = open('glucosecache.txt', 'w')
	file.write(glucose_level)
	file.close()

	file = open('bloodcache.txt', 'w')
	file.write(blood_group)
	file.close()

	with open('User.txt') as file:
		lines = [line.rstrip() for line in file]
		print('lines are', lines)

	if username.strip() ==lines[0].strip()  and password.strip() ==lines[1].strip() :
		print('match')
		template = '4.image.html'
	elif username!=lines[0].strip() or password != lines[1].strip() :
		print('No')
		template = '3.loginfail.html'


	return render_template(template)


 
@app.route('/image',methods=['POST'])
def image():
	if request.method == 'POST':
		f=request.form['csvfile']
		if not f:
			print('Error')
	print(f)
	image_file  = f
	img = cv2.imread(f)
	print(img.shape)
	
	n_classes = 101

	# base model is inception_v3 weights pre-trained on ImageNet
	base_model = InceptionV3(
    weights='imagenet',
    include_top=False,
    input_shape=(299,299,3)
		)

	x = base_model.output

	# added layers to the base model
	x = AveragePooling2D(pool_size=(8, 8))(x)
	x = Dropout(.4)(x)
	x = Flatten()(x)

	# add softmax activation
	predictions = Dense(n_classes, activation='softmax')(x)

	model = Model(inputs=base_model.input, outputs=predictions)

	## Load the class labels
	with open('labels.txt', 'r') as f:
		food101 = [l.strip().lower() for l in f]
	model.load_weights('Food_model/food101.h5')
	img = cv2.resize(img, (299, 299)) 
	print(img.shape)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	img = np.expand_dims(img, axis=0)
	img = preprocess_input(img)
	predicted_vec = model.predict(img)
	predicted_label = food101[np.argmax(predicted_vec)]
	print(predicted_label)
	

	food = predicted_label
	food = food.capitalize()
	# save the food detected
	file = open('food.txt', 'w')
	file.write(food)
	file.close()
	
	#food = 'Omelette'



	model_path = 'yolov8s-seg-v1.onnx'
	image_array = plt.imread(image_file)
	print(image_array.shape, ' Got')
	results = predict(image_array, 'yolov8s-seg-v1.onnx')
	# counting the number of pixels
	out = results['masks'][0]
	number_of_Food_pix = np.sum(out == 1)
	number_of_BG_pix = np.sum(out == 0)

	print('Number of white/Food pixels:', number_of_Food_pix)
	print('Number of black/Background pixels:', number_of_BG_pix)

	number_of_Food_pix
	number_of_BG_pix
	total_pix = number_of_Food_pix + number_of_BG_pix
	total_pix

	percentage_Food_pix = (number_of_Food_pix/total_pix)*100
	if percentage_Food_pix > 50:
		Quantity = number_of_Food_pix/5000
	elif percentage_Food_pix < 50:
		Quantity = number_of_Food_pix/100

	serving = Quantity


	print('Serving quantity is ',Quantity, ' gms')

	#serving = 500.0
	

	dataNutrition = pd.read_csv('Nutrition_Dataset_updated_with_labels.csv')
	list={food}
	item=dataNutrition[dataNutrition['FoodName'].isin(list)]
	print(item)
	netcarbs=float(item["Totalfat(g)"]+item["Availablecarbohydrateswithsugaralcohols(g)"]+item["Availablecarbohydrateswithoutsugaralcohol(g)"]
                   -item["Alcohol(g)"]-item["Starch(g)"]+item["Totalsaturatedfat(g)"]+item["Totalmonounsaturatedfat(g)"]+item["Totalpolyunsaturatedfat(g)"]
                   +item["Totaltransfattyacids(mg)"])
	GI=item["GyclemicIndex"].values
	GlycemicLoad=(float)(netcarbs*GI*serving)/10000.0
	print()



	if(GlycemicLoad<=10.0):
		print("Food is appropriate for consumption")
		text = 'You are totally okay to have it, Enjoy. keep monitoring your glucose level and follow the diet'
		template = '6.prediction.html'

	

	elif(GlycemicLoad<=19.0 and sugarlevel<=110.0):
		print("Food is appropriate for consumption")
		text = 'You are totally okay to have it, Enjoy. keep monitoring your glucose level and follow the diet'
		template = '6.prediction.html'


	elif(GlycemicLoad>=20.0 and GI<=55.0):
		print("If food is consumed in lesser quatity, it would be fit for consumption")
		text = 'If food is consumed in lesser quatity, it would be fit for consumption'
		#descision = input("Do you want a healthier food substitute(Y/N):")
		template = '5.prediction.html'

		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo('Gmail')
		server.starttls()
		server.login(email,password)
		fromaddr = 'From line here.'

		# The To Address
		toaddrs  = "shamsudheenmmp@gmail.com"
		server.sendmail(fromaddr,toaddrs,message.as_string())
		server.quit()

	

	else:
		print("Food is inappropriate for consumption")
		#descision=input("Do you want a healthier food substitute(Y/N):")
		text = "Food is inappropriate for consumption"
		template = '5.prediction.html'

		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo('Gmail')
		server.starttls()
		server.login(email,password)
		fromaddr = 'From line here.'

		# The To Address
		toaddrs  = "shamsudheenmmp@gmail.com"
		server.sendmail(fromaddr,toaddrs,message.as_string())
		server.quit()


	return render_template(template, text = text, food = food, serving = serving)




@app.route('/recommend',methods=['POST'])
def recommend():
	if request.method == 'POST':
		# Read teh food
		file = open("food.txt", "r")
		food = file.read()
		print(food)
		file.close()
		print(type(food))
		data = pd.read_csv('Nutrition_Dataset_updated_with_labels.csv')
		list={food}
		f=data[data['FoodName'].isin(list)]
		group = f['labels']
		others = data[data['labels'] == int(group.values)]
		GI = f['GyclemicIndex']
		data = data[data['GyclemicIndex'] < int(GI.values)]
		data = data.sort_values("GyclemicIndex")
		recom = data.iloc[[-1]]
		recom = recom['FoodName'].values
		print(recom)
		print(type(recom))
		text = 'You may have ' + recom[0] + ' in a limited quantity'


	return render_template('7.recomendation.html', text = text) # Render home.html    


# Run the Flask server
if(__name__=='__main__'):
    app.run(debug=True)        