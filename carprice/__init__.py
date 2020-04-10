import yaml
from carprice.exception import CarException
import os
import sys
import numpy as np
import dill
import pandas as pd
from carprice.constant import *
from urllib import request


def write_yaml_file(file_path: str, data: dict = None):
    """
    Writes a dictionary to a YAML file.
    
    Args:
        file_path (str): Path to the YAML file to be created or updated.
        data (dict): Data to be written to the YAML file.
    """
    try:
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w") as yaml_file:
            if data is not None:
                yaml.dump(data, yaml_file)
    except Exception as e:
        raise CarException(e, sys) from e


def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its contents as a dictionary.
    
    Args:
        file_path (str): Path to the YAML file.
    
    Returns:
        dict: Dictionary containing the contents of the YAML file.
    """
    try:
        with open(file_path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CarException(e, sys) from e


def save_numpy_array(file_path: str, array: np.ndarray):
    """
    Saves a NumPy array to a binary file.
    
    Args:
        file_path (str): Path to the file where the array will be saved.
        array (np.ndarray): NumPy array to save.
    """
    try:
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise CarException(e, sys) from e


def load_numpy_array(file_path: str) -> np.ndarray:
    """
    Loads a NumPy array from a binary file.
    
    Args:
        file_path (str): Path to the file containing the NumPy array.
    
    Returns:
        np.ndarray: Loaded NumPy array.
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CarException(e, sys) from e


def save_object(file_path: str, obj):
    """
    Saves a Python object to a file using `dill`.
    
    Args:
        file_path (str): Path to the file where the object will be saved.
        obj: Python object to save.
    """
    try:
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CarException(e, sys) from e


def load_object(file_path: str):
    """
    Loads a Python object from a file using `dill`.
    
    Args:
        file_path (str): Path to the file containing the object.
    
    Returns:
        object: Loaded Python object.
    """
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CarException(e, sys) from e


def load_data(file_path: str, schema_file_path: str) -> pd.DataFrame:
    """
    Loads and validates a dataset based on a schema.
    
    Args:
        file_path (str): Path to the dataset file.
        schema_file_path (str): Path to the schema file.
    
    Returns:
        pd.DataFrame: Validated dataset as a Pandas DataFrame.
    """
    try:
        # Load the schema
        dataset_schema = read_yaml_file(schema_file_path)
        schema = dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]

        # Load the dataset
        dataframe = pd.read_csv(file_path)

        # Validate columns against the schema
        error_message = ""
        for column in dataframe.columns:
            if column in schema:
                dataframe[column] = dataframe[column].astype(schema[column])
            else:
                error_message += f"\nColumn: [{column}] is not in the schema."

        if error_message:
            raise ValueError(error_message)

        return dataframe

    except Exception as e:
        raise CarException(e, sys) from e


def get_car_list() -> list:
    """
    Fetches a list of unique car names from a remote dataset.
    
    Returns:
        list: List of unique car names.
    """
    try:
        # URL of the dataset
        data_url = ""
        df = pd.read_csv(data_url)
        car_list = list(df["car_name"].unique())
        return car_list
    except Exception as e:
        raise CarException(e, sys) from e