from src.forcasting.preprocessing.NumpyPreprocessor import NumpyPreprocessor
from src.forcasting.model.LinearRegression import LinearRegression


def get_Linear_Regression_pipeline() -> tuple[NumpyPreprocessor, LinearRegression]:
    return NumpyPreprocessor, LinearRegression
