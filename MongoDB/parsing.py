import pandas as pd
import math
import re
from image_manager import upload_image


def parse_hurricane_michael(row):
    hazard_effect_document = {
        "damage_state": row["status"],
        "date": row["date"],
        "assessment_type": row["assessment_type"],
        "sampling_method": math.nan,
        "photos": process_photos(row["all_photos"], "Hurricane_Michael_Photos"),
        "photos_caption": row["all_photos_caption"],
        "surveyor_notes": collect_notes(
            [
                row["general_notes"],
                row["overall_damage_notes"],
                row["structural_notes"],
                row["wind_damage_details"],
                row["water_induced_damage_notes"],
            ]
        ),
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
        "wall_fenestration_damage": compute_average_value(
            row["front_wall_fenestration_damage"],
            row["left_wall_fenestration_damage"],
            row["right_wall_fenestration_damage"],
            row["back_wall_fenestration_damage"],
        ),
        "soffit_damage": row["soffit_damage"],
        "fascia_damage": row["fascia_damage_"],
        "stories_with_damage": parse_stories_with_damage(row["stories_with_damage"]),
        "piles_missing_or_collapsed": row["_piles_missing_or_collapsed"],
        "piles_leaning_or_broken": row["_piles_leaning_or_broken"],
        "cause_of_foundation_damage": row["cause_of_foundation_damage"],
        "damaged_windows_percentage": math.nan,
        "damaged_doors_percentage": math.nan,
    }
    building_specific_document = {
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "building_address": row["address_full"],
        "building_type": row["building_type"],
        "number_of_stories": row["number_of_stories"],
        "understory_pct_of_building_footprint": row[
            "understory_pct_of_building_footprint"
        ],
        "elevation_height": row["first_floor_elevation_feet"],
        "year_built": convert_to_int(row["year_built"]),
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
        "wall_substrate": split_to_array(row["wall_substrate"]),
        "wall_cladding": split_to_array_comma(row["wall_cladding"]),
        "soffit_type": row["soffit_type"],
        "wall_fenestration_ratio": compute_average_value(
            row["front_wall_fenestration_ratio"],
            row["back_wall_fenestration_ratio"],
            row["left_wall_fenestration_ratio"],
            row["right_wall_fenestration_ratio"],
        ),
        "large_door_present": True if row["large_door_present"] == "yes" else False,
        "large_door_opening_type": group_to_array(
            [
                row["large_door_opening_type_front"],
                row["large_door_opening_type_back"],
                row["large_door_opening_type_left"],
                row["large_door_opening_type_right"],
            ]
        ),
        "secondary_water_barrier": row["secondary_water_barrier"],
        "overhang_length": row["overhang_length"],
        "parapet_height": row["parapet_height_inches"],
        "reroof_year": row["reroof_year"],
    }
    return hazard_effect_document, building_specific_document


def parse_hurricane_laura(row):
    hazard_effect_document = {
        "damage_state": row["status"],
        "date": row["date"],
        "assessment_type": row["assessment_type"],
        "sampling_method": row["sampling_method"],
        "photos": process_photos(
            row["overall_photos_front_left_right_back"], "Hurricane_Laura_Photos"
        ),
        "photos_caption": row["overall_photos_front_left_right_back_caption"],
        "surveyor_notes": collect_notes(
            [
                row["general_notes"],
                row["overall_damage_notes"],
                row["attribute_notes"],
                row["structural_notes"],
                row["wind_damage_details"],
                row["water_induced_damage_notes"],
            ]
        ),
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
        "wall_fenestration_damage": math.nan,
        "soffit_damage": row["soffit_damage"],
        "fascia_damage": row["fascia_damage_"],
        "stories_with_damage": parse_stories_with_damage(row["stories_with_damage"]),
        "piles_missing_or_collapsed": row["_piles_missing_or_collapsed"],
        "piles_leaning_or_broken": row["_piles_leaning_or_broken"],
        "cause_of_foundation_damage": row["cause_of_foundation_damage"],
        "damaged_windows_percentage": row["_damaged_windows"],
        "damaged_doors_percentage": row["_damaged_doors"],
    }
    building_specific_document = {
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "building_address": row["address_full"],
        "building_type": row["building_type"],
        "number_of_stories": row["number_of_stories"],
        "understory_pct_of_building_footprint": row[
            "understory_pct_of_building_footprint"
        ],
        "elevation_height": row["first_floor_elevation_feet"],
        "year_built": convert_to_int(row["year_built"]),
        "roof_shape": row["roof_shape"],
        "roof_system": split_to_array(row["roof_system"]),
        "roof_to_wall_attachment": row["r2wall_attachment"],
        "roof_substrate_type": row["roof_substrate_type"],
        "roof_cover": split_to_array(row["roof_cover"]),
        "roof_slope": row["roof_slope"],
        "main_wind_force_resisting_system": math.nan,
        "foundation_type": row["foundation_type"],
        "wall_anchorage_type": row["wall_anchorage_type"],
        "wall_structure": math.nan,
        "wall_substrate": split_to_array(row["wall_substrate"]),
        "wall_cladding": split_to_array_comma(row["wall_cladding"]),
        "soffit_type": row["soffit_type"],
        "wall_fenestration_ratio": math.nan,
        "large_door_present": True if row["large_door_present"] == "yes" else False,
        "large_door_opening_type": row["large_door_opening_type_"],
        "secondary_water_barrier": row["secondary_water_barrier"],
        "overhang_length": row["overhang_length"],
        "parapet_height": row["parapet_height_inches"],
        "reroof_year": row["reroof_year"],
    }
    return hazard_effect_document, building_specific_document


