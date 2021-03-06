import os
import pickle
import numpy as np
import xml.etree.ElementTree as ET
import random
import svgwrite
from IPython.display import SVG, display

def get_bounds(data, factor):
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    abs_x = 0
    abs_y = 0
    for i in range(len(data)):
        x = float(data[i,0])/factor
        y = float(data[i,1])/factor
        abs_x += x
        abs_y += y
        min_x = min(min_x, abs_x)
        min_y = min(min_y, abs_y)
        max_x = max(max_x, abs_x)
        max_y = max(max_y, abs_y)

    return (min_x, max_x, min_y, max_y)

# old version, where each path is entire stroke (smaller svg size, but have to keep same color)
def draw_strokes(data, factor=10, svg_filename = 'sample.svg'):
    min_x, max_x, min_y, max_y = get_bounds(data, factor)
    dims = (50 + max_x - min_x, 50 + max_y - min_y)

    dwg = svgwrite.Drawing(svg_filename, size=dims)
    dwg.add(dwg.rect(insert=(0, 0), size=dims,fill='white'))

    lift_pen = 1

    abs_x = 25 - min_x
    abs_y = 25 - min_y
    p = "M%s,%s " % (abs_x, abs_y)

    command = "m"

    for i in range(len(data)):
        if (lift_pen == 1):
            command = "m"
        elif (command != "l"):
            command = "l"
        else:
            command = ""
        x = float(data[i,0])/factor
        y = float(data[i,1])/factor
        lift_pen = data[i, 2]
        p += command+str(x)+","+str(y)+" "

    the_color = "black"
    stroke_width = 1

    dwg.add(dwg.path(p).stroke(the_color,stroke_width).fill("none"))

    dwg.save()
    display(SVG(dwg.tostring()))

def draw_strokes_eos_weighted(stroke, param, factor=10, svg_filename = 'sample_eos.svg'):
    c_data_eos = np.zeros((len(stroke), 3))
    for i in range(len(param)):
        c_data_eos[i, :] = (1-param[i][6][0])*225 # make color gray scale, darker = more likely to eos
    draw_strokes_custom_color(stroke, factor = factor, svg_filename = svg_filename, color_data = c_data_eos, stroke_width = 3)

def draw_strokes_random_color(stroke, factor=10, svg_filename = 'sample_random_color.svg', per_stroke_mode = True):
    c_data = np.array(np.random.rand(len(stroke), 3)*240, dtype=np.uint8)
    if per_stroke_mode:
        switch_color = False
        for i in range(len(stroke)):
            if switch_color == False and i > 0:
                c_data[i] = c_data[i-1]
            if stroke[i, 2] < 1: # same strike
                switch_color = False
            else:
                switch_color = True
    draw_strokes_custom_color(stroke, factor = factor, svg_filename = svg_filename, color_data = c_data, stroke_width = 2)

def draw_strokes_custom_color(data, factor=10, svg_filename = 'test.svg', color_data = None, stroke_width = 1):
    min_x, max_x, min_y, max_y = get_bounds(data, factor)
    dims = (50 + max_x - min_x, 50 + max_y - min_y)

    dwg = svgwrite.Drawing(svg_filename, size=dims)
    dwg.add(dwg.rect(insert=(0, 0), size=dims,fill='white'))

    lift_pen = 1
    abs_x = 25 - min_x
    abs_y = 25 - min_y

    for i in range(len(data)):

        x = float(data[i,0])/factor
        y = float(data[i,1])/factor

        prev_x = abs_x
        prev_y = abs_y

        abs_x += x
        abs_y += y

        if (lift_pen == 1):
            p = "M "+str(abs_x)+","+str(abs_y)+" "
        else:
            p = "M +"+str(prev_x)+","+str(prev_y)+" L "+str(abs_x)+","+str(abs_y)+" "

        lift_pen = data[i, 2]

        the_color = "black"

        if (color_data is not None):
            the_color = "rgb("+str(int(color_data[i, 0]))+","+str(int(color_data[i, 1]))+","+str(int(color_data[i, 2]))+")"

        dwg.add(dwg.path(p).stroke(the_color,stroke_width).fill(the_color))
    dwg.save()
    display(SVG(dwg.tostring()))

    dwg.tostring()


