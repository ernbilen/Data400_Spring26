

#### Research Question: *What is the relationship between historical hazardous toxic exposure/waste and growth of urban green space in the NYC metropolitan area? Has the presence of toxic waste led to an increase in environmental remediation efforts through urban green spaces?*


##### TRI Toxins data
CSV file
##### NYC department of parks and rec GIS
CSV file

#### Model Specifications:
##### Primary model: Panel Fixed Effects with Lagged Toxic Exposure
This model explores if neighborhoods with higher historical toxic exposure experience more or less greening later.

GreenSpacei~t~ = β~1~ToxicExposure~i,t−k~ + α~i~ + γ~t~ + ϵ~i,t~
i = neighborhood (census tract or grid cell)
t = year
ToxicExposure~i,t−k~ = lagged TRI exposure (e.g., 5-year lag)
α~i~ = neighborhood fixed effects
γ~t~= year fixed effects

##### Growth Model:
This model measures whether polluted neighborhoods experienced faster greening growth.
ΔGreenSpace~i,t~ = GreenSpace~i,t~ − GreenSpace~i,t−1~

#### Implications for stakeholders:

This project could involve local government and urban planning agencies, local communities and residents, environmental and public health organizations and environmental regulators.

- My findings would reveal whether green space development is growing in areas that actually need it such as polluted areas as a remediation effort, or whether it is disproportionately benefiting clean neighborhoods and enhancing environmental inequalities.
- If there is a positive relationship between polluted neighborhoods and growth of green spaces then it shows that remediation efforts are occurring and that urban planning agencies/policy are moving in the right direction
- If there is a negative relationship then it reveals that systemic inequalities are being exacerbated and that there is a lack of investment targeting high toxic exposure communities and neighborhoods. This would provide evidence to policy makers that they should increase funding in environmentally degraded areas and lower the inequality gap regarding green spaces.

#### Ethical, Legal, and Societal Implications

This was touched on in the earlier section for stakeholders, but this project would highlight environmental justice and historical environmental inequalities. There is ample research that exists on highly polluting factories and industries situating themselves in low income predominantly black neighborhoods. This legacy continues into today and it has serious health implications for the residents in the area. 

Asthma rates go up due to air pollution, water becomes contaminated due to hazardous waste material leaching into ground water, and contamination due to contact with the toxic chemicals. Depending on the chemicals and exposure rates, this has led to the decline in health of the surrounding communities and has highlighted environmental racism and systemic problems that need to be addressed. 

While this project will not necessarily target those responsible for these wrongdoings, it will draw attention to whether there has been measurable improvement in these neighborhoods due to an increase in green spaces. 







