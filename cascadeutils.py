import os

def generate_negative_description_file():
    # open the output file for writing. will overwrite all existing data in there
    with open('neg.txt', 'w') as f:
        # loop over all the filenames
        for filename in os.listdir('negative'):
            f.write('negative/' + filename + '\n')
#  positive images
# D:\Programing\opencv-3.4.11\opencv\build\x64\vc15\bin
if "__main__" == __name__:
    generate_negative_description_file()


# D:/Programing/opencv-3.4.11/opencv/build/x64/vc15/bin/opencv_annotation.exe --annotations=pos.txt --images=positive/
# D:/Programing/opencv-3.4.11/opencv/build/x64/vc15/bin/opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 1000 -vec pos.vec
# D:/Programing/opencv-3.4.11/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -w 24 -h 24 -numPos 30 -numNeg 15 -numStages 5 

# press "c" to conferm
# press "d" to undo
# press "esc" to exit