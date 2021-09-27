from flask import Flask, request, render_template, redirect, url_for
from mips_blueprint import mips_blueprint

app = Flask(__name__)

#registering of
app.register_blueprint(mips_blueprint)

@app.route("/")
def main(): 
    return render_template("index.html")
    

@app.route("/ip_to_binary", methods=["GET","POST"])
def ip_to_binary(): 
    print('a')
    binary_string = ""
    if request.method == "POST": 
        print('b')
        ip_address = request.form.get('ip_address')
        if any(c.isalpha() for c in ip_address): 
            return redirect(url_for('error')) 
        value_array = ip_address.split(".")
        for i in range(len(value_array)): 
            binary_string += '{0:08b}'.format(int(value_array[i]))
            binary_string += " " 
        print(binary_string)
    return render_template("ip_to_binary.html", test=binary_string)


@app.route("/error")
def error(): 
    return render_template("error.html")


@app.route("/truthtable")
def tt(): 
    return render_template("truth_table.html")





