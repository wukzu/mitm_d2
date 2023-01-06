import json

cells_game = [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,                    0,      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,                   28,  14, 1,         -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,                  56,  42,  29,  15, 2,       -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,                 84,  70,  57,  43,  30,  16, 3,           -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,                112, 98,  85,  71,  58,  44,  31,  17,  4,           -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,               140, 126, 113, 99,  86,  72,  59,  45,  32,  18,  5,             -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,              168, 154, 141, 127, 114, 100, 87,  73,  60,  46,  33,  19,  6,             -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,             196, 182, 169, 155, 142, 128, 115, 101, 88,  74,  61,  47,  34,  20,  7,           -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,            224, 210, 197, 183, 170, 156, 143, 129, 116, 102, 89,  75,  62,  48,  35,  21,  8,           -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,           252, 238, 225, 211, 198, 184, 171, 157, 144, 130, 117, 103, 90,  76,  63,  49,  36,  22,  9,              -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1,          280, 266, 253, 239, 226, 212, 199, 185, 172, 158, 145, 131, 118, 104, 91,  77,  64,  50,  37,  23,  10,               -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1,         308, 294, 281, 267, 254, 240, 227, 213, 200, 186, 173, 159, 146, 132, 119, 105, 92,  78,  65,  51,  38,  24,  11,            -1, -1],
        [-1, -1, -1, -1, -1, -1, -1,        336, 322, 309, 295, 282, 268, 255, 241, 228, 214, 201, 187, 174, 160, 147, 133, 120, 106, 93,  79,  66,  52,  39,  25,  12,           -1],
        [-1, -1, -1, -1, -1, -1,       364, 350, 337, 323, 310, 296, 283, 269, 256, 242, 229, 215, 202, 188, 175, 161, 148, 134, 121, 107, 94,  80,  67,  53,  40,  26,  13            ],
        [-1, -1, -1, -1, -1,      392, 378, 365, 351, 338, 324, 311, 297, 284, 270, 257, 243, 230, 216, 203, 189, 176, 162, 149, 135, 122, 108, 95,  81,  68,  54,  41,  27            ],
        [-1, -1, -1, -1,     420, 406, 393, 379, 366, 352, 339, 325, 312, 298, 285, 271, 258, 244, 231, 217, 204, 190, 177, 163, 150, 136, 123, 109, 96,  82,  69,  55,           -1],
        [-1, -1, -1,    448, 434, 421, 407, 394, 380, 367, 353, 340, 326, 313, 299, 286, 272, 259, 245, 232, 218, 205, 191, 178, 164, 151, 137, 124, 110, 97,  83,            -1, -1],
        [-1, -1,   476, 462, 449, 435, 422, 408, 395, 381, 368, 354, 341, 327, 314, 300, 287, 273, 260, 246, 233, 219, 206, 192, 179, 165, 152, 138, 125, 111,          -1, -1, -1],
        [-1,  504, 490, 477, 463, 450, 436, 423, 409, 396, 382, 369, 355, 342, 328, 315, 301, 288, 274, 261, 247, 234, 220, 207, 193, 180, 166, 153, 139,            -1, -1, -1, -1],
        [532, 518, 505, 491, 478, 464, 451, 437, 424, 410, 397, 383, 370, 356, 343, 329, 316, 302, 289, 275, 262, 248, 235, 221, 208, 194, 181, 167,                 -1, -1, -1, -1, -1],
        [546, 533, 519, 506, 492, 479, 465, 452, 438, 425, 411, 398, 384, 371, 357, 344, 330, 317, 303, 290, 276, 263, 249, 236, 222, 209, 195,              -1, -1, -1, -1, -1, -1],
        [-1,  547, 534, 520, 507, 493, 480, 466, 453, 439, 426, 412, 399, 385, 372, 358, 345, 331, 318, 304, 291, 277, 264, 250, 237, 223,                -1,                -1, -1, -1, -1, -1, -1],
        [-1, -1,   548, 535, 521, 508, 494, 481, 467, 454, 440, 427, 413, 400, 386, 373, 359, 346, 332, 319, 305, 292, 278, 265, 251,                 -1,             -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1,    549, 536, 522, 509, 495, 482, 468, 455, 441, 428, 414, 401, 387, 374, 360, 347, 333, 320, 306, 293, 279,               -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1,     550, 537, 523, 510, 496, 483, 469, 456, 442, 429, 415, 402, 388, 375, 361, 348, 334, 321, 307,              -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1,      551, 538, 524, 511, 497, 484, 470, 457, 443, 430, 416, 403, 389, 376, 362, 349, 335,               -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1,       552, 539, 525, 512, 498, 485, 471, 458, 444, 431, 417, 404, 390, 377, 363,                 -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1,        553, 540, 526, 513, 499, 486, 472, 459, 445, 432, 418, 405, 391,                -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1,         554, 541, 527, 514, 500, 487, 473, 460, 446, 433, 419,                 -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1,          555, 542, 528, 515, 501, 488, 474, 461, 447,               -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,           556, 543, 529, 516, 502, 489, 475,                     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,            557, 544, 530, 517, 503,               -1,               -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,             558, 545, 531,                 -1,              -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,              559,                    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    ]

# f = open('C:\\Users\\llegay\\Desktop\\pydofus\\PyDofus\\input\\20972289.json')
# data = json.load(f)

# fightNonWalkable = []
# fightNonMov = []

# movLine = []
# result = []

# print(len(data['cells']))
# i = 0
# count = 0
# for cell in data['cells']:
#     print('i :', str(i))
#     #if cell['nonWalkableDuringFight'] == False:
#     #    fightNonWalkable.append(i)
#     if cell['los'] == False:
#         fightNonMov.append(i)
#         movLine.append('X')
#     else:
#         movLine.append('.')
    
#     if count == 13:
#         result.append(movLine)
#         movLine = []
#         count = 0
#     i = i + 1
#     count = count + 1


#print(len(fightNonWalkable))


import json
def openJsonMap(mapId):
    i = 0
    dp = 0
    while dp < 6:
        while i < 10:
            try:
                print("trying " +str(dp) + " - " + str(i))
                file = open("C:/Users/33630/Desktop/mitm/mitm_d2/sources/data/maps/maps" + str(dp) + ".d2p/" + str(i) + "/" + str(mapId) + ".json")
                data = json.load(file)
                return data
                break
            except IOError:
                pass
            i = i + 1
        dp = dp + 1
        i = 0

  
result = openJsonMap(188745222)

mapDataCell = result['cells']

print('zergre')
print(mapDataCell[308])
print(mapDataCell[57]['mov'])

line = []
wallLine = []
cells = []
wallCells = []
cellIndex = 0
for cellLine in cells_game:
    for cellId in cellLine:
        if cellId != -1:
            # no nwalkable (walls)
            if mapDataCell[cellId]['mov'] == False or mapDataCell[cellId]['nonWalkableDuringFight'] == True or mapDataCell[cellId]['los'] == False:
                line.append('X')
                if mapDataCell[cellId]['los'] == False:
                    wallLine.append('X')
                else:
                    wallLine.append('0')
            else:
                line.append('0')
                wallLine.append('0')

            cellIndex = cellIndex + 1
        else:
            line.append('-')
            wallLine.append('-')
    cells.append(line)
    wallCells.append(wallLine)
    line = []
    wallLine = []

for cell in wallCells:
    print(cell)