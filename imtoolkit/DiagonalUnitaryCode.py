# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import itertools
import numpy as np
from .Modulator import *
from .Util import *

class DiagonalUnitaryCode:
    """Diagonal unitary code (DUC). A seminal research can be found in [1].

    [1] B. M. Hochwald and W. Sweldens, ``Differential unitary space-time modulation,'' IEEE Trans. Commun., vol. 48, no. 12, pp. 2041--2052, 2000.

    Args:
        M (int): the number of transmit antennas.
        L (int): the constellation size.
    """

    def __init__(self, M, L):
        self.Nc = L
        self.B = np.log2(L)
        self.codes = np.zeros((L, M, M), dtype=np.complex)
        u = self.getDiversityMaximizingFactors(M, L)
        for l in range(L):
            self.codes[l] = np.diag(np.exp(1j * 2.0 * np.pi / L * u * l))

    def putRate(self):
        print("B = %d [bit/symbol]" % self.B)
    
    def getDiversityMaximizingFactors(self, M, L):
        if M == 1 and L == 4:
        	u = [1]
        elif M == 1 and L == 2:
        	u = [1]
        elif M == 2 and L == 2:
        	u = [1, 1]
        elif M == 2 and L == 4:
        	u = [1, 1]
        elif M == 2 and L == 16:
        	u = [1, 7]
        elif M == 2 and L == 256:
        	# maxp = 0.0988238
        	u = [1, 75]
        elif M == 2 and L == 1024:
        	# maxp = 0.00296903
        	u = [1, 429]
        elif M == 3 and L == 8:
        	u = [1, 1, 3]
        elif M == 3 and L == 64:
        	u = [1, 11, 27]
        elif M == 4 and L == 4:
        	u = [1, 1, 1, 1]
        elif M == 4 and L == 16:
        	u = [1, 3, 5, 7]
        elif M == 4 and L == 256:
        	u = [1, 25, 97, 107]
        elif M == 4 and L == 4096:
        	# maxp = 0.10357
        	u = [1, 575, 1059, 1921]
        elif M == 4 and L == 65536:
        	# maxp = 0.0459484
        	u = [1, 12301, 15259, 29983]
        elif M == 5 and L == 32:
        	u = [1, 5, 7, 9, 11]
        elif M == 5 and L == 1024:
        	u = [1, 157, 283, 415, 487]
        elif M == 8 and L == 16:
        	# maxp = 0.0697013
        	u = [1, 5, 5, 5, 5, 5, 6, 7]
        elif M == 8 and L == 256:
        	# maxp = 0.00532698
        	u = [1, 84, 87, 88, 89, 91, 91, 97]
        elif M == 8 and L == 65536:
        	# maxp = 6.43277e-06
        	u = [1, 16722, 17014, 20852, 22321, 23781, 24192, 29994]
        elif M == 16 and L == 2:
        	# maxp = 1
        	u = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        elif M == 16 and L == 4:
        	# maxp = 0.707107
        	u = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
        elif M == 16 and L == 16:
        	# maxp = 0.545254
        	u = [1, 1, 1, 1, 3, 3, 3, 3, 5, 5, 5, 5, 7, 7, 7, 7]
        elif M == 16 and L == 256:
        	# maxp = 0.387993
        	u = [3, 13, 19, 31, 33, 53, 61, 67, 69, 77, 87, 91, 111, 119, 123, 127]
        elif M == 16 and L == 64:
        	#maxp = 0.510949
        	u = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]
        elif M == 16 and L == 1024:
        	# maxp = 0.000236564
        	u = [1, 223, 258, 278, 305, 320, 322, 347, 356, 359, 362, 362, 362, 386, 394, 403]
        elif M == 16 and L == 2048:
        	# maxp = 0.000117768
        	u = [1, 446, 516, 555, 609, 640, 644, 694, 712, 718, 723, 724, 724, 772, 787, 805]
        elif M == 16 and L == 4096:
        	# maxp = 5.86961e-05
        	u = [1, 892, 1031, 1110, 1217, 1280, 1287, 1388, 1424, 1436, 1445, 1447, 1448, 1543, 1573, 1610]
        elif M == 16 and L == 65536:
        	# maxp = 0.166058
        	u = [3, 1469, 3125, 7251, 8857, 10843, 11229, 13703, 14535, 17301, 17379, 19229, 23447, 24741, 30717, 32767]
        elif M == 64 and L == 128:
        	# maxp = 0.454461
        	u = [2, 3, 3, 3, 3, 3, 3, 5, 5, 7, 9, 13, 13, 13, 13, 13, 15, 17, 17, 19, 19, 21, 23, 23, 25, 25, 27, 27, 27, 27, 29, 29, 29, 31, 31, 31, 35, 35, 35, 37, 37, 41, 41, 43, 43, 43, 45, 45, 45, 47, 49, 49, 49, 51, 53, 55, 55, 57, 59, 61, 63, 63, 63, 63]
        elif M == 64 and L == 256:
        	# maxp = 2.87193e-12
        	u = [1, 12, 26, 26, 27, 29, 30, 31, 32, 42, 47, 50, 50, 53, 54, 54, 56, 57, 57, 58, 61, 62, 64, 66, 68, 68, 68, 69, 69, 71, 76, 77, 78, 79, 79, 80, 80, 81, 82, 84, 86, 88, 89, 90, 90, 90, 90, 93, 95, 96, 97, 98, 102, 104, 105, 105, 106, 110, 111, 116, 120, 122, 122, 125]
        elif M == 256 and L == 1024:
        	# maxp = 8.25184e-57
        	u = [1, 14, 17, 18, 31, 31, 41, 43, 44, 46, 48, 51, 54, 55, 57, 60, 62, 64, 64, 74, 76, 86, 93, 93, 96, 98, 98, 101, 104, 105, 107, 107, 109, 110, 111, 113, 113, 116, 117, 117, 120, 122, 123, 126, 127, 128, 130, 133, 135, 138, 138, 139, 145, 149, 150, 154, 159, 159, 159, 160, 161, 163, 164, 166, 169, 173, 174, 176, 177, 180, 181, 184, 189, 190, 191, 193, 194, 195, 195, 198, 201, 201, 202, 203, 207, 207, 209, 213, 220, 222, 222, 225, 225, 230, 230, 231, 237, 238, 239, 240, 241, 243, 245, 250, 252, 252, 252, 255, 256, 259, 261, 264, 265, 266, 268, 269, 269, 270, 271, 273, 275, 275, 279, 280, 280, 281, 281, 285, 285, 286, 288, 290, 291, 293, 295, 296, 301, 301, 302, 303, 306, 306, 308, 308, 310, 310, 314, 314, 315, 315, 315, 325, 330, 330, 331, 333, 335, 335, 336, 337, 340, 340, 341, 343, 343, 343, 346, 346, 349, 349, 350, 352, 352, 356, 358, 358, 359, 364, 365, 368, 369, 369, 372, 373, 374, 376, 378, 378, 379, 384, 385, 386, 387, 389, 390, 393, 395, 397, 401, 401, 402, 404, 406, 406, 407, 411, 416, 418, 420, 420, 422, 424, 425, 426, 427, 431, 432, 434, 436, 439, 440, 441, 442, 442, 448, 449, 450, 451, 452, 453, 453, 455, 456, 461, 463, 465, 465, 466, 467, 468, 468, 470, 474, 476, 477, 479, 479, 482, 482, 484, 485, 485, 486, 487, 493, 495]
        elif M == 1024 and L == 4096:
        	# maxp = 3.30684e-271
        	u = [1, 18, 22, 22, 25, 29, 33, 35, 40, 40, 42, 50, 51, 52, 57, 57, 67, 67, 67, 75, 76, 78, 78, 80, 85, 87, 89, 94, 94, 95, 99, 100, 101, 101, 105, 115, 116, 118, 118, 119, 119, 121, 137, 139, 141, 141, 141, 143, 155, 158, 160, 162, 163, 166, 168, 174, 176, 178, 181, 181, 188, 189, 189, 190, 190, 194, 196, 196, 197, 199, 200, 204, 210, 214, 215, 216, 219, 222, 225, 226, 226, 232, 233, 235, 237, 238, 238, 239, 240, 241, 244, 245, 247, 251, 252, 252, 255, 260, 261, 263, 263, 266, 270, 270, 272, 273, 273, 276, 276, 278, 286, 288, 293, 303, 305, 310, 313, 313, 315, 315, 315, 316, 318, 318, 318, 319, 319, 322, 326, 327, 329, 329, 330, 330, 331, 332, 334, 337, 337, 338, 338, 339, 343, 346, 346, 347, 354, 355, 355, 357, 357, 359, 363, 363, 363, 366, 369, 379, 382, 391, 397, 400, 401, 404, 405, 406, 407, 408, 408, 409, 410, 411, 416, 416, 419, 419, 421, 421, 423, 430, 430, 431, 431, 432, 432, 432, 435, 435, 439, 440, 441, 443, 445, 445, 445, 447, 448, 451, 451, 452, 453, 456, 460, 465, 465, 466, 466, 467, 469, 474, 476, 477, 478, 479, 487, 488, 489, 491, 493, 496, 497, 499, 503, 504, 505, 508, 509, 510, 514, 516, 518, 518, 518, 519, 525, 526, 527, 529, 530, 534, 541, 541, 542, 543, 543, 544, 547, 548, 550, 550, 554, 555, 561, 564, 569, 572, 572, 574, 576, 578, 578, 579, 583, 583, 587, 592, 594, 596, 609, 616, 622, 623, 624, 630, 633, 634, 635, 637, 642, 646, 649, 651, 651, 653, 662, 663, 666, 667, 668, 671, 672, 674, 674, 676, 676, 682, 684, 685, 685, 687, 687, 688, 698, 699, 704, 708, 709, 710, 711, 715, 716, 716, 717, 718, 718, 723, 724, 724, 725, 726, 727, 729, 730, 736, 739, 743, 744, 744, 745, 748, 749, 751, 755, 761, 761, 762, 762, 766, 769, 771, 776, 778, 778, 779, 780, 780, 783, 787, 788, 789, 790, 792, 792, 793, 793, 794, 795, 795, 795, 796, 796, 799, 801, 803, 803, 804, 807, 807, 814, 815, 822, 822, 824, 824, 825, 835, 836, 837, 837, 838, 844, 844, 846, 847, 847, 849, 850, 850, 854, 855, 857, 857, 862, 863, 867, 869, 869, 870, 875, 876, 876, 882, 883, 884, 885, 886, 888, 890, 892, 893, 894, 895, 897, 901, 905, 908, 909, 909, 911, 911, 916, 918, 918, 921, 922, 923, 927, 928, 932, 938, 940, 940, 945, 946, 946, 948, 949, 949, 951, 957, 958, 959, 962, 963, 965, 965, 969, 971, 979, 981, 983, 984, 986, 990, 992, 995, 997, 997, 998, 1001, 1002, 1003, 1006, 1016, 1021, 1023, 1025, 1026, 1028, 1029, 1031, 1033, 1033, 1036, 1037, 1038, 1039, 1039, 1041, 1041, 1041, 1042, 1042, 1043, 1043, 1044, 1044, 1044, 1051, 1054, 1056, 1060, 1060, 1065, 1065, 1069, 1070, 1073, 1074, 1075, 1078, 1078, 1080, 1081, 1082, 1083, 1084, 1086, 1089, 1089, 1090, 1092, 1097, 1099, 1101, 1101, 1101, 1102, 1104, 1106, 1107, 1114, 1117, 1118, 1118, 1121, 1123, 1124, 1124, 1125, 1126, 1128, 1131, 1133, 1134, 1135, 1135, 1135, 1138, 1145, 1146, 1149, 1150, 1156, 1158, 1158, 1159, 1160, 1161, 1162, 1163, 1168, 1169, 1169, 1171, 1174, 1178, 1179, 1182, 1182, 1183, 1183, 1184, 1188, 1188, 1192, 1194, 1194, 1194, 1197, 1198, 1199, 1201, 1205, 1207, 1208, 1210, 1211, 1212, 1215, 1216, 1217, 1217, 1219, 1219, 1224, 1224, 1224, 1228, 1229, 1233, 1234, 1237, 1237, 1237, 1238, 1242, 1242, 1242, 1245, 1246, 1250, 1251, 1253, 1253, 1253, 1254, 1255, 1255, 1256, 1256, 1257, 1259, 1261, 1262, 1266, 1267, 1268, 1269, 1270, 1272, 1277, 1282, 1283, 1288, 1289, 1291, 1296, 1296, 1296, 1297, 1297, 1298, 1299, 1299, 1302, 1303, 1304, 1305, 1307, 1309, 1312, 1314, 1315, 1316, 1321, 1322, 1326, 1329, 1331, 1331, 1335, 1335, 1336, 1340, 1342, 1342, 1342, 1344, 1344, 1347, 1347, 1354, 1356, 1359, 1362, 1362, 1362, 1363, 1364, 1366, 1367, 1372, 1374, 1376, 1377, 1378, 1380, 1380, 1380, 1384, 1385, 1385, 1386, 1386, 1389, 1390, 1391, 1393, 1393, 1394, 1396, 1397, 1401, 1401, 1406, 1409, 1412, 1415, 1415, 1417, 1421, 1421, 1422, 1423, 1425, 1427, 1428, 1429, 1429, 1432, 1436, 1436, 1437, 1442, 1443, 1445, 1446, 1447, 1448, 1448, 1453, 1455, 1459, 1460, 1460, 1461, 1461, 1463, 1463, 1463, 1464, 1466, 1469, 1474, 1475, 1476, 1476, 1477, 1486, 1486, 1487, 1488, 1488, 1491, 1502, 1504, 1504, 1504, 1505, 1508, 1510, 1512, 1513, 1513, 1516, 1524, 1525, 1528, 1528, 1534, 1536, 1536, 1540, 1542, 1543, 1545, 1545, 1547, 1547, 1551, 1552, 1554, 1554, 1555, 1556, 1557, 1557, 1557, 1559, 1560, 1562, 1562, 1564, 1565, 1565, 1567, 1570, 1572, 1575, 1576, 1581, 1585, 1587, 1588, 1589, 1589, 1591, 1592, 1592, 1594, 1596, 1598, 1601, 1608, 1610, 1612, 1612, 1616, 1618, 1620, 1621, 1624, 1629, 1630, 1631, 1632, 1634, 1635, 1638, 1640, 1640, 1641, 1642, 1643, 1648, 1650, 1654, 1655, 1656, 1664, 1666, 1670, 1674, 1674, 1677, 1678, 1678, 1682, 1683, 1687, 1687, 1688, 1688, 1690, 1691, 1694, 1695, 1699, 1699, 1700, 1702, 1703, 1706, 1707, 1709, 1711, 1712, 1718, 1720, 1722, 1722, 1726, 1727, 1729, 1729, 1730, 1732, 1732, 1734, 1735, 1739, 1740, 1742, 1742, 1743, 1746, 1746, 1747, 1748, 1749, 1750, 1753, 1754, 1762, 1764, 1766, 1767, 1767, 1769, 1770, 1770, 1774, 1776, 1782, 1783, 1785, 1785, 1787, 1792, 1794, 1796, 1806, 1808, 1812, 1813, 1818, 1819, 1821, 1826, 1826, 1833, 1834, 1834, 1836, 1841, 1841, 1841, 1842, 1843, 1845, 1846, 1847, 1850, 1850, 1855, 1859, 1862, 1862, 1863, 1864, 1864, 1864, 1867, 1868, 1872, 1872, 1873, 1875, 1875, 1881, 1887, 1888, 1888, 1890, 1892, 1897, 1898, 1902, 1903, 1904, 1905, 1907, 1910, 1911, 1913, 1913, 1914, 1914, 1915, 1920, 1920, 1923, 1923, 1926, 1927, 1927, 1928, 1930, 1933, 1936, 1940, 1944, 1945, 1946, 1946, 1947, 1948, 1948, 1949, 1951, 1952, 1954, 1957, 1958, 1964, 1965, 1967, 1970, 1972, 1973, 1973, 1982, 1987, 1987, 1987, 1988, 1989, 1993, 1993, 1994, 1996, 1999, 2000, 2001, 2003, 2005, 2006, 2008, 2008, 2011, 2013, 2020, 2024, 2025, 2027, 2030, 2033, 2035, 2038, 2041, 2045, 2046, 2046]
        else:
        	print("DiagonalUnitaryCode.py does not support the given parameters M = %d and L = %d" % (M, L))
        	u = zeros(M)

        return np.array(u)
