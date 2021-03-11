# Water Quality, Perception and Knowledge in China: *Data Analysis (condensed)*

This document is the data analysis of water quality, water quality perception, and water quality knowledge in China. The analysis is driven primarily by two datasets - water quality (2017, per prefecture) and a national general social survey (China General Social Survey, 2010) with an environmental module.

## Research Questions and Hypotheses

| Research Question | H0 (Null Hypothesis)                                                       | H1 (Hypothesis)                                                                                                         |
|:------------------|:----------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------|
| R1 Is there a relationship between water quality and perception of water quality? (I.e. do perceptions and reality match) | Worse local water quality is independent of water quality perception.      | Worse local (provincial) water quality relates to an increased perception of severity of water quality issues. |
| R2 Does knowledge of water quality affect perception?                | Increased knowledge is independent of perception.                          | An increase knowledge of water quality issues relates to an increased perception of severity.                              |
| R3 Does the level of obtained education relate to water quality knowledge?                | Increased education is independent of knowledge of water quality.          | Increased education relates to more knowledge about water quality.                                                         |
| R4 Does the level of obtained education relate perception?                | Increased education is independent of an increased perception of severity. | Increased education relates to an increased perception of severity                                                         |
| R5 Are there differences between water quality perception, and water quality knowledge, in rural vs. urban households?                | There is no significant difference between urban and rural households.     | There is a significant difference in perception of severity of water quality issues between urban and rural households.    |

## Core Analyzed Data

| Code  | English                                                                                                                                           | Chinese                                                          | Value Range (used)                           |
|:-------:|---------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|----------------------------------------------|
| s41   | Province                                                                                                                                          | 省                                                                | Range, *see data analysis*                   |
| a2    | Gender                                                                                                                                            | 性别                                                               | 1 = male, 2 = female                         |
| a3a   | Birth year                                                                                                                                        | 您的出生日期是什么                                                        | Birth year                                   |
| a7a   | Highest level of obtained education                                                                                                               | 您目前的最高教育程度是                                                      | 1 = none, 13 = master's and above            |
| a91   | Rural / agricultural household                                                                                                                    | 请问目前您或者您配偶是否为农业户口(或者户口所在地为农村),且在农村(包括家乡和其它地方)有承包的旱地、水田、山林、水面等土地? | 1 = yes, 2 = no                              |
| l14d  | "How do you think the pollution of rivers, rivers and lakes in China is harmful to the environment?" (*Used to measure perception*)               | 您认为中国的江、河、湖泊的污染对环境的危害程度是?                                        | 1 = very important, 5 = not important at all |
| l2409 | "In the domestic water pollution report, the water quality of Category V (5) is better than that of Category I (1)" (*Used to measure knowledge, response==2 is correct*) | 国内水体污染报告中,V(5)类水质要比I(1)类水质好                                      | 1 = correct, **2 = incorrect**               |


More information about the thesis, motivation, and methodology is located in the main "thesis_analysis.ipynb" document.

## Load Data

Load Python libraries

import pandas as pd
from pandas import DataFrame
import numpy as np # for some regression visualizations
import matplotlib as mpl
import matplotlib.pyplot as plt # for some visualizations
import seaborn as sns # for plots
import statsmodels.api as sm # for statistical analysis
import statsmodels.formula.api as smf # for statistical analysis
from sklearn import preprocessing # for normalizing data
import pingouin as pi # for statistical analysis

# Returns ALL columns when displaying DataFrame, useful for finding column names
pd.set_option('display.max_columns', None)

# Set the standard theme for plots
sns.set_theme(
    # palette='twilight'
    )
sns.set_style("ticks")

Load CGSS (social survey) data from a Stata file

cgss = pd.read_stata('../data/cgss2010_12.dta', preserve_dtypes = True, convert_categoricals=False)

List categorical data

categoricals = ["s41","a2","a91","l1a","l1b","l7a","l7b","l2409"]

List important questions

important = ['score','s41','a2','a3a','a7a','a8a','a91','l1a','l1b','l6a','l6b','l7a','l7b','l8a','l8b','l137','l14d','l15a','l15b','l16c','l20e','l2409','province','province_en']

