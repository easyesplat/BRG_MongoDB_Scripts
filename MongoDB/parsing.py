import pandas as pd
import math
import re
from insert import process_hurricane_harvey

def parse_hurricane_michael_csv_file(input_file_name: str):
    data = pd.read_csv(input_file_name)
    rows = len(data.index)
    for i in range(1):
        row = pd.Series(data.iloc[i]).to_dict()
        hazard_effect_document = {
            "damage_state": row["status"],
            "date": row["date"],
            "assessment_type": row["assessment_type"],
            "photo": row["all_photos"],
            "photo_caption": row["all_photos_caption"],
            "surveyor_notes": collect_notes([row["general_notes"], row["overall_damage_notes"],
                                            row["structural_notes"], row["wind_damage_details"],
                                            row["water_induced_damage_notes"]]),
            "hazards_present": split_to_array_comma(row["hazards_present"]),
            "wind_damage_rating": row["wind_damage_rating"],
            "surge_damage_rating": row["surge_damage_rating"],
            "rainwater_ingress_damage_rating": row["rainwater_ingress_damage_rating"],
            "roof_structure_damage": row["roof_structure_damage_"],
            "roof_substrate_damage": row["roof_substrate_damage"],
            "roof_cover_damage": row["roof_cover_damage_"],
            "wall_structure_damage": row["wall_structure_damage_"],
            "wall_substrate_damage": row["wall_substrate_damage_"],
            "building_envelope_damage": row["building_envelope_damage_"],
            "wall_fenestration_damage": compute_average_value(row["front_wall_fenestration_damage"], row["left_wall_fenestration_damage"],
                                                              row["right_wall_fenestration_damage"], row["back_wall_fenestration_damage"]),
            "soffit_damage": row["soffit_damage"],
            "fascia_damage": row["fascia_damage_"],
            "stories_with_damage": row["stories_with_damage"],
            "piles_missing_or_collapsed": row["_piles_missing_or_collapsed"],
            "piles_leaning_or_broken": row["_piles_leaning_or_broken"],
            "cause_of_foundation_damage": row["cause_of_foundation_damage"]
        }
        housing_document = {
            "latitude": row['latitude'],
            "longitude": row["longitude"],
            "building_address": row["address_full"],
            "building_type": row["building_type"],
            "number_of_stories": row["number_of_stories"],
            "understory_pct_of_building_footprint": row["understory_pct_of_building_footprint"],
            "elevation_height": row["first_floor_elevation_feet"],
            "year_built": int(row["year_built"]),
            "roof_shape": row["roof_shape"],
            "roof_system": split_to_array(row["roof_system"]),
            "roof_to_wall_attachment": row["r2wall_attachment"],
            "roof_substrate_type": row["roof_substrate_type"],
            "roof_cover": split_to_array(row["roof_cover"]),
            "roof_slope": row["roof_slope"],
            "main_wind_force_resisting_system": split_to_array(row["mwfrs"]),
            "foundation_type": row["foundation_type"],
            "wall_anchorage_type": row["wall_anchorage_type"],
            "wall_structure": row["wall_structure"],
            "wall_substrate": row["wall_substrate"],
            "wall_cladding": row["wall_cladding"],
            "soffit_type": row["soffit_type"],
            "wall_fenestration_ratio": compute_average_value(row["front_wall_fenestration_ratio"], row["front_wall_fenestration_ratio"],
                                                                  row["front_wall_fenestration_ratio"], row["front_wall_fenestration_ratio"]),
            "large_door_present": True if row["large_door_present"] == "yes" else False,
            "large_door_opening_type": group_to_array([row["large_door_opening_type_front"], row["large_door_opening_type_front"],
                                                       row["large_door_opening_type_front"], row["large_door_opening_type_front"]]),
            "secondary_water_barrier": row["secondary_water_barrier"],
            "overhang_length": row["overhang_length"],
            "parapet_height": row["parapet_height_inches"],
            "reroof_year": row["reroof_year"]
        }
        process_hurricane_harvey(housing_document, hazard_effect_document)

def compute_average_value(front, left, right, back):
    fenestration_ratio_sum, count = 0, 0
    if not math.isnan(front):
        fenestration_ratio_sum += front
        count += 1
    if not math.isnan(left):
        fenestration_ratio_sum += left
        count += 1
    if not math.isnan(right):
        fenestration_ratio_sum += right
        count += 1
    if not math.isnan(back):
        fenestration_ratio_sum += back
        count += 1
    return math.nan if count == 0 else fenestration_ratio_sum / count

# Helper function for grouping multiple columns into an array.
def group_to_array(arr):
    ret_arr = []
    for elem in arr:
        if not math.isnan(elem): ret_arr.append(elem)
    return ret_arr

# Helper function to split array csv string into an actual array.
# Ex. "Roof Diaphragm, wood","Wall Diaphragm, wood" -> ["Roof Diaphragm, wood", "Wall Diaphragm, wood"]
def split_to_array(str):
    return re.findall(r'"(.*?)"', str)

# Helper function to split array csv string into an actual array by the comma.
# Ex. "tree, wind" -> ["tree", "wind"]
def split_to_array_comma(str):
    return str.split(',')

def collect_notes(arr):
    ret_str = ""
    for elem in arr:
        if not math.isnan(elem): ret_str += elem
    return math.nan if len(ret_str) == 0 else ret_str


if __name__ == "__main__":
    parse_hurricane_michael_csv_file("../Data/Hurricane_Michael/HM_D2D_Building.csv")