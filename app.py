from flask import Flask, render_template, request, redirect, url_for
import requests
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

app = Flask(__name__)

API_KEY = '5EEEJXY5G114MLPC'  # Replace with your Alpha Vantage API Key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    symbol = request.form['symbol']
    chart_type = request.form['chart_type']
    time_series = request.form['time_series']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    # Validate dates
    if start_date >= end_date:
        return "Error: End date must be after start date."

    # Fetch stock data from Alpha Vantage API
    api_url = f'https://www.alphavantage.co/query?function={time_series}&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(api_url)
    data = response.json()

    # Process data and filter by date range
    time_series_key = list(data.keys())[1]  # Adjust based on the response format
    stock_data = {date: values for date, values in data[time_series_key].items() if start_date <= date <= end_date}
    
    if not stock_data:
        return "Error: No data available for this date range."

    # Plot the data
    dates = list(stock_data.keys())
    prices = [float(values['4. close']) for values in stock_data.values()]
    dates.reverse()
    prices.reverse()

    plt.figure(figsize=(10, 6))
    if chart_type == 'line':
        plt.plot(dates, prices, label=symbol)
    elif chart_type == 'bar':
        plt.bar(dates, prices, label=symbol)

    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.title(f'{symbol} Stock Data')
    plt.legend()

    # Save the plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode image to display in browser
    graph = base64.b64encode(image_png).decode('utf-8')
    return render_template('result.html', graph=graph)

if __name__ == '__main__':
    app.run(debug=True)