
import os
from pathlib import Path
import json
from datetime import datetime

BASE_PATH = Path(os.getcwd())
DATA_FOLDER_PATH = BASE_PATH / "data"
RESULT_PATH = DATA_FOLDER_PATH / "result.json"

class FileService:

    default_result = {
                "app": {
                    "name": "Advanced Topics in Database Systems ~ Midterm Project ",
                    "description": "This SE 308 course project simulates database transactions using two user types (A for updates, B for reads) and analyzes their performance. We develop a program to run concurrent simulations with varying numbers of users, measuring execution times and deadlocks under different transaction isolation levels and with or without indexes on specific tables.", 
                    "class_code": "SE 308 01",
                    "authors": [
                        "Fatih Bahadir",
                        "Orkun Kurul"
                    ],
                    "created_at": "16/05/2024"
                },
                "saves": {}
            }
    
    @classmethod
    def save_result(cls, data: dict):

        for key, val in data.items():
            print(key, "*", val, "*", type(val))
        
        if not cls._check_params(data):
            print("Save Result Param Error")
            return

        cls._create_file_if_not_exist(RESULT_PATH)

        result = cls._read_result_file(RESULT_PATH)

        result["saves"][cls._get_curr_date()] = {
                "params": {
                    "transaction_level": data["transaction_level"],
                    "has_index": data["has_index"],
                    "num_of_a_users": data["num_of_a_users"],
                    "num_of_b_users": data["num_of_b_users"]
                },
                "result": {
                    "a_deadlock": data["a_deadlock"],
                    "b_deadlock": data["b_deadlock"],
                    "a_average": data["a_average"],
                    "b_average": data["b_average"]
                }
        }

        cls._save_result_file(RESULT_PATH, result)

    @classmethod
    def _create_file_if_not_exist(cls, path: Path):
        
        if (os.path.exists(path)):
            return

        folder_path = path.parent
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        cls._save_result_file(RESULT_PATH, cls.default_result)

    @staticmethod
    def _check_params(data: dict):

        keys = ["transaction_level", "has_index", "num_of_a_users", "num_of_b_users",
                "a_deadlock", "b_deadlock", "a_average", "b_average"]
        
        is_matching = True
        for key in keys:
            if key not in data:
                is_matching = False
                if not is_matching: break
        return is_matching

    @staticmethod
    def _read_result_file(save_result: Path):

        with open(save_result, "r") as f:
            data = json.load(f)
        return data
    
    @staticmethod
    def _save_result_file(save_result: Path, data: dict):

        with open(save_result, "w") as f:
            json.dump(data, f, indent=4)
    
    @staticmethod
    def _get_curr_date() -> str:
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")