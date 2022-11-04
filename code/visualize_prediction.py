import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv('/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/prediction.csv')

    
plt.rc('font', size=12)
fig, ax = plt.subplots(figsize=(20, 13))

# Specify how our lines should look
ax.plot(dataset.Date, dataset.prediction, color='tab:orange', label='Prediction')
# Use linestyle keyword to style our plot
ax.plot(dataset.Date, dataset.AirNow_O3, color='green', linestyle='--',
        label='AirNow')

ax.plot(dataset.Date, dataset.O3_AVG, color='blue', linestyle='--',
        label='CMAQ_O3')
# Redisplay the legend to show our new wind gust line
ax.legend(loc='upper left')
# Same as above
ax.set_xlabel('Time')
plt.xticks(rotation=45)
ax.set_ylabel('Values')
ax.set_title('Compare Observed, Prediction, CMAQ Simulation')
ax.grid(True)
ax.legend(loc='upper left')
fig.savefig('/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/pred.png')

