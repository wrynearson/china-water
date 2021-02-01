#  Methodology
## Data Sources
The main analysis of this thesis center around two datasets, described below.

### Chinese General Social Survey (CGSS)

This national survey, originally launched in 2003, aims to monitor and document relationships between quality of life (in both individual and collective scope) and social structures, both in urban and rural environments. [@HomeZhongGuoZongHeSheHuiDiaoCha] One of the main benefits is its longitudinal design, however this feature is not utilized in this thesis, which will be discussed later. The survey has been conducted nearly annually since 2003, with a major redesign conducted in 2010. Thus, surveys conducted prior to 2010 are referred to as "Cycle II" while surveys conducted in 2010 or later are referred to as "Cycle II."

The CGSS is conducted by face-to-face interviews, which on average require 90 minutes to complete. [@ImplementationZhongGuoZongHeSheHuiDiaoCha] The survey consists of a questionnaire, which is composed of three modules (beginning in Cycle II):

| *Module*              | Frequency                | Dimensions | Variables | Coverage         | Comments                                                     |
|-----------------------|--------------------------|------------|-----------|------------------|--------------------------------------------------------------|
| Core                  | Annual                   | 11         | 152       | All participants |                                                              |
| ^Background Variables | Annual                   |            | 71        | All participants |                                                              |
| ^Social Change Trends | Annual                   |            | 81        | All participants |                                                              |
| Topic                 | Annual (5 year rotation) |            |           | All participants | *Either one or two topic modules per year.*                  |
| Additional            |                          |            |           | 1/3 - 1/2        | *Coverage depends on quantity of other questions and demand* | 
[@QuestionnairesZhongGuoZongHeSheHuiDiaoCha]

The Environmental Module ("环境(ISSP)" or "L部分") is of particular interest in this analysis. [@DiaoChaWenJuanZhongGuoZongHeSheHuiDiaoCha] It asks 25 questions and subquestions, most of which are directly or indirectly related to the environment. There are several interesting questions which ask things related to environmental protection, importance, perception and knowledge.

**Talk about specific questions, etc.**

The published data is in the form of a Stata file, which consists of 11783 rows (respondents) and 871 columns (variables). 

### Blue City Water Quality Index Ranking (WQIR)
The second dataset was compiled by the author from a report from the Institute of Public & Environmental Affairs, a non-profit environmental research organization based in Beijing. [@IPE] The report, the *Blue City Water Quality Index 2019*, compiles various surface, drinking. and ground water quality data published by various government agencies and assignes a score (their proprietary *Blue City Water Quatlity Index Score (BCWQI)*) and publishes the results at a sub-provincial level (second administrative level, or "admin 2"). [@jun2018BlueCity] The methodology and conversion to the government's [[water quality score]] is provided. This report was chosen as the basis for this dataset since it was the most comprehensive data the author could find with the closest publication date to the CGSS. The difference in time of the two datasets is discussed in the #limitations section. In the appendix of this report, the BCWQI for each second administrative level, including the city name, province, and ranking, is included. This data, in a table in the PDF report, was exported into a comma separated value (.csv) file for later analysis.

## Analysis
Analysis for this thesis was conducted using the general-purpose computer programming language Python. To allow for accessibility, readability, and reproducibility, the primary data analysis medium was a Jupyter notebook [@kluyverJupyterNotebooksPublishing], a document format which allows for text and code to be read and execute in an easy-to-read format, which was hosted on Github, to allow for accessability. [@WrynearsonChinawater] This was chosen after initial data analysis was conducted in a more traditional Python file, which was less collaborative and more cumbersome.

## Interviews

## Limitations
