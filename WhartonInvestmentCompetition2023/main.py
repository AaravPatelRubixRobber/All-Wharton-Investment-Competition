import numpy as np
import pandas as pd
from matplotlib import cm
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
import yfinance as yf

#https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html - can use this data
#VXUS IS THE INTERNATIONAL FULL MARKET PORTFOLIO


#CAN SAY FOR SAKE OF SIMULATION, USED THE S&P 500 SINCE HAS THE MOST DATA

assets = ['SPY', 'BND']

"""
def getOldData():
    pf_data = pd.DataFrame()
    for x in assets:
        pf_data[x] = yf.download(x, '1970-1-1')['Adj Close']#wb.DataReader(x, data_source = 'yahoo', start = '2015-1-1')['Adj Close']

    return pf_data
"""

def adjustSPYbeta(spy_data = [100, 102, 103, 106, 103], beta=1):
    pct_changes = []

    for i in range(len(spy_data)-1):
        pct_changes.append(spy_data[i+1]/spy_data[i])

    new_pct_changes = [(i-1)*beta + 1 for i in pct_changes]

    new_spy_data = [spy_data[0]]
    for i in range(len(spy_data)-1):
        new_spy_data.append(new_spy_data[-1]*new_pct_changes[i])

    print(new_spy_data)
    return new_spy_data



def getNewData(beta = 1):
    import pandas as pd
    df = pd.read_excel('HistoricReturnsNYU.xlsx')

    selected_columns = ['S&P 500 (includes dividends)3', 'US T. Bond5']
    filtered_df = df[selected_columns]

    filtered_df['S&P 500 (includes dividends)3'] = adjustSPYbeta(filtered_df['S&P 500 (includes dividends)3'].astype(float).tolist(), beta)
    filtered_df['US T. Bond5'] = filtered_df['US T. Bond5'].astype(float)

    return filtered_df


def conduct_calculations(show_graphs = True):

    all_simulations = pd.DataFrame()

    for hundred_beta in range(50, 151):
        print('beta number: ', hundred_beta/100)
        pf_data = getNewData(hundred_beta/100)
        #pf_test_data = getOldData()

        if show_graphs:
            (pf_data / pf_data.iloc[0]*100).plot()
            plt.show()

        log_returns = np.log(pf_data/pf_data.shift(1))

        #log_returns.mean() * 250

        #log_returns.cov() * 250

        #log_returns.corr()

        portfolio_weights = []
        portfolio_returns = []
        portfolio_volatilities = []
        for x in range(1001):
            '''weights = np.random.random(len(assets))
            weights /= np.sum(weights)'''
            weights = np.array([x/1000, 1-x/1000])

            portfolio_weights.append(weights[0])
            portfolio_returns.append(np.sum(weights * log_returns.mean())) #* 250
            portfolio_volatilities.append(np.sqrt(np.dot(weights.T, np.dot(log_returns.cov(), weights)))) #cov() * 250

        portfolio_weights = np.array(portfolio_weights)
        portfolio_returns = np.array(portfolio_returns)
        portfolio_volatilities = np.array(portfolio_volatilities)

        #print(portfolio_weights, portfolio_returns, portfolio_volatilities)

        #np.sum(weights * log_returns.mean())# * 250

        #np.sqrt(np.dot(weights.T, np.dot(log_returns.cov(), weights))) #log_returns.cov() * 250

        color = '#{:02X}{:02X}{:02X}'.format(0, 2*(hundred_beta-50), 255)
        portfolios = pd.DataFrame({'SPYBeta': hundred_beta/100, 'SPYWeight': portfolio_weights, 'Return': portfolio_returns, 'Volatility':portfolio_volatilities, 'Color': color})

        if show_graphs:
            portfolios.plot(x='Volatility', y='Return', kind='scatter', figsize=(15,10));
            plt.xlabel('Expected Volatility')
            plt.ylabel('Expected Return')

            norm = plt.Normalize(50, 150)
            sm = cm.ScalarMappable(cmap='plasma', norm=norm)
            sm.set_array([])
            plt.colorbar(sm, label='Color bar key')

            plt.show()

        #print(portfolios)

        all_simulations = pd.concat([all_simulations, portfolios], ignore_index=True)

    print(all_simulations)

    return all_simulations

def show_all_simulation_data(all_simulations):
    all_simulations.plot(x='Volatility', y='Return', kind='scatter', figsize=(15,10), c='Color')
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.show()

    return all_simulations

all_simulations_df = pd.read_csv('all_simulations_df.csv')#conduct_calculations(True)#pd.read_csv('all_simulations_df.csv')#conduct_calculations(False)
all_simulations_df.to_csv('all_simulations_df.csv', index=False)

#show_all_simulation_data(all_simulations_df)

min_vol = min(all_simulations_df['Volatility'])
max_vol = max(all_simulations_df['Volatility'])

efficient_frontier_portfolios = pd.DataFrame()

for i in range(100):
    lb_vol = min_vol + i*(max_vol - min_vol)/100
    ub_vol = min_vol + (i+1)*(max_vol - min_vol)/100
    print(lb_vol, ub_vol)

    parsed_df = all_simulations_df[(all_simulations_df['Volatility'] >= lb_vol) & (all_simulations_df['Volatility'] <= ub_vol)]
    print(parsed_df)

    max_index = parsed_df['Return'].idxmax()
    max_row = parsed_df.loc[max_index]

    efficient_frontier_portfolios = efficient_frontier_portfolios.append(max_row)

def show_efficient_frontier_data(all_simulations, efficient_frontier):
    all_simulations.loc[all_simulations.index.isin(list(efficient_frontier.index)), 'Color'] = 'r'
    column_name = 'Color'
    specific_value = 'r'
    mask = all_simulations[column_name] == specific_value
    all_simulations = pd.concat([all_simulations[~mask], all_simulations[mask]])

    all_simulations.plot(x='Volatility', y='Return', kind='scatter', figsize=(15,10), c='Color')
    #plt.plot(all_simulations[['Volatility', 'Return']], color='g', label='all portfolios')#all_simulations['Color']
    #efficient_frontier.plot(x='Volatility', y='Return', kind='scatter', figsize=(15,10), c='Red')
    #plt.plot(efficient_frontier[['Volatility', 'Return']], color='r', label='efficient frontier')

    plt.title('Portfolio Return v Volatility')
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.show()

print(efficient_frontier_portfolios)
efficient_frontier_portfolios.to_csv('efficient_frontier_df.csv', index=False)

show_efficient_frontier_data(all_simulations_df, efficient_frontier_portfolios)