def parse_hurricane_harvey(row):
    hazard_effect_document = {
        "damage_state": int(row["total_damage_rating"][0]),
        "date": row["date_of_survey"],
        "assessment_type": math.nan,
        "sampling_method": math.nan,
        "photos": process_photos(row["photos"], "Hurricane_Harvey_Photos"),
        "photos_caption": row["photos_caption"],
        "surveyor_notes": collect_notes([row["notes"]]),
        "hazards_present": math.nan,
        "wind_damage_rating": math.nan,
        "surge_damage_rating": math.nan,
        "rainwater_ingress_damage_rating": math.nan,
        "roof_structure_damage": row["roof_structure_damage_"],
        "roof_substrate_damage": row["roof_substrate_damage"],
        "roof_cover_damage": row["roof_cover_damage_"],
        "wall_structure_damage": row["wall_structure_damage_"],
        "wall_substrate_damage": row["wall_substrate_damage_"],
        "building_envelope_damage": math.nan,
        "wall_fenestration_damage": math.nan,
        "soffit_damage": math.nan,
        "fascia_damage": math.nan,
        "stories_with_damage": math.nan,
        "piles_missing_or_collapsed": math.nan,
        "piles_leaning_or_broken": math.nan,
        "cause_of_foundation_damage": row["cause_of_foundation_damage"],
        "damaged_windows_percentage": row["_damaged_windows"],
        "damaged_doors_percentage": math.nan,
    }
    building_specific_document = {
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "building_address": row["address_full"],
        "building_type": row["building_type"],
        "number_of_stories": row["number_of_stories"],
        "understory_pct_of_building_footprint": math.nan,
        "elevation_height": row["first_floor_elevation_feet"],
        "year_built": convert_to_int(row["year_built"]),
        "roof_shape": row["roof_shape"],
        "roof_system": split_to_array(row["roof_system"]),
        "roof_to_wall_attachment": math.nan,
        "roof_substrate_type": math.nan,
        "roof_cover": split_to_array(row["roof_cover"]),
        "roof_slope": math.nan,
        "main_wind_force_resisting_system": math.nan,
        "foundation_type": math.nan,
        "wall_anchorage_type": math.nan,
        "wall_structure": row["wall_structure"],
        "wall_substrate": math.nan,
        "wall_cladding": split_to_array_comma(row["wall_cladding"]),
        "soffit_type": math.nan,
        "wall_fenestration_ratio": math.nan,
        "large_door_present": math.nan,
        "large_door_opening_type": math.nan,
        "secondary_water_barrier": math.nan,
        "overhang_length": math.nan,
        "parapet_height": math.nan,
        "reroof_year": math.nan,
    }
    return hazard_effect_document, building_specific_document


