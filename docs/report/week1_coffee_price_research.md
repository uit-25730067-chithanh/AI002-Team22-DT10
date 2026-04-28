# 📊 Week 1 Report – Coffee Price Forecasting (Thinh)

## 1. Executive Summary
Vietnam is one of the largest coffee producers globally. Coffee prices are influenced by global futures markets, weather conditions, production levels, and macroeconomic factors.

The current farm-gate price is approximately **98,000 – 99,500 VND/kg (~4.2 USD/kg)**.

👉 This report identifies key variables affecting coffee prices and defines the main prediction target.

---

## 2. Objective

- Identify factors affecting coffee prices  
- Determine the most important price for prediction  

---

## 3. Factors Affecting Coffee Prices

### 3.1 Economic Factors
- Robusta futures (London): https://www.investing.com/commodities/london-coffee  
- Arabica futures (New York): https://finance.yahoo.com/quote/KC%3DF  
- Exchange rate (USD/VND): https://api.exchangeratesapi.io/latest?base=USD&symbols=VND  

👉 Global market movements directly impact domestic prices  

---

### 3.2 Agricultural Factors
- Production (USDA report): https://apps.fas.usda.gov  
- Area & yield (Vietnam statistics): https://www.gso.gov.vn  

👉 Higher supply → lower price  

---

### 3.3 Climate Factors
- Weather data (NOAA API): https://www.ncei.noaa.gov  
- ENSO index: https://www.noaa.gov  

👉 Extreme weather → lower yield → higher price  

---

### 3.4 Cost & Competition
- Fertilizer price: https://www.fao.org/faostat  
- Fuel price (Brent oil): https://www.investing.com/commodities/brent-oil  

---

### 3.5 Policy Factors
- Trade agreements (EVFTA, CPTPP)  
- Environmental regulations (EUDR)  

---

## 4. Target Price Selection

👉 **Selected target: Farm-gate price (VND/kg)**  

### Source:
- https://giathitruongcaphe.com/price  

### Reason:
- Directly affects farmers  
- Reflects real market value  
- Most practical for prediction  

👉 Other prices (futures, FOB) are used as input features  

---

## 5. Data Collection Plan

### Frequency
- Daily: price, exchange rate  
- Weekly: weather  
- Yearly: production  

### Sources
- Local price: https://giathitruongcaphe.com  
- Futures: Investing / Yahoo Finance  
- Weather: NOAA API  
- Production: USDA / GSO  

---

## 6. Dataset Structure

Minimum dataset:

- date  
- region  
- farm_gate_price  
- robusta_futures  
- arabica_futures  
- usd_vnd  
- rainfall  
- temperature  
- enso_index  
- production  

---

## 7. Modeling Direction

- Time-series models:
  - SARIMA  
  - LSTM  

### Techniques:
- Lag features  
- Seasonality (harvest season Oct–Dec)  

---

## 8. Evaluation Metrics

- MAE  
- RMSE  

---

## 9. Conclusion

Coffee prices are mainly influenced by:
- Supply  
- Demand  
- Weather  

👉 Farm-gate price is the most appropriate prediction target.  

---

## 10. Variables Dataset

🔗 [View Variables Sheet](https://docs.google.com/spreadsheets/d/1S4Mmu3_0EVyRm1AV_xjeK-iRWynAuaqHejPcjozjNuw/edit?usp=sharing)
