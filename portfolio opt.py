import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

stock_data={}
for i in stocks:
  ticker=yf.Ticker(i)
  stock_data[i]= ticker.history(start=start_date, end=end_date,)['Close']
stock_prices =pd.DataFrame(stock_data)

log_returns=np.log(stock_prices/stock_prices.shift(1))

print("Stock          Annulated Returns")
print(log_returns.mean()*NUM_TRADING_DAYS*100)

print("Stocks         Volatility(Risk)")
print(np.std(log_returns)*np.sqrt(NUM_TRADING_DAYS))

portfolio_return=[]
portfolio_risk=[]
portfolio_weight=[]

for _ in range(NUM_SIMULATIONS):
  w= np.random.random(len(stocks))
  w/=np.sum(w)
  portfolio_weight.append(w)
  p_return= np.sum(log_returns.mean()*w)*NUM_TRADING_DAYS
  portfolio_return.append(p_return)
  p_risk=np.sqrt(np.dot(w.T,np.dot(log_returns.cov()*NUM_TRADING_DAYS,w)))
  portfolio_risk.append(p_risk)

portfolio_weight=np.array(portfolio_weight)
portfolio_risk=np.array(portfolio_risk)
portfolio_return=np.array(portfolio_return)

portfolios =pd.DataFrame({"Returns":portfolio_return,"Risk":portfolio_risk, "Sharpe_Ratio":portfolio_return/portfolio_risk})

plt.figure(figsize=(10,6))
plt.scatter(portfolio_risk, portfolio_return, c=portfolio_return/portfolio_risk,marker='o')
plt.grid(True)
plt.xlabel('Expected_risk')
plt.ylabel('Expected_Return')
plt.colorbar(label="Sharpe Ratio")
plt.title("Expected Risk vs Expected Return")
plt.tight_layout()

ind=0
sharpe_ratio=portfolio_return/portfolio_risk
for i in range(len(sharpe_ratio)):
  if sharpe_ratio[i]==np.max(sharpe_ratio):
    ind=i

print("Stocks with their corresponding weights")
for i in range(len(stocks)):
  print(stocks[i],"----->",np.round(portfolio_weight[ind][i],5))

plt.figure(figsize=(10,6))
plt.scatter(portfolio_risk,portfolio_return,
            c=portfolio_return/portfolio_risk,marker='o')
plt.grid(True)
plt.xlabel('Expected_Risk')
plt.ylabel('Expected_Return')
plt.colorbar(label = "Sharpe Ratio")
plt.plot(portfolio_risk[ind],portfolio_return[ind],'r*',markersize=10.0)
plt.title("Expected Returns vs Expected_Risk")
plt.tight_layout()

ind1=0

for i in range(len(portfolio_risk)):
  if(portfolio_risk[i]==np.min(portfolio_risk)):
    ind1=i

plt.figure(figsize=(10,6))
plt.scatter(portfolio_risk,portfolio_return,
            c=portfolio_return/portfolio_risk,marker='o')
plt.grid(True)
plt.xlabel('Expected_Risk')
plt.ylabel('Expected_Return')
plt.colorbar(label = "Sharpe Ratio")
plt.plot(portfolio_risk[ind1],portfolio_return[ind1],'b*',markersize=10.0)
plt.title("Expected Returns vs Expected_Risk")
plt.tight_layout()