---
CJKmainfont: Noto Sans CJK HK, Light
---

#  Methodology

## Data Sources
The main analysis of this thesis center around two data sets, described below.

### Chinese General Social Survey (CGSS)

This national survey, originally launched in 2003, aims to monitor and document relationships between quality of life (in both individual and collective scope) and social structures, both in urban and rural environments. [@HomeZhongGuoZongHeSheHuiDiaoCha] One of the main benefits is its longitudinal design – however this feature is not utilized in this thesis, which will be discussed later. The survey has been conducted nearly annually since 2003, with a major redesign conducted in 2010. Thus, surveys conducted prior to 2010 are referred to as "Cycle II" while surveys conducted in 2010 or later are referred to as "Cycle II."

The CGSS is conducted by face-to-face interviews, which on average require 90 minutes to complete. [@ImplementationZhongGuoZongHeSheHuiDiaoCha] The survey consists of a questionnaire, which is composed of three modules (beginning in Cycle II):

```{table} CGSS2010 Components and Description 
:name: cgss2010-components
<!-- ~ put table here -->
```

| *Module*               | Frequency                | Dimensions | Variables | Coverage         | Comments                                                     |
|------------------------|--------------------------|------------|-----------|------------------|--------------------------------------------------------------|
| Core                   | Annual                   | 11         | 152       | All participants | -                                                            |
| *Background Variables* | Annual                   | -          | 71        | All participants | -                                                            |
| *Social Change Trends* | Annual                   | -          | 81        | All participants | -                                                            |
| Topic                  | Annual (5 year rotation) | -          | -         | All participants | *Either one or two topic modules per year.*                  |
| Additional             | -                        | -          | -         | 1/3 - 1/2        | *Coverage depends on quantity of other questions and demand* |

[@QuestionnairesZhongGuoZongHeSheHuiDiaoCha]

The published data is in the form of a Stata file, which consists of 11783 rows (respondents) and 871 columns (variables).

The Environmental Module ("环境(ISSP)" or "L部分"[^2]) is of particular interest in this analysis. [@DiaoChaWenJuanZhongGuoZongHeSheHuiDiaoCha] It asks 25 questions and sub-questions, most of which are directly or indirectly related to the environment. There are several interesting questions which ask things related to environmental protection, importance, perception and knowledge:

The primary question regarding water quality perception was question `l14d` ask about the severity of harm to the environment caused by pollution of rivers and lakes.[^2]. Survey participants can respond with a range from one to five, with one being "extremely harmful to the environment," to five being "there is no harm at all." [^3] This question is significant because it quantifies the respondents' perception of the severity of water quality on the environment. However, this question does not directly regard the perception of drinking water quality, or the importance of drinking water quality for health or other factors.

The primary question regarding water quality knowledge was question `l2409` tests respondents' knowledge of the water quality scale used by China. The question requires respondents to state if a statement about water quality is correct, incorrect, or if they don't know. [^4] This question is important since it tests respondents' knowledge of the water quality scoring system used in China. However, this question does not directly test users knowledge of the underlying environmental and pollutant issues which are the basis of this water quality scale, nor does it test their knowledge or education about environmental issues or protection directly.

Many other interesting questions are present in the data set. For this thesis, several others were selected, and the values were analyzed. This discussion is presented later in this thesis.

### Blue City Water Quality Index Ranking (WQIR)
The second data set was compiled by the author from a report from the Institute of Public & Environmental Affairs, a non-profit environmental research organization based in Beijing. [@IPE] The report, the *Blue City Water Quality Index 2019*, compiles various surface, drinking, and ground water quality data published by various government agencies and assigns a score (their proprietary *Blue City Water Quality Index Score (BCWQI)*) and publishes the results at a sub-provincial level (second administrative level, or "admin 2"). [@jun2018BlueCity] The methodology and conversion to the government's water quality score is provided. This report was chosen as the basis for this data set since it was the most comprehensive data the author could find with the closest publication date to the CGSS. The difference in time of the two data sets is discussed in the #limitations section. In the appendix of this report, the BCWQI for each second administrative level, including the city name, province, and ranking, is included. This data, in a table in the PDF report, was exported into a comma separated value (.csv) file for later analysis.

It should also be noted that the water quality score used in the WQIR data set is derived from the official Chinese water quality scoring system. The following table translates between the two scoring systems: [@jun2018BlueCity, p.5]

