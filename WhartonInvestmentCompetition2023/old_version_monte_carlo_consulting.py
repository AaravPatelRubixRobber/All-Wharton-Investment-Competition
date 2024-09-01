import random
import numpy as np
import matplotlib.pyplot as plt
import csv


# Monte Carlo Parameters
iterations = 500  # between 10,000 to 100,000
initial_costs = 6000#28000  # annual
salary_costs = 40000
investmentamt = 75000  # how much money we are investing in the portfolio
average_inflation = 0.04

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

            netchange = portfoliovalue * max(marketreturn, -0.9)  # money gained/lost #put -0.9 because it should not be able to go down any further (the market won't dissapear)
            #print("Yearly starting portfolio value: " + str(portfoliovalue))
            #print("Net change: " + str(netchange))
            portfoliovalue = portfoliovalue + netchange/12#(netchange**(1/12) if netchange>0 else -(-netchange)**(1/12))  # adjust portfolio value
            #print("Ending Portfolio value: " + str(portfoliovalue))

            salaryprice = salaryprice + salaryprice * average_inflation/12 #update yearly rent

            if (portfoliovalue < salaryprice and t>15) or t>=40: #ends the simulation if does successfully for 40 years; won't end preumptively before the rent payments start
                j = 1

            else:
                t = t + 1/12
                if t>15:
                    portfoliovalue = portfoliovalue - salaryprice/12
                #print("After Rent (if year>15): " + str(portfoliovalue))

        #print("SIM OVER")
        results.append(t-15)


    print("RESULTS")
    print(results)
    print(f"mean = {np.mean(results)}, std = {np.std(results)}")
    print(f"Percentiles: 10th-{np.percentile(results, 10)}, 25th-{np.percentile(results, 25)}, 50th-{np.percentile(results, 50)}, 75th-{np.percentile(results, 75)}, 90th-{np.percentile(results, 90)}")
    print(f"% survival 10 years {sum([(1 if y>=10 else 0) for y in results])/len(results)}; % survival 25 years {sum([(1 if y>=25 else 0) for y in results])/len(results)}")

    simstats = {"portfolio volatility": volatility,
                "mean years": np.mean(results),
                "std years": np.std(results),
                "10th per": np.percentile(results, 10),
                "25th per": np.percentile(results, 25),
                "50th per": np.percentile(results, 50),
                "75th per": np.percentile(results, 75),
                "90th per": np.percentile(results, 90),
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


plt.plot(volatilities_list, mean_years, color='#111111')
plt.title('Yoga Studio Expected Years v. Portfolio Beta')
plt.xlabel('Portfolio Beta (Risk-reward)')
plt.ylabel('Expected Years')
plt.fill_between(volatilities_list, mean_years, color='#F8D7FF')
plt.show()

