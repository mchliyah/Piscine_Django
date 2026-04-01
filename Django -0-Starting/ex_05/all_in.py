import sys

def find_match(query, states, capitals):
    """
    Finds if a query is a state or a capital and returns the corresponding output string.
    """
    # Clean up the query: remove extra spaces and convert to title case for consistent matching
    normalized_query = ' '.join(query.strip().split()).title()

    # Check if the normalized query is a state name
    if normalized_query in states:
        capital = states[normalized_query]
        return f"{capital} is the capital of {normalized_query}"

    # Check if the normalized query is a capital city name
    if normalized_query in capitals:
        state = capitals[normalized_query]
        return f"{normalized_query} is the capital of {state}"

    # If no match is found
    return f"{query.strip()} is neither a capital city nor a state"

def all_in():
    """
    Main function to process command-line arguments and find state/capital relationships.
    """
    # Check for the correct number of command-line arguments
    if len(sys.argv) != 2:
        return

    # Dictionaries for states and capitals
    states = {
        "Oregon" : "Salem", "Alabama" : "Montgomery", "Alaska" : "Juneau", "Arizona" : "Phoenix",
        "Arkansas" : "Little Rock", "California" : "Sacramento", "Colorado" : "Denver",
        "Connecticut" : "Hartford", "Delaware" : "Dover", "Florida" : "Tallahassee",
        "Georgia" : "Atlanta", "Hawaii" : "Honolulu", "Idaho" : "Boise", "Illinois" : "Springfield",
        "Indiana" : "Indianapolis", "Iowa" : "Des Moines", "Kansas" : "Topeka", "Kentucky" : "Frankfort",
        "Louisiana" : "Baton Rouge", "Maine" : "Augusta", "Maryland" : "Annapolis",
        "Massachusetts" : "Boston", "Michigan" : "Lansing", "Minnesota" : "Saint Paul",
        "Mississippi" : "Jackson", "Missouri" : "Jefferson City", "Montana" : "Helena",
        "Nebraska" : "Lincoln", "Nevada" : "Carson City", "New Hampshire" : "Concord",
        "New Jersey" : "Trenton", "New Mexico" : "Santa Fe", "New York" : "Albany",
        "North Carolina" : "Raleigh", "North Dakota" : "Bismarck", "Ohio" : "Columbus",
        "Oklahoma" : "Oklahoma City", "Pennsylvania" : "Harrisburg", "Rhode Island" : "Providence",
        "South Carolina" : "Columbia", "South Dakota" : "Pierre", "Tennessee" : "Nashville",
        "Texas" : "Austin", "Utah" : "Salt Lake City", "Vermont" : "Montpelier",
        "Virginia" : "Richmond", "Washington" : "Olympia", "West Virginia" : "Charleston",
        "Wisconsin" : "Madison", "Wyoming" : "Cheyenne",
    }
    capitals = {v: k for k, v in states.items()}

    # Split the input string by commas
    queries = sys.argv[1].split(',')

    # Process each query
    for query in queries:
        # Ignore empty strings that result from successive commas or just whitespace
        if not query.strip():
            continue
        
        result = find_match(query, states, capitals)
        print(result)

if __name__ == '__main__':
    all_in()