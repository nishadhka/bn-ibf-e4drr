import netCDF4 as nc
from pprint import pprint

def describe_nc_file(path):
    ds = nc.Dataset(path)

    print("metadata dict:")
    pprint(ds.__dict__)

    print("\ndimensions:")
    for dim in ds.dimensions.values():
        print(dim.name, dim.size)

    print("\nvariables:")
    for var in ds.variables.values():
        print(var)
        print()

if __name__ == "__main__":
    def main(num):
        id_to_path = {
            1: "disasters-dataset.csv",
            2: "ecmwf_dataset.nc",
            3: "extreme_value_dataset.nc",
            4: "gefs_dataset.nc",
            5: "geosfm_dataset.csv",
            6: "imerg_dataset.nc",
            7: "impact_dataset.nc",
            8: "population_dataset.nc",
            9: "rfev2_dataset.nc",
            10: "road_dataset.nc",
            11: "verification_dataset.nc"
        }
        print(id_to_path[num], ":")
        describe_nc_file("data/" + id_to_path[num])

    main(3)