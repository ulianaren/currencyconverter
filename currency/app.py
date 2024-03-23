from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

currencies = [
    'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 
    'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 
    'BSD', 'BTC', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLF', 
    'CLP', 'CNH', 'CNY', 'COP', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 
    'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 
    'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 
    'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 
    'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 
    'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 
    'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 
    'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 
    'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 
    'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 
    'SOS', 'SRD', 'SSP', 'STD', 'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 
    'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 
    'UYU', 'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XAG', 'XAU', 'XCD', 
    'XDR', 'XOF', 'XPD', 'XPF', 'XPT', 'YER', 'ZAR', 'ZMW', 'ZWL'
]



@app.route("/")
def index():
    return render_template("index.html", currencies=currencies) #connect html file and give a list of currencies to use it there


@app.route('/convert', methods=['POST'])
def convert():
    currency_input=request.form['currency_input'] #get input currency from user
    currency_output=request.form['currency_output'] #get output currency from user
    amount = request.form['amount'] #get amount from user

    
    converted_amount = round(conversion(currency_input, currency_output, amount), 2) #get result of conversion
    

    result = {
        'amount': amount,
        'currency_input': currency_input,
        'converted_amount': converted_amount,
        'currency_output': currency_output
    }

    return jsonify(result)


#get all rates from API
def get_rates():

    url = 'https://openexchangerates.org/api/latest.json'   # API URL
    access_key = "f42a02d62a6c422c83e7b5a86be99d82"  # API Access Key 
    params = {
        'app_id': access_key,  
        'base': 'USD',         # Base currency
    }

    # Send GET request to the API
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        rates = data["rates"] # get all the rates to USD
        return rates
    else:
        print("Failed to fetch exchange rates.")

#convert currency, return result
def conversion(currency_input, currency_output, amount):
    rates = get_rates()
    source_currency = rates[currency_input]
    target_currency = rates[currency_output]

    result = float(target_currency)*float(amount)/float(source_currency)
    return result

if __name__ == "__main__":
    app.run(debug=True)