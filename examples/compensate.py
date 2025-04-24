import pandas as pd
from pathlib import Path

import DiverDataProcessor as ddp
from DiverDataProcessor import figures, processing

projectdir = Path(r"c:\repos\DiverDataProcessor\tmp")

path_metadata = projectdir.joinpath("data", "metadata.xlsx")
path_baro = projectdir.joinpath("data", "BARO.CSV")
path_divers = projectdir.joinpath("data", 'diver_data')

start_date = "2024-03-01"
end_date = "2024-06-30"

project_baro = ddp.read_baro_diver(path_baro)
project_baro = project_baro.reindex_time(start_date, end_date)
metadata = pd.read_excel(path_metadata, sheet_name="metadata", index_col="Location_ID")

divers = metadata.index.to_list()

for diver in divers:
    metadata_well = metadata.loc[diver]
    geology_well = pd.read_excel(path_metadata, sheet_name=f"geology_{diver}")

    path_diver = next(path_divers.glob(f"*{metadata_well.name}*.CSV"), None)

    diver = ddp.read_td_diver(path_diver)
    diver = diver.reindex_time(start_date, end_date)

    observation_well = ddp.ObservationWell(
        name=metadata_well["Name"],
        diver_code=metadata_well["Div_code"],
        surface_level=metadata_well["Elevation_m"],
        top_well_to_sl=metadata_well["top_of_well_to_sl_cm"] / 100,
        well_depth=metadata_well["well_depth_cm"] / 100,
        cable_length=metadata_well["cable_length_cm"] / 100,
    )

    geology = ddp.Geology(
        tops=geology_well["top (cm-sl)"].values / 100,
        bottoms=geology_well["bottom (cm-sl)"].values / 100,
        lithology=geology_well["lithology"].str.replace(" ", "_").values,
        surface_level=metadata_well["Elevation_m"],
    )

    water_level = processing.baro_compensate(
        project_baro,
        diver,
        None,
        observation_well,
        method="cable",
    )

    path_csv = projectdir.joinpath(f"exports/{metadata_well.name}.csv")
    water_level.data.to_csv(path_csv) # output in meters +datum

    fig = figures.GeologyGroundwater(observation_well, figsize=(8.27, 11.69 / 2))
    fig.plot_geology(geology, units="m")
    fig.plot_water_level(water_level.resample("d")["water_level (m datum)"], units="m")
