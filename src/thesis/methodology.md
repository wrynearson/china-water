#  Methodology
## Data Sources
The main analysis of this thesis center around two datasets, described below.

### Chinese General Social Survey (CGSS)

This national survey, originally launched in 2003, aims to monitor and document relationships between quality of life (in both individual and collective scope) and social structures, both in urban and rural environments. [@HomeZhongGuoZongHeSheHuiDiaoCha] One of the main benefits is its longitudinal design, however this feature is not utilized in this thesis, which will be discussed later. The survey has been conducted nearly annually since 2003, with a major redesign conducted in 2010. Thus, surveys conducted prior to 2010 are referred to as "Cycle II" while surveys conducted in 2010 or later are referred to as "Cycle II."

The CGSS is conducted by face-to-face interviews, which on average require 90 minutes to complete. [@ImplementationZhongGuoZongHeSheHuiDiaoCha] The survey consists of a questionnaire, which is composed of three modules (beginning in Cycle II):

```{table} CGSS2010 Components and Description 
:name: cgss2010-components

| *Module*              | Frequency                | Dimensions | Variables | Coverage         | Comments                                                     |
|-----------------------|--------------------------|------------|-----------|------------------|--------------------------------------------------------------|
| Core                  | Annual                   | 11         | 152       | All participants |                                                              |
| ^Background Variables | Annual                   |            | 71        | All participants |                                                              |
| ^Social Change Trends | Annual                   |            | 81        | All participants |                                                              |
| Topic                 | Annual (5 year rotation) |            |           | All participants | *Either one or two topic modules per year.*                  |
| Additional            |                          |            |           | 1/3 - 1/2        | *Coverage depends on quantity of other questions and demand* | 
```
[@QuestionnairesZhongGuoZongHeSheHuiDiaoCha]

The Environmental Module ("环境(ISSP)" or "L部分") is of particular interest in this analysis. [@DiaoChaWenJuanZhongGuoZongHeSheHuiDiaoCha] It asks 25 questions and subquestions, most of which are directly or indirectly related to the environment. There are several interesting questions which ask things related to environmental protection, importance, perception and knowledge.

**Talk about specific questions, etc.**

The published data is in the form of a Stata file, which consists of 11783 rows (respondents) and 871 columns (variables). 

### Blue City Water Quality Index Ranking (WQIR)
The second dataset was compiled by the author from a report from the Institute of Public & Environmental Affairs, a non-profit environmental research organization based in Beijing. [@IPE] The report, the *Blue City Water Quality Index 2019*, compiles various surface, drinking. and ground water quality data published by various government agencies and assignes a score (their proprietary *Blue City Water Quatlity Index Score (BCWQI)*) and publishes the results at a sub-provincial level (second administrative level, or "admin 2"). [@jun2018BlueCity] The methodology and conversion to the government's [[water quality score]] is provided. This report was chosen as the basis for this dataset since it was the most comprehensive data the author could find with the closest publication date to the CGSS. The difference in time of the two datasets is discussed in the #limitations section. In the appendix of this report, the BCWQI for each second administrative level, including the city name, province, and ranking, is included. This data, in a table in the PDF report, was exported into a comma separated value (.csv) file for later analysis.

## Analysis
Analysis for this thesis was conducted using the general-purpose computer programming language Python. To allow for accessibility, readability, and reproducibility, the primary data analysis medium was a Jupyter notebook [@kluyverJupyterNotebooksPublishing], a document format which allows for text and code to be read and execute in an easy-to-read format, which was hosted on Github, to allow for accessability. [@rynearsonWrynearsonChinawater2020] This was chosen after initial data analysis was conducted in a more traditional Python file, which was less collaborative and more cumbersome.

The two main datasets were loaded into the Jupyter notebook and reviewed for initial analysis, beginning with the CGSS2010. Then, after reviewing the data, it was cleaned and processed in several ways:

### Chosing Approprate Questions
#### Demographic Questions
The thesis proposal and hypothesis were created before the author reviewed the dataset, and before the author was aware of the environmental module of the CGSS. While many variables were deemed interesting, several variables were initially selected for broader analysis: [^1]

```{table} Relevant CGSS2010 Demographic Components 
:name: cgss2010-demographic

| Code | Variable (English)             | Variable (Chinese) | Importance                        | Utilized? |
|------|--------------------------------|--------------------|-----------------------------------|-----------|
| s41  | Province                       |                    | Location of the individual        | X         |
| a2   | Gender                         |                    |                                   | X         |
| a3a  | Birth year                     |                    | Age of respondant                 | X         |
| a7a  | Highest level of education     |                    | Link to perception and knowledge? | X         |
| a8a  | Personal total income          |                    |                                   | X         |
| a15  | Subjective personal health     |                    |                                   |           |
| a62  | Family total income            |                    |                                   |           |
| a91  | Rural / agricultural household |                    |                                   | X         |
```
As evident, not all of the variables were utilized, for several reasons.