def draw_strokes_pdf(data, param, factor=10, svg_filename = 'sample_pdf.svg'):
    min_x, max_x, min_y, max_y = get_bounds(data, factor)
    dims = (50 + max_x - min_x, 50 + max_y - min_y)

    dwg = svgwrite.Drawing(svg_filename, size=dims)
    dwg.add(dwg.rect(insert=(0, 0), size=dims,fill='white'))

    abs_x = 25 - min_x
    abs_y = 25 - min_y

    num_mixture = len(param[0][0])

    for i in range(len(data)):

        x = float(data[i,0])/factor
        y = float(data[i,1])/factor

        for k in range(num_mixture):
            pi = param[i][0][k]
            if pi > 0.01: # optimisation, ignore pi's less than 1% chance
                mu1 = param[i][1][k]
                mu2 = param[i][2][k]
                s1 = param[i][3][k]
                s2 = param[i][4][k]
                sigma = np.sqrt(s1*s2)
                dwg.add(dwg.circle(center=(abs_x+mu1*factor, abs_y+mu2*factor), r=int(sigma*factor)).fill('red', opacity=pi/(sigma*sigma*factor)))

        prev_x = abs_x
        prev_y = abs_y

        abs_x += x
        abs_y += y


    dwg.save()
    display(SVG(dwg.tostring()))

def vectorization(c, char_dict):
    x = np.zeros((len(c), len(char_dict) + 1), dtype=np.bool)
    for i, c_i in enumerate(c):
        #if char_dict.has_key(c_i):
        if c_i in char_dict:
            x[i, char_dict[c_i]] = 1
        else:
            x[i, 0] = 1
    return x

class IAM():
    '''
        Note: 
            + The return data is point offset rather than absolute coordinates
            + The reason why each sample contain exactly "seq_length" points is because we simply select the first "seq_length" points in 1 sample
    
        Public methods:
            1. __init__
            2. reset_batch_pointer: reset the batch pointer to the start of data
            3. next_batch: return a batch of samples starting from the batch pointer
            4. random_batch: randomly return a batch of samples
        Public members:
            1. data_dir
            2. batch_size
            3. seq_length: the length of points in one sample, e.g., 300
            4. scale_factor: divide every point coordinate by this factor
            5. limit: remove large noisy gaps in the data
            6. chars: set of characters that appear in the data
            7. pointers_per_char
            8. num_batches
            9. char2indices
            10. max_U: max number of characters in one sample
        Private methods:
            1. _preprocess: preprocess iam data and store points and characters information to a pickle file
            2. _load_preprocessed: load the pickle file and build the final data
        
    '''
    # load_data()
    def __init__(self, data_dir, batch_size, seq_length=300, scale_factor = 10,
                 chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ',
                 points_per_char=25, limit = 500):
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.scale_factor = scale_factor # divide data by this factor
        self.limit = limit # removes large noisy gaps in the data
        self.chars = chars
        self.points_per_char = points_per_char

        data_pkl = os.path.join(self.data_dir, "strokes_training_data.cpkl")
        raw_data_dir = self.data_dir+"/lineStrokes"

        if not (os.path.exists(data_pkl)) :
            print("creating training data pkl file from raw source")
            self._preprocess(raw_data_dir, data_pkl)

        self._load_preprocessed(data_pkl)
        self.reset_batch_pointer()

    def reset_batch_pointer(self):
        self.pointer = 0
        
    def next_batch(self):
        '''
            x_batch: the offset from the previous point, except for the first point in a stroke. The offsets are calculated in 1 stroke. (B, seq_length, 3)
            y_batch: shifted version of x_batch # (B, seq_length, 3)
        '''
        x_batch = []
        y_batch = []
        c_vec_batch = []
        c_batch = []
        for i in range(self.batch_size):
            data = self.data[self.pointer]
            x_batch.append(np.copy(data[0:self.seq_length])) # extract the first "seq_length" points
            y_batch.append(np.copy(data[1:self.seq_length + 1]))
            c_vec_batch.append(self.c_vec[self.pointer])
            c_batch.append(self.c[self.pointer])
            
            self.pointer += 1
            if (self.pointer >= len(self.data)):
                self.pointer = 0
                
        return np.asarray(x_batch), np.asarray(y_batch), np.asarray(c_vec_batch), np.asarray(c_batch)

    def random_batch(self):
        '''
            randomly return a batch of samples. (This function does not influence self.pointer)
        '''
        x_batch = []
        y_batch = []
        c_vec_batch = []
        c_batch = []

        pointer = random.randint(0, len(self.data) - 1)
        for i in range(self.batch_size):
            data = self.data[pointer]
            x_batch.append(np.copy(data[0:self.seq_length]))
            y_batch.append(np.copy(data[1:self.seq_length + 1]))
            c_vec_batch.append(self.c_vec[pointer])
            c_batch.append(self.c[pointer])
        return x_batch, y_batch, c_vec_batch, c_batch



        
    def _preprocess(self, raw_data_dir, data_pkl):
        '''
            raw_data_dir: e.g., data/raw/lineStrokes
        '''
        filelist = []
        for dirName, subdirList, fileList in os.walk(raw_data_dir):
            for fname in fileList:
                filelist.append(dirName+"/"+fname)

        # function to read each individual xml file
        def get_strokes(filename):
            tree = ET.parse(filename)
            root = tree.getroot()

            strokes = []

            x_offset = 1e20
            y_offset = 1e20
            y_height = 0
            for i in range(1, 4):
                x_offset = min(x_offset, float(root[0][i].attrib['x']))
                y_offset = min(y_offset, float(root[0][i].attrib['y']))
                y_height = max(y_height, float(root[0][i].attrib['y']))
            y_height -= y_offset
            x_offset -= 100
            y_offset -= 100

            for stroke in root[1].findall('Stroke'):
                points = []
                for point in stroke.findall('Point'):
                    points.append([float(point.attrib['x'])-x_offset,float(point.attrib['y'])-y_offset])
                strokes.append(points)

            return strokes

        # converts a list of arrays into a 2d numpy int16 array
        def convert_strokes_to_array(strokes):

