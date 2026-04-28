# 📊 Week 1 Report – Coffee Price Analysis (Thinh)

---

## 1. Objective

- Identify factors affecting coffee prices  
- Determine the most important price for prediction  

---

## 2. Factors Affecting Coffee Prices

Coffee prices are influenced by multiple factors, which can be grouped as follows:

### 2.1 Economic Factors
- Robusta futures price (London market)  
- Arabica futures price (New York market)  
- Exchange rate (USD/VND)  

👉 Global price movements directly impact domestic coffee prices.

---

### 2.2 Agricultural Factors
- Production volume  
- Cultivation area  
- Yield  

👉 Higher supply leads to lower prices and vice versa.

---

### 2.3 Climate Factors
- Rainfall  
- Temperature  
- ENSO index (El Niño / La Niña)  

👉 Extreme weather conditions can reduce yield and increase prices.

---

### 2.4 Cost & Competition Factors
- Fertilizer prices  
- Labor costs  
- Fuel prices  
- Competing crops (pepper, rubber, etc.)  

👉 Higher production costs can push prices upward.

---

### 2.5 Policy Factors
- Export tax  
- Trade agreements (EVFTA, CPTPP)  
- Environmental regulations (EUDR)  

👉 Policy changes can affect both supply and export conditions.

---

## 3. Target Price Selection

👉 **Selected target: Farm-gate price (VND/kg)**  

### Reason:
- Directly reflects farmers' income  
- Represents real market conditions  
- Suitable as the prediction target (label)  

👉 Other prices (futures, exchange rate, etc.) will be used as input features.

---

## 4. Data Orientation (Supporting Dataset Design)

To support model development, the dataset should include:

- Farm-gate price (target variable)  
- Global coffee futures prices  
- Exchange rate (USD/VND)  
- Weather data (rainfall, temperature, ENSO)  
- Production and agricultural data  

👉 The dataset will use **farm-gate price as the target variable** and the remaining variables as input features for machine learning models.

👉 Specific data sources and data collection methods will be handled by the data collection team.

---

## 5. Conclusion

Coffee prices are mainly influenced by:
- Supply  
- Demand  
- Weather conditions  

👉 Farm-gate price is the most appropriate target for prediction models.

---