#### Environmental Questions
The CGSS includes many demographic data on each respondant. Of which, the following were deemed important for one or more reasons: [^1]

```{table} Relevant CGSS2010 Environmental Components 
:name: cgss2010-env

| Code     | Question (English)                                                                                                               | Question (Chinese) | Response Types | Importance | Utilized? |
|----------|----------------------------------------------------------------------------------------------------------------------------------|--------------------|----------------|------------|-----------|
| l1a      | In your opinion, in terms of the current situation in our country, which of the following issues is the most important?          |                    |                |            |           |
| l1b      | *like l1a, but 2nd most important*                                                                                               |                    |                |            |           |
| l6a      | In your opinion, in terms of the current situation in our country, which of the following issues is the most important?          |                    |                |            |           |
| l6b      | How serious are env. problems facing China?                                                                                      |                    |                |            |           |
| l7a      | Which is most important env. issue in China?                                                                                     |                    |                |            |           |
| l7b      | Which has greatest impact on you/family?                                                                                         |                    |                |            |           |
| l8a      | Knowledge of causes of environmental problems from ?l7                                                                           |                    |                |            |           |
| l8b      | Knowledge of solutions of environmental problems from ?l7                                                                        |                    |                |            |           |
| l12a     | In order to protect the environment, to what extent are you willing to pay a higher price?                                       |                    |                |            |           |
| l12b     | *like l12a, but with higher taxes"                                                                                               |                    |                |            |           |
| l12c     | *like l12a/b, but with willingness to lower living standards*                                                                    |                    |                |            |           |
| l137     | Environmental issues directly affect my daily life                                                                               |                    |                |            |           |
| l14d     | How do you think the pollution of rivers, rivers and lakes in China is harmful to the environment?                               |                    |                |            |           |
| l15a / b | *see question, about statements of responsibility for environmental protection (individuals/companies, government, etc.)*        |                    |                |            |           |
| l16c     | In terms of solving environmental problems in your area, how do you think the local government has done in the past five years?" |                    |                |            |           |
| l20e     | Do you often save water or reuse water specifically for environmental protection?                                                |                    |                |            |           |
| l2409    | In the domestic water pollution report, the water quality of Category V (5) is better than that of Category I (1)                |                    |                |            |           |
```

As evident, these questions include questions related to the environment in general, perceptions of the local, national and global environment, water, and knowledge of water quality issues.

#### Other Survey Questions
Many more survey questions were included in the main and additional module sections. Many of these relate to social satisfaction, political involvement, and future aspirations. Future analysis could be done with many of these questions, but were not within the scope of this analysis.

### Geographic Alignment
The two datasets are of differing geographic precision. The CGSS2010 (and all CGSSII data sets) include data on the province of where the respondent resided. Based on the structure of the data, it is assumed that more precise geographic information is included, however the CGSS publishing team choses only to release the provincial information.

This is different than the WQIR2018 data, which is published at the sub-provincial level (admin 2). Thus, for comparative analysis, the mean water quality per province was calculated (more on this below).

### Procedure
Once the data sets were loaded and reviewed for importance and quality, initial data analysis was conducted. Due to the author's limited experience with Python, multiple versions of the analysis were conducted in order to gain working knowledge of Python and of the data set.

For provincial comparative analysis, the data was sorted by province `s41` and grouped into visual and numerical approaches of looking for differences between provinces. Several functions were created which allowed the author, and users, to see provincial comparative analyses on any question by inputing the question code. Either quantities of resonses or their mean value would be output, as well as a heatmap for quick comparison. This initial analysis helped the author validate the main variables that were analyzed, which are discussed later.

Then, the WQIR2018 data was loaded. An initial plot was created to see the distribution of water quality per sub-province, sorted by province. Histograms were added to visualize the distribution of water quality measurements and values.

```{figure} ../wqir2018.svg

:name: wqir2018-vis
WQIR2018 distribution per province.
```

From the previous steps, a subset of questions were created. The subset `cgss_strict`, which include only variables s41, l14d and l2409 were used for further initial analysis for simplicity.

Within these subsets, some values were revealed to be outside of the acceptable range (negative numbers). Since the origin or reason behind these values could not be determined, they were discarded. This lead to further discrepencies in the number of values depending on the province.

## Interviews

## Limitations

—

[^1]: Translated from Chinese into English.