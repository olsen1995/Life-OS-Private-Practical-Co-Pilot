from modes.dayplanner import handle_dayplanner_mode
from modes.fixit import handle_fixit_mode
from modes.fridge_scanner import handle_fridge_scanner_mode
from modes.home_organizer import handle_home_organizer_mode

class ModeRouter:
    def __init__(self):
        self.modes = {
            "DayPlanner": handle_dayplanner_mode,
            "FixIt": handle_fixit_mode,
            "FridgeScanner": handle_fridge_scanner_mode,
            "HomeOrganizer": handle_home_organizer_mode
        }

    def handle_mode(self, mode, input_text):
        if mode in self.modes:
            return self.modes[mode](input_text)
        else:
            return {"error": f"Mode '{mode}' not supported."}
