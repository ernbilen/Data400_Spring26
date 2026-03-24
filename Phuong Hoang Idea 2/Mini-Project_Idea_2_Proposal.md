# Mini-Project Idea Proposal: How ICE Enforcement Affects Labor Outcomes in the U.S.? 
## - Data from different sectors
By Phuong Hoang
> *“We lead the world because, unique among nations, we draw our people — our strength — from every country and every corner of the world. And by doing so we continuously renew and enrich our nation.”* — President Ronald Reagan

--

#### Project goal

- The goal of this project is to quantitatively assess whether variations in ICE immigration enforcement (specifically arrests and detentions) are associated with changes in employment outcomes across different economic sectors at the county level. The focus is on understanding whether more intense enforcement correlates with differential impacts on labor market participation in immigrant-intensive sectors (such as agriculture, construction, and hospitality) compared with sectors that are less reliant on immigrant labor, using regression models and DiD.


#### Tractable Data
- This project relies on two publicly available, well-documented, and widely used datasets. The first dataset is ICE enforcement data from the Deportation Data Project, which compiles arrest and detention records obtained through Freedom of Information Act requests. These data provide information on the timing and location of ICE enforcement actions and can be aggregated to the county/state and annual or quarterly level to construct measures of enforcement intensity. The ICE data are publicly accessible at [Deportation Data Project](https://deportationdata.org/data/ice.html).

- The second dataset is the Quarterly Census of Employment and Wages (QCEW) produced by the U.S. Bureau of Labor Statistics. The QCEW provides comprehensive employment and wage data by industry (NAICS codes) and county, allowing for consistent measurement of sector-specific labor outcomes over time. The QCEW downloadable data files are available at [QCEW data files](https://www.bls.gov/cew/downloadable-data-files.htm)

#### Data Retrieval
-  ICE enforcement data will be downloaded in CSV format directly from the Deportation Data Project website and aggregated to create county-level measures of arrests and detentions by year or quarter. Employment data will be retrieved from the BLS QCEW county-level files, focusing on high-level industry classifications. The two datasets will be merged using county identifiers and time periods to create a panel dataset with observations by county, sector, and time. Additional variables, such as arrest rates per capita and sector-specific employment growth rates, will be constructed to facilitate comparison across regions and industries.


#### Exploratory Data Analysis 
###### [attentive to change]
- Exploratory data analysis will be used to visualize patterns in both ICE enforcement and sectoral employment before any formal modeling. This will include time-series plots showing trends in enforcement intensity and employment levels across selected industries, as well as comparisons between counties with high and low levels of ICE activity. Geographic visualizations and sector-level summaries will help identify whether immigrant-intensive industries display different employment dynamics in areas experiencing sustained enforcement. These exploratory analyses will provide intuition about the data and help motivate the subsequent empirical approach.

#### Implications for stakeholders
- The findings from this project have potential implications for multiple stakeholders. For employers and industry groups, particularly in sectors reliant on immigrant labor, the analysis may highlight vulnerabilities in workforce stability associated with enforcement intensity. 
- For local governments and workforce development agencies, understanding sector-specific labor responses to enforcement could inform planning efforts, training programs, and resource allocation. For policymakers and economists, the results may offer empirical evidence on the broader economic consequences of immigration enforcement policies.

#### Ethical, legal, societal implications
- This project raises important ethical and societal considerations. All analyses will be conducted at an aggregated county and sector level to protect individual privacy and avoid identifying specific persons or cases. The ICE data originate from FOIA requests and are used in accordance with the documentation and guidance provided by the Deportation Data Project. From a societal perspective, immigration enforcement affects communities and families in complex ways, and the analysis will be framed carefully to avoid dehumanizing interpretations. The project will also acknowledge its limitations, including the fact that observed correlations may reflect broader local conditions rather than direct causal effects of enforcement alone.