def parse_hurricane_dorian(row):
    hazard_effect_document = {
        "damage_state": math.nan,
        "date": row["date"],
        "assessment_type": row["assessment_type"],
        "sampling_method": math.nan,
        "photos": process_photos(row["all_photos"], "Hurricane_Dorian_Photos"),
        "photos_caption": math.nan,
        "surveyor_notes": collect_notes(
            [
                row["general_notes"],
                row["overall_damage_notes"],
                row["structural_notes"],
                row["wind_damage_details"],
                row["water_induced_damage_notes"],
            ]
        ),
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
        "wall_fenestration_damage": compute_average_value(
            row["front_wall_fenestration_damage"],
            row["left_wall_fenestration_damage"],
            row["right_wall_fenestration_damage"],
            row["back_wall_fenestration_damage"],
        ),
        "soffit_damage": row["soffit_damage"],
        "fascia_damage": row["fascia_damage_"],
        "stories_with_damage": parse_stories_with_damage(row["stories_with_damage"]),
        "piles_missing_or_collapsed": row["_piles_missing_or_collapsed"],
        "piles_leaning_or_broken": row["_piles_leaning_or_broken"],
        "cause_of_foundation_damage": row["cause_of_foundation_damage"],
        "damaged_windows_percentage": math.nan,
        "damaged_doors_percentage": math.nan,
    }
    building_specific_document = {
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "building_address": process_missing_address(
            row["address_sub_thoroughfare"],
            row["address_thoroughfare"],
            row["address_suite"],
            row["address_locality"],
            row["address_sub_admin_area"],
            row["address_admin_area"],
            row["address_postal_code"],
            row["address_country"],
        ),
        "building_type": row["building_type"],
        "number_of_stories": row["number_of_stories"],
        "understory_pct_of_building_footprint": row[
            "understory_pct_of_building_footprint"
        ],
        "elevation_height": row["first_floor_elevation_feet"],
        "year_built": convert_to_int(row["year_built"]),
        "roof_shape": row["roof_shape"],
        "roof_system": math.nan,
        "roof_to_wall_attachment": math.nan,
        "roof_substrate_type": math.nan,
        "roof_cover": math.nan,
        "roof_slope": row["roof_slope"],
        "main_wind_force_resisting_system": split_to_array(row["mwfrs"]),
        "foundation_type": row["foundation_type"],
        "wall_anchorage_type": row["wall_anchorage_type"],
        "wall_structure": row["wall_structure"],
        "wall_substrate": split_to_array(row["wall_substrate"]),
        "wall_cladding": split_to_array_comma(row["wall_cladding"]),
        "soffit_type": row["soffit_type"],
        "wall_fenestration_ratio": compute_average_value(
            row["front_wall_fenestration_ratio"],
            row["back_wall_fenestration_ratio"],
            row["left_wall_fenestration_ratio"],
            row["right_wall_fenestration_ratio"],
        ),
        "large_door_present": True if row["large_door_present"] == "yes" else False,
        "large_door_opening_type": group_to_array(
            [
                row["large_door_opening_type_front"],
                row["large_door_opening_type_back"],
                row["large_door_opening_type_left"],
                row["large_door_opening_type_right"],
            ]
        ),
        "secondary_water_barrier": row["secondary_water_barrier"],
        "overhang_length": row["overhang_length"],
        "parapet_height": row["parapet_height_inches"],
        "reroof_year": row["reroof_year"],
    }
    print(hazard_effect_document["surveyor_notes"])
    return hazard_effect_document, building_specific_document


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


# Helper function to convert float values to int. Checks for any NaN values.
def convert_to_int(value):
    if math.isnan(value):
        return value
    return int(value)


# Helper function for grouping multiple columns into an array.
def group_to_array(arr):
    ret_arr = []
    for elem in arr:
        if not isinstance(elem, str) and math.isnan(elem):
            continue
        ret_arr.append(elem)
    return ret_arr


# Helper function to split array csv string into an actual array.
# Ex. "Roof Diaphragm, wood","Wall Diaphragm, wood" -> ["Roof Diaphragm, wood", "Wall Diaphragm, wood"]
def split_to_array(elem):
    if not isinstance(elem, str) and math.isnan(elem):
        return elem
    return re.findall(r'"(.*?)"', elem)


# Helper function to split array csv string into an actual array by the comma.
# Ex. "tree, wind" -> ["tree", "wind"]
def split_to_array_comma(elem):
    if not isinstance(elem, str) and math.isnan(elem):
        return elem
    return elem.split(",")


def parse_stories_with_damage(elem):
    if isinstance(elem, str):
        try:
            split_arr = split_to_array_comma(elem)
            ret_arr = [int(x) for x in split_arr]
            return ret_arr
        except:
            try:
                split_arr = elem.split(" and ")
                ret_arr = [int(x) for x in split_arr]
                return ret_arr
            except:
                return []
    if math.isnan(elem):
        return []
    if isinstance(elem, int):
        return [elem]


def collect_notes(arr):
    ret_str = ""
    for elem in arr:
        if not isinstance(elem, str) and math.isnan(elem):
            continue
        ret_str += str(elem)
    return math.nan if len(ret_str) == 0 else ret_str


def process_photos(photo_str, photo_path):
    if not isinstance(photo_str, str) and math.isnan(photo_str):
        return photo_str
    image_ids = []
    photo_ids = photo_str.split(",")
    for photo_id in photo_ids:
        image_id = upload_image(photo_id, photo_path)
        if image_id:
            image_ids.append(image_id)
    return image_ids


def process_missing_address(
    address_sub_thoroughfare,
    address_thoroughfare,
    address_suite,
    address_locality,
    address_sub_admin_area,
    address_admin_area,
    address_postal_code,
    address_country,
):
    full_address = ""
    if isinstance(address_sub_thoroughfare, str):
        full_address += address_sub_thoroughfare
    if isinstance(address_thoroughfare, str):
        full_address += address_thoroughfare
    if isinstance(address_suite, str):
        full_address += address_suite
    if isinstance(address_locality, str):
        full_address += address_locality
    if isinstance(address_sub_admin_area, str):
        full_address += address_sub_thoroughfare
    if isinstance(address_admin_area, str):
        full_address += address_admin_area
    if isinstance(address_postal_code, str):
        full_address += address_postal_code
    if isinstance(address_country, str):
        full_address += address_country
    return full_address
