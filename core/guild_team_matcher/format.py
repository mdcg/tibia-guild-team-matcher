def format_possible_teams(possible_teams):
    """From a list containing all possible teams, we formatted the information
    to facilitate the final presentation.

    Args:
        possible_teams (list): List with all possible teams formed.

    Returns:
        str: Text containing all possible teams with a better presentation.
    """
    possible_teams_text = ""
    for members in possible_teams:
        possible_teams_text += " | ".join([str(p) for p in members])
        possible_teams_text += "\n"

    return possible_teams_text
