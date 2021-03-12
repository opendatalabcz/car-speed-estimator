import cv2
import argparse
from src.carSpeedEstimator import *

parser = argparse.ArgumentParser(description="Car speed estimation")
parser.add_argument('video', type=str, help="Video adress")
parser.add_argument('-sfp', '--sline_first_point', type=int, nargs=2,
                    required= True,  help="First point for starting line")
parser.add_argument('-ssp', '--sline_second_point', type=int, nargs=2,
                    help="Second points for starting line")
parser.add_argument('-efp', '--eline_first_point', type=int, nargs=2,
                    required=True, help="First point for end line")
parser.add_argument('-esp', '--eline_second_point', type=int, nargs=2,
                    required=True, help="Second point for end line")
parser.add_argument('-l', '--length', type=int, required=True, help="Real length between line in meters")
args = parser.parse_args()

if __name__ == '__main__':
    start_line = [tuple(args.sline_first_point), tuple(args.sline_second_point)]
    end_line = [tuple(args.eline_first_point), tuple(args.eline_second_point)]
    cap = cv2.VideoCapture(args.video)
    test = CarSpeedEstimator(cap, start_line, end_line, args.length)
    test.run()


#first_line = [(330, 100), (550, 100)]
#second_line = [(300, 150), (600, 150)]
#cap = cv2.VideoCapture("Data/my_traffic.mp4")
#test = CarSpeedEstimator(cap, first_line, second_line, 10)
#test.run()


