import yfinance as yf
import GrowthEstimateScraper
import SentimentAnalysis
import pandas as pd
import os
import datetime

basicMaterials = ['APD', 'ACH', '00914', 'ASH', '500820', '500027', '509480', 'BHP', 'CAR', 'CHNR', 'CLW', 'CSNA3', 'CTVA', 'EMN', 'FMC', 'FCX', 'FFHL', 'GLEN', '500440', 'IOSP', 'JMAT', 'KALU', 'KL', 'KLBN11', 'MNDI', 'NTIC', 'NTR', 'PKX', 'KWR', 'RIO', 'RGLD', 'SUZB3', '500470', '532538', 'X', 'VALE3', '500295']#[]#['APD', 'ACH', 'ASH', '500027', 'BHP', 'BRKM5', 'CHNR', 'CLW', 'CSNA3', 'EMN', 'FMC', 'FCX', 'FFHL', 'GGBR4', 'GLEN', '500440', 'IOSP', 'JMAT', 'KALU', 'KL', 'KLBN11', 'MMAT', 'NP', 'NTIC', 'PKX', 'KWR', 'ROLL', 'RIO', 'RGLD', 'SUZB3', '500470', 'X', 'VALE3', '500295']
consumerDiscretionary = ['ANF', 'BABA', 'AMZN', 'AEO', 'APTV', 'AZO', '532977', 'BNED', '500043', 'BBBY', 'BBY', 'BWA', '500530', 'BBW', 'BURL', 'CZR', 'GOOS', 'KMX', 'CCL', 'CAKE', 'CAAS', '601888', 'CMG', 'CPG', 'DG', 'DLTR', 'DOL', 'DOM', 'ETSY', 'FL', 'F', 'GPS', 'GRMN', 'GM', 'GRPN', 'HRB', 'HOG', 'HAS', '500182', 'HIBB', 'HD', 'HMC', 'HSW', 'H', 'IHG', '533155', 'LE', 'LVS', 'LCII', 'LREN3', 'LOOK', 'LOW', 'LULU', 'M', 'MGLU3', '500520', 'MAR', '532500', 'MAT', 'MCD', '03690', '000333', 'MOV', 'EDU', 'NXT', 'NKE', 'NCLH', 'OTB', 'ORLY', 'PZZA', 'PTON', 'PLNT', 'QSR', 'SWBI', 'SONY', 'SBUX', 'SFIX', 'TAL', 'TGT', '500570', 'TSLA', 'TXRH', 'TCS', 'WEN', '500114', 'TJX', 'TM', 'ULTA', 'UAA', 'URBN', 'VRA', 'VFC', 'WTB', 'WSM', 'WH', 'YUM']#[]#['ANF', 'ATVI', 'AC', 'BABA', 'ATD.B', 'AMZN', 'AMC', 'AAL', 'AEO', 'APTV', 'AZO', 'AVP', '532977', 'BNED', '500043', 'BBBY', 'BBY', 'BWA', '500530', 'BYD', 'BBW', 'BURL', 'CZR', 'GOOS', 'KMX', 'CCL', 'CAKE', 'CAAS', 'CEA', 'ZNH', '601888', 'CMG', 'CPG', 'COST', 'DJCO', 'DAL', 'DG', 'DLTR', 'DOL', 'DOM', 'DPZ', 'EZJ', 'EDR', 'ETSY', 'FL', 'F', 'GPS', 'GM', 'HRB', 'HOG', 'HAS', '500182', 'HIBB', 'HD', 'HMC', 'HSW', 'H', 'IMAX', 'IHG', 'JBLU', '533155', 'LE', 'LVS', 'LCII', 'RENT3', 'LAME4', 'LREN3', 'LOOK', 'LULU', 'LYFT', 'M', 'MGLU3', '500520', 'MAR', '532500', 'MAT', 'MCD', '000333', 'MOV', 'NTES', 'NFLX', 'EDU', 'NXT', 'NKE', 'NCLH', 'OTB', 'ORLY', 'PZZA', 'PSON', 'PTON', 'PLNT', 'QSR', 'REV', 'RBA', 'SIRI', 'SKYW', 'SWBI', 'SONY', 'LUV', 'SAVE', 'SPOT', 'SBUX', 'SFIX', 'TAL', 'TGT', '500570', 'TSLA', 'TXRH', 'TCS', 'EL', 'DIS', 'WEN', 'NCTY', '500114', 'TJX', 'TM', 'UBER', 'ULTA', 'UAA', 'URBN', 'VRA', 'VFC', 'WMT', 'WTB', 'WSM', 'WH', 'YUM', 'ZNGA']
consumerStaples = ['ATD.B', 'ABEV3', 'CRFB3', 'BRFS3', 'CPB', 'CASY', 'KO', 'CL', 'COST', 'DEO', 'GIS', '540743', '532424', '500696', '500875', 'JJSF', 'JBSS3', 'K', 'KDP', '600519', 'MDIA3', 'MKC', 'TAP', 'MNST', 'FIZZ', 'NTCO3', '500790', 'PEP', 'PG', 'RADL3', 'RKT', 'REV', 'RAD', 'SBRY', 'SFM', 'SYY', 'EL', 'HSY', 'TR', 'THS', 'TSN', 'ULVR', 'UL', 'UNFI', 'WBA', 'WMT', 'WDFC', '000858', 'WYN']#[]#['RKT', 'ABEV3', 'CRFB3', 'BRFS3', 'CPB', 'CASY', 'KO', 'CL', 'CORE', 'CTVA', 'CVS', 'DEO', 'GIS', '540743', '532424', '500696', '500875', 'JJSF', 'SBRY', 'JBSS3', 'K', 'KDP', '600519', 'MDIA3', 'MKC', 'MCK', 'TAP', 'MNST', 'FIZZ', '500790', 'PEP', 'PG', 'RADL3', 'RKT', 'RAD', 'SFM', 'SYY', 'HSY', 'TR', 'THS', 'TSN', 'UL', 'ULVR', 'UNFI', 'WBA', 'WDFC', '000858', 'WYN']
energy = ['AMTX', 'BP', 'CCJ', 'CNQ', 'CVX', 'SNP', '533278', 'CLR', 'CSAN3', 'ENB', 'ET', 'XOM', 'HES', 'KMI', 'LAM', 'NGS', 'NOV', '500312', 'OKE', 'PTR', 'PETR3', 'PSX', '500325', 'RDSA', 'SU', 'SUN', 'TRP', 'TLW', 'UGPA3']#[]#['AMTX', 'BP', 'CCJ', 'CNQ', 'CVX', 'SNP', '00386', '533278', 'CLR', 'CSAN3', 'ET', 'XOM', '532155', 'HES', 'LAM', 'NGS', 'NOV', '500312', 'OKE', 'BRDT3', 'PTR', '00857', 'PETR3', 'PETR4', 'PSX', '500325', 'RDSA', 'SU', 'SUN', 'TLW', 'UGPA3']
financials = ['AFL', 'ALL', 'AXP', 'APAM', 'AV.', '532215', 'B3SA3', '532978', 'BPAC11', 'BBAS3', 'SANB11', 'BBDC3', 'BAC', '002142', 'BNS', 'OZK', 'BCS', 'BBSE3', 'BLK', 'BX', 'BAM', 'CWB', '00939', 'JRJC', 'C', 'CLIG', 'CS', 'DB', 'DFS', 'FFH', 'BEN', 'GBCI', 'GS', 'GWO', '500180', '500010', 'HSBA', '532174', 'ICE', 'IRBR3', 'JPM', 'KEY', 'KKR', '500247', 'LAZ', 'LLOY', 'L', 'MTB', '500271', 'MET', 'MCO', 'MS', 'NWG', 'ONB', 'OPY', '02318', '500302', 'PNC', 'PSSA3', 'TROW', 'PRU', '532955', 'RF', 'RY', 'SDR', 'SEIC', 'STAN', '500112', 'SULA11', 'UBS', 'WFC', '532648']#[]#['AFL', 'ALL', 'APAM', 'AV.', '532215', 'B3SA3', '532978', 'BBDC3', 'BBDC4', 'BPAC11', 'BBAS3', 'SANB11', 'BAC', '002142', 'BNS', 'OZK', 'BCS', 'BBSE3', 'BLK', 'BX', 'BPFH', 'CWB', '00939', 'JRJC', 'C', 'CLIG', 'CS', 'DB', 'DFS', 'FFH', 'BEN', 'GBCI', 'GS', 'GEG', 'GWO', '500180', '500010', 'HSBA', '532174', 'ICE', 'IRBR3', 'ITUB4', 'ITSA4', 'JPM', 'KEY', 'KKR', '500247', 'LAZ', 'LLOY', 'L', 'MTB', '500271', 'MET', 'MCO', 'MS', 'NWG', 'ONB', 'OPY', '02318', 'PNC', 'PSSA3', 'PRU', '532955', 'RF', 'RY', 'SDR', 'SEIC', 'STAN', '500112', 'SULA11', 'TROW', 'UBS', 'WFC', 'WBK', '532648']
healthCare = ['ABT', 'ABBV', 'ACHC', 'AMGN', 'AMN', 'AZN', '524804', 'ACB', 'BAX', 'BMY', 'CSII', 'CPRX', 'CNC', '500087', 'CVS', '500124', 'ENDP', 'GMAB', 'GILD', 'GSK', 'GMED', '532482', 'GEG', 'HBIO', 'HYPE3', 'ILMN', 'IQV', '600276', 'JNJ', 'MCK', 'MDC', 'MRK', 'MYGN', 'GNDI3', 'NVS', 'PFE', 'PBH', 'REGN', '300760', 'SN.', '524715', 'TEVA', 'UNH', 'VEEV', 'VYNT', 'ZGNX']#['EGIE3.SA']#['ABT', 'ABBV', 'ACHC', 'AMGN', 'AZN', '524804', 'ACB', 'BAX', 'BMY', 'CSII', 'CPRX', 'CNC', '500087', '500124', 'ENDP', 'GMAB', 'GILD', 'GSK', 'GMED', '532482', 'HBIO', 'HYPE3', 'ILMN', 'IQV', '600276', 'JNJ', 'MDC', 'MRK', 'MYGN', 'GNDI3', 'NVS', 'PFE', '500302', 'PBH', 'REGN', '300760', 'SN.', '524715', 'TEVA', 'TVTY', 'UNH', 'VEEV', 'VYNT', 'ZGNX']
industrials = ['AC', 'AAL', 'ARCB', 'ASGN', 'BECN', '500103', 'BA', 'BBD.B', 'BYD', 'BNZL', 'CNI', 'CP', 'CJT', 'CAT', 'CCRO3', 'CEA', 'ZNH', '03311', 'CYD', '00267', 'DE', 'DAL', 'DSCV', 'PLOW', 'EZJ', 'EMBR3', 'EXPN', 'FERG', 'FCN', 'GD', 'GE', 'ROCK', 'GAPB', 'HTLD', 'JBLU', '500510', 'RENT3', 'LMT', 'LYFT', 'NOC', 'PCAR', 'RTX', 'ROLL', 'RBA', 'RR.', 'RAIL3', '600009', 'SKYW', 'SMIN', 'SNA', 'LUV', 'SAVE', 'MIDD', 'TWI', 'TREX', 'UBER', 'VRSK', 'WNC', 'WEGE3', 'ZTO']#[]#['AXP', 'AMN', '600585', '00914', 'ARCB', 'ASGN', '500820', 'BECN', '509480', '500103', 'BILL', 'BA', 'BBD.B', 'BNZL', 'CAR', 'CJT', 'CAT', 'CCRO3', '03311', 'CYD', 'CIEL3', '00267', 'DE', 'PLOW', 'EMBR3', 'EXPN', 'FICO', 'FERG', 'FCN', 'GE', 'ROCK', 'GAPB', 'HTLD', 'KSU', '500510', 'LMT', 'MA', 'MNDI', '500304', 'PCAR', 'PYPL', 'RTX', 'RR.', 'RAIL3', '600009', 'SMIN', 'SNA', 'MIDD', 'TWI', 'TREX', '532538', 'VRSK', 'V', 'WNC', 'WEGE3', 'ZTO']
realEstate = ['BRML3', '000002', '600007', 'DLR', 'EXR', 'IRM', 'MULT3', 'DOC', 'PSA', 'GEO']#[]#['BRML3', '000002', '02202', '600007', 'DLR', 'EXR', 'IRM', 'MULT3', 'DOC', 'PSA', 'RMV', 'GEO']
technology = ['ADBE', 'AMD', 'AAPL', 'ANET', '532493', 'BNFT', 'BILL', 'AVGO', 'CIEL3', 'CSCO', 'CTSH', 'CSU', 'DBX', 'DXC', '532927', 'ENGH', 'FICO', 'FTNT', '601138', '002415', '532281', '500209', 'INTC', 'MANH', 'MA', 'MMAT', 'MCRO', 'MSFT', '532819', '500304', 'NVDA', 'NXPI', 'ORCL', 'PYPL', 'QCOM', 'SGE', 'CRM', 'SAP', 'SHOP', 'SNOW', 'TSM', '532540', '532755', 'TXN', 'UTSI', 'V', '507685', 'XRX']#[]#['ADBE', 'GOOG', 'AAPL', 'BIDU', 'BNFT', 'CTSH', 'CSU', 'DSCV', 'DXC', '532927', 'ENGH', 'FB', 'FTNT', 'GRPN', '002415', '532281', '500209', '535648', 'MANH', 'MTCH', '03690', 'MCRO', 'MSFT', '532819', 'NVDA', 'NXPI', 'ORCL', 'QCOM', 'SGE', 'CRM', 'SAP', 'SHOP', 'SOHU', '532540', '532755', '00700', 'TWTR', '507685', 'XRX']
telecommunications = ['ATVI', 'GOOG', 'AMC', 'T', 'BIDU', 'BCE', '532454', 'BT.A', '00941', 'CMCSA', 'DJCO', 'EDR', 'FB', 'GOGO', 'IMAX', '535648', 'MTCH', 'NTES', 'NFLX', 'PSON', 'RMV', 'RCI', 'SIRI', 'SOHU', 'SPOT', 'TU', '00700', 'DIS', 'NCTY', 'TWTR', 'VEON', 'VZ', 'VOD']#[]#['ANET', '532493', 'T', 'BCE', '532454', 'BT.A', '00941', 'CMCSA', '601138', 'GOGO', 'VIVT3', 'UTSI', 'VEON', 'VZ', 'VOD']
utilities = ['AEP', 'AWK', 'CU', 'ELET3', '00384', '600900', 'SBSP3', 'CPFE3', 'D', 'EGIE3', 'EQTL3', 'FE', 'FTS', '532155', '517300', 'HNP', 'MSEX', 'NFG', '532555', 'PCG', '532898', 'SRE', 'SVT', '533206', 'SJW', 'SO', 'SSE', '500400', 'YORW', 'UGI', 'UU.']#[]#['AEP', 'AWK', 'CU', 'ELET3', 'ELET6', '00384', '600900', 'SBSP3', 'CMIG4', 'CPFE3', 'D', 'ENGI11', 'EGIE3', 'EQTL3', 'FE', '517300', 'HNP', 'MSEX', 'NFG', '532555', 'PCG', '532898', 'SRE', 'SVT', '533206', 'SJW', 'SO', 'SSE', '500400', 'YORW', 'UGI', 'UU.']


