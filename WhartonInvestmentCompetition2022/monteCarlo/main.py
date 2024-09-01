import random
import numpy as np
import matplotlib.pyplot as plt
import csv

# General Plan
# Use Capm with beta as IV and ER as DV
# Use Monte Carlo to run a simulation within a standard deviation of some number to determine how many years we can rent the apartment

# Monte Carlo Parameters
iterations = 100000  # between 10,000 to 100,000
startrentprice = 28000#28000  # annual
marketstandarddeviation = 0.15#0.3162  # CHANGE #says 15% here (http://www.moneychimp.com/articles/volatility/standard_deviation.htm)
investmentamt = 80000  # how much money we are investing in the portfolio

# Capital Asset Pricing Model (CAPM) Parameters
riskfreerate = 0.03943  # risk-free rate
averagerentgrowth = 0.038 #historical rent from years 1980-2020(https://ipropertymanagement.com/research/average-rent-by-year) #how much rent grows on average
betalist = [i/10 for i in range(0, 21)]#[0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00, 2.25, 2.50, 2.75, 3.00, 4.00, 5.00]  # list of betas to test
# beta of the investment (how much risk the investment will add to a portfolio that looks like the market)
# note:if a stock is riskier than the market, it will have a beta greater than one
er_market = 0.1188  # expected return of the market

# Writing to datafile
datafilename = "MonteCarloSim_01.csv"
header = ['beta-value', 'expected-investment-return', 'avg-years-alive']

datafile = open(datafilename, 'w+')
writer = csv.writer(datafile)
writer.writerow(header)


def capm_alg(betavalue):
    er_investment = 0  # expected return on investment
    marketriskpremium = er_market - riskfreerate  # return expected from the market above the risk-free rate
    i = betavalue * marketriskpremium
    er_investment = riskfreerate + i

    return er_investment

resultsstats = []
def monte_carlo(er_investment, iterations, investmentamt, betavalue):
    results = []


    for i in range(iterations):
        rentprice = startrentprice
        portfoliovalue = investmentamt  # value of the portfolio, investmentamt is initial value
        j = 0  # counter
        t = 1  # years that can pay rent

        while j == 0:
            #print("Year: " + str(t))
            # generate random value (weighted random for standard deviation from er_investment) - percentage
            mu = er_investment#mean return
            sigma = marketstandarddeviation*betavalue#standard deviation of investment
            marketreturn = np.random.normal(mu, sigma)  # value described above (for now just using the er_investment)

            netchange = portfoliovalue * max(marketreturn, -0.9)  # money gained/lost #put -0.9 because it should not be able to go down any further (the market won't dissapear)
            #print("Yearly starting portfolio value: " + str(portfoliovalue))
            #print("Net change: " + str(netchange))
            portfoliovalue = portfoliovalue + netchange  # adjust portfolio value
            #print("Ending Portfolio value: " + str(portfoliovalue))

            rentprice = rentprice + rentprice * averagerentgrowth #update yearly rent

            if (portfoliovalue < rentprice and t>15) or t>=40: #ends the simulation if does successfully for 40 years; won't end preumptively before the rent payments start
                j = 1

            else:
                t = t + 1
                if t>15:
                    portfoliovalue = portfoliovalue - rentprice
                #print("After Rent (if year>15): " + str(portfoliovalue))

        #print("SIM OVER")
        results.append(t-15)
    print("RESULTS")
    print(results)
    print(f"mean = {np.mean(results)}, std = {np.std(results)}")
    print(f"Percentiles: 10th-{np.percentile(results, 10)}, 25th-{np.percentile(results, 25)}, 50th-{np.percentile(results, 50)}, 75th-{np.percentile(results, 75)}, 90th-{np.percentile(results, 90)}")
    print(f"% survival 10 years {sum([(1 if y>=10 else 0) for y in results])/len(results)}; % survival 25 years {sum([(1 if y>=25 else 0) for y in results])/len(results)}")

    simstats = {"portfolio beta": betavalue,
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
    fig, axs = plt.subplots(1, 1,
                            figsize=(10, 7),
                            tight_layout=True)

    #axs.hist(results, bins=25)

    #plt.show()
    avg_year = sum(results) / iterations
    return avg_year


def run_sim(betalist, iterations, investmentamt):
    # for each beta, return the er_investment
    for beta in betalist:
        er_investment = capm_alg(beta)
        monte_carlo(er_investment, iterations, investmentamt, beta)
        #csvrow = [beta]
        #er_investment = capm_alg(beta)
        #print(er_investment)
        #csvrow.append(er_investment)
        #csvrow.append(monte_carlo(er_investment, iterations, investmentamt, beta))
        #writer.writerow(csvrow)


run_sim(betalist, iterations, investmentamt)

print('resultsstats')
mean_years = []
for i in resultsstats:
    print(i)
    mean_years.append(i["mean years"])

plt.plot(betalist, mean_years, color='#111111')
plt.title('Yoga Studio Expected Years v. Portfolio Beta')
plt.xlabel('Portfolio Beta (Risk-reward)')
plt.ylabel('Expected Years')
plt.fill_between(betalist, mean_years, color='#F8D7FF')
plt.show()

