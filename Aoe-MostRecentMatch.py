import requests
from datetime import datetime

# Timestamp to date
def convert_timestamp_to_date(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Civ Mapping (might change with new civs DLC)

civ_list = {
    0: "Armenians", 1: "Aztecs", 2: "Bengalis", 3: "Berbers", 4: "Bohemians",
    5: "Britons", 6: "Bulgarians", 7: "Burgundians", 8: "Burmese", 9: "Byzantines",
    10: "Celts", 11: "Chinese", 12: "Cumans", 13: "Dravidians", 14: "Ethiopians",
    15: "Franks", 16: "Georgians", 17: "Goths", 18: "Gurjaras", 19: "Huns",
    20: "Incas", 21: "Hindustanis", 22: "Italians", 23: "Japanese", 24: "Khmer",
    25: "Koreans", 26: "Lithuanians", 27: "Magyars", 28: "Malay", 29: "Malians",
    30: "Mayans", 31: "Mongols", 32: "Persians", 33: "Poles", 34: "Portuguese",
    35: "Romans", 36: "Saracens", 37: "Sicilians", 38: "Slavs", 39: "Spanish",
    40: "Tatars", 41: "Teutons", 42: "Turks", 43: "Vietnamese", 44: "Vikings",
    45: "Shu", 46: "Wei", 47: "Wu", 48: "Jurchens", 49: "Khitans",
    50: "Achaemenids", 51: "Athenians", 52: "Spartans", 
    53: "Macedonians", 54: "Thracians", 55: "Puru"
}

# Prompt user to choose between /steam/ and /xboxlive/
print("Choose the player's ID:")
print("1. Steam ID")
print("2. Xbox Live ID")
platform_choice = input("Enter the number of your choice: ")

# Validate user input
while platform_choice not in ['1', '2']:
    print("Invalid choice. Please enter either '1' for Steam or '2' for Xbox Live.")
    platform_choice = input("Enter the number of your choice: ")

# Set platform based on user choice
if platform_choice == '1':
    platform = 'steam'
else:
    platform = 'xboxlive'

# Prompt user for the player's ID
playerid = input("Type in the player's ID: ")

# API
URL = f"https://aoe-api.worldsedgelink.com/community/leaderboard/getRecentMatchHistory?title=age2&profile_names=[%22/{platform}/{playerid}%22]"
TIMEOUT = 10


# Get data
try:
    response = requests.get(URL, timeout=10)
    player_data = response.json()

    # Check if 'matchHistoryStats' key is present
    if 'matchHistoryStats' in player_data:
        # Process the matches
        matches = player_data['matchHistoryStats']

        profiles = player_data['profiles']
        profile_id_to_alias = {profile['profile_id']: profile['alias'] for profile in profiles}

        # Convert timestamp to date
        for match in matches:
            match['startgametime'] = convert_timestamp_to_date(match['startgametime'])

        # Keep only the most recent match
        most_recent_match = max(matches, key=lambda x: x['startgametime'])
        matches = [most_recent_match]

        # Extract player information
        player_info = []
        for match in matches:
            for member in match['matchhistorymember']:
                profile_id = member['profile_id']
                alias = profile_id_to_alias.get(profile_id, f"Unknown Alias for {profile_id}")
                player_info.append({
                    'alias': alias,
                    'name': member['profile_id'],
                    'civ': member['civilization_id'],
                    'elo': member['oldrating'],
                    'team': member['teamid']
                })

        # Replace civ numbers with civ names
        for player in player_info:
            player['civ'] = civ_list.get(player['civ'], "Unknown")

        # Group player information by team
        grouped_by_team = {}

        for player in player_info:
            team_id = player['team']
            if team_id not in grouped_by_team:
                grouped_by_team[team_id] = []
            grouped_by_team[team_id].append(player)

        # Print date and map
        print(f"\n==========================\nDate: {most_recent_match['startgametime']} \nMap: {most_recent_match['mapname']}\n")

        # Sort team ids
        sorted_team_ids = sorted(grouped_by_team.keys())

        # Print player information grouped by team
        for team_id in sorted_team_ids:
            players = grouped_by_team[team_id]
            print(f"Team {team_id+1}")
            for player in players:
                print(f"{player['alias']} ({player['elo']}) - {player['civ']}")
            print()
    else:
        print(f"No matches found for Steam ID: {playerid}")

except requests.RequestException as e:
    print(f"Request failed: {e}")
except KeyError:
    print(f"Invalid response format. No 'matchHistoryStats' key found. No matches for Steam ID: {playerid}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")












