import pyathena as pa
from pyathena.tigress_ncr.phase import assign_phase

import sys
import os
import xarray as xr

from mpi4py import MPI

if __name__ == "__main__":
    COMM = MPI.COMM_WORLD

    if len(sys.argv) == 1:
        raise ("Provide full path to the model directory")

    basedir = sys.argv[1]
    print(basedir)

    sim = pa.LoadSimTIGRESSNCR(basedir)
    dname = os.path.join(sim.savdir, "Zprj")
    os.makedirs(dname, exist_ok=True)

    mynums = []
    for i, num in enumerate(sim.nums):
        if (i % COMM.size) == COMM.rank:
            mynums.append(num)

    for num in mynums:
        print(f"rank {COMM.rank}: {num}")
        fname = os.path.join(dname, f"{sim.basename}.{num:04d}.Zprj.nc")
        if os.path.isfile(fname):
            os.remove(fname)

        ds = sim.load_vtk(num)
        data = ds.get_field(
            ["nH", "T", "xHI", "xH2", "xHII", "xe", "specific_scalar[0]", "ne"]
        )
        data = data.rename({"specific_scalar[0]": "Z"})
        phase = assign_phase(sim, data, kind="five2")

        Z_proj_EM = dict()
        Z_proj_rho = dict()
        for i, ph in enumerate(phase.attrs["phlist"]):
            EM = (phase == i) * data["ne"] ** 2
            rho = (phase == i) * data["nH"]
            # EM weighted mean Z
            Z_proj_EM[ph] = (EM * data["Z"]).sum(dim="z") / 0.02 / EM.sum(dim="z")
            # density weighted mean Z
            Z_proj_rho[ph] = (rho * data["Z"]).sum(dim="z") / 0.02 / rho.sum(dim="z")

        EM = data["ne"] ** 2
        rho = data["nH"]
        # EM weighted mean Z
        Z_proj_EM["all"] = (EM * data["Z"]).sum(dim="z") / 0.02 / EM.sum(dim="z")
        # density weighted mean Z
        Z_proj_rho["all"] = (rho * data["Z"]).sum(dim="z") / 0.02 / rho.sum(dim="z")

        dset = xr.Dataset()
        for Z_proj in [Z_proj_EM, Z_proj_rho]:
            dset["EM"] = xr.Dataset(Z_proj).to_array("phase")
            dset["rho"] = xr.Dataset(Z_proj).to_array("phase")
        dset.to_netcdf(fname)