| IPE Score     | IPE Level (EN)          | IPE Level (ZH) | EQ  Water |
|:-------------:|:-----------------------:|:--------------:|:---------:|
| 0.00 - 4.79   | Excellent               | 优             | II     |
| 4.79 - 10.28  | Good                    | 良             |III    |
| 10.28 - 16.85 | Moderate                | 一般           | IV     |
| 16.85 - 24.74 | Relatively Poor         | 较差           | V       |
| 24.70 - 50.00 | Poor                    | 差             | V      |

## Analysis
Analysis for this thesis was conducted using the general-purpose computer programming language Python. To allow for accessibility, readability, and reproducibility, the primary data analysis medium was a Jupyter notebook [@kluyverJupyterNotebooksPublishing], a document format which allows for text and code to be read and execute in an easy-to-read format, which was hosted on GitHub, to allow for accessibility. [@rynearsonWrynearsonChinawater2020] This was chosen after initial data analysis was conducted in a more traditional Python file, which was less collaborative and more cumbersome.

The two main data sets were loaded into the Jupyter notebook and reviewed for initial analysis, beginning with the CGSS2010. Then, after reviewing the data, it was cleaned and processed in several ways:

### Choosing Appropriate Questions

#### Demographic Questions
The thesis proposal and hypothesis were created before the author reviewed the data set, and before the author was aware of the environmental module of the CGSS. While many variables were deemed interesting, several variables were initially selected for broader analysis: [^1]

```{table} Relevant CGSS2010 Demographic Components 
:name: cgss2010-demographic
<!-- ~put table here -->

```


| Code | Variable (English)             | Variable (Chinese) | Importance                                             | Analyzed? |
|------|--------------------------------|--------------------|--------------------------------------------------------|-----------|
| s41  | Province                       |                    | Location of the individual                             | X         |
| a2   | Gender                         |                    | Possible control                                       | X         |
| a3a  | Birth year                     |                    | Age of respondant                                      | X         |
| a7a  | Highest level of education     |                    | Education could be linked to perception and knowledge? | X         |
| a91  | Rural / agricultural household |                    | Possible control                                       | X         |

Not all of the variables were utilized, such as income and subjective personal health, since they were outside of the scope of this thesis. 

#### Environmental Questions
The CGSS includes many demographic data on each respondent. Of which, the following were deemed important for one or more reasons: [^1]

```{table} Relevant CGSS2010 Environmental Components 
:name: cgss2010-env
<!-- ~put table here -->
 
```

| Code     | Question (English)                                                                                                               | Question (Chinese) | Response Types | Importance | Drawback                                                                    | Analyzed? |
|----------|----------------------------------------------------------------------------------------------------------------------------------|--------------------|----------------|------------|-----------------------------------------------------------------------------|-----------|
| l1a      | In your opinion, in terms of the current situation in our country, which of the following issues is the most important?          |                    |                |            |                                                                             | Yes       |
| l1b      | *like l1a, but 2nd most important*                                                                                               |                    |                |            |                                                                             | Yes       |
| l6a      | In your opinion, in terms of the current situation in our country, which of the following issues is the most important?          |                    |                |            |                                                                             | No        |
| l6b      | How serious are env. problems facing China?                                                                                      |                    |                |            |                                                                             | No        |
| l7a      | Which is most important env. issue in China?                                                                                     |                    |                |            | Response types are categorical, so differences in severity is not captured. |           |
| l7b      | Which has greatest impact on you/family?                                                                                         |                    |                |            |                                                                             |           |
| l8a      | Knowledge of causes of environmental problems from ?l7                                                                           |                    |                |            |                                                                             |           |
| l8b      | Knowledge of solutions of environmental problems from ?l7                                                                        |                    |                |            |                                                                             |           |
| l12a     | In order to protect the environment, to what extent are you willing to pay a higher price?                                       |                    |                |            |                                                                             |           |
| l12b     | *like l12a, but with higher taxes*                                                                                               |                    |                |            |                                                                             |           |
| l12c     | *like l12a/b, but with willingness to lower living standards*                                                                    |                    |                |            |                                                                             |           |
| l137     | Environmental issues directly affect my daily life                                                                               |                    |                |            |                                                                             |           |
| l14d     | How do you think the pollution of rivers, rivers and lakes in China is harmful to the environment?                               |                    |                |            |                                                                             | X         |
| l15a / b | *see question, about statements of responsibility for environmental protection (individuals/companies, government, etc.)*        |                    |                |            |                                                                             |           |
| l16c     | In terms of solving environmental problems in your area, how do you think the local government has done in the past five years?" |                    |                |            |                                                                             |           |
| l20e     | Do you often save water or reuse water specifically for environmental protection?                                                |                    |                |            |                                                                             |           |
| l2409    | In the domestic water pollution report, the water quality of Category V (5) is better than that of Category I (1)                |                    |                |            |                                                                             | X         |

