import random
import numpy as np
import matplotlib.pyplot as plt
import csv


# Monte Carlo Parameters
iterations = 5000  # between 10,000 to 100,000
initial_costs = 6000#28000  # annual
salary_costs = 60000/12
investmentamt = 75000  # how much money we are investing in the portfolio
average_inflation = 1.04**(1/12) - 1

resultsstats = []
def monte_carlo(expected_return, volatility, investmentamt, iterations):
    results = []

    for i in range(iterations):
        salaryprice = salary_costs
        portfoliovalue = investmentamt  # value of the portfolio, investmentamt is initial value
        j = 0  # counter
        t = 1.0  # years that can pay rent

        while j == 0:
            if int(t*12) % 12 == 0: #update every year because otherwise compounding it would lead to issues
                mu = expected_return#mean return
                sigma = volatility#standard deviation of investment
                marketreturn = np.random.normal(mu, sigma)  # value described above (for now just using the er_investment)

            netchange = portfoliovalue * max(marketreturn, -0.9)/12  # money gained/lost #put -0.9 because it should not be able to go down any further (the market won't dissapear)
            #print("Yearly starting portfolio value: " + str(portfoliovalue))
            #print("Net change: " + str(netchange))
            portfoliovalue = portfoliovalue + netchange#(netchange**(1/12) if netchange>0 else -(-netchange)**(1/12))  # adjust portfolio value
            #print("Ending Portfolio value: " + str(portfoliovalue))

            salaryprice = salaryprice + salaryprice * average_inflation #update yearly rent

            if (portfoliovalue < salaryprice and t>15) or t>=25: #ends the simulation if does successfully for 40 years; won't end preumptively before the rent payments start
                j = 1

            else:
                t = t + 1/12
                if t==15: #initial costs
                    portfoliovalue = portfoliovalue - initial_costs
                if t>=15: #salary
                    portfoliovalue = portfoliovalue - salaryprice
                #print("After Rent (if year>15): " + str(portfoliovalue))

        #print("SIM OVER")
        results.append(t-15)


    print("RESULTS")
    print(results)
    print(f"mean = {np.mean(results)}, std = {np.std(results)}")
    print(f"Percentiles: 5th-{np.percentile(results, 5)}, 25th-{np.percentile(results, 25)}, 50th-{np.percentile(results, 50)}, 75th-{np.percentile(results, 75)}, 95th-{np.percentile(results, 95)}")
    print(f"% survival 10 years {sum([(1 if y>=10 else 0) for y in results])/len(results)}; % survival 25 years {sum([(1 if y>=25 else 0) for y in results])/len(results)}")

    simstats = {"portfolio volatility": volatility,
                "mean years": np.mean(results),
                "std years": np.std(results),
                "5th per": np.percentile(results, 5),
                "25th per": np.percentile(results, 25),
                "50th per": np.percentile(results, 50),
                "75th per": np.percentile(results, 75),
                "95th per": np.percentile(results, 95),
                "10 year survival rate": sum([(1 if y>=10 else 0) for y in results])/len(results),
                "25 year survival rate": sum([(1 if y>=25 else 0) for y in results])/len(results)}
    resultsstats.append(simstats)

    # plt.axhline(y=10, color='r', linestyle='-')
    #plt.title("Beta Value: " + str(betavalue))
    #plt.xlabel("Iterations")
    #plt.ylabel("Probability")
    #plt.plot(results)
    #plt.xlim(0, iterations)
    #plt.ylim(0, 50)


    #plt.hist(results, 13, density=1)
    '''fig, axs = plt.subplots(1, 1,
                            figsize=(10, 7),
                            tight_layout=True)'''

    #axs.hist(results, bins=25)

    #plt.show()
    avg_year = sum(results) / iterations
    return avg_year




def run_sim(returns, volatilities, investmentamt, iterations):
    # for each beta, return the er_investment
    for r, v in zip(returns, volatilities):
        monte_carlo(r, v, investmentamt, iterations)


#START OF THE PROGRAM
import pandas as pd
efficient_frontier_df = pd.read_csv('efficient_frontier_df.csv')


returns_list = efficient_frontier_df['Return']#[0.1, 0.1, 0.1]
volatilities_list = efficient_frontier_df['Volatility']#[0.20, 0.24, 0.25]
run_sim(returns_list, volatilities_list, investmentamt, iterations)

print('resultsstats')
mean_years = []
for i in resultsstats:
    print(i)
    mean_years.append(i["mean years"])

b5_years = []
for i in resultsstats:
    print(i)
    b5_years.append(i["5th per"])
Q1_years = []
for i in resultsstats:
    print(i)
    Q1_years.append(i["25th per"])
median_years = []
for i in resultsstats:
    print(i)
    median_years.append(i["50th per"])
Q3_years = []
for i in resultsstats:
    print(i)
    Q3_years.append(i["75th per"])
b95_years = []
for i in resultsstats:
    print(i)
    b95_years.append(i["95th per"])


plt.plot(volatilities_list, b5_years, color='red')#'#111111'
plt.plot(volatilities_list, Q1_years, color='yellow')
plt.plot(volatilities_list, median_years, color='green')
plt.plot(volatilities_list, Q3_years, color='blue')
plt.plot(volatilities_list, b95_years, color='purple')
plt.title('Expected Years of Salary Payments v. Portfolio Volatility')
plt.xlabel('Portfolio Volatility')
plt.ylabel('Expected Years')

custom_handles = [plt.Line2D([0], [0], color='purple', lw=2),
                  plt.Line2D([0], [0], color='blue', lw=2),
                  plt.Line2D([0], [0], color='green', lw=2),
                  plt.Line2D([0], [0], color='yellow', lw=2),
                  plt.Line2D([0], [0], color='red', lw=2)
                  ]
custom_labels = ['95th%', '75th%', '50th%', '25th%', '5th%']

# Add the legend with custom labels
plt.legend(custom_handles, custom_labels, loc='upper right')
#plt.fill_between(volatilities_list, mean_years, color='#F8D7FF')
plt.show()

