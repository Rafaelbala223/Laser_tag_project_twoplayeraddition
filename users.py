class User:
    rownum: int 
    equipment_ID: int
    user_ID: int
    username: str
    game_score: int
    has_hit_base: bool
    
    # from UserInterface UI get this information in row form
    def __init__(self, rownum, equipment_ID, user_ID, username) -> None:
        self.rownum = rownum
        self.equipment_ID = equipment_ID
        self.user_ID = user_ID
        self.username = username
        self.game_score = 0
        self.has_hit_base = False

    # String representation of User object
    # Print on a single string
    def __str__(self) -> str:
        return f"Username: {self.username}\nEquipment ID: {self.equipment_ID}\nUser ID: {self.user_ID}\nGame Score: {self.game_score}\nHas Hit Base: {self.has_hit_base}\n\n"
    