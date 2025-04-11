import pandas as pd

import DiverDataProcessor as ddp
from DiverDataProcessor import figures, processing

path_metadata = r"data/metadata.xlsx"
path_baro = r"data/BARO.csv"

start_date = "2024-03-01"
end_date = "2024-06-30"

project_baro = ddp.read_baro_diver(path_baro)
project_baro = project_baro.reindex_time(start_date, end_date)
metadata = pd.read_excel(path_metadata, sheet_name="metadata", index_col="Location_ID")

divers = metadata.index.to_list()

for diver in divers:
    metadata_well = metadata.loc[diver]
    geology_well = pd.read_excel(path_metadata, sheet_name=f"geology_{diver}")

    path_diver = f"data/{diver}.csv"

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

    fig = figures.GeologyGroundwater(observation_well, figsize=(8.27, 11.69 / 2))
    fig.plot_geology(geology, units="m")
    fig.plot_water_level(water_level.resample("d")["water_level (m datum)"], units="m")
