import pandas as pd


class PandasQuerySetMixin:
    def to_pandas(self, *values):
        return pd.DataFrame(list(self.values_list(*values, named=True)))
