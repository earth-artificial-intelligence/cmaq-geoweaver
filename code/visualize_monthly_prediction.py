import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv('/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/prediction.csv')

plt.rc('font', size=15)
fig, ax = plt.subplots(figsize=(25, 4))

# Specify how our lines should look
ax.plot(dataset.Date, dataset.prediction, color='tab:red',  label='Prediction')
ax.plot(dataset.Date, dataset.O3_AVG, color='tab:blue',
        label='CMAQ')

# Use linestyle keyword to style our plot
ax.plot(dataset.Date, dataset.AirNow_O3, color='tab:green',
        label='AirNow',linestyle='--')

# Same as above
ax.set_xlabel('Date',size=20)
ax.set_ylabel('O3 (ppbv)',size=20)
ax.set_title('February',fontsize=25)
ax.grid(True)
plt.xticks(rotation=45)
ax.legend(loc='upper left')
fig.savefig('/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/pred_monthly.png')


