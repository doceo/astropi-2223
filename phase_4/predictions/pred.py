import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX


class SarimaxModel:
    def __init__(self, name):
        self.name = name.split(".csv")[0].lower()
        self.df = pd.read_csv(f"{self.name}.csv").sort_index(ascending=True, axis=0)

    def train(self):
        self.mdl = SARIMAX(
            self.df["Average NDVI"],
            exog=self.df["Year"],
            order=(0, 1, 1),
            enforce_invertibility=False,
            enforce_stationarity=False,
        )

    def predict(self, years):
        results = list(
            self.mdl.fit().predict(
                start=len(self.df.index),
                end=len(self.df.index) + len(years) - 1,
                exog=years,
            )
        )

        for i in zip(years, results):
            self.df.loc[len(self.df)] = i[0], i[1]

    def export(self):
        self.df.to_csv(f"{self.name}_results.csv", index=False)


if __name__ == "__main__":
    for i in ["Blouber", "Leshiba"]:
        mdl = SarimaxModel(i)
        mdl.train()
        mdl.predict(range(2024, 2034))
        mdl.export()
