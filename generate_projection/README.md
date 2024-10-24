# Purpose

Scripts in this folder is to read raw TIGRESS-NCR output to create phase-separated metallicity projection files.

# Example
Run on stellar for model in `/projects/EOSTRIKER`

```sh
salloc -N1 -n96 --kill-command=SIGTERM --time=0:30:00 ./run.sh R8_8pc_NCR.full.b10.v3.iCR4.Zg1.Zd1.xy2048.eps0.0
```

# Output
Outputs will be stored under `basedir/Zprj` in the form of `xarray.Dataset`
