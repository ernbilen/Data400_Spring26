## Research Idea 1 : The World Through the Eyes of U.S. Media. What country got mentioned the most during each era from 1900 to 2025

## Abstract
Media coverage plays a central role in shaping public awareness and collective consciousness about global events. In the United States, newspaper headlines particularly front-page stories have long served as a focal point for daily conversations about international affairs. This project examines how global attention has shifted over time by analyzing front-page headlines published by The New York Times between 1900 and 2025.

Using the New York Times digital archive, this study identifies which countries most frequently appeared in prominent news coverage during different historical periods. By tracking the rise and decline of country mentions across more than a century, this research aims to reveal how wars, political conflicts, economic power shifts, and global crises influence which parts of the world occupy U.S. media attention at any given time.
## Hypothetical Scenarios / Expectations
Based on historical context, certain periods are expected to show concentrated coverage of specific regions or countries. For example:
- 1967–1975: Heavy emphasis on Vietnam due to the Vietnam War, alongside coverage of the Yom Kippur War and broader Cold War dynamics.
- 1940–1945: Predominant focus on European and Axis powers during World War II.
- 2001–2011: Increased coverage of Afghanistan and Iraq following the September 11 attacks and subsequent wars.
These patterns are expected to demonstrate how geopolitical events shape media focus over time.
## Data Sources
1. The New York Times Article Archive API
Source: https://developer.nytimes.com/
2. Metadata fields used include headline text, publication date, article type, section, and page placement.
3. Considering other article API such as The Economist,... 
## Methodology / Strategy
This project uses web scraping and API-based data collection to retrieve articles published between 1900 and 2025. The dataset is filtered to include only:
- Articles classified as “news” or “article”
- Stories that appeared on the front page or section front
- Country mentions are identified through keyword matching that includes: official country names, common acronyms, major cities
## Methods
NLP Approach 
- I use named entity recognition to extract place names from front-page headlines, normalize those entities to countries, and aggregate their frequencies by historical era to analyze shifts in U.S. media attention.

Frequency Analysis
- Count how many times each country appears in front-page headlines
- Aggregate counts by era (e.g., decades or historical periods)
- Rank countries by frequency within each era
Time Series Trend Analysis
To show change over time:
- Track country mentions year-by-year or decade-by-decade
Identify:
- Peaks (wars, crises)
- Declines (post-conflict periods)
- Compare long-term trends across countries
## Ethical Considerations
- To understand how U.S. media attention toward different countries has changed over time
- To examine how major global events (wars, political conflicts, economic crises) influence which countries dominate U.S. news coverage
- To analyze front-page headlines as a reflection of collective awareness and national priorities in the United States
- To treat media coverage as a lens shaping public perception, rather than an objective measure of global importance
## Who benefits from the research
1. Media scholars and journalists
- Gain insight into long-term patterns of media attention and editorial priorities
- Better understand how news institutions shape public awareness of global events

2. Historians and political scientists
- Use the findings to contextualize U.S. perspectives on international relations across different historical periods
- Identify how wars, diplomacy, and power shifts influence media focus
3. Policy analysts and international relations researchers
- Understand which countries have historically dominated U.S. media attention and how that visibility aligns with foreign policy priorities