Convert categorical data into categorical data types

cgss[categoricals].astype('category')

Load province data from a .csv, set province code as the index

provinces = pd.read_csv('prov.csv')

Load water quality data

wqir = pd.read_csv('../data/wqir2018_zh.csv', sep=' ', encoding = "UTF-8")

---

## Merge data into one dataframe

Group the water quality data (WQIR) by province and compute the mean

wqir_mean = wqir.groupby(by='province').agg('mean')

Merge the mean water quality per province and the province dataframe (matching names and province codes)

merge = pd.merge(wqir_mean, provinces, on='province')

Drop rank column, merge the previously merged column into the main cgss dataframe so that each entry has the mean water score from their province, plus the names of their province (Chinese short and full and English).

wq = merge[['s41','score','province','province_full','province_en']]
cgss_wq_full = pd.merge(cgss,wq,on='s41')

Only analyze important questions and variables (drop remaining ones)

cgss_wq = cgss_wq_full[important]

---

## Testing Hypotheses (Descriptive Analysis)

### H1 - Worse local (provincial) water quality (`score` increases) relates to an increased perception of severity of water quality issues (`l14d` decreases).

First, clean the data for `l14d` by dropping NaN, negative and "cannot answer" values:

cgss_wq_l14d = cgss_wq[cgss_wq["l14d"]>0]
cgss_wq_l14d = cgss_wq_l14d[cgss_wq_l14d["l14d"]<6]

Visualize the results: Perception vs. Water Quality (more details about sns.lmplot in the Hypothesis 4 section)

h1_fig1 = sns.lmplot(
    data=cgss_wq_l14d,
    x = 'l14d',
    y = 'score',
    x_estimator=np.mean,
    )
h1_fig1.savefig('outputs/h1_fig1.svg')

pi.corr(x=cgss_wq_l14d['score'], y=cgss_wq_l14d['l14d'])

#### Initial findings:
- While the correlation is significant (Low $p$ value == more compelled to reject null hypothesis), there is a poor regression fit (low r²)
- Multivariable analysis required for further investigation

### H2 - An increase knowledge of water quality issues (`l2409`) relates to an increased perception of severity (`l14d`).

