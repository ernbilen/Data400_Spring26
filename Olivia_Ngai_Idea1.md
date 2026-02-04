# Idea #1
#### _Renewable energy pathways strengthening energy price stability during fuel shock periods_
Olivia Ngai
#### **Research Question:** 
Do states with more wind and solar sources show better electricity price stability for consumers during fuel supply shock periods such as during the pandemic, geopolitical conflicts and recessions?

#### **Why:** 
Current analysis of electricity data on a state by state basis reveals that there is no statistically significant relationship between increased renewable energy sources changing consumer electricity prices. While the Biden administration argued energy prices would go down with the growth of the renewable energy sector, the Trump administration has been touting the exact opposite. As it currently stands, the numbers do not support either claims. Changes in electricity costs align more with other dynamic factors such as global pandemics and lockdowns, disturbances in supply chains, recession periods and inflation. 

I hypothesize that states with a larger proportions of renewable energy infrastructure such as wind and solar will have less intense fluctuations in electricity pricing due to a lower dependence on fossil fuels whose prices are coupled with the global market. Energy independence is a pressing issue, especially during times of global conflict where supply chains are disturbed and diplomatic relations are tense. 
#### **Who are the stakeholders?**
The stakeholder who might be interested in these findings include consumers who pay for electricity for their homes. Policy makers who could use this information to advocate for investments in the renewable energy sector. Industrial companies that require large amounts of electricity to continue their operations. The long term benefits of having stable electricity costs mean that during times of economic hardship, there would be one less financial burden for consumers and coorporations to stress over.

#### **Ethical, legal and societal concerns?** 
There are a lot of confounding variables at play with this research question, so while this study/analysis may provide some association or insight into the longterm benefits of incorporating renewable energy into the grid, it would not prove causation. This study would only be to prove the longterm benefits of energy independence but it does not advocate for reckless placement or over placement ("green sprawl") of renewables such as wind or solar. The climatic and environmental benefits of renewable energy are great, but they must be strategically placed in order to avoid unintended environmental or ecological impacts.

#### **Data Retrieval:**
U.S. Energy Information Administration (API request)
Electricity sales to Ultimate Customers monthly by state from January 2001 to November 2025
https://www.eia.gov/opendata/browser/electricity/retail-sales?frequency=monthly&data=price;&start=2001-01&end=2025-11&sortColumn=period;&sortDirection=desc;
U.S. Energy Information Administration Historical State Data (Excel)
Monthly Data from Electric Power Monthly
Net Generation by State by Type of Producer by Energy Source (2001 – Present)
https://www.eia.gov/electricity/data/state/

#### **Model Specifications**

State-level panel using OLS model:
Volatility~it~ = β~0~ + β~1~RenewShare~it~ + β~2~Shock~t~ + β~3~(RenewShare~it~×Shock~t~) + X~it~γ + α~i~ + δ~t~ + ε~it~

***i*** indexes U.S. states and ***t*** indexes months.

##### **Response Variable:**

**Electricity Price Volatility (Volatility~it~)**
- I will run the model on two different time frames: 12 month and 24 month. These windows will be defined by the rolling standard deviation of the log of retail electricity prices (cents per kWh) for each state. This measure captures within-state price changes over time, especially during fuel supply shock periods.
- The longer window will allow me to see pre-shock, shock, and recovery dynamics in a single measure. The shorter window will capture more spikes and nuanced dynamics in detail.
- In addition this measure captures price stability rather than price levels.
- Higher values will indicate greater month-to-month price fluctuations faced by consumers.

##### **Explanatory Variables:**

**Renewable Energy Share (RenewShare~it~)** 
The proportion of total in-state electricity generation coming from wind and solar sources:

RenewShare~it~= $$\frac{Wind~it~+Solar~it~}{Total Generation~it~}$$

**Fuel Supply Shock Indicator (Shock~t~)**
A binary indicator equal to 1 during periods characterized by major fuel supply disruptions, and 0 otherwise.

**Shock period of focus:** The COVID-19 pandemic (2020–2021)

**Interaction Term**
Renewable Share × Fuel Shock (RenewShare~it~×Shock~t~)

This interaction term measures whether states with higher renewable energy sources experience smaller increases in electricity price volatility during fuel shock periods.

A negative and statistically significant coefficient on this interaction indicates that renewable energy acts as a stabilizing force during periods of fuel market disruption.


**Control Variables (X~it~)**

The following variables include time-varying state-level controls to account for alternative drivers of electricity price volatility:

**Natural gas generation share**: captures the exposure to fuel prices closely linked to global markets.
**Coal generation share**: controls for legacy fossil fuel dependence.
**Electricity demand (log of total electricity sales)**: accounts for demand-driven price pressures.
**Inflation (CPI)**: controls for general price level changes affecting utility costs.

**Fixed Effects (α~i~ + δ~t~)**
The fixed effects control for unobserved factors that could bias the estimated relationship between renewable energy and electricity price volatility. The state fixed effect ensures each state has its own baseline level of price volatility and the time fixed effects accounts for shocks common to all states in a given month.


