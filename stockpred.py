#!/bin/python3

import pandas as pd
from scipy.io.arff import loadarff

data_file = '/home/notclaytonjohnson/weka_data/AAPL.arff'

"""
Linear Regression Model

Close =

      0.9141 * Open +
      0.0974 * Lag_Close-1 +
     -0.052  * Lag_Close-6 +
      0.1038 * Lag_Close-7 +
     -0.1445 * Lag_Close-8 +
      0.0805 * Lag_Close-9 +
      0.1647

"""

def get_signed_string(val):
  if val > 0 :
    return '+{:.2f}'.format(val)
  else:
    return '{:.2f}'.format(val)


def predict_close_with_open(df, open_price=-1.0):
  # Find the lagged values
  lg1 = df['Close'][-1]
  lg6 = df['Close'][-6]
  lg7 = df['Close'][-7]
  lg8 = df['Close'][-8]
  lg9 = df['Close'][-9]

  # Project and return the closing price with the predefined coefficients
  close_price = (0.9141*open_price) + (0.0974*lg1) + (-0.052*lg6) + (0.1038*lg7) + (-0.1445*lg8) + (0.0805*lg9) + 0.1647
  return close_price

def evaluate_learner(df, days):
  error_total = 0

  #print(df.tail(10))
  print('\t\t\t\tPredicted\tReal')
  print('Date\t\t\tOpen\tClose\tDelta\tClose\tDelta\tError')
  for i in range(days, 0, -1):
    #print('-------------------------')
    data_today = df.tail(i).head(1)
    data_history = df.head( len(df.index)-i )

    #print('Last of larger set:')
    #print(data_history.tail(1))
    #print('Next day:')
    #print(data_today)

    # Get the data and predicted data for today
    date = data_today.index[0]
    open_today = data_today['Open'][0]
    close_pred = predict_close_with_open(data_history, open_today)
    delta_pred = close_pred - open_today
    close_real = data_today['Close'][0]
    delta_real = close_real - open_today
    error = close_pred - close_real
    error_total += error
  
    print('{}\t{:.2f}\t{:.2f}\t{}\t{:.2f}\t{}\t{}'.format(date, open_today, close_pred, get_signed_string(delta_pred), close_real, get_signed_string(delta_real), get_signed_string(error)))
  print('\t\t\t\t\t\t\t\t{:.2f}'.format(error_total))

  #if error_total < 0:
  #  print('The model is 

  
if __name__ == '__main__':
  # Import the arff file
  data_raw = loadarff(data_file)

  # Convert the imported arff file to a pandas dataframe
  df = pd.DataFrame(data_raw[0])

  # Make the 'Date' attribute the index of the data frame instead of n
  df.index = df['Date']

  # Remove the now redundant 'Date' attribute
  del df['Date']

  # Print the data at the end of the data frame to make sure everyone is on the same page
  print('-------------- Most Recent Data ----------------')
  print(df.tail())
  print('------------------------------------------------')

  # Set the opening price recorded today
  open_price = 286.25

  # Use the predefined model to predict the closing price
  pred_close = predict_close_with_open(df, open_price)

  # Output projected closing price
  print('The \'ol wise one predicts....')
  print('\tApple will close on {} ({}) today.'.format(pred_close, '+' + str(pred_close-open_price) if pred_close - open_price > 0 else pred_close-open_price)) 

  print('Evaluating the learner...')
  evaluate_learner(df, 10)