As evident, these questions include questions related to the environment in general, perceptions of the local, national and global environment, water, and knowledge of water quality issues.

Many more survey questions were included in the main and additional module sections. Many of these relate to social satisfaction, political involvement, and future aspirations. Future analysis could be done with many of these questions, but were not within the scope of this analysis.

### Important Questions

Within the previously-identified relevant variables, the following have been identified as the most relevant for the scope of this study.

| Code  | English                                                                                                                                           | Chinese                                                          | Value Range (used)                           |
|-------|---------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|----------------------------------------------|
| s41   | Province                                                                                                                                          | 省                                                                | Range, *see data analysis*                   |
| a2    | Gender                                                                                                                                            | 性别                                                               | 1 = male, 2 = female                         |
| a3a   | Birth year                                                                                                                                        | 您的出生日期是什么                                                        | Birth year                                   |
| a7a   | Highest level of obtained education                                                                                                               | 您目前的最高教育程度是                                                      | 1 = none, 13 = master's and above            |
| a91   | Rural / agricultural household                                                                                                                    | 请问目前您或者您配偶是否为农业户口(或者户口所在地为农村),且在农村(包括家乡和其它地方)有承包的旱地、水田、山林、水面等土地? | 1 = yes, 2 = no                              |
| l14d  | "How do you think the pollution of rivers, rivers and lakes in China is harmful to the environment?" (*Used to measure perception*)               | 您认为中国的江、河、湖泊的污染对环境的危害程度是?                                        | 1 = very important, 5 = not important at all |
| l2409 | "In the domestic water pollution report, the water quality of Category V (5) is better than that of Category I (1)" (*Used to measure knowledge*) | 国内水体污染报告中,V(5)类水质要比I(1)类水质好                                      | 1 = correct, **2 = incorrect**               |

### Geographic Alignment
The two data sets are of differing geographic precision. The CGSS2010 (and all CGSSII data sets) include data on the province of where the respondent resided. Based on the structure of the data, it is assumed that more precise geographic information is included, however the CGSS publishing team chooses only to release the provincial information.

This is different than the WQIR2018 data, which is published at the sub-provincial level (admin 2). Thus, for comparative analysis, the mean water quality per province was calculated (more on this below).

**Insert Admin1 and Admin 2 maps here.**

### Procedure
Once the data sets were loaded and reviewed for importance and quality, initial data analysis was conducted. Due to the author's limited experience with Python, multiple versions of the analysis were conducted in order to gain working knowledge of Python and of the data set.

For provincial comparative analysis, the data was sorted by province `s41` and grouped into visual and numerical approaches of looking for differences between provinces. Several functions were created which allowed the author, and users, to see provincial comparative analyses on any question by inputting the question code. Either quantities of responses or their mean value would be output, as well as a heatmap for quick comparison. This initial analysis helped the author validate the main variables that were analyzed, which are discussed later.

Then, the WQIR2018 data was loaded. An initial plot was created to see the distribution of water quality per sub-province, sorted by province. Histograms were added to visualize the distribution of water quality measurements and values.

```{figure} ../wqir2018.svg
:name: wqir2018-vis
WQIR2018 distribution per province.
```
![wqir2018.svg](../wqir2018.svg)


From the previous steps, a subset of questions were created. Two main questions and one demographic variable were identified for further analysis: question `l14d` was used as the the main question to quantify perception[^2]; `l2409` was used as the main question to quantify water quality knowledge[^4]; and `a7a` was used to quantify education.[^5] These questions are discussed more in depth in the following limitations section. Other demographic data was used to control for results of the analysis. Many other relevant and interesting questions could be investigated from the data, but they are outside of the scope of this thesis.

Next, the values of these were examined. The author spent significant effort on this stage to better understand the state of the data set, and to understand the implications of choices in cleaning this data. Several revealed to be outside of the acceptable range, such as being recorded as negative numbers not present in the valid response list. Since the origin or reason behind these values could not be determined, they were discarded. This lead to further discrepancies in the number of values per category, including per province, education, perception and knowledge. This is discussed further in the analysis section.

