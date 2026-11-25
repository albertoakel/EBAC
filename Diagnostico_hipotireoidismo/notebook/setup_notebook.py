from pathlib import Path
import sys
import warnings


NOTEBOOK_DIR = Path.cwd().resolve()


if NOTEBOOK_DIR.name.lower() == "notebook":
    PROJECT_ROOT = NOTEBOOK_DIR.parent
else:
    PROJECT_ROOT = NOTEBOOK_DIR

SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

## importações
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# sklearnmodels
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    make_scorer, precision_score, recall_score, f1_score,
    average_precision_score, roc_auc_score,
    classification_report, ConfusionMatrixDisplay)
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

from xgboost import XGBClassifier
from scipy.stats import chi2_contingency, fisher_exact
from scipy.stats.contingency import association
import warnings
warnings.filterwarnings("ignore")

from utils import (
    color_palette21,color_palette41,
    inital_describe,
    bar_bar_cat,
    mult_plt2,cor_N)

from ml_utils import importancia_permutacao_cv
