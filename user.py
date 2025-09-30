from pathlib import Path
from datetime import datetime, date
from typing import Optional, Dict, Tuple, List
import config

class UsrData:
    def __init__(self) -> None:
        self.db_path = Path(config.DB_DIR)
        self.usr_path = self.db_path / config.USR_DIR
        self.workouts_path = self.db_path / config.WORKOUTS_DIR
        self.usr_name_path = self.usr_path / config.NAME_FILE
        self.usr_weight_path = self.usr_path / config.WEIGHT_FILE
        self.usr_goal_weight_path = self.usr_path / config.GOAL_FILE
        self.lifts_path = self.db_path / config.LIFTS_DIR
        
        self.db_path.mkdir(parents=True, exist_ok=True)
        self.usr_path.mkdir(parents=True, exist_ok=True)
        self.workouts_path.mkdir(parents=True, exist_ok=True)
        self.lifts_path.mkdir(parents=True, exist_ok=True)
        
        self.usr_name: str = ""
        self.usr_weight: str = ""
        self.usr_target: str = ""
        
        self.workouts_dic: Dict[str, Path] = {}
        self.workouts = []
        for item in self.workouts_path.iterdir():
            if item.is_file():
                self.workouts_dic[item.stem] = item
                self.workouts.append(item.stem)

        self.lifts_dic:Dict[str, Path] = {}
        self.lifts = []
        for item in self.lifts_path.iterdir():
            if item.is_file():
                self.lifts_dic[item.stem] = item
                self.lifts.append(item.stem)

    
    def validate_weight(self, weight: str) -> Tuple[bool, str]:
        """Validate weight is a number within reasonable bounds"""
        try:
            w = float(weight)
            if config.MIN_WEIGHT <= w <= config.MAX_WEIGHT:
                return True, ""
            else:
                return False, config.MSG_INVALID_WEIGHT
        except (ValueError, TypeError):
            return False, config.MSG_WEIGHT_REQUIRED
    
    def validate_date(self, date_str: str) -> Tuple[bool, str]:
        """Validate date format"""
        try:
            datetime.strptime(date_str, config.DATE_FORMAT)
            return True, ""
        except ValueError:
            return False, config.MSG_INVALID_DATE
    
    def has_weight_for_date(self, date_str: str) -> bool:
        """Check if weight already exists for given date"""
        if not self.usr_weight_path.exists():
            return False
        
        with open(self.usr_weight_path, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        for i in range(1, len(lines), 2):
            if lines[i] == date_str:
                return True
        return False
    
    def need_login(self) -> bool:
        """Check if user needs to login"""
        return not (self.usr_name_path.exists() and 
                   self.usr_weight_path.exists() and 
                   self.usr_goal_weight_path.exists())
    
    def write_usr_name(self, name: str) -> Tuple[bool, str]:
        """Write username to file"""
        if not name.strip():
            return False, config.MSG_NAME_REQUIRED
        
        with open(self.usr_name_path, 'w') as f:
            f.write(name.strip())
        self.usr_name = name.strip()
        return True, ""
    
    def write_usr_weight_first(self, weight: str) -> Tuple[bool, str]:
        """Write initial weight (for first login)"""
        valid, msg = self.validate_weight(weight)
        if not valid:
            return False, msg
        
        date_str = date.today().strftime(config.DATE_FORMAT)
        full_str = f"{weight}\n{date_str}"
        with open(self.usr_weight_path, 'w') as f:
            f.write(full_str)
        self.usr_weight = weight
        return True, ""
    
    def write_usr_weight(self, weight: str, date_str: str = "") -> Tuple[bool, str]:
        """Add new weight entry"""
        valid, msg = self.validate_weight(weight)
        if not valid:
            return False, msg
        
        if not date_str:
            date_str = date.today().strftime(config.DATE_FORMAT)
        
        valid, msg = self.validate_date(date_str)
        if not valid:
            return False, msg
        
        if self.has_weight_for_date(date_str):
            return False, config.MSG_DUPLICATE_DATE
        
        full_str = f"\n{weight}\n{date_str}"
        with open(self.usr_weight_path, 'a') as f:
            f.write(full_str)
        
        self.usr_weight = weight
        return True, config.MSG_WEIGHT_UPDATED
    
    def write_usr_target_weight(self, target: str) -> Tuple[bool, str]:
        """Write target weight"""
        valid, msg = self.validate_weight(target)
        if not valid:
            return False, msg
        
        with open(self.usr_goal_weight_path, 'w') as f:
            f.write(target)
        self.usr_target = target
        return True, ""
    
    def update_weight(self, weight: str, date_str: str = "") -> Tuple[bool, str]:
        """Update weight (single source of truth)"""
        return self.write_usr_weight(weight, date_str)
    
    def get_name(self) -> str:
        """Get username from file"""
        if not self.usr_name_path.exists():
            return ""
        with open(self.usr_name_path, 'r') as f:
            return f.readline().strip()
    
    def get_weight(self) -> str:
        """Get most recent weight"""
        if not self.usr_weight_path.exists():
            return ""
        
        weight = ""
        with open(self.usr_weight_path, 'r') as f:
            count = 0
            for line in f:
                if count % 2 == 0:  
                    weight = line.strip()
                count += 1
        return weight
    
    def get_goal_weight(self) -> str:
        """Get target weight"""
        if not self.usr_goal_weight_path.exists():
            return ""
        with open(self.usr_goal_weight_path, 'r') as f:
            return f.readline().strip()
    
    def get_weight_history(self) -> List[Tuple[str, str]]:
        """Get all weight entries as list of (weight, date) tuples"""
        if not self.usr_weight_path.exists():
            return []
        
        with open(self.usr_weight_path, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        history = []
        for i in range(0, len(lines), 2):
            if i + 1 < len(lines):
                history.append((lines[i], lines[i + 1]))
        return history
    
    def set_starting_vals(self) -> None:
        """Initialize values from files"""
        self.usr_name = self.get_name()
        self.usr_weight = self.get_weight()
        self.usr_target = self.get_goal_weight()
    
    def get_weight_difference(self) -> float:
        """Calculate difference between current and target weight"""
        try:
            return float(self.usr_weight) - float(self.usr_target)
        except (ValueError, TypeError):
            return 0.0


    def write_workout(self,workout:str,lifts:list[str]):
        lifts_str = "\n".join(lifts).strip()
        workout = workout + ".txt"
        f_name = self.workouts_path / workout
        with open(f_name, 'w') as f:
            f.write(lifts_str)

