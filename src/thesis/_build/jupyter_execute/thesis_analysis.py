# Water Quality, Perception and Knowledge in China
## Master's thesis data for Tsinghua University

This document is the data analysis of water quality, water quality perception, and water quality knowledge in China. The analysis is driven primarily by two datasets - water quality (2017, per prefecture) and a national general social survey (China General Social Survey, 2010) with an environmental module.

Several questions are examined:
- How do peoples perception of water quality (importance, status, severity, their knowledge, etc) align with actual water quality?
- Is there a correlation between water quality and perception of water quality? (I.e. do perceptions and reality match)?
- Does knowledge of water quality affect perception? 
- Does general education affect perception?

This document show the progression of analysis, thus not all cells and text are relevant to the final findings of this thesis.

<div class="alert alert-block alert-info">
<b>Note:</b> Work in progress (Jan 31, 2021).</div>

---

## Table of Contents

[Load Data](#Load-Data)  
[Initial Data Exploration](#Initial-Data-Exploration)  
[Combining Data](#Combining-Data)  
[Individual Data Analysis](#Individual-Data-Analysis)

---

## Load Data

import pandas as pd
from pandas import DataFrame
import matplotlib as mpl
import seaborn as sns 
import matplotlib.pyplot as plt
import numpy as np
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.multivariate.manova import MANOVA
import sklearn
from sklearn import preprocessing

# Returns ALL columns when displaying DataFrame, useful for finding column names
pd.set_option('display.max_columns', None)

### 1. China General Social Survey (2010)

The first dataset is the China General Social Survey (CGSS), an annual national comprehensive survey consisting of demographic data, social indicators, and rotating modules. The year 2010 is used since it is the latest published which includes the environmental module, 20+ questions about quality of the environment, peoples' thoughts on the importance of the environment, the severity of environmental degredation, etc. (more details below).

http://cgss.ruc.edu.cn/index.php?r=index/index&hl=en

# Load cgss2010 Stata file, display the first 5 rows (.head())
cgss = pd.read_stata('../data/cgss2010_12.dta', convert_categoricals=False)
cgss.info()

#### General Demographics
s41 - province codes

a2 - gender

a3a - birth year

a3b - birth month

a3c - birth date

a7a - highest current level of education

a8a - personal total income

a15 - subjective physical health

a62 - family total income (2009)

a91 - rural / agricultural household *(1=yes, 2=no)*

a92 - rural / agricultural household *(1=yes, 2=no) (verified by surveyor)*


#### Environmental Module (Part L)
l1a - "In your opinion, in terms of the current situation in our country, which of the following issues is the most important?" **(4 = environment)**

l1b - *like l1a, but 2nd most important*

l6a - "In your opinion, in terms of the current situation in our country, which of the following issues is the most important?" *(1 = not at all, 5 = very concerned)*

l6b - How serious are env. problems facing China? *(1 = very, 5 = not at all)*

l7a - Which is most important env. issue in China? **(4 = water pollution)**

l7b - Which has greatest impact on you/family? **(4 = water pollution)**

l8a - Knowledge of causes of environmental problems from ?l7

l8b - Knowledge of solutions of environmental problems from ?l7

l12a - "In order to protect the environment, to what extent are you willing to pay a higher price?" *(1 = very willing, 5 = very reluctant)*

l12b - *like l12a, but with higher taxes*

l12c - like l12a/b, but with willingness to lower living standards

l137 - "Environmental issues directly affect my daily life" *(1 = disagree, 5 = agree)*

l14d - "How do you think the pollution of rivers, rivers and lakes in China is harmful to the environment?" *(1 = extremely, 5 = not at all)*

l15a/b - *see question, about statements of responsibility for environmental protection (individuals/companies, government, etc.)*

l16c - "In terms of solving environmental problems in your area, how do you think the local government has done in the past five years?" *(1 = ignored, 5 = successful)*

l20e - "Do you often save water or reuse water specifically for environmental protection?" *(1 = always, 4 = never)*

l2409 - "In the domestic water pollution report, the water quality of Category V (5) is better than that of Category I (1)" *(1 = correct, 2 = incorrect, 8 = cannot choose)*


important_questions = ['score','s41','a2','a3a','a3b','a3c','a7a','a8a','a15','a62','a91','a92','l1a','l1b','l6a','l7a','l7b','l8a','l8b','l12a','l12b','l12c','l137','l14d','l15a','l15b','l16c','l20e','l2409']

Below is a subset of only important questions from the environmental module (including and omitting`s41`)

environment = ['s41','l1a','l1b','l6a','l7a','l7b','l8a','l8b','l12a','l12b','l12c','l137','l14d','l15a','l15b','l16c','l20e','l2409']

part_l = ['l1a','l1b','l6a','l7a','l7b','l8a','l8b','l12a','l12b','l12c','l137','l14d','l15a','l15b','l16c','l20e','l2409']

*For some reason, I need to manually copy the list of important column codes. They are the same as the `important questions` above.*

cgss_important = cgss[['s41','a2','a3a','a3b','a3c','a7a','a8a','a15','a62','a91','a92','l1a','l1b','l6a','l7a','l7b','l8a','l8b','l12a','l12b','l12c','l137','l14d','l15a','l15b','l16c','l20e','l2409']]
cgss_important.describe()

#### Very Limited Subset of Questions (for initial analysis)

This only includes the most important questions,

columns_strict = ['s41','l14d','l2409']

cgss_strict = cgss[columns_strict]

Only include the strict set of 3 columns

The survey uses geographic identifiers in columns s41 (and I think s42-44). However, only province level information is released, due to privacy concerns (see [this link](http://cgss.ruc.edu.cn/index.php?r=index/artabout&aid=18)). They are listed below, in a dictionary (Chinese)

provinces = pd.read_csv('prov.csv')
provinces.set_index('s41')

---

### 2. 2018 Blue City Water Quality Index Ranking

The second dataset is the water quality of every prefecture (sub-province) from a 2018 publication (using 2017 measurements). **Add more details**

https://wwwoa.ipe.org.cn//Upload/201909201147459274.pdf (en)

wqir = pd.read_csv('../data/wqir2018_zh.csv', sep=' ', encoding = "UTF-8")

province = wqir['province']
score = wqir['score']
city = wqir['city']
category = wqir['level']

---

## Initial Data Exploration

### CGSS2010

#### Heatmap Function

The following function asks the user to imput a column title (question code). Any column name can be entered, but for interesting results, choose one from the above list of important survey questions.

Once the column name is entered, the function displays a visual heatmap of the response types by decimal (total = 1.0) on the x axis, sorted by province on the y axis.

Enter `heatmap()` to execute this function.

def heatmap():
    user_column = input('Enter a column code: ')
    user = cgss[cgss[user_column] >= 1]
    # Group by provence, count people in each province, then sort them by asceding order.
    user_grouped = (user.groupby(['s41', user_column])
        .size()
        .unstack(fill_value=0)
        .sort_index(axis=1, ascending=True)
        )
    user_grouped_percent=user_grouped.div(user.groupby(['s41']).size(), axis=0)
    user_grouped_percent=user_grouped_percent.round(1)
    fig, ax = plt.subplots()
    sns.set_theme(
        style="white",
        font='AR PL UMing CN',
        font_scale=.30,
        )
    sns.heatmap(
        user_grouped_percent,
        vmin=0,
        vmax=1,
        yticklabels=1,
        annot=True,
        cmap='viridis',
        square=True,
        cbar=False,
        )
    ax.set_title(user_column)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    plt.setp(ax.get_yticklabels(), rotation=0, ha="center", rotation_mode="anchor")
    fig.tight_layout()

#### Count Function

The following function does the same initial steps as the `heatmap` function, but without normalizing by the number of responses per province (it only sums the responses by type and by province).

Enter `count()` to execute this function.

def count():
    user_column = input('Enter a column code: ')
    user = cgss[cgss[user_column] >= 1]
    user_grouped = (user.groupby(['s41', user_column])
        .size()
        .unstack(fill_value=0)
        .sort_index(axis=1, ascending=True)
        )
    return user_grouped

#### Percent Function

The following function is the same as the `count` function, but also normalizes per province to make quanities comparable. It's essentially the `heatmap` function without the visualization.

Enter `percent()` to execute this function.

def percent():
    user_column = input('Enter a column code: ')
    user = cgss[cgss[user_column] >= 1]
    user_grouped = (user.groupby(['s41', user_column])
        .size()
        .unstack(fill_value=0)
        .sort_index(axis=1, ascending=True)
        )
    user_grouped_percent=user_grouped.div(user.groupby(['s41']).size(), axis=0)
    user_grouped_percent=user_grouped_percent
    user_grouped_percent=user_grouped_percent
    return user_grouped_percent

#### Individual Question Countplot

The following function visualizes number of responses (total, not per province) for each response type of an entered column (question code).

Enter `countplot()` to execute this function.

def countplot():
    user_column = input('Enter a column code: ')
    sns.countplot(
        data=cgss,
        x=cgss[user_column],
        )

---

### 2018 Blue City Water Quality Index Ranking Visualization (WQIR2018)

The following shows statististical information for the WQIR2018 dataset. Let's see the data, loaded above. As evident, the `Province`, `City`, `Score`, `Rank`, and the `Level` for the water quality level.

*Run `wqir.head()` to see the shape of the dataframe*

On page 5 of the report [here](https://wwwoa.ipe.org.cn//Upload/201909201147459274.pdf) (mentioned above), the following are the score/level to water quality classes (outlined [here](http://english.mee.gov.cn/SOE/soechina1997/water/standard.htm)):

| IPE Score     | IPE Level (EN)          | IPE Level (ZH) | EQ  Water |
|:-------------:|:-----------------------:|:--------------:|:---------:|
| 0.00 - 4.79   | Excellent               | 优             | II     |
| 4.79 - 10.28  | Good                    | 良             |III    |
| 10.28 - 16.85 | Moderate                | 一般           | IV     |
| 16.85 - 24.74 | Relatively Poor         | 较差           | V       |
| 24.70 - 50.00 | Poor                    | 差             | V      |

*Note: The EQ equivalents above refer "The total score (equivalent to the local water
quality average) met or surpassed the requirements of Class `X` (II-V) water quality..."*

wqir_mean = wqir.groupby(by='province').agg('mean')

The following plot visualizes the WQIR2018 values by province (y axis), with each prefecture's score lined up on the x axis. This is to visualize the range of water quality values in each province. On the top and right, two histograms count the occurances at each value (horizontal, top one bins water quality scores, while the vertical, right one bins the number of prefecture regions per province).

sns.set_theme(
    style="ticks",
    font='AR PL UMing CN',
    font_scale=.85,
    )

g = sns.JointGrid(
    ratio=7,
    space=.25,
    marginal_ticks=True,
    xlim=(0,45),
    x=score,
    y=province,
    palette="gist_earth",
    hue=category,
    data=wqir,
) 
  
sns.despine(trim=False, left=True, bottom=False)
g.plot(sns.scatterplot, sns.histplot)

The provinces of 青海 (Qinghai), 海南 (Hainan), and 西藏 (Tibet) have good water quality which is relatively uniform. These make for good comparison with provinces with worse water quality.

---

## Combining Data

In this section, I will try to link the data from CGSS2010 and WQIR2018 and compare them across provinces.

## Sorting Data

This section has the data loaded previously sorted, usually by province.

First, count the values of the `cgss_strict` df (so it's easier to deal with and understand) by province `s41`. I learned this [here](https://kanoki.org/2020/03/09/how-to-use-pandas-count-and-value_counts/).

*Run `cgss_strict.groupby(by='s41').agg('count')` to see the number of responses per province*

### `l14d`

Sort by response types for `l14d`, see the number of responses. Column `s41` is irrelavent, this is just to see all response types for `l14d` to check for incorrect values.

Call one column `l14d`, then count instances of values with `.value_counts()`, then make a dataframe with `.to_frame()`, then sort by the response value with `.sort_index()`

cgss_strict['l14d'].value_counts().to_frame().sort_index()

As we can see, there are negative values, which are not valid response types. Let's see which provinces they're in, to see if we can safely drop the values.

cgss_strict[cgss_strict['l14d'] < 0].groupby(by='s41').agg('count')

### `l2409`

repeat

cgss_strict['l2409'].value_counts().to_frame().sort_index()

cgss_strict[cgss_strict['l2409'] < 0].groupby(by='s41').agg('count')

---

For the first question `l14d`, the negative values are fairly spread out between columns. It's safe to drop them.


However, for `l2409`, they make up a large proportion of the total response values for province 25, which is Tibet. As seen below, filtered just for Tibet for question l2409, 17/19 responses are invalid. Because water quality for Tibet also isn't included, we're forced to remove it from this analysis.

cgss_strict[cgss_strict['s41']==25].groupby('l2409').agg('count')

The response value of 8 refers to "cannot choose", so for now, let's drop those (it may be important later)

Let's drop the two problmatic values -3 and -2, and 8, group by province again, and calculate the mean.

## **If I filter out 8, then Ningxia province get's taken out... find a fix**

cgss_strict_mean = cgss_strict.replace([-3,-2,],).groupby(by='s41').agg('mean')

### Merge Data

The following merges the `wqir_mean` values with the `provinces` dataframe.

merge = pd.merge(wqir_mean, provinces, on='province')

Add water quality mean (per province) to each individual row:

Then, the `cgss_strict_clean` values are merged in. (I didn't know how to do this in one step)

merged = pd.merge(merge,cgss_strict_mean,on='s41')

Quick check to see if there are visible trends...

sns.scatterplot(
    x='score',
    y='l14d',
    data=merged,
)

---

Now, let's do this with the larger `cgss_important` dataframe:

*Trying to get a df with values as index and frequency per question (column), but can't...*

cgss_part_l = cgss_important[part_l]
for column in cgss_part_l:
    counts = cgss_part_l[column].value_counts()
    counts.append(counts)

Create the mean of all values from `cgss_important`:

cgss_imp_mean = cgss_important.groupby(by='s41').agg('mean')

Merge with water quality and provinces:

merged_imp = pd.merge(merge,cgss_imp_mean,on='s41')

*Play around with some correlations:*

corr = cgss_important.corr(method="pearson")

corr_mean = merged_imp.corr(method="pearson")

Plot, first set the theme

sns.set_theme(
    style="white",
    font='AR PL UMing CN',
    font_scale=.2,
    )

corr_hm = sns.heatmap(
    corr,
    vmin=-1,
    vmax=1,
    annot=True,
    cmap='BrBG',
    square=True,
    cbar=True,
    center=0
    )

figure1 = corr_hm.get_figure()

corr_mean_hm = sns.heatmap(
    corr_mean,
    vmin=-1,
    vmax=1,
    center=0,
    annot=True,
    cmap='BrBG',
    square=True,
    cbar=True,
    )

# figure2 = corr_mean_hm.get_figure()
# figure2.savefig('corr_mean_hm.svg', dpi=800)

Check quickly for a .37 correlation (haven't filtered out 8 value responses yet)

sns.set_theme(
    style="white",
    font_scale=1,
    )
sns.scatterplot(
    x='score',
    y='l14d',
    palette="gist_earth",
    data=merged_imp,
)

---

## Individual Data Analysis

This section adds mean water quality scores per province to each individual response of the `cgss` dataframe, thus analysis with more statistical significance can be done.

First, take only the s41 codes and wq mean scores from the `merge` dataframe, then add the water quality `score` to the main `cgss` dataframe:

wq = merge[['s41','score']]
cgss_wq = pd.merge(cgss,wq,on='s41')

This analysis will first be done on the `important` columns, from above:

cgss_wq_imp = cgss_wq[important_questions]
cgss_wq_imp_clean = cgss_wq_imp.dropna()

Filter out negative values and unknown ('8')

wq_imp_clean = cgss_wq_imp_clean[
    (cgss_wq_imp_clean.l14d > 0) 
     & (cgss_wq_imp_clean.l14d < 6) 
     & (cgss_wq_imp_clean.l2409 > 0) 
     # (cgss_wq_imp_clean.l2409 < 3)
    ]

clean_prov = wq_imp_clean.groupby('s41').agg('mean')

maov = MANOVA.from_formula('l14d + l2409 ~ s41 + score', data=wq_imp_clean)
print(maov.mv_test())

Conduct OLS regression with l14d dependent on gender, age (year) and income:

ols_perception = smf.ols('l14d ~ score + a2 + a3a + a7a', data = wq_imp_clean).fit()
print(ols_perception.summary())

*Think of a way to run the ols for knowledge without the l2409 = 8 values*

ols_knowledge = smf.ols('l2409 ~ s41 + score + a2 + a3a + a7a + a91', data = wq_imp_clean).fit()
print(ols_knowledge.summary())

### Initial Findings
With P>|t| ~0.05 or less (0.055), this can be argued that an increased wq score (worse) leads to an decreased number for l14d (perceived to be more harmful)

The higher the education (a7a increases), the l14d number goes down (the perceived severity increases)

(The coef is negative for both, which indicates a negative relation/correlation)

**Keep in `l2409` unsure (8) since it increases observations and therefore statistical power (.02 vs .055)**

Thus: Water quality (score) is correlated with perception (l14d) & education (a7a) is correlated to perception, Also (not shown) education is coorelated with wq knowledge (l2409), but score is not correlated with wq knowledge.

#### Test for divergence
Seeing if there's a correlation between the difference between perception and score, and another variable.

Import main data, groupby and take mean...

tst = wq_imp_clean[['score','s41','l14d']].groupby('s41').agg('mean')
tst.describe()

Normalize the data (0-1) using code I found [here](https://stackoverflow.com/questions/26414913/normalize-columns-of-pandas-data-frame): 

test = tst.apply(lambda x: x/x.max(), axis=0)

Make new column with the difference between the score and perception. Perception number goes up as perceived severity goes down. Score goes up as water quality gets worse. 

Diff increases when the two are more different (positive if poor wq and severe perception, negative if good wq and good perception)

test['diff'] = test['score'] - test['l14d']
test

Plot difference vs wq score

sns.relplot(
    data=test,
    x="score",
    y="diff",
    hue='l14d'
    )

sns.relplot(
    data=clean_prov,
    x='score',
    y='l14d',
    label='s41'
)

Interesting! ^