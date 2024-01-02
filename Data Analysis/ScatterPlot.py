from matplotlib import patches
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('finalDataset.csv', header=0, index_col=[0,3], na_filter=False)
df = df.drop(columns='Country Code')
df = df.replace('\n', '')
df = df.replace('', np.nan)
df = df.astype(dtype= {"HDI":"float64", "DALYs":"float64","GDP":"float64",
                "Life Expectancy":"float64", 'Mortality':"float64",
                "Inflation":"float64", "Healthcare expenditure":"float64",
                'Net Migration Rate':"float64"})

print(df.describe())
df = df.transpose()

ConCodes = list(set(df.loc['Continent Code',:]))
ConCodes.remove('Unknown')
colors = np.array(['tab:blue', 'tab:red', 'tab:orange', 'tab:green', 'tab:brown', 'tab:pink'])
colors = np.array(['darkgreen', 'limegreen', 'orange', 'red'])

# europe = patches.Patch(color='tab:blue', label='Europe')
# asia = patches.Patch(color='tab:green', label='Asia')
# oceania = patches.Patch(color='tab:pink', label='Oceania')
# northAm = patches.Patch(color='tab:red', label='North America')
# southAm = patches.Patch(color='tab:orange', label='South America')
# africa = patches.Patch(color='tab:brown', label='Africa')

vhigh = patches.Patch(color='darkgreen', label='Very High')
high = patches.Patch(color='limegreen', label='High')
med = patches.Patch(color='orange', label='Medium')
low = patches.Patch(color='red', label='Low')

fig = plt.figure()

def animateByYear(x, y, z=0, timeAnimation=True):
    ax = fig.add_subplot()
    ax.axis("off")
    threeDim = False
    endYear = 2021
    if z!=0:
        threeDim = True
        ax = fig.add_subplot(projection='3d')
    if not timeAnimation:
        endYear = 1991
    for year in range(1990, endYear):
        plt.cla()
        title =''
        if timeAnimation:
            title += f'{year} - '
        title += f'Variation of {x} according to {y} '
        if threeDim: 
            title += f'and {z}'
        ax.set_title(title)
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        # ax.set_yscale('log', base=10)
        if threeDim: ax.set_zlabel(z)
        plt.xlim(-40,40)
        plt.ylim(-50,50)
        
        if timeAnimation: temp = df.loc[:,(slice(None), year)]
        else: temp = df.loc[:,(slice(None), range(2000,2020))]
        # print(temp)
        
        temp = temp.transpose()
        temp = temp[temp['Continent Code']!="Unknown"]
        temp = temp[temp['HDI']>0]
        temp.fillna(method='bfill')
        # for col in temp.columns:

        xAx, yAx = list(temp.loc[:,x]), list(temp.loc[:,y])
        xAx = list(map(lambda x: round(x, ndigits=3), xAx))
        yAx = list(map(lambda x: round(x, ndigits=3), yAx))
        
        if threeDim: 
            zAx = (temp.loc[:,z])
            zAx = list(map(lambda x: round(x, ndigits=3), zAx))

        # continents = list(temp['Continent Code'])
        # categories = []
        # for c in continents:
        #     if c == "EU": categories.append(0)
        #     elif c == "NA": categories.append(1)
        #     elif c == "SA": categories.append(2)
        #     elif c == "AS": categories.append(3)
        #     elif c == "AF": categories.append(4)
        #     elif c == "OC": categories.append(5)
        #     else: print(c)
            
        hdis = list(temp['HDI'])
        categories = []
        for h in hdis:
            if h >= 0.8: categories.append(0)
            elif h >= 0.7: categories.append(1)
            elif h >= 0.55: categories.append(2)
            elif h > 0: categories.append(3)
            else: print(h)

        if threeDim:
            ax.scatter(xAx, yAx, zAx, marker='o', s=20, c=colors[categories], alpha=0.7)
            ax.set_xlim(-20,20)

            # ax.set_ylim(-10,20) #GDP
            # ax.set_zlim(-10, 100) #Inflation
            ax.set_ylim(10,50) #Mortality
            ax.set_zlim(0,100_000) #DALYs
        else:
            ax.scatter(xAx, yAx, s=20, c=colors[categories], alpha=0.3)
        # plt.legend(handles=[europe, asia, northAm, southAm, africa, oceania], 
        #                         bbox_to_anchor=(-0.5, 0),
        #                         loc='lower left'),        
        plt.legend(handles=[vhigh, high, med, low], 
                                bbox_to_anchor=(-0.5, 0),
                                loc='lower left',
                                title = 'Human Development Index'),
        plt.pause(1)
    plt.show()

if __name__ == '__main__':
    animateByYear("Net Migration Rate", "Mortality", "DALYs", True)#, "Mortality from CVD", False)