Once invalid values were removed, the two data sets were merged on their shared province values. This was done in two separate ways, which allowed for different analysis.

1. **On Provinces**:  The mean water quality per province was added to the mean value per province of each analyzed variable. This allows for simpler data analysis, but loses some individual demographic data (gender, income, age, education, etc.).
2. **On Individuals**: The mean water quality per province was added to the individual response values. This makes the analysis slightly more complicated, but allows for comparison across the demographic data mentioned above. However, it should be noted that it runs the risk of providing a false sense of improved precision, and the mean water quality of the province may not accurately reflect the local situation of the individual.

While the author spent substantial time on analysis using the first method, the results of this study are mostly presented using the second method as they are more robust. The author conducted a large correlation test examining the correlation between every combination of questions and demographic data. While this test provided interesting results and provided inspiration for further investigation, most of the findings were outside of the scope of this thesis.

Once the data was analyzed, the author aligned the research questions and hypothesis with the data set variables. Each research question, and each tested hypothesis, was examined for correlations between two relevant variables, and were compared against one or more variables as a control. The analysis and findings are mentioned in the analysis section.

## Limitations

Several limitations exist based on the scope of both data sets, as well as limitation with some of the assumptions made by the author.

First, as discussed previously, there is misalignment between the CGSS and the WQIR data sets on two dimensions. The first is geographic. Since water quality data offered more geographic precision than the social survey responses (i.e. smaller regions), the effectiveness of comparison is reduced. This is in addition to the fact that water quality scores were originally presented as mean values per prefectural regions. This is different than the CGSS responses – while they were recorded at a more local level, geographic alignment information is only available at the provincial level. Further, the comparison between individuals and mean values per prefectural region results in the possibility that an two individuals in the same prefectural region experience different water quality, which is not possible to account for in the current methodology.

The second misaligned dimension is temporal, as the CGSS responses and water quality data differ by seven years. This is not ideal, since multiple indicators could have changed between that time. One is water quality, which has changed due to factors including the national government's initiatives, but this change has not been uniform across the country. Another indicator which could have changed is knowledge about water quality issues. Third, perception of water quality could have changed as well.

Further limitations come from the perceived findings based upon the CGSS question set. The two main questions which were analyzed, `l14d` and `l2409`, are not perfectly analogous to the conclusions the author made. `l14d` refers more to rivers and lakes in China, which are not necessarily the drinking water sources which are used by the respondent. Further, the severity of pollution being harmful to the environment is not necessarily the same as the respondents' perception. `l2409` directly tests respondents' knowledge of water quality scales used by China, but this question, and `l14d`, do not necessarily test for knowledge, and perception, of the local water quality - the question refers to China in general.

—
# Notes
- Those who are more aware about environmental issues may be more knowledgeable about water issues (`l7a`).
- Mention that water pollution is the 2nd highest category counted for `l7a` and 3rd for `l7b`
    - To ask perception in a different way, I could use respondents who say water is \#1\ from `l7a` `l7b` instead of `l14d`and if the trends matching education, perception and quality are the same.
        - Those who think `l14d` is harmful probably think that water pollution is \#1\ for `l7a` and `l7b`

—

[^1]: Translated from Chinese into English.
[^2]: "How do you think the pollution of rivers, rivers and lakes in China is harmful to the environment?" which has been translated from the original Chinese question "您认为中国的江、河、湖泊的污染对环境的危害程度是?"
[^3]: Extremely harmful to the environment – 1; Very harmful – 2; Some hazards – 3; Not very harmful – 4; There is no harm at all – 5; Cannot select – 8. This was translated from 对环境极其有害 – 1; 非常有害 – 2; 有些危害 – 3; 不是很有害 – 4; 完全没有危害 – 5; 无法选择 – 8
[^4]: The question is in a superset of knowledge about environmental knowledge, which states: "We also want to know your mastery of environmental protection knowledge. Please listen carefully to each of the following statements, and according to your solution to determine whether they are correct." The question is: "In the domestic water pollution report, the water quality of Category V (5) is better than that of Category I (1)," which is false. This question was translated from: "国内水体污染报告中,V(5)类水质要比I(1)类水质好."
[^5]: "What is your current highest education level (including those currently studying)." The values range from 1 - no education to 13 - postgraduate and above, in progressive order. This question was translated from "您目前的最高教育程度是(包括目前在读的)"