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

def predict_close_with_open(df, open_price=-1.0):
  # Compute the predict in accordance to the model above
  lg1 = df['Close'][-1]
  lg6 = df['Close'][-6]
  lg7 = df['Close'][-7]
  lg8 = df['Close'][-8]
  lg9 = df['Close'][-9]
  # This isn't the correct method for the date
  #date_remapped = create_millis(date.today())
  close_price = (0.9141*open_price) + (0.0974*lg1) + (-0.052*lg6) + (0.1038*lg7) + (-0.1445*lg8) + (0.0805*lg9) + 0.1647
  return close_price
  
  
if __name__ == '__main__':
  data_raw = loadarff(data_file)
  df = pd.DataFrame(data_raw[0])
  df.index = df['Date']
  del df['Date']
  print('-------------- Most Recent Data ----------------')
  print(df.tail())
  print('------------------------------------------------')

  open_price = 286.25
  pred_close = predict_close_with_open(df, open_price)

  print('The \'ol wise one predicts....')
  print('\tApple will close on {} ({}) today.'.format(pred_close, '+' + str(pred_close-open_price) if pred_close - open_price > 0 else pred_close-open_price)) 
