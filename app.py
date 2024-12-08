from flask import Flask, render_template, jsonify, flash, redirect, url_for, request, get_flashed_messages
import os, datetime, csv

app = Flask(__name__)
app.secret_key= 'jajhfajksbvhusia'


@app.route('/')
def home():  
    path = "data"
    files = get_files(path)
    return render_template('index.html', files = files)

@app.route('/file/show')
def data():
    filename = request.args.get('filename', '').strip()
    file_path = os.path.join("data" , filename + '.csv')

    data = read_csv(file_path)
    return render_template('data.html', data = data, filename= filename)


@app.route('/file/delete', methods=['POST', 'GET']) #verified
def delete_file():
    filename = request.args.get('filename', '').strip() + '.csv'
    file_path = os.path.join("data" , filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return redirect(url_for('files'))
    else:
        return f'File Not Found...{file_path}'


@app.route('/file/create', methods=['POST', 'GET']) #verified
def Add_file():
    filename = request.args.get('filename', '').strip() + '.csv'
    file_path = os.path.join("data" , filename)

    if os.path.exists(file_path):
        return 'File Already Exists...'
    
    with open(file_path, mode='w', encoding='utf-8') as file:
        return redirect(url_for('files'))



def read_csv(file_path):
    data = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def get_files(folder_path):
    files_data = []
    if not os.path.exists(folder_path):
        return files_data 
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):  
            file_info = {
                'name': filename,
                'size': os.path.getsize(file_path),  
            }
            files_data.append(file_info)
    return files_data


if __name__ == "__main__":
    app.run(debug=True, port=5000)