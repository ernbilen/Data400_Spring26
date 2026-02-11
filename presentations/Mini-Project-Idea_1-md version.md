<!DOCTYPE html><html><head><meta charset="utf-8"><title>Idea 1.md</title><style></style></head><body id="preview">
<h4 class="code-line" data-line-start=0 data-line-end=1 ><a id="Idea_1_Environmental_Regulation_Enforcement_and_Health_Disparities_in_Communities_0"></a>Idea 1: Environmental Regulation Enforcement and Health Disparities in Communities</h4>
<h5 class="code-line" data-line-start=2 data-line-end=3 ><a id="Research_Question_2"></a>Research Question:</h5>
<p class="has-line-data" data-line-start="3" data-line-end="4">How does environmental regulation enforcement differ across communities where pollution exposure is similar, and what are the implications of these enforcement differences for population health outcomes?</p>
<h5 class="code-line" data-line-start=5 data-line-end=6 ><a id="Abstract_5"></a>Abstract</h5>
<p class="has-line-data" data-line-start="6" data-line-end="7">For this project, I will aim to examine whether differences in environmental regulation enforcement are associated with differences in population health outcomes across communities that face comparable levels of industrial pollution. Focusing on communities in a specific state (for eg. Louisiana) with similar numbers of industrial facilities and similar toxic emissions, the analysis shifts attention away from pollution levels themselves and toward variation in regulatory enforcement, including inspections, violations, penalties, and enforcement delays. Using publicly available administrative and health data, the project constructs a parish-year dataset combining pollution exposure, enforcement activity, and health indicators. Through exploratory data analysis, the project assesses whether communities receiving less regulatory attention experience worse health outcomes despite facing similar environmental risks. The goal is not causal estimation, but to document systematic patterns consistent with a political economy perspective in which the governance of environmental risk, rather than exposure alone, shapes health disparities.</p>
<h5 class="code-line" data-line-start=8 data-line-end=9 ><a id="Data_Sources_8"></a>Data Sources</h5>
<ul>
<li class="has-line-data" data-line-start="9" data-line-end="12">EPA Toxic Release Inventory (TRI)<br>
Provides facility-level data on toxic emissions, facility locations, and reporting years.<br>
<a href="https://www.epa.gov/toxics-release-inventory-tri-program">https://www.epa.gov/toxics-release-inventory-tri-program</a></li>
<li class="has-line-data" data-line-start="12" data-line-end="15">EPA Enforcement and Compliance History Online (ECHO)<br>
Contains records of environmental inspections, violations, enforcement actions, penalties, and dates of regulatory activity.<br>
<a href="https://echo.epa.gov">https://echo.epa.gov</a></li>
<li class="has-line-data" data-line-start="15" data-line-end="19">CDC PLACES<br>
Provides small-area estimates of health outcomes such as asthma prevalence, cardiovascular disease, and other chronic conditions at the parish level.<br>
<a href="https://www.cdc.gov/places">https://www.cdc.gov/places</a></li>
</ul>
<h5 class="code-line" data-line-start=19 data-line-end=20 ><a id="Strategy_19"></a>Strategy</h5>
<ol>
<li class="has-line-data" data-line-start="20" data-line-end="24">
<p class="has-line-data" data-line-start="20" data-line-end="23">Community Selection<br>
-Identify two communites with similar numbers of industrial facilities, similar total TRI-reported toxic emissions.<br>
-Example candidates include St. James Parish and Ascension Parish in Louisiana, subject to confirmation through TRI summary statistics.</p>
</li>
<li class="has-line-data" data-line-start="24" data-line-end="27">
<p class="has-line-data" data-line-start="24" data-line-end="26">Pollution Measurement<br>
Aggregate TRI facility-level emissions to the parish-year level and use these measures to confirm that pollution exposure is comparable between selected parishes.</p>
</li>
<li class="has-line-data" data-line-start="27" data-line-end="34">
<p class="has-line-data" data-line-start="27" data-line-end="33">Enforcement Measurement<br>
Aggregate ECHO data to the parish-year level. Construct enforcement indicators including:<br>
-Inspections per facility<br>
-Violations per facility<br>
-Total penalties per facility<br>
-Average time between violation and enforcement action</p>
</li>
<li class="has-line-data" data-line-start="34" data-line-end="37">
<p class="has-line-data" data-line-start="34" data-line-end="36">Health Outcomes<br>
Merge parish-year enforcement and pollution data with CDC PLACES health indicators. Focus on outcomes plausibly linked to environmental exposure (e.g., asthma, cardiovascular disease prevalence).</p>
</li>
<li class="has-line-data" data-line-start="37" data-line-end="41">
<p class="has-line-data" data-line-start="37" data-line-end="40">Exploratory Data Analysis (EDA)<br>
Compare distributions of enforcement metrics across parishes with similar pollution levels.<br>
Visualize time trends in enforcement activity and health outcomes.</p>
</li>
</ol>
<h5 class="code-line" data-line-start=41 data-line-end=42 ><a id="Ethical_Implications_41"></a>Ethical Implications</h5>
<p class="has-line-data" data-line-start="42" data-line-end="43">This project raises ethical concerns related to environmental justice and state accountability. By focusing on enforcement rather than exposure alone, the analysis highlights how unequal regulatory attention may contribute to health disparities even when environmental risks are similar. The use of aggregated parish-level data limits the ability to capture individual exposure and may obscure within-community heterogeneity, raising the risk of ecological fallacy. Results must therefore be interpreted as patterns at the community level, not individual causal effects. Nonetheless, documenting systematic enforcement disparities has ethical significance, as it informs debates about how public institutions distribute protection from environmental harm and whose health is prioritized under existing regulatory regimes.</p>

</body></html>