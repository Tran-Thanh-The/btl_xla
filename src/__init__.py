from flask import Blueprint

IP = Blueprint("ImageProcessing", __name__)

# Import all routes from individual modules
from . import negative, threshold, logarith, gamma, balance, median, weighted_average
from . import knn_average, roberts, sobel, prewitt, laplacian, canny, otsu
