import pandas as pd
import random
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

# This is where we put density, area, and population into a df
pdf = pd.read_csv("plots/State_Populations.csv")
sdf = pd.read_csv("plots/State_Densities.csv")
adf = pd.read_csv("plots/Areas.csv")

dens1970 = []
dens1980 = []
dens1990 = []
dens2000 = []
dens2010 = []

statePop1970 = []
statePop1980 = []
statePop1990 = []
statePop2000 = []
statePop2010 = []

area = []
stateName = []

for i in range(0, len(pdf)):
    statePop1970.append(pdf.iloc[i, 0])
    statePop1980.append(pdf.iloc[i, 1])
    statePop1990.append(pdf.iloc[i, 2])
    statePop2000.append(pdf.iloc[i, 3])
    statePop2010.append(pdf.iloc[i, 4])

    dens1970.append(sdf.iloc[i, 0])
    dens1980.append(sdf.iloc[i, 1])
    dens1990.append(sdf.iloc[i, 2])
    dens2000.append(sdf.iloc[i, 3])
    dens2010.append(sdf.iloc[i, 4])

    area.append(adf.iloc[i, 0])

    stateName.append(adf.iloc[i, 1])

s1970 = {
    'statePop': statePop1970,
    'stateDens': dens1970,
    'area': area,
    'stateName': stateName
}

s1980 = {
    'statePop': statePop1980,
    'stateDens': dens1980,
    'area': area,
    'stateName': stateName
}
s1990 = {
    'statePop': statePop1990,
    'stateDens': dens1990,
    'area': area,
    'stateName': stateName
}
s2000 = {
    'statePop': statePop2000,
    'stateDens': dens2000,
    'area': area,
    'stateName': stateName
}
s2010 = {
    'statePop': statePop2010,
    'stateDens': dens2010,
    'area': area,
    'stateName': stateName
}

df1970 = pd.DataFrame(s1970, columns=['statePop', 'stateDens', 'area', 'stateName'])
df1980 = pd.DataFrame(s1980, columns=['statePop', 'stateDens', 'area', 'stateName'])
df1990 = pd.DataFrame(s1990, columns=['statePop', 'stateDens', 'area', 'stateName'])
df2000 = pd.DataFrame(s2000, columns=['statePop', 'stateDens', 'area', 'stateName'])
df2010 = pd.DataFrame(s2010, columns=['statePop', 'stateDens', 'area', 'stateName'])

# Change the following code to include every election using the corresponding winner values
#1 = republican state
#0 = democrat state
Y = [1,1,1,1,0,1,0,0,0,1,1,0,1,0,1,0,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,0,1,0,1,0,1]
Y2 = []

#print("length of Y = {p1}".format(p1 = len(Y)))


for i in range(0, 51):
    Y.append(random.randrange(0, 2))
    Y2.append(random.randrange(0, 2))

X_train = df1970.iloc[:, 0:3]

regr = linear_model.LinearRegression()
regr.fit(X_train, Y)

X_test = df1980.iloc[:, 0:3]

y_pred = regr.predict(X_test)

print('Coefficients: \n', regr.coef_)
# The mean squared error
print('Mean squared error: %.2f'
      % mean_squared_error(Y2, y_pred))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f'
      % r2_score(Y2, y_pred))