sectorIndices = {0: "basicMaterials",
             1: "consumerDiscretionary",
             2: "consumerStaples",
             3: "energy",
             4: "financials",
             5: "healthCare",
             6: "industrials",
             7: "realEstate",
             8: "technology",
             9: "telecommunications",
             10: "utilities"}

allStocks = [basicMaterials,
             consumerDiscretionary,
             consumerStaples,
             energy,
             financials,
             healthCare,
             industrials,
             realEstate,
             technology,
             telecommunications,
             utilities]

#def calcScoreRisk(ticker):
"""
def calcScoreValue(ticker):
    print('Calculating value score...')

    score = 0
    passCriteria = 1

    #GETS TICKER INFO
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        print('info', info)
        assert(len(info) > 10)
    except:
        print('error with retrieving ticker')
        return -1

    #CALCULATES SCORES FOR EACH METRIC

    #forwardPE
    try:
        forwardPE = 1000/info['forwardPE']
        if info['forwardPE'] > 25 or info['forwardPE'] < 0: passCriteria -= 2
        print('forwardPE', info['forwardPE'])
    except:
        print('error with forward p/e... will try supplementing with trailing p/e')
        try:
            forwardPE = 1000/info['trailingPE']
            if info['trailingPE'] > 25 or info['trailingPE'] < 0: passCriteria -= 2
            print('trailingPE', info['trailingPE'])
        except:
            print('error with trailing p/e')
            forwardPE = 0


    #currentRatio
    try:
        currentRatio = 7*info['currentRatio']
        if info['currentRatio'] < 1:
            passCriteria -= 1
            currentRatio = -75
        elif info['currentRatio'] < 1: currentRatio = -35
        print('current ratio', info['currentRatio'])
    except:
        print('error with current ratio')
        currentRatio = 0

    #profit margins
    try:
        profitMargin = 15*abs(info['profitMargins'])**0.5
        if info['profitMargins'] < 0.12: passCriteria -= 1
        print('profit margin', info['profitMargins'])
    except:
        print('error with profit margin')
        profitMargin = 0

    #debt to Equity
    try:
        debtToEquity = (200-info['debtToEquity'])/8
        if info['debtToEquity'] > 200 or info['debtToEquity'] < 0: passCriteria -= 1
        print('debt to equity', info['debtToEquity'])
    except:
        print('error with debt to equity')
        debtToEquity = 0

    if passCriteria <= 0:
        print('failed criteria')
        return -1


    #CALCULATES FINAL SCORE
    score = forwardPE + currentRatio + profitMargin + debtToEquity
    return score
"""

