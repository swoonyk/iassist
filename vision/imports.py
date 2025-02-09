import cv2
import time
import numpy as np
from collections import defaultdict
import os
from ultralytics import YOLO
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import requests
import re
import ollama
from collections import deque
from ultralytics.utils.plotting import Annotator, colors
import os
from groq import Groq
from dotenv import load_dotenv
