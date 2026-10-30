# Data Science Beginner's Cheatsheet

A reference for the concepts, definitions and rules of thumb covered in the course and our sessions.
German course terms are given in parentheses where they differ from the English ones.

**Contents**

1. [The big picture](#1-the-big-picture)
2. [Glossary of terms and abbreviations](#2-glossary-of-terms-and-abbreviations)
3. [The Python toolbox](#3-the-python-toolbox)
4. [Statistics essentials](#4-statistics-essentials)
5. [Data preparation and missing data](#5-data-preparation-and-missing-data)
6. [Correlation, causation and cognitive effects](#6-correlation-causation-and-cognitive-effects)
7. [Machine learning basics](#7-machine-learning-basics)
8. [Evaluating models: metrics](#8-evaluating-models-metrics)
9. [Anomaly detection](#9-anomaly-detection)
10. [Data architecture and cloud](#10-data-architecture-and-cloud)
11. [Business side: KPIs, decisions, storytelling](#11-business-side-kpis-decisions-storytelling)
12. [Data protection (DSGVO / GDPR)](#12-data-protection-dsgvo--gdpr)
13. [Project template and checklist](#13-project-template-and-checklist)

---

## 1. The big picture

**Data Science (DS)** is the umbrella term: using data, statistics, programming and domain knowledge to answer questions and support decisions.

The typical workflow:

1. **Business question:** what decision should the result support? ("Push until you get to a decision, not a topic.")
2. **Data collection and understanding:** where does the data come from, what does each column mean, who collected it, and how?
3. **Cleaning and preparation:** missing values, duplicates, outliers, wrong types.
4. **Exploration (EDA):** summaries and plots to find patterns and problems.
5. **Modelling:** statistics or machine learning.
6. **Evaluation:** with metrics that match the cost of mistakes.
7. **Communication:** a result that decision makers can act on.
8. **Operation and monitoring:** models degrade when the world changes.

**Types of analytics** (each builds on the previous):

| Type | Question | Example |
|---|---|---|
| Descriptive | What happened? | Average wait time last month |
| Diagnostic | Why did it happen? | Waits rose because of flu season |
| Predictive | What will happen? | Expected patients tomorrow |
| Prescriptive | What should we do? | Add one nurse on Monday mornings |

**Prediction versus causation:** a model can predict well without telling you what to *change* (see section 6).

---

## 2. Glossary of terms and abbreviations

### General

| Term | Meaning |
|---|---|
| **AI / KI** | Artificial Intelligence (Künstliche Intelligenz). Broad umbrella for systems that perform tasks that normally need human intelligence. ML is a part of it. |
| **ML** | Machine Learning. Algorithms that learn patterns from data instead of being explicitly programmed. |
| **DL** | Deep Learning. ML with neural networks that have many layers. |
| **DS** | Data Science. Umbrella for the whole discipline. |
| **Advanced Analytics** | Predictive and prescriptive methods (statistics and ML) beyond classic reporting. It is one *tool within* data science, not "statistics without ML". |
| **BI** | Business Intelligence. Reports and dashboards about the past and present. |
| **EDA** | Exploratory Data Analysis. Looking at the data (summaries, plots) before modelling. |
| **KPI** | Key Performance Indicator (Kennzahl). A measurable number showing progress toward a goal. |
| **OKR** | Objectives and Key Results. A goal-setting method: an ambitious objective plus measurable key results. |
| **ETL / ELT** | Extract-Transform-Load / Extract-Load-Transform. See section 10. |
| **API** | Application Programming Interface. A defined way for programs to talk to each other. |
| **SQL** | Structured Query Language. Language for querying relational databases. |
| **CSV** | Comma-Separated Values. Plain-text table format. |
| **CLI** | Command Line Interface. Using a program by typing commands. |
| **RCT** | Randomized Controlled Trial. Randomly assign subjects to treatment or control to measure causal effects. |
| **A/B test** | An RCT on a website or product: version A versus version B. |

### Data terms

| Term | Meaning |
|---|---|
| **Feature** (Merkmal) | An input column the model uses to predict, e.g. age, overtime. Also called predictor, independent variable, `X`. |
| **Target / label** (Zielvariable) | The column you want to predict, e.g. `Attrition`. Also called dependent variable, `y`. |
| **Variable** | Any column or quantity in the data. Features and target are both variables. |
| **Parameter** | A value the model learns *during* training (weights, split points). |
| **Hyperparameter** | A setting *you* choose *before* training (tree depth, learning rate, number of layers). |
| **Train / test split** | Training data fits the model, test data is held back to judge it honestly. Also a validation set for tuning. See *Training and validation: key terms* in section 7. |
| **Overfitting** | The model memorizes noise in the training data and does badly on new data. |
| **Underfitting** | The model is too simple to capture the real pattern. |
| **Data leakage** | Information from the test data or from the future sneaks into training, producing too-good results. Details and fixes in section 7. |
| **Imbalanced classes** | One class is rare (e.g. 16 % leavers). Accuracy then misleads. |
| **Outlier** | A value far from the rest. It can be an error or a real rare event. |
| **Anomaly** | A rare observation that deviates from normal behaviour. Often what you are looking for. |
| **Categorical / numerical** | Data type: categories (department) versus numbers (income). |
| **Binary target** | A target with exactly two values (yes/no, 0/1). Leads to a classification problem. |
| **Pipeline** | A chain of steps (impute, scale, model) applied identically to train and test data. |

### Data protection terms

| Term | Meaning |
|---|---|
| **DSGVO / GDPR** | Datenschutz-Grundverordnung / General Data Protection Regulation (EU). |
| **BDSG** | Bundesdatenschutzgesetz. German federal data protection act (§26: employee data). |
| **AVV** | Auftragsverarbeitungsvertrag. Data processing agreement between controller and processor (Art. 28 DSGVO). |
| **Verantwortlicher** | Controller. Decides why and how personal data is processed. |
| **Auftragsverarbeiter** | Processor. Processes data on the controller's behalf and instructions. |

---

## 3. The Python toolbox

| Tool | What it does |
|---|---|
| **Python** | The main language for DS. |
| **uv** | Fast modern tool for virtual environments and packages (`uv venv`, `uv pip install`). |
| **Virtual environment (venv)** | Isolated Python install per project so package versions do not clash. |
| **pandas** | Tables ("DataFrames"): load, filter, group, join, clean. Think "Excel/SQL in code". |
| **NumPy** | Fast numerical arrays; pandas is built on it. |
| **matplotlib** | Basic plotting library. |
| **seaborn** | Statistical plots on top of matplotlib (nicer defaults). |
| **scikit-learn** | The standard ML library: models, pipelines, metrics, imputers, train/test split. |
| **XGBoost / LightGBM / CatBoost** | Fast gradient boosting libraries, strong on tabular data. |
| **SHAP** | Explains individual predictions and feature importance. |
| **SciPy / statsmodels** | Statistical tests and classic statistical models. |
| **Jupyter** | Notebooks mixing code, output and text. |
| **jupytext** | Lets you write notebooks as plain `.py` files with `# %%` cell markers (works well in Neovim). |
| **SQLite** | Small file-based SQL database, handy for practice. |
| **Kaggle CLI** | Download datasets from the command line (needs the API token in `~/.kaggle/`, permissions `chmod 600`). |
| **Git** | Version control. |

**Typical project layout**

```
project/
├── data/raw/          # untouched originals, never edited
├── data/processed/    # cleaned data
├── notebooks/         # exploration
├── src/               # reusable code
└── .venv/
```

**First five lines on any new dataset**

```python
import pandas as pd
df = pd.read_csv("data/raw/file.csv")
df.info()                 # columns, types, non-null counts
df.isna().sum()           # missing values per column
df.describe()             # summary statistics of numeric columns
```

`df.info()` and friends print to the console or notebook output; they are not saved anywhere unless you save them.

---

## 4. Statistics essentials

### Describing data

| Measure | Definition | Python |
|---|---|---|
| **Mean** (Mittelwert) | Sum of values divided by their count | `df["x"].mean()` |
| **Median** | Middle value when sorted. Robust against outliers. | `df["x"].median()` |
| **Variance** (Varianz) | Average squared distance from the mean | `df["x"].var()` |
| **Standard deviation** (σ, Standardabweichung) | Square root of variance, same unit as the data | `df["x"].std()` |
| **Quartiles** | Q1 = 25 % mark, Q2 = median, Q3 = 75 % mark | `df["x"].quantile([.25,.5,.75])` |
| **IQR** | Interquartile Range = Q3 − Q1. The spread of the middle 50 %. | `Q3 - Q1` |

**Variance formulas.** Population: divide by `n`. Sample: divide by `n − 1` (corrects the underestimate from using the sample mean). pandas uses `n − 1` by default, NumPy uses `n` by default (`ddof=0`).

### Outlier rules

- **Z-score:** `z = (x − mean) / std`. Flag if `|z| > 3` (a common rule). Assumes roughly normal data and is itself distorted by outliers.
- **IQR rule:** flag values below `Q1 − 1.5·IQR` or above `Q3 + 1.5·IQR`. Robust, no normality assumption.

### Hypothesis testing and p-hacking

- **p-value:** the probability of seeing a result at least this extreme *if there were no real effect*. It is **not** the probability that the result is true.
- **Significance level α:** the threshold, typically 0.05.
- **p-hacking:** testing many things until something is significant, then reporting only that. Run 20 tests and one will look "significant" by chance.
- **Fixes:**
  - **Bonferroni correction:** divide α by the number of tests `m` (strict).
  - **Benjamini-Hochberg:** controls the *False Discovery Rate* (less strict, more power).
  - **Exploratory/confirmatory split:** explore on one part of the data, confirm hypotheses on a separate part (or a new experiment).
  - Pre-register the hypotheses before looking.
- **Winner's curse:** the effects you pick *because* they looked largest are usually overestimated.

### Sample size for comparing two proportions

Rule of thumb per group (80 % power, α = 0.05, two-sided):

```
n ≈ 16 · p(1 − p) / Δ²
```

- `p` = baseline rate, `Δ` = smallest difference worth detecting.
- The 16 comes from `2 · (1.96 + 0.84)² ≈ 15.7`, where **1.96** is the z-value for 95 % confidence (two-sided; `scipy.stats.norm.ppf(0.975)`) and **0.84** is the z-value for 80 % power (`norm.ppf(0.80)`).
- Halving the detectable difference means about four times the sample size.

---

## 5. Data preparation and missing data

### Standard cleaning checklist

- Correct data types (dates as dates, numbers as numbers).
- Duplicates and impossible values (negative age).
- Inconsistent categories ("Berlin", "berlin ", "BER").
- Outliers: decide whether they are errors or real.
- Missing values (below).
- Keep raw data untouched; do all changes in code so they are reproducible.

### Why is a value missing? MCAR, MAR, MNAR

| Type | Meaning | Example | Dropping rows |
|---|---|---|---|
| **MCAR** (Missing Completely At Random) | Chance only; unrelated to any data | Sensor glitch, lost form | Safe, just less data |
| **MAR** (Missing At Random) | Depends on *another observed* column | Older people skip the online question | Biased; impute using the other columns |
| **MNAR** (Missing Not At Random) | Depends on the *missing value itself* | High earners hide income; unhappy staff skip satisfaction | Biased; simple imputing does not fix it |

You can sometimes detect MAR in the data (do rows with gaps differ in other columns?). MNAR can only be argued from domain knowledge.

### What to do about missing values

| Option | When |
|---|---|
| Drop rows (`dropna`) | Few rows (< ~5 %) and gaps look random |
| Drop the column | Mostly empty and not important |
| Impute median (numeric) / most frequent (category) | Simple default; median is robust to outliers |
| Impute using other columns (group-wise, KNN, iterative) | MAR situations |
| Add a missing-indicator column | Missingness itself may be informative (MNAR) |
| Use a model that handles NaN natively (XGBoost, LightGBM) | Tabular data with many gaps |

**Pitfalls**

- Fit the imputer on the **training data only**, then apply it to test data (use a `Pipeline`), otherwise you leak information.
- Never impute the **target**.
- Imputing the mean shrinks variance and can distort correlations.
- `0` is not the same as "unknown".
- Document every choice, and check whether the conclusions change under another choice.

---

## 6. Correlation, causation and cognitive effects

### Core distinctions

- **Correlation:** two variables move together. It says nothing about why.
- **Causation:** changing A actually changes B.
- **Prediction** only needs correlation to hold in the future. **Action** (an intervention) needs causation.

### Why a correlation may not be causal

| Concept | Meaning | Example |
|---|---|---|
| **Confounder** (Konfundierer) | A third factor causing *both* A and B | Season/flu wave drives both staffing shortages and long waits |
| **Mediator** | A link *on the path* from cause to effect (A → M → B) | Higher patient volume carries the effect of the flu wave onto wait times |
| **Moderator** | A factor that changes the *strength* of the effect | Training works better for new hires than for veterans |
| **Reverse causation** | B actually causes A | Hospitals with long waits hire more staff, so "more staff correlates with long waits" |
| **Selective labels** | Outcomes are only observed for those who got the treatment/decision | A loan model only sees repayment for people who were approved |
| **Simpson's paradox** | A trend in the total reverses when you split into groups | Treatment looks worse overall but better within each severity group |
| **Coincidence** | Spurious correlation by chance | Ice cream sales and shark attacks |

**Confounder versus mediator in one line:** a confounder is a *common cause* (control for it), a mediator is *part of the mechanism* (controlling for it hides the effect).

### Methods for causal questions

| Method | Idea |
|---|---|
| **RCT / A/B test** | Randomize who gets the treatment; the gold standard |
| **Difference-in-differences** | Compare the change over time in treated versus untreated groups |
| **Regression discontinuity** | Compare units just above and just below a cutoff |
| **Instrumental variables** | Use a factor that affects treatment but not the outcome directly |
| **Propensity score matching** | Compare treated and untreated units that were similarly likely to be treated |
| **Synthetic control** | Build an artificial comparison unit from a weighted mix of others |
| **Natural experiment** | Exploit a policy change or accident that mimics random assignment |

### Effects and biases to know

| Effect | Short definition |
|---|---|
| **Survivorship bias** | Only looking at what "survived" the selection process |
| **Regression to the mean** | Extreme values tend to be followed by more average ones, without any intervention |
| **Hawthorne effect** | People change behaviour because they know they are observed |
| **Pygmalion / Rosenthal effect** | Higher expectations of someone lead to better performance |
| **Goodhart's law** | When a measure becomes a target, it stops being a good measure |
| **Automation bias** | Over-trusting automated recommendations |
| **Anchoring** | The first number seen biases later judgements |
| **Aggregation hiding effects** | An effect can vanish in the overall average while being strong in a subgroup (see Simpson's paradox) |

**What goes wrong when management reads correlation as cause:** wasted money on levers that do nothing, side effects, gaming of metrics, and unfair decisions about people.

---

## 7. Machine learning basics

### Main learning types

| Type | Definition | Example |
|---|---|---|
| **Supervised learning** | Learn from examples with known answers (labels) | Predict wait time, predict who leaves |
| **Unsupervised learning** | Find structure without labels | Cluster patients into groups |
| **Reinforcement learning** | Learn by trial and reward | Game-playing agents |

Supervised problems split into:

- **Classification:** predict a category (leaves yes/no; binary or multi-class).
- **Regression:** predict a number (wait time in minutes).

*(Note: "regression" is both a problem type and one simple algorithm, linear regression. ML is not "a regression"; regression is one of many ML methods.)*

### Common models

| Model | Idea | Strengths | Weaknesses |
|---|---|---|---|
| **Linear regression** | Fit a straight line/plane to predict a number | Simple, explainable | Only linear relations |
| **Logistic regression** | Linear model that outputs a probability for a class | Good baseline, explainable | Limited to simple patterns |
| **Decision tree** | A sequence of yes/no questions | Easy to read | Overfits easily |
| **Random forest** | Many trees trained independently on random subsets (**bagging**), then averaged | Robust, few tuning needs | Less explainable, slower |
| **Gradient boosting** | Trees built **one after another**, each fitting the *errors (residuals)* of the previous ones | Often best on tabular data | Needs tuning, can overfit |
| **Neural network** | Layers of connected units that learn features automatically | Excels on images, text, sound, huge data | Needs lots of data, hard to explain, tuning-heavy |
| **K-means clustering** | Group points around k centres | Simple unsupervised grouping | Need to choose k |

**Always start with a simple baseline** (logistic or linear regression, or just the average) and require a more complex model to beat it clearly.

### Neural networks in brief

- **Neuron:** computes a weighted sum of its inputs, then applies an **activation function** (e.g. ReLU).
- **Layers:** input layer, **hidden layers** (where the learning of combined features happens), output layer.
- Why add a layer: a single layer can only learn simple boundaries; hidden layers can combine features (the classic XOR example needs a hidden layer).
- **Training:** predict → measure error (loss) → **backpropagation** computes how to adjust each weight → optimizer (e.g. **Adam**) updates the weights → repeat.
- **Early stopping:** stop training when validation error stops improving.
- **No exact rule** like "features² = neurons". Start small (1 to 2 hidden layers, number of neurons somewhere between input and output size), then increase while validation performance improves.
- Typically need much more data than tree-based models; for small tabular data, gradient boosting often wins.

### Tuning

1. Define the metric first (section 8).
2. Split into train / validation / test (or use cross-validation).
3. Search hyperparameters (grid search, random search) using validation data only.
4. Touch the test set **once**, at the very end.
5. Watch the gap between training and validation performance: a big gap means overfitting.

### Training and validation: key terms

*(Worked through in `05_Modellauswahl/05_Notebookpreise_Modell.ipynb` and the day-10 pipeline in `10_MLOPS/`.)*

| Term | Definition |
|---|---|
| **Hold-out** (train/test split, Hold-out-Verfahren) | Set a part of the data aside (typically 20 to 30 %) that is **never used for training or tuning**. After the model is chosen, test it **once** on this part to get an honest estimate of how it performs on new data. |
| **Cross-validation** (Kreuzvalidierung, CV) | Split the training data into `k` parts (folds). Train `k` times, each time on `k − 1` folds, and validate on the remaining one. Every row is used for validation exactly once. Result: `k` scores, reported as **mean** (how good) and **spread** (how stable). |
| **Stratification** (Stratifizierung) | A split that **keeps the class proportions** in every part. With 16 % leavers, each fold has about 16 % leavers, too. Without it, a small split can end up with few or no rare cases. |
| **Data leakage** (Datenleck) | Information the model would **not have at prediction time** flows into training. The result looks too good and fails in operation. |
| **Feature scaling** (Skalierung) | Bringing numeric features to comparable ranges. German "Skalierung" is "feature scaling" in English. Two common types: **standardization** and **normalization** (below). |
| **Reinforcement learning** (bestärkendes Lernen, RL) | A third learning type next to supervised and unsupervised. An **agent** takes **actions** in an **environment**, gets a **reward**, and learns a **policy** that maximizes the total reward over time. There is no labelled correct answer per step. |
| **Regularization** (Regularisierung) | A **penalty on model complexity** that is added to the training loss. It makes the model prefer simpler solutions and so fights overfitting. |
| **Bias** (in the ML sense) | Error from a model that is **too simple or wrongly assumed**: it misses the real pattern in a systematic way (underfitting). |
| **Variance** (in the ML sense) | How strongly the model **changes when the training data changes**. High variance means it fits noise of its particular training set (overfitting). |
| **Early stopping** (frühes Stoppen) | Stop an iterative training process **as soon as the validation error no longer improves**, instead of running a fixed number of rounds. |
| **Oversampling** | Make the rare class larger in the **training data** (copy rows or create synthetic ones). |
| **Undersampling** | Make the common class smaller in the **training data** (remove rows). |

#### Hold-out

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

- `random_state` fixes the shuffle so the split is reproducible.
- **Weakness:** one split depends on luck (maybe the test rows were easy or hard), and with little data the 20 % held back is missing for training.
- **Three parts:** training (learn), validation (compare models, tune hyperparameters), test (final grade, once). Cross-validation replaces the fixed validation part.
- After the test is done, you may refit the final model on **all** the data for use in production (the test only served to judge it).

#### Cross-validation

```python
from sklearn.model_selection import cross_val_score, cross_validate, KFold
cv = KFold(n_splits=5, shuffle=True, random_state=42)
cross_val_score(model, X_train, y_train, cv=cv, scoring="neg_mean_absolute_error")      # one metric
cross_validate(model, X_train, y_train, cv=cv, scoring=("neg_mean_absolute_error", "r2"))  # several metrics, times
```

- **Each run trains a fresh copy** of the model from scratch (`fit` happens inside the function), so your own `model` stays untrained. Fit the final model yourself afterwards.
- **Cost:** `k` times the training time (5 models × 5 folds = 25 trainings).
- sklearn returns errors **negative** ("greater is better"), so put a minus in front.
- **Keep the test set outside:** run CV only on the training part. Otherwise the test rows have already influenced the model choice.
- **Time series:** never shuffle. Use `TimeSeriesSplit` (always validate on the future).
- `cross_val_score` is the short form for one metric, `cross_validate` returns a dictionary (`test_<metric>`, `fit_time`, ...). The "test" in these names means the validation fold, not the real test set.

#### Stratification

```python
train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
from sklearn.model_selection import StratifiedKFold   # use as cv for classification
```

- Important for **imbalanced classes** (fraud 1 %, leavers 16 %).
- For classification only (for a regression target you can stratify on bins of the target).
- sklearn's `cross_val_score` already uses stratified folds for classifiers when you pass `cv=5`.

#### Data leakage

Two typical sources:

| Source | Example | Fix |
|---|---|---|
| **Target leakage:** a feature contains the answer | Yield = annual rent / price. Rent and price **define** the target, so they must not be features. | Ask for every column: "Do I know this at prediction time, and can I compute the target from it?" |
| **Train-test contamination:** test information used in preparation | Scaling or imputing on the full data **before** the split | Split first, fit scalers and imputers on training data only (use a `Pipeline`) |
| **Future information** (time series) | A rolling average that includes days after the cutoff | Use only the past (`shift(1)`), split by time |

Symptom: results that are too good to be true. The model then fails in production.

#### Feature scaling

| Method | Formula | Result | Note |
|---|---|---|---|
| **Standardization** (z-score) | `z = (x − mean) / std` | mean 0, std 1 | The usual default. `StandardScaler`. Two steps: shift the data so the mean is 0, then rescale so the standard deviation is 1. The **shape** of the distribution stays the same (skew and outliers remain). `std` = standard deviation, see section 4. |
| **Normalization** (min-max) | `x' = (x − min) / (max − min)` | range 0 to 1 | Sensitive to outliers. `MinMaxScaler` |
| **Robust scaling** | `(x − median) / IQR` | outliers matter less | `RobustScaler` |

- **Needed** for models based on distances or gradients and for regularized models: k-nearest neighbours, k-means, SVM, neural networks, ridge/lasso. **Not needed** for trees and forests.
- Fit the scaler on the **training data only**, then apply it to test data (in a `Pipeline`).
- Scaling does not change a linear model's accuracy, but makes coefficients comparable.

#### Reinforcement learning

| Part | Meaning | Example: chess program |
|---|---|---|
| **Agent** | The learner that decides | The program |
| **Environment** | What it acts in | The board and opponent |
| **State** | Current situation | Piece positions |
| **Action** | A possible decision | A move |
| **Reward** | Feedback number, often delayed | +1 win, −1 loss at the end |
| **Policy** | The learned rule "state → action" | What to play in which position |

- **Difference from supervised learning:** no correct label per step, only a reward, often much later. The agent must **explore** (try new things) and **exploit** (use what works).
- **Examples:** game agents, robot control, dynamic pricing, recommendation, tuning of language models with human feedback.
- **Weaknesses:** needs very many trials, a simulator or a safe environment, and a carefully designed reward (an agent will exploit loopholes in it, see Goodhart's law in section 6).

#### Regularization

- **L2 (Ridge):** penalizes the sum of squared weights; shrinks all weights toward 0.
- **L1 (Lasso):** penalizes the sum of absolute weights; sets some weights **exactly to 0** (acts as feature selection).
- **Strength is a hyperparameter:** `alpha` in `Ridge`/`Lasso` (larger = stronger), `C` in `LogisticRegression` (inverse: smaller C = stronger).
- **Other forms:** limit tree depth (`max_depth`, `min_samples_leaf`), **dropout** and **weight decay** in neural networks, early stopping.
- Scale features first, otherwise the penalty hits large-scale features unfairly.
- Effect: **more bias, less variance** (see below).

#### Bias and variance

| | High bias | High variance |
|---|---|---|
| Problem | Underfitting: too simple | Overfitting: too flexible |
| Error on training data | high | low |
| Error on validation data | high (similar to training) | much higher than training |
| Example | Straight line through a curved pattern | Decision tree of depth 12 |
| Remedy | More flexible model, better features | More data, simpler model, regularization, averaging (random forest) |

- **Trade-off:** more model flexibility lowers bias but raises variance. The goal is the sweet spot with the lowest error on **unseen** data. Rough decomposition: expected error = bias² + variance + irreducible noise.
- **The word "bias" has several meanings** in this cheatsheet. Do not mix them up:
  - **Model bias** (here): systematic error from an over-simple model.
  - **Mean Error / bias of a forecast** (section 8): average signed error, shows if a forecast is too high or too low.
  - **Bias as unfairness** (section 12): a model that disadvantages groups.
  - **Statistical biases** (section 6): survivorship bias, selection bias, anchoring and similar.
- **Variance** here means "sensitivity to the training data", not the statistical variance of a column (section 4).

#### Early stopping

- Training runs in rounds (epochs in a neural network, trees in boosting). Training error keeps falling, **validation error** falls and then rises again once the model starts to memorize.
- Rule: stop when validation error has not improved for `patience` rounds, and keep the best round.
- sklearn: `GradientBoostingRegressor(n_iter_no_change=10, validation_fraction=0.1)`, `MLPClassifier(early_stopping=True)`. XGBoost/LightGBM: `early_stopping_rounds`.
- Needs its **own validation set**, separate from the test set, otherwise the test set is used for tuning.

#### Oversampling and undersampling

For imbalanced classes (accuracy then misleads, see section 8).

| | Oversampling | Undersampling |
|---|---|---|
| Idea | More rare-class rows | Fewer common-class rows |
| Methods | Random duplication; **SMOTE** (creates synthetic rows between neighbouring rare cases) | Random removal; Tomek links (remove borderline rows) |
| Pro | No information lost | Fast, smaller data |
| Con | Duplicates can cause overfitting | Throws away information |
| Package | `imbalanced-learn` (not installed in the course venv by default) | same |

- **Only on the training data, after the split.** If you resample before splitting, copies of the same row land in both training and test: that is data leakage and inflates the scores. Inside cross-validation use the `imblearn` pipeline so that resampling happens per fold.
- **The test set keeps its real class proportions.** It must reflect reality.
- Resampling distorts predicted probabilities (the model thinks the rare class is more common than it is). Choose the decision threshold on unchanged validation data.
- **Alternatives:** `class_weight="balanced"` (rare errors count more, no data changed), lowering the decision threshold, and metrics that suit rare classes (recall, precision, PR-AUC).

### Explainability

- **Feature importance:** which inputs the model relies on overall.
- **SHAP (SHapley Additive exPlanations):** based on Shapley values from game theory. Splits a single prediction into contributions per feature (each feature's push up or down from the average prediction). Computed *after* training on the final model, not during the build of each tree. TreeSHAP is the fast version for tree models.
- Feature importance shows what the model *uses*, not what *causes* the outcome.

---

## 8. Evaluating models: metrics

A **metric** is a number that compares predictions with the true answers on unseen data.

### Confusion matrix (classification)

|  | Predicted positive | Predicted negative |
|---|---|---|
| **Actually positive** | **TP** true positive | **FN** false negative (missed case) |
| **Actually negative** | **FP** false positive (false alarm) | **TN** true negative |

### Classification metrics

| Metric | Formula | One-liner |
|---|---|---|
| **Accuracy** | (TP + TN) / all | Share of all predictions that were correct. Misleading with imbalanced classes. |
| **Precision** | TP / (TP + FP) | When the model says "positive", how often is it right? |
| **Recall** (sensitivity) | TP / (TP + FN) | Of all real positives, how many did the model find? |
| **F1** | 2·P·R / (P + R) | Harmonic mean of precision and recall; low if either is low. |
| **ROC-AUC** | area under the ROC curve | How well the model ranks positives above negatives across all thresholds. 0.5 = chance, 1.0 = perfect. |
| **PR-AUC** | area under the precision-recall curve | Like ROC-AUC but more informative with rare positives. |
| **Macro-F1** | average of per-class F1 | Multi-class; small classes count equally. |

**Why accuracy fails:** if only 16 % of employees leave, "predict nobody leaves" is 84 % accurate with recall 0.

### Regression metrics

| Metric | Formula (n values, true `y`, predicted `ŷ`) | One-liner |
|---|---|---|
| **MAE** (Mean Absolute Error) | (1/n) · Σ \|y − ŷ\| | Average error in the target's own unit. MAE 6 = off by 6 minutes on average. |
| **RMSE** (Root Mean Squared Error) | √[(1/n) · Σ (y − ŷ)²] | Like MAE but punishes large errors more. |
| **MAPE** (Mean Absolute Percentage Error) | (100/n) · Σ \|(y − ŷ)/y\| | Average error in percent. Breaks down when `y` is near 0. |
| **R²** | 1 − SS_res / SS_tot | Share of the target's variation explained by the model. 1 = perfect, 0 = no better than predicting the mean. |

(`Σ` means "sum over all rows"; `|…|` is the absolute value; `ŷ` is read "y-hat", the prediction.)

#### More regression metrics: which are worth it?

*(Worked through on day 7, `07_Use-Case-Design/07_Loesung_Arbeitsauftrag1und2.md`, section 8; the bias and MedAE discussion is from day 8, `08_Praxis-Use-Cases/08_Loesung_Arbeitsauftrag1und2.md`.)*

Judging a model by MAE and RMSE alone is like judging a car by fuel consumption only. Notation: `yᵢ` = actual value, `ŷᵢ` = prediction (the hat means "estimated"), `eᵢ = yᵢ − ŷᵢ` = error. Here `eᵢ > 0` means the model predicted **too low**, `eᵢ < 0` means **too high**.

The values come from the day-7 exercise (two models, 10 rows each). Model A has even errors (2 or 3). Model B has eight errors of 1 and two errors of 15.

| Metric | Formula | Model A | Model B | When useful |
|---|---|---:|---:|---|
| **MAE** | (1/n) · Σ \|eᵢ\| | 2.40 | 3.80 | Typical error in the **unit** of the data. Every error counts linearly. |
| **RMSE** | √[(1/n) · Σ eᵢ²] | 2.45 | 6.77 | When **big errors are disproportionately costly**. |
| **MAPE** | (100/n) · Σ \|eᵢ\| / \|yᵢ\| | 2.27 % | 6.83 % | Error **in percent**, comparable across data of different size. |
| **WAPE** (weighted MAPE) | Σ \|eᵢ\| / Σ \|yᵢ\| | 2.21 % | 6.73 % | Like MAPE, but **stable with small or zero actuals** (common in demand planning). |
| **sMAPE** (symmetric MAPE) | (100/n) · Σ 2·\|eᵢ\| / (\|yᵢ\| + \|ŷᵢ\|) | 2.27 % | 6.82 % | When over- and under-prediction should be treated alike. |
| **ME** (Mean Error, **bias**) | (1/n) · Σ eᵢ | 0.0 | 0.0 | Is the model **systematically** too high or too low? |
| **MedAE** (median absolute error) | median of \|eᵢ\| | 2 | 1 | **Typical** error, insensitive to outliers. |
| **Max error** | max \|eᵢ\| | 3 | 15 | The **worst single case**. |
| **R²** | 1 − SS_res / SS_tot | 0.96 | 0.25 | What **share of the variation** in `y` does the model explain? (1 = all, 0 = no better than the mean) |

`SS_res = Σ eᵢ²` (sum of squared errors), `SS_tot = Σ (yᵢ − ȳ)²` (sum of squared deviations from the mean `ȳ`).

**How to read the numbers**

- **RMSE ≥ MAE always.** They are equal only if all absolute errors are equal. The **ratio RMSE / MAE** is a diagnostic: near 1 means even errors (Model A: 1.02), clearly above 1 means a few large errors dominate (Model B: 1.78). The maximum is √n.
- Model B's two errors of 15 make up 79 % of its MAE sum but **98 % of its squared-error sum**. Squaring is what makes RMSE react.
- **ME = 0 for both models** because the errors are half positive and half negative and cancel. That is why the plain mean of errors is never used for the *size* of the error. ME still has a job: it shows **direction**.
- Model A and B have different value ranges (about 108 vs. about 57), so their MAEs are not directly comparable. In percent (MAPE/WAPE) A is clearly better.

**MAE, MedAE or RMSE: which one?** Each metric assumes a different cost shape.

| Metric | Assumed cost shape | Reaction to outliers | Answers the question |
|---|---|---|---|
| **MAE** | linear: 20 off costs twice as much as 10 off | every error counts in proportion | What does the error cost on average, bad days included? |
| **MedAE** | none (pure location measure) | outliers ignored | How far off is the model on a **typical** day? |
| **RMSE** | more than linear: 20 off costs four times as much as 10 off | big errors dominate | How bad are the big misses? |

RMSE is **not** always better. Use MAE when costs are roughly linear and the bad days are real. Use MedAE when outliers are noise nobody could predict (till glitch, strike, data entry error). Use RMSE when one big miss is much worse than several small ones. Read them side by side: MAE clearly above MedAE means a good typical day but a few very bad days, so look at those days (data error, or a real costly miss?). Caution: MedAE can make a model look fine that fails badly on a few *important* days (Christmas, main promotion).

**Why ME (bias) on top?** MAE, MedAE and RMSE drop the sign, so they say *how far* but not *in which direction*. Two forecasts can have the same MAE and still be very different:

```
ME = (1/n) · Σ (yᵢ − ŷᵢ)       ME > 0: forecast too low on average
                               ME < 0: forecast too high on average

Actual = 100 on five days
Forecast A: 90, 110, 90, 110, 100   →  MAE = 40/5 = 8,  ME = 0/5 = 0
Forecast B: 92, 92, 92, 92, 92      →  MAE = 40/5 = 8,  ME = 40/5 = +8
```

B is 8 too low every day (always sold out), but MAE shows nothing. Two kinds of error:

| | Systematic error (bias) | Scatter ("restless" model) |
|---|---|---|
| Example | B: always 8 too low | A: sometimes +10, sometimes −10 |
| Visible as | ME ≠ 0 | ME ≈ 0 but MAE > 0 |
| Pattern in the error? | Yes, always the same direction | No |
| Fix | often simple: add a constant (B + 8 = 100) | hard: better features or a better model (shifting A by 8 gives +18 and −2) |

A constant shift only treats the symptom. If the bias comes from the data (e.g. sold-out days understate demand) or varies by weekday, compute the ME per weekday or group and fix the cause. ME = 0 does not mean the model is good, since positive and negative errors cancel: **MAE says how big, ME says which way.**

**MAPE: strengths and traps**

| Trap | Explanation |
|---|---|
| **Actual = 0** | Division by zero, MAPE undefined. A real problem for demand with zero-sales days. |
| **Small actuals** | A small error on a small value becomes a huge percentage and dominates the average. |
| **Asymmetry** | Under-predictions are capped at 100 %, over-predictions are unbounded, so MAPE punishes "too high" more. |
| **No link to cost** | 10 % off on a 1 € item counts the same as 10 % off on a 1,000 € item. |

Remedy: WAPE (sums instead of single ratios) or sMAPE.

**Which metric for which question?**

| Question | Metric |
|---|---|
| How big is the **typical** error in the unit? | **MAE** (plus MedAE) |
| Are **big outliers** especially costly? | **RMSE** |
| Compare **different datasets** or magnitudes? | **MAPE or WAPE** (WAPE when zeros occur) |
| **Systematically** too high or too low? | **ME (bias)** |
| How much of the variation is explained? | **R²** (rule of thumb for the overall picture) |

In practice, show **several metrics together**, at least MAE, RMSE and MAPE. When "too much" and "too little" cost different amounts (stock, orders), use an **asymmetric loss**, e.g. the quantile (pinball) loss: order at the quantile `τ = C_under / (C_under + C_over)` of the forecast, e.g. 1.20 € lost margin vs. 0.30 € waste gives τ = 0.8, so order at the 80 % quantile, slightly above the expected demand.

### Choosing a metric: match the cost of mistakes

**Total cost = FN × C_FN + FP × C_FP**, with C_FN and C_FP the price of each mistake type.

- If FN is expensive (missed leaver, missed tumour) → watch **recall**. Recall is the only classic metric where FN is the only error term.
- If FP is expensive (good mail in spam, false fraud freeze) → watch **precision**.
- If both matter → **F1** or the precision-recall trade-off.
- **Decision threshold rule:** flag a case if its predicted probability `p > C_FP / (C_FP + C_FN)`. With a miss costing 10× a false alarm, the threshold is 1/11 ≈ 9 %, far below the default 50 %.
- Lowering the threshold raises recall and lowers precision. No free lunch.
- Costs come from the client; if unknown, state your assumption and show how conclusions change if the ratio changes (sensitivity analysis).
- Regression: use RMSE if big misses are disproportionately bad, MAE if all errors cost about the same per unit.

---

## 9. Anomaly detection

Goal: find observations that deviate from normal behaviour (fraud, faults, unusual hospital days). Usually very few anomalies, so evaluate with precision, recall and F1, not accuracy.

| Method | Idea | Complexity |
|---|---|---|
| **Z-score** | Flag values more than ~3 standard deviations from the mean | Lowest |
| **IQR rule** | Flag values beyond Q1 − 1.5·IQR or Q3 + 1.5·IQR | Low |
| **Isolation Forest** | Random trees try to isolate points; anomalies are isolated in *few* splits because they are rare and different | Medium; works on many features |
| **Autoencoder** | Neural net compresses and reconstructs normal data; a large **reconstruction error** signals an anomaly | Highest; needs more data |

Rule of thumb: start simple (z-score/IQR for one variable), move to Isolation Forest for many variables, use autoencoders when data and complexity justify it.
An anomaly is a flag to investigate, not automatically an error: check whether it is a data problem or a real event.

---

## 10. Data architecture and cloud

### Storage

| | Data lake | Data warehouse |
|---|---|---|
| Content | Raw data in any format (files, logs, images) | Cleaned, structured, modelled tables |
| Structure applied | When reading (**schema-on-read**) | When writing (**schema-on-write**) |
| Users | Data scientists, engineers | Analysts, BI, management |
| Strength | Flexible, cheap | Fast, reliable, consistent reporting |

### ETL versus ELT

- **ETL:** Extract → **Transform** → Load. Clean data *before* it enters the warehouse. Classic warehouse approach.
- **ELT:** Extract → Load → **Transform**. Load raw data first, transform inside the lake/warehouse. Fits lakes and cloud.

### Batch versus streaming

- **Batch:** process data in chunks on a schedule (nightly). Simpler and cheaper.
- **Streaming:** process events continuously in near real time. More complex and costly; use it only when the decision truly needs speed (fraud alert, bed capacity now).
- Ask: "How fast does the decision need to be made?" before choosing.

### Cloud considerations

- **Stateless servers:** keep no session data on an individual server; store state in a shared place (database or session store) so servers can be added, removed or restarted freely. A **stateful** design (state stuck on one server) blocks scaling.
- **Scaling risks:** costs growing faster than expected, **vendor lock-in** (hard to switch provider), data residency and GDPR (where is the data physically stored?), dependency on provider outages, security misconfiguration.

### Prioritizing which data process to tackle first

Score each candidate on a 1-5 scale and combine, e.g. **Priority = Business impact × Urgency × Risk**.
Define the rubric first (what does a 1 and a 5 mean for each factor, in money, time or legal exposure), otherwise scores are arbitrary. This is analogous to the FMEA risk priority number (RPN) in engineering.

---

## 11. Business side: KPIs, decisions, storytelling

### KPI basics

- A good KPI is measurable, tied to a goal, has an owner, and has a defined calculation and time frame.
- Prefer showing **absolute values with context** (current value, previous value, target) so people see real numbers, not only percentages. Showing a *reduction* (e.g. wait time reduced by X) tells you the effect of an intervention; the raw value alone does not say what changed.

### Leading versus lagging indicators

| | Leading (Frühindikator) | Lagging (Ergebnis-KPI, Spätindikator) |
|---|---|---|
| Looks | Forward | Backward |
| Question | Where are we heading? | What was the result? |
| Can you still act? | Yes | No, it already happened |
| Example (hospital) | Expected patient numbers, staff utilization | Critical wait-time breaches, satisfaction, treated patients |

A leading indicator is only useful if it truly predicts the outcome, which must be checked in the data. Combine both kinds on a dashboard.

### Output, outcome, impact

| Level | Meaning | Hospital example |
|---|---|---|
| **Output** | What was produced or done | Number of forecasts delivered, patients treated |
| **Outcome** | The short- to medium-term change for users | Shorter average waiting time |
| **Impact** | The long-term, strategic effect | Better patient health, lower costs, higher reputation |

### KPI versus OKR

- **KPI:** an ongoing health measure (is the number where it should be?).
- **OKR:** a time-boxed, ambitious goal (Objective) with measurable Key Results. KPIs can serve as Key Results.

### Decision levels

| Level | Time horizon | Example |
|---|---|---|
| **Operative** | Daily / hourly | Shift lead moves a nurse to the emergency room |
| **Taktisch** (tactical) | Weeks to months | Plan next quarter's rosters |
| **Strategisch** (strategic) | Years | Build a new wing, invest in a forecasting system |

### Data-informed versus data-driven

- **Dateninformiert (data-informed):** data is one input; people combine it with experience and context and keep the final say.
- **Datengetrieben (data-driven):** decisions are largely derived from data/automated rules, with humans overseeing exceptions.
- Most organizations should start data-informed, especially where decisions affect people.

### Data storytelling and dashboards

- **Data storytelling:** combine data, visuals and narrative to move an audience to a decision. Structure: context → insight → recommendation → next step.
- **Executive dashboard:** few KPIs (about 4 to 6) on one screen, each with current value, trend (sparkline), and a traffic-light or target comparison; drill-down on click for details; clear definitions in the footer.
- **Management presentation (8 steps):** Executive Summary, Ausgangslage and Handlungsbedarf, Analyse and Erkenntnisse, Handlungsoptionen, Empfehlung, Business Impact, Umsetzung and Governance, Management Decision.
- Lead with the recommendation, not the method.

---

## 12. Data protection (DSGVO / GDPR)

**Key concepts**

- **Personal data:** any information relating to an identifiable person (name, address, IP, customer number combined with other data). **Company data** (a firm, not a person) is generally not personal data.
- **Special categories (Art. 9):** health data, religion, ethnicity, biometrics etc. Strictest rules. Employee sick-leave and hospital data fall here (plus §26 BDSG for employment).
- **Controller versus processor:** the controller decides purposes and means; a processor acts on the controller's instructions and needs an **AVV** (Art. 28).
- **Pseudonymization:** identifiers replaced (e.g. salted hash of name), but re-identification is still possible with extra information, so it is **still personal data**. The key must be kept separately by the controller.
- **Anonymization:** re-identification is practically impossible; then the DSGVO no longer applies. Genuinely hard to achieve.

**Techniques**

- Salted hashing of identifiers (key kept by the controller).
- Geographic masking: aggregate addresses to postcode (PLZ) areas; adding random noise to coordinates reduces precision.
- **k-anonymity:** every combination of identifying attributes occurs for at least k people (a common rule of thumb is k ≥ 5).
- Data minimization: only collect and keep what you need, for as long as you need it.

**Practical points**

- Work on-site or inside the controller's environment, under their authority, with a written AVV.
- Watch for leakage paths: cloud sync, USB sticks, private laptops, sending files to external AI tools.
- The legal question is who determines the purpose, whether a lawful basis exists, and whether processing is documented, not simply whether someone "looks at" the data.
- Anonymized data limits the possible analyses (individual-level and location-level insight shrinks); plan the project question around what is legally and ethically available.
- For employee or HR data, also consider fairness: models can discriminate by gender, age or origin even when those columns are removed (proxies).

*(This is general information, not legal advice. Check specifics with a data protection officer.)*

---

## 13. Project template and checklist

### Example project: employee attrition prediction

- **Data:** Kaggle "IBM HR Analytics Employee Attrition & Performance" (1,470 rows, about 35 features, binary target `Attrition`). It is **synthetic**, say so in your write-up.
- **Business question:** which employees are likely to leave, and what factors matter?
- **Steps:**
  1. Frame the problem: target, who acts on predictions, costs of FN versus FP.
  2. EDA and data quality: class imbalance (about 16 % leavers), correlations, outliers.
  3. Baseline (logistic regression) versus a stronger model (random forest / gradient boosting).
  4. Metrics: recall, precision, F1, PR-AUC; justify with the cost argument.
  5. Explain with SHAP / feature importance.
  6. Discuss prediction versus causation (overtime predicts leaving, but cutting overtime may not prevent it).
  7. Ethics, fairness and DSGVO.
  8. Limitations and recommendations.
- **Encode the target:** `df["Attrition"] = df["Attrition"].map({"Yes": 1, "No": 0})`.

### Pre-flight checklist for any analysis

- [ ] Is the business question clear, and what decision follows?
- [ ] Do I understand every column and how the data was collected?
- [ ] Missing data: what type (MCAR/MAR/MNAR), what treatment, and is it documented?
- [ ] Is there a split between train and test, with no leakage?
- [ ] Is there a simple baseline to beat?
- [ ] Is the metric matched to the cost of mistakes, not just accuracy?
- [ ] Have I looked at subgroups (Simpson's paradox, fairness)?
- [ ] Did I test many things? Correct for multiple comparisons.
- [ ] Correlation or causation: am I recommending an action the data cannot support?
- [ ] Is personal data protected (DSGVO, AVV, minimization)?
- [ ] Is the result explained in business language with a recommendation and its limits?

### Common beginner mistakes

1. Judging a model by accuracy on imbalanced data.
2. Scaling or imputing on the full dataset before splitting (leakage).
3. Treating a feature's importance as proof of cause.
4. Dropping outliers or missing values without asking why they exist.
5. Reporting only the significant results from many tests.
6. Starting with a complex model instead of a baseline.
7. Presenting methods instead of a decision.