Clean data for `l2409` using previously cleaned `l14d` dataframe:
**NOTE**: Only keeping binary responses (dropping *Can't respond* value `8`)

cgss_wq_l14d_l2409 = cgss_wq_l14d[cgss_wq_l14d["l2409"]>0]
cgss_wq_l14d_l2409 = cgss_wq_l14d_l2409[cgss_wq_l14d_l2409["l2409"]<3]

h2 = cgss_wq_l14d_l2409.groupby('l2409').agg('mean')
h2

Count the number of responses per `l2409`

cgss_wq_l14d_l2409["l2409"].value_counts()

Now, plot: (`l2409==2` is the correct answer)

h2_fig1 = sns.catplot(
    data=cgss_wq_l14d_l2409,
    x = 'l2409',
    y = 'l14d',
    hue='a91',
    split=True,
    kind='violin',
    scale='count',
    )
h2_fig1.savefig('outputs/h2_fig1.svg')

Plot again - note that the line connecting the two isn't relevant or accurate

sns.catplot(
    data=cgss_wq_l14d_l2409,
    x = 'l2409',
    y = 'l14d',
    kind='point',
    #hue='a91',
    )

pi.corr(x=cgss_wq_l14d_l2409['l2409'], y=cgss_wq_l14d_l2409['l14d'], method='kendall')

#### Initial findings:
- Increased water quality knowledge `l2409==2` has an increased perception (decreased `l14d`).
    - Statistically significant ($p<=0.05$) but weakly correlated ($0<r<.19$)
- However, this trend is no longer visible when factoring for rural/urban `a91`, education level `a7a`, etc
- Other large differences between rural/non-rural exist (see `h2` above)
- More analysis is needed

### H3 - Increased education (`a7a`) relates to more knowledge about water quality (`l2409`).


Clean data for `l2409`

Again, **NOTE**: Only keeping binary responses (dropping *Can't respond* value `8`)

cgss_wq_l2409 = cgss_wq[cgss_wq["l2409"]>0]
cgss_wq_l2409 = cgss_wq_l2409[cgss_wq_l2409["l2409"]<3]

Now, clean for education `a7a`

cgss_wq_l2409_a7a = cgss_wq_l2409[cgss_wq_l2409["a7a"]>=0]
cgss_wq_l2409_a7a = cgss_wq_l2409_a7a[cgss_wq_l2409_a7a["a7a"]<14]

Now, plot:

h3_fig1 = sns.lmplot(
    data=cgss_wq_l2409_a7a,
    x = 'a7a',
    y = 'l2409',
    x_estimator=np.mean,
    )
h3_fig1.savefig('outputs/h3_fig1.svg')

h3_fig2 = sns.catplot(
    data=cgss_wq_l2409_a7a,
    x = 'l2409',
    y = 'a7a',
    hue='a91',
    split=True,
    kind='violin',
    scale='count',
    )
h3_fig2.savefig('outputs/h3_fig2.svg')

pi.corr(x=cgss_wq_l2409_a7a['l2409'], y=cgss_wq_l2409_a7a['a7a'], method='spearman')

#### Initial findings
- There seems to be a slight trend (education increase relates to knowledge increase)
- The violin plots show differences in rural vs non-rural responses
- More analysis is needed

21

First, see the distribution of education:

cgss_wq[["a7a","l14d"]].hist()

Make new cleaned dataset with cleaned `a7a` values from the previously cleaned `l14d` values

cgss_wq_l14d_a7a = cgss_wq_l14d[cgss_wq_l14d['a7a']>=0]

Group by each education level (year) and aggregate the mean

h4 = cgss_wq_l14d_a7a.groupby('a7a').agg('mean')

Plot result (perception vs. education level). 

**Note**: Since `a7a` is the index of h4, it needs to be reset before being plotted in regplot (info [here](https://www.reddit.com/r/learnpython/comments/3cjnpg/seaborn_xaxis_as_index/))

h4_fig1 = sns.lmplot(
    data=h4.reset_index(),
    x = 'a7a',
    y = 'l14d'
    )
h4_fig1.savefig('outputs/h4_fig1.svg')

It's better (?) to use an lmplot (similar to regplot) and calculate the mean per x bin, from [here](https://seaborn.pydata.org/tutorial/regression.html).
> A second option is to collapse over the observations in each discrete bin to plot an estimate of central tendency along with a confidence interval:

Additionally, the lmplot allows for multiple regressions to be plotted on the same plot.

h4_fig2 = sns.lmplot(
    data=cgss_wq_l14d_a7a,
    x = 'a7a',
    y = 'l14d',
    x_estimator=np.mean,
    hue='a91',
    markers=(["o", "x"]),
    )
h4_fig2.savefig('outputs/h4_fig2.svg')

pi.corr(x=cgss_wq_l14d_a7a['a7a'], y=cgss_wq_l14d_a7a['l14d'])

### Initial findings:
- There is a clear trend between education and perception
- Rural households have a higher `l14d` than non-rural at each education level
    - This difference decreases as education increases

### H5 - There is a significant difference in perception of severity of water quality issues (`l14d`) between urban and rural households (`a91`).

Reuse the cleaned data from `H1` for question `l14d`, see number of responses by type by grouping by `a91`, where a91==1 is rural

cgss_wq_l14d[['a91','l14d']].groupby('a91').agg('count')

Calculate the mean `l14d` grouped by rural / urban

h5 = cgss_wq_l14d.groupby('a91').agg('mean')
h5.describe()

pi.corr(x=cgss_wq_l14d['a91'], y=cgss_wq_l14d['l14d'], method='spearman')

#### Initial findings: 
- There is a difference between rural and urban households (rural have less severe perception of water quality)
- Education level (`a7a`) is significantly different between urban and rural households

---

<div class="alert alert-block alert-info">
<b>Note:</b> Sections below are not final. Work in progress (March 8th, 2021).</div>

---

## Additional descriptive analysis

### `l6`
Start with `l6`, where:
- `l6a` asks "Generally speaking, how much do you care about environmental issues?
- `l6b` asks "Based on your own judgment, on the whole, do you think the environmental problems facing China are serious?"

First, clean data: (**Note**: When I tried this in one step (two columns), I was having graph issues later, so I did each step individually)

cgss_wq_l6 = cgss_wq[cgss_wq['l6a']>0]
cgss_wq_l6 = cgss_wq_l6[cgss_wq_l6['l6a']<6]
cgss_wq_l6 = cgss_wq_l6[cgss_wq_l6['l6b']>0]
cgss_wq_l6 = cgss_wq_l6[cgss_wq_l6['l6b']<6]

Plot

fig, ax = plt.subplots()
cgss_wq_l6.hist(['l6a','l6b'], ax=ax)
fig.savefig('outputs/l6_fig1.svg')

l6_fig2 = sns.lmplot(
    data=cgss_wq_l6,
    x = 'l6a',
    y = 'l6b',
    x_estimator=np.mean,
    hue='a91'
    )
l6_fig2.savefig('outputs/l6_fig2.svg')

pi.corr(x=cgss_wq_l6['l6a'], y=cgss_wq_l6['l6b'])

### `l7`

Compare with `l7` ("Which issue do you think is the most important environmental issue in China?")
- `l7a`: most important
- `l7b`: 2nd most important

Values:
- Air Pollution - 1
- Fertilizer and pesticide pollution - 2
- Water scarcity - 3
- Water pollution - 4
- Nuclear waste - 5
- Disposal of domestic waste - 6
- Climate Change - 7
- Genetically modified food - 8
- Depletion of natural resources - 9
- None of the above - 10
- Cannot select - 98

Make label dictionary

l7_labels = {'Air Pollution':1, 'Fertilizer and pesticide pollution':2, 'Water scarcity':3, 'Water pollution':4, 'Nuclear waste':5, 'Disposal of domestic waste':6, 'Climate Change':7, 'Genetically modified food':8, 'Depletion of natural resources':9, 'None of the above': 10, 'Cannot select':98}

Convert to dataframe

l7_df = pd.DataFrame.from_dict(l7_labels, orient='index', columns=['l7a'])

**Attempting to put labels on histogram below, but can't**

Clean data, drop 10 & 98 (use the '~' to negate the .isin() function)
Cleaning both at the same time results in the same as doing it individually

cgss_wq_l7=cgss_wq[~cgss_wq[['l7a','l7b']].isin([-3,-1,98])]

cgss_wq_l7[['l7a','l7b']].describe()

fig, ax = plt.subplots()
cgss_wq_l7.hist(['l7a','l7b'], ax=ax)
fig.savefig('outputs/l7_fig1.svg')

l7_fig2 = sns.displot(
    data=cgss_wq_l7, 
    x='l7a', 
    # hue='l7b', 
    discrete = True, 
    # multiple='stack',
    kind = 'hist'
    )
l7_fig2.savefig('outputs/l7_fig2.svg')

l7_fig3 = sns.displot(
    data=cgss_wq_l7, 
    x='l7b',
    # hue='l7b', 
    discrete = True, 
    # multiple='stack', 
    kind = 'hist'
    )
l7_fig3.savefig('outputs/l7_fig3.svg')

---

## Normalize Data

---

## Multivariable statistical analysis

ols_perception = smf.ols('l14d ~ score + C(a2) + a3a + a7a + C(a91)', data = cgss_wq).fit()
ols_perception.summary()

ols_knowledge = smf.ols('l2409 ~ score + C(a2) + C(a91)', data = cgss_wq).fit()
ols_knowledge.summary()

## NOTES
- Normalize variables (variance is different)
- Cannot use OLS, use LOGIT (logistic regression)

Things to change in the code
1. not use OLS for categorical output but use LOGIT (logitstic regression) to model categorical output
2. normalise continous variables as in the example notebook
3. Use the C(...) for categoricals 
4. To use to logit, you need a binary output:
4.a remove '8' answers to construct a first model and validate it
4.b. since most answers are '8' and you don't want to discard them, create a new logistic regression model with ternary output (this is possible)

R² shows model explains variation in dependent variable, while R is correlation between one variable and another
- With my correlation analysis, use R
- If I use OLS, use R²