#             n_point = 0
            num_points = sum([len(stroke) for stroke in strokes])
#             for i in range(len(stroke)):
#                 n_point += len(stroke[i])
            stroke_data = np.zeros((num_points, 3), dtype=np.int16)

            prev_x = 0 # corresponds to 1 stroke
            prev_y = 0
            counter = 0

            for j in range(len(strokes)):
                for k in range(len(strokes[j])):
                    stroke_data[counter, 0] = int(strokes[j][k][0]) - prev_x
                    stroke_data[counter, 1] = int(strokes[j][k][1]) - prev_y
                    prev_x = int(strokes[j][k][0])
                    prev_y = int(strokes[j][k][1])
                    stroke_data[counter, 2] = 0
                    if (k == (len(strokes[j])-1)): # end of stroke
                        stroke_data[counter, 2] = 1
                    counter += 1
            return stroke_data

        def find_c_of_xml(filename): # filename: e.g., data/raw/lineStrokes/b07/b07-580/b07-580z-05.xml
            num = int(filename[-6: -4])
            txt = open(filename.replace(raw_data_dir, self.data_dir + '/ascii')[0:-7] + '.txt', 'r').readlines()

            for i, t in enumerate(txt):
                if t[0:4] == 'CSR:':
                    if (i + num + 1 < len(txt)):
                        return txt[i + num + 1][0:-1]
                    else:
                        print("error in " + filename)
                        return None

        # build stroke database of every xml file inside iam database
        strokes = [] # its element represents 1 handwriting image
        c = []

        for i in range(len(filelist)):
            if (filelist[i][-3:] == 'xml'):
                print('processing '+filelist[i])
                c_i = find_c_of_xml(filelist[i])
                if c_i:
                    c.append(c_i)
                    strokes.append(convert_strokes_to_array(get_strokes(filelist[i])))


        #f = open(data_pkl,"wb")
        with open(data_pkl, 'wb') as f:
            pickle.dump((strokes, c), f, protocol=2)
        #f.close()

        
    def _load_preprocessed(self, data_pkl):
        with open(data_pkl, 'rb') as f:
            (self.raw_data, self.raw_c) = pickle.load(f)

        # goes thru the list, and only keeps the text entries that have more than seq_length points
        self.data = []
        self.c = []
        counter = 0
        for i, data in enumerate(self.raw_data): # data: 1 handwriting image
            if len(data) > (self.seq_length + 2) and len(self.raw_c[i]) >= 10:
                # removes large gaps from the data
                data = np.minimum(data, self.limit)
                data = np.maximum(data, -self.limit)
                data = np.array(data,dtype=np.float32)
                data[:,0:2] /= self.scale_factor
                self.data.append(data)
                self.c.append(self.raw_c[i])
                counter += int(len(data)/((self.seq_length+2))) # number of equiv batches this datapoint is worth

#         print("%d strokes available" % len(self.data))
        # minus 1, since we want the ydata to be a shifted version of x data
        self.num_batches = int(counter / self.batch_size)
        self.max_U = int(self.seq_length / self.points_per_char)
        self.char2indices = dict((c, i + 1) for i, c in enumerate(self.chars)) # 0 for unknown
        self.c_vec = []
        for i in range(len(self.c)):
            if len(self.c[i]) >= self.max_U:
                self.c[i] = self.c[i][:self.max_U]
            else:
                self.c[i] = self.c[i] + ' ' * (self.max_U - len(self.c[i]))
            self.c_vec.append(vectorization(self.c[i], self.char2indices))
