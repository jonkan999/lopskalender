def extract_distance(distances, distance_item):
    #ALMOST CORRECT
    if "KM" in distance_item or "km" in distance_item or "k" in distance_item or "K" in distance_item:
        # Split distance_item on " " to separate potential number and distance unit
        parts = distance_item.split()
        for i in range(len(parts)):
            part = parts[i]
            if "," in part or "." in part:
                distance_item = distance_item.split(",")[0] #get first digit if fraction
                distances.append(int(distance_item)*1000)
                break #should not break here, this will cause the loop to only run once when it finds decimals but it should run for all elements
            elif part[-1] in ['k', 'K', 'm', 'M']:
                # Extract the number and multiply it by 1000
                reduced_part = part[:-1].replace(",", "").replace(".", "").replace("km", "").replace("KM", "").replace("K", "").replace("k", "")
                reduced_parts = parts[i-1].replace(",", "").replace(".", "").replace("km", "").replace("KM", "").replace("K", "").replace("k", "")
                if reduced_part.isdigit():
                    distances.append(int(float(reduced_part)*1000))
                elif reduced_parts.isdigit():
                    distances.append(int(float(reduced_parts)*1000))


def test_extract_distance():
    distances = []

    # Test with a single valid distance item
    distance_item = "10km"
    extract_distance(distances, distance_item)
    print(distances)
    assert distances == [10000]
    distances = []
    # Test with multiple valid distance items
    distance_item = "10k 20 km 5K"
    extract_distance(distances, distance_item)
    print(distances)
    assert distances == [10000, 20000, 5000]

    distances = []
    # Test with a valid distance item containing a comma
    distance_item = "7,5 km"
    extract_distance(distances, distance_item)
    print(distances)
    assert distances == [7000]

    distances = []
    # Test with an invalid distance item
    distance_item = "10h"
    extract_distance(distances, distance_item)
    assert distances == []

    distances = []
    # Test with a distance item with a valid unit but no number
    distance_item = "km"
    extract_distance(distances, distance_item)
    assert distances == []

    distances = []
    # Test with an empty distance item
    distance_item = ""
    extract_distance(distances, distance_item)
    assert distances == []

    print("All tests passed!")

if __name__ == "__main__":
    test_extract_distance()
