from flask import Flask, render_template, request, redirect, url_for, session
import csv

app = Flask(__name__)
app.secret_key = "jackHasaSmallD1ck"

dic = {}
green = {}

#Input page
@app.route("/", methods=["POST","GET"])
def home():
	#True if enter is pressed after entering data into the text input
	if request.method == "POST":
		#tries to see if inserted data is a valid address
		try:
			inp = dic[request.form["input"].upper()]
			session["user"] = inp[0]
			#checks to see if its in a red or green location
			try:
				session["usercolor"] = green[inp[1]]
			except:
				session["usercolor"] = "Red"
			#sends to output page
			return redirect(url_for("output"))
		except:
			#if fails reloads page
			redirect(url_for("home"))
			session.clear()
			print("Error: Request failed")
		
	return render_template("index.html")

#output page
@app.route("/output")
def output():
	#Checks to see if there is valid data
	if "user" in session:
		user = session["user"]
		color = session["usercolor"]
		#returns page with transfered values on it
		return render_template("output.html", place = user, color = color)
	else:
		return redirect(url_for("home"))
	

#startup
if __name__ == "__main__":
	#reads all the addresses wards and tracts
	with open("Address.csv") as csvfile:
		reader = csv.reader(csvfile, delimiter=",")
		#inserts the data into a dictionary (address: [ward, tract])
		for row in reader:
			dic.update({row[0].upper(): [row[1], row[2]]})
	#reads all the green tracts
	with open("gr.csv") as csvfile:
		reader = csv.reader(csvfile, delimiter=",")
		for row in reader:
			#i cant figure out how to make this a list so its a dict (tract: "Green")
			green.update({row[0]: row[1]})
	print(" * CSV files read")
	#starts up the server
	app.run(debug=True)