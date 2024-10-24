# Purpose

Scripts in this folder is to read raw TIGRESS-NCR output to create phase-separated metallicity projection files.

# Requirements

Besides usual packages, you will need [`xarray`](https://docs.xarray.dev/en/stable/) and `netCDF4`, which can be installed via `conda`

```sh
conda install -c conda-forge xarray netCDF4
```

or via `pip`

```sh
python -m pip install xarray
```

see https://docs.xarray.dev/en/stable/getting-started-guide/installing.html

# Data
A few selected snapshots are located at `example_data/` in this repository (every 50 snapshots). Full data is available at this URL (to be updated).

The example data is from Model `R8-b10-Z1.0` presented in [Kim et al. (2024)](https://ui.adsabs.harvard.edu/abs/2024ApJ...972...67K).
