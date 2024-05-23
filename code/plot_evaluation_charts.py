import pandas as pd
import os
import matplotlib.pyplot as plt


def draw_charts(column_name, ai_df_sorted, cmaq_df_clipped):
  # Plot the RMSE values
  plt.figure(figsize=(12, 6))
  plt.plot(ai_df_sorted['DATE'], ai_df_sorted[column_name], label='AI', color='green')
  plt.plot(cmaq_df_clipped['DATE'], cmaq_df_clipped[column_name], label='CMAQ', color='blue')

  # Customize the plot
  plt.xlabel('Date')
  plt.ylabel(column_name)
  plt.title(f'CMAQ AI Metrics - {column_name}')
  plt.legend()

  # Save the plot as a PNG file
  plt.grid(True)
  plt.tight_layout()
  plot_png_path = f'/groups/ESS3/zsun/cmaq/ai_results/evaluation/{column_name}_plot.png'
  plt.savefig(plot_png_path)
  print(f"Plot saved to {plot_png_path}")

def do_it():
  # read the CMAQ evaluation txt
  cmaq_eval_txt = "/groups/ESS/share/projects/SWUS3km/graph/12km/alleva_12km_o3_fore.txt"
  cmaq_df = pd.read_csv(cmaq_eval_txt)  # Assuming your data has no header
  
  # read all txt files in the evaluation folder
  directory_path = '/groups/ESS3/zsun/cmaq/ai_results/evaluation/'

  # Initialize an empty list to store DataFrames.
  dfs = []
  
  column_names = ['DATE', 'NSITES', 'AVG_OBS', 'AVG_MOD', 'RMSE', 'CORR', 'NMB', 'NME', 'MB', 'ME', 'AH', 'AFAR']
  
  # Iterate over the files in the directory.
  for filename in os.listdir(directory_path):
      if filename.startswith('eval'):  # Adjust the file extension as needed.
          file_path = os.path.join(directory_path, filename)

          # Read the CSV file into a DataFrame.
          df = pd.read_csv(file_path, names = column_names, header=None)  # Assuming your data has no header.

          # Append the DataFrame to the list.
          dfs.append(df)

  # Concatenate all DataFrames into a single DataFrame.
  ai_df = pd.concat(dfs, ignore_index=True)
  
  # Convert the 'DATE' column to a datetime object
  ai_df['DATE'] = pd.to_datetime(ai_df['DATE'], format='%Y%m%d')
  cmaq_df['DATE'] = pd.to_datetime(cmaq_df['DATE'], format='%Y%m%d')
  
  # Sort the DataFrame by the 'DATE' column
  ai_df_sorted = ai_df.sort_values(by='DATE')
  cmaq_df_sorted = cmaq_df.sort_values(by='DATE')
  
  min_date = ai_df_sorted['DATE'].min()
  cmaq_df_clipped = cmaq_df_sorted[cmaq_df_sorted['DATE'] >= min_date]
  cmaq_df_clipped.loc[cmaq_df_clipped['AH'] < 0, 'AH'] = 0
  
  for column_name in column_names:
    if column_name != "DATE":
      draw_charts(column_name, ai_df_sorted, cmaq_df_clipped)
  
  print("all done")
  
do_it()