def calcScoreValue(ticker):
    print('Calculating value score...')

    score = 0
    passCriteria = 2

    #GETS TICKER INFO
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        print('info', info)
        assert(len(info) > 10)
    except:
        print('error with retrieving ticker')
        return -1

    #CALCULATES SCORES FOR EACH METRIC

    #forwardPE
    try:
        if info['forwardPE'] > 25 or info['forwardPE'] < 0:
            passCriteria -= 2
            forwardPE = 0
        elif info['forwardPE'] > 20 or info['forwardPE'] < 0:
            forwardPE = 1
        else:
            forwardPE = 2
        print('forwardPE', info['forwardPE'])
    except:
        print('error with forward p/e... will try supplementing with trailing p/e')
        try:
            if info['trailingPE'] > 25 or info['trailingPE'] < 0:
                passCriteria -= 2
                forwardPE = 0
            elif info['trailingPE'] > 20 or info['trailingPE'] < 0:
                forwardPE = 1
            else:
                forwardPE = 2
            print('trailingPE', info['trailingPE'])

        except:
            print('error with trailing p/e')
            forwardPE = -1


    #currentRatio
    try:
        if info['currentRatio'] < 1:
            passCriteria -= 1
            currentRatio = 0
        elif info['currentRatio'] < 2:
            currentRatio = 1
        else:
            currentRatio = 2
        print('current ratio', info['currentRatio'])
    except:
        print('error with current ratio')
        currentRatio = -1

    #profit margins
    try:
        if info['profitMargins'] < 0.12:
            passCriteria -= 1
            profitMargin = 0
        elif info['profitMargins'] < 0.2:
            profitMargin = 1
        else:
            profitMargin = 2
        print('profit margin', info['profitMargins'])
    except:
        print('error with profit margin')
        profitMargin = -1

    #debt to Equity
    try:
        if info['debtToEquity'] > 200 or info['debtToEquity'] < 0:
            passCriteria -= 1
            debtToEquity = 0
        elif info['debtToEquity']  > 100 or info['debtToEquity'] < 0:
            debtToEquity = 1
        else:
            debtToEquity = 2
        print('debt to equity', info['debtToEquity'])
    except:
        print('error with debt to equity')
        debtToEquity = -1

    #return on Equity
    try:
        if info['returnOnEquity'] < 0.12:
            passCriteria -= 1
            returnOnEquity = 0
        elif info['returnOnEquity']  <0.20:
            returnOnEquity = 1
        else:
            returnOnEquity = 2
        print('return on equity', info['returnOnEquity'])
    except:
        print('error with return on equity')
        returnOnEquity = -1



    #CALCULATES FINAL SCORE
    score = max(forwardPE, 0) + max(currentRatio, 0) + max(profitMargin, 0) + max(debtToEquity, 0) + max(returnOnEquity, 0)
    if passCriteria <= 0:
        print('failed criteria')
        score = -1


    return [info['beta'], score, forwardPE, currentRatio, profitMargin, debtToEquity, returnOnEquity, info['longBusinessSummary']]

