from flask import Flask, render_template, request, redirect
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
EXCEL_FILE = r'C:\Users\nurulamirah\Documents\Data Analyst\Tasks\2025\Nathaniel\FeedbackTool\feedback_data.xlsx'

def init_excel():
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=['Name', 'Region', 'Category', 'Content', 'Timestamp', 'Status', 'Upvotes', 'Downvotes'])
        df.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def index():
    df = pd.read_excel(EXCEL_FILE, keep_default_na=False)
    df['NetScore'] = df['Upvotes'] - df['Downvotes']
    sorted_df = df.sort_values(by='NetScore', ascending=False)
    sorted_df = sorted_df.drop(columns=['NetScore'])
    feedback_list = sorted_df.to_dict(orient='records')
    return render_template('index.html', feedback=feedback_list)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        designation = request.form.get('designation', '').strip()
        region = request.form.get('region', 'NA').strip()
        category = request.form.get('category', '').strip()
        content = request.form.get('content', '').strip()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        new_feedback = {
            'Name': name,
            'Designation': designation,
            'Region': region,
            'Category': category,
            'Content': content,
            'Timestamp': timestamp,
            'Status': 'New',
            'Upvotes': 0,
            'Downvotes': 0
        }

        df = pd.read_excel(EXCEL_FILE, keep_default_na=False)
        df = pd.concat([df, pd.DataFrame([new_feedback])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        return redirect('/')
    return render_template('submit.html')

@app.route('/upvote/<timestamp>')
def upvote(timestamp):
    df = pd.read_excel(EXCEL_FILE, keep_default_na=False)
    index = df[df['Timestamp'] == timestamp].index
    if not index.empty:
        df.at[index[0], 'Upvotes'] += 1
        df.to_excel(EXCEL_FILE, index=False)
    return redirect('/')

@app.route('/downvote/<timestamp>')
def downvote(timestamp):
    df = pd.read_excel(EXCEL_FILE, keep_default_na=False)
    index = df[df['Timestamp'] == timestamp].index
    if not index.empty:
        df.at[index[0], 'Downvotes'] += 1
        df.to_excel(EXCEL_FILE, index=False)
    return redirect('/')

if __name__ == '__main__':
    init_excel()
    app.run(debug=True)





