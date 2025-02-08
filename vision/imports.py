import cv2
import time
import numpy as np
from collections import defaultdict
from ultralytics import YOLO
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import pyttsx3
import requests
import ollama