def calcScoreGrowth(ticker):
    return -1
    """print('Calculating growth score...')
    score = 0
    passCriteria = 1
    # GETS TICKER
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        assert (len(info) > 10)
    except:
        print('error with retrieving ticker')
        return -1

    # CALCULATES SCORES FOR EACH METRIC

    #PEG ratio
    try:
        pegRatio = 100 / info['pegRatio']
        if info['pegRatio'] > 4: passCriteria -= 2
        print('pegRatio', info['pegRatio'])
    except:
        print('error with pegRatio')
        pegRatio = 0

    #estimated growth
    try:
        CalcGrowth = float(GrowthEstimateScraper.getLTGrowthRate(ticker))
        if CalcGrowth < 15: passCriteria -= 2
        forcastedGrowth = 40*min(1+CalcGrowth/100, 1.7)**5
        print('forcastedGrowth', CalcGrowth)
        #print('forwardEPS', info["forwardEPS"])
        #print('trailingEPS', info["trailingEPS"])
    except:
        print('error with forcastedGrowth')
        forcastedGrowth = 0

    #return on Equity
    try:
        returnOnEquity = 200*min(info['returnOnEquity'], 0.7)
        if info['returnOnEquity'] < 0.1:
            passCriteria -= 1
            returnOnEquity = -20
        print('returnOnEquity', info['returnOnEquity'])
    except:
        print('error with returnOnEquity')
        returnOnEquity = 0

    #currentRatio
    try:
        currentRatio = 5*info['currentRatio']
        if info['currentRatio'] < 0.7:
            passCriteria -= 1
            currentRatio = -75
        elif info['currentRatio'] < 1: currentRatio = -35
        print('current ratio', info['currentRatio'])
    except:
        print('error with current ratio')
        currentRatio = 0

    #gross margins
    try:
        grossMargin = 15*abs(info['grossMargins'])**0.5
        if info['grossMargins'] < 0.2: passCriteria -= 1
        print('gross margin', info['grossMargins'])
    except:
        print('error with gross margin')
        grossMargin = 0

    #debt to Equity
    try:
        debtToEquity = (200-info['debtToEquity'])/8
        if info['debtToEquity'] > 200 or info['debtToEquity'] < 0: passCriteria -= 1
        print('debt to equity', info['debtToEquity'])
    except:
        print('error with debt to equity')
        debtToEquity = 0

    #insider ownership
    try:
        insiderOwnership = 25*abs(info['heldPercentInsiders'])**0.5
        print('insider ownership', info['heldPercentInsiders'])
    except:
        print('error with insider ownership')
        insiderOwnership = 0

    if passCriteria < 0:
        print('failed criteria')
        return -1


    score = pegRatio + forcastedGrowth + returnOnEquity + currentRatio + grossMargin + debtToEquity + insiderOwnership
    return score"""

