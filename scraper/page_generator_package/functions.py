def map_distance(distance, race_type, distance_mapping, distance_units):
    if isinstance(distance, str):
        return distance_mapping.get(distance, distance) # If distance is not in the mapping, return the original value
    elif isinstance(distance, list):
        return [map_distance(d, race_type, distance_mapping, distance_units) for d in distance] # Recursively map each distance in the list
    elif isinstance(distance, (int, float)):
        if race_type == 'track':
            for unit in distance_units:
                if unit['range'][0] <= distance <= unit['range'][1]:
                    return f"{int(distance)} {unit['label']}"
            return f"{int(distance)} meter"
        else:
            distance = distance / 1000
            for unit in distance_units:
                if unit['range'][0] <= distance <= unit['range'][1]:
                    return f"{unit['label']}"
            return f"{int(distance)} km"