def calcTechnicalScore(ticker):

    return -1
    """score = 0
    # GETS TICKER
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        assert (len(info) > 10)
    except:
        print('error with retrieving ticker')
        return -1

    try:
        twoHundredDayAverage = info["twoHundredDayAverage"]
        fiftyDayAverage = info["fiftyDayAverage"]
        print("two hundred day average: ", twoHundredDayAverage)
        print("fifty day average: ", fiftyDayAverage)
        momentum = 100 if twoHundredDayAverage < fiftyDayAverage else 0
    except:
        print('error with momentum')
        momentum = 0
        returnOnEquity = 0

    try:
        sentiment = SentimentAnalysis.getSentiment(ticker)
        print("sentiment -", sentiment)
        sentimentScore = sentiment*500
    except:
        print('error getting company sentiment')
        sentiment = 0
        sentimentScore = 0

    score = momentum + sentimentScore
    return score"""


if __name__ == "__main__":

    PATH = f"C:\\AaravWorld\\WhartonInvestmentCompetition2022\\StockScores\\"#"C:\\Users\\Aarav\\KWHSStockScores\\"#path csv file of stock scores should be exported to

    stockScores = {}

    #calculates all stock scores
    sectorIndex = 0
    stockScoresAll = {}
    for sector in allStocks:
        sectorName = sectorIndices[sectorIndex]
        stockScores[sectorIndices[sectorIndex]] = {}

        print('\n\n\n' + sectorIndices[sectorIndex].upper())
        for stock in sector:
            try:
                print(2 * '\n', '***' + stock + '***', '\n----------')
                stockScoreValue = calcScoreValue(stock)
                print()
                stockScoreGrowth = calcScoreGrowth(stock)
                print()
                stockScoreTechnical = calcTechnicalScore(stock)
                print(stock + ' scores: ', 'value-' + str(stockScoreValue[1]) + ', growth-' + str(stockScoreGrowth) + ', technical-' + str(stockScoreTechnical))
                stockScoresAll[stock] = [sectorName ,stockScoreValue[1], stockScoreGrowth, stockScoreTechnical]
                stockScores[sectorIndices[sectorIndex]][stock] = stockScoreValue
            except Exception as e:
                print('there was an ERROR', e)
                stockScoresAll[stock] = [-1, -1, -1, -1]
                stockScores[sectorIndices[sectorIndex]][stock] = [-1, -1, -1, -1, -1, -1, -1, -1]
        sectorIndex += 1

    print('stockScores', stockScores)
    stockScoresAllDf = pd.DataFrame.from_dict(stockScoresAll, orient ='index', columns = ["sector", "value", "growth", "technical"])#pd.DataFrame(stockScoresAll, columns = ["value", "growth", "technical"])
    stockScoresAllDf.to_csv(PATH + "//stockScoresAll.csv")

    #filters out the top 20% of stocks per sector
    sectorIndex = 0
    for sector in stockScores.values():

        sectorName = sectorIndices[sectorIndex]
        print('\n' + sectorName)
        sectorIndex += 1

        topValue = {}
        topGrowth = {}
        valueMinScore = 0
        valueItems = max(int(len(sector)/3), 7)

        """for s, scores in sector.items():
            try:
                if scores[0] > valueMinScore:
                    topValue[s] = scores[0]
                    if len(topValue) >= valueItems:
                        minKey = min(topValue, key=topValue.get)
                        del topValue[minKey]

                if scores[1] > growthMinScore:
                    topGrowth[s] = scores[1]
                    if len(topGrowth) >= growthItems:
                        minKey = min(topGrowth, key=topGrowth.get)
                        del topGrowth[minKey]
            except:
                pass"""
        #    return [info['beta'], score, forwardPE, currentRatio, profitMargin, debtToEquity, returnOnEquity, info['longBusinessSummary']]
        dfValue = pd.DataFrame.from_dict(sector, orient ='index', columns = ["beta", "score", "forwardPE", "currentRatio", "profitMargin", "debtToEquity", "returnOnEquity", "longBusinessSummary"])
        dfValue = dfValue.sort_values(by=['score'], ascending=False)
        print(dfValue)

        #adds as a file
        tempPATH = PATH + '\\' + sectorName
        try:
            os.makedirs(tempPATH)
        except:
            pass

        dfValue.to_csv(tempPATH + "\\KWHSStockScoresValue.csv")
