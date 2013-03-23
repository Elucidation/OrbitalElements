# -*- coding: utf-8 -*-
import numpy as np
from datetime import datetime, timedelta
import pytz
sqrt = np.sqrt
pi = np.pi

# Standard Gravitational parameter in km^3 / s^2 of Earth
GM = 398600.4418

# Values to be set (temporary testing)
semi_major_axis  = -1
eccentricity     = -1
inclination      = -1
argument_perigee = -1
right_ascension  = -1
true_anomaly     = -1

def npa(arr):
    return np.array(arr)

def getInclination(k, ang_momentum_vec):
    return np.arccos(k/h)


elem1 = """ISS (ZARYA)
1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"""

def splitElem(tle):
    "Splits a two line element set into title and it's two lines with stripped lines"
    return map(lambda x: x.strip(), tle.split('\n'))

def checkValid(tle):
    "Checks with checksum to make sure element is valid"
    title, line1, line2 =  splitElem(tle)

    return line1[0] == '1' and line2[0] == '2' and \
           line1[2:7] == line2[2:7] and \
           int(line1[-1]) == doChecksum(line1) and int(line2[-1]) == doChecksum(line2)

def stringScientificNotationToFloat(sn):
    "Specific format is 5 digits, a + or -, and 1 digit, ex: 01234-5 which is 0.01234e-5"
    return 0.00001*float(sn[5]) * 10**int(sn[6:])

def pretty_print(tle):
    "Returns commented information on a two line element"
    title, line1, line2 =  splitElem(tle)
    if not checkValid(tle):
        print "Invalid element."
        return

    satellite_number                                        = int(line1[2:7])
    classification                                          = line1[7:8]
    international_designator_year                           = int(line1[9:11])
    international_designator_launch_number                  = int(line1[11:14])
    international_designator_piece_of_launch                = line1[14:17]
    epoch_year                                              = int(line1[18:20])
    epoch                                                   = float(line1[20:32])
    first_time_derivative_of_the_mean_motion_divided_by_two = float(line1[33:43])
    second_time_derivative_of_mean_motion_divided_by_six    = stringScientificNotationToFloat(line1[44:52])
    bstar_drag_term                                         = stringScientificNotationToFloat(line1[53:61])
    the_number_0                                            = float(line1[62:63])
    element_number                                          = float(line1[64:68])
    checksum1                                               = float(line1[68:69])

    satellite        = int(line2[2:7])
    inclination      = float(line2[8:16])
    right_ascension  = float(line2[17:25])
    eccentricity     = float(line2[26:33]) * 0.0000001
    argument_perigee = float(line2[34:42])
    mean_anomaly     = float(line2[43:51])
    mean_motion      = float(line2[52:63])
    revolution       = float(line2[63:68])
    checksum2        = float(line2[68:69])

    # Inferred Epoch date
    year = 2000 + epoch_year if epoch_year < 70 else 1900 + epoch_year
    epoch_date = datetime(year=year, month=1, day=1, tzinfo=pytz.utc) + timedelta(days=epoch)

    # Inferred period
    day_seconds = 24*60*60
    period = day_seconds * 1./mean_motion

    # Inferred semi-major axis (in km)
    semi_major_axis = (period**2 / (2*pi) * GM)**(1./3)

    print "Satellite number                                          = %g (%s)" % (satellite_number, "Unclassified" if classification == 'U' else "Classified")
    print "International Designator                                  = YR: %02d, LAUNCH #%d, PIECE: %s" % (international_designator_year, international_designator_launch_number, international_designator_piece_of_launch)
    print "Epoch Date                                                = %s  (YR:%02d DAY:%.11g)" % (epoch_date.strftime("%Y-%m-%d %H:%M:%S.%f %Z"), epoch_year, epoch)
    print "First Time Derivative of the Mean Motion divided by two   = %g" % first_time_derivative_of_the_mean_motion_divided_by_two
    print "Second Time Derivative of Mean Motion divided by six      = %g" % second_time_derivative_of_mean_motion_divided_by_six
    print "BSTAR drag term                                           = %g" % bstar_drag_term
    print "The number 0                                              = %g" % the_number_0
    print "Element number                                            = %g" % element_number
    print
    print "Inclination [Degrees]                                     = %g°" % inclination
    print "Right Ascension of the Ascending Node [Degrees]           = %g°" % right_ascension
    print "Eccentricity                                              = %g" % eccentricity
    print "Argument of Perigee [Degrees]                             = %g°" % argument_perigee
    print "Mean Anomaly [Degrees] Anomaly                            = %g°" % mean_anomaly
    print "Mean Motion [Revs per day] Motion                         = %g" % mean_motion
    print "Period                                                    = %ss" % timedelta(seconds=period)
    print "Revolution number at epoch [Revs]                         = %g" % revolution


    print "semi_major_axis = %gkm" % semi_major_axis
    print "eccentricity    = %g" % eccentricity
    print "inclination     = %g°" % inclination
    print "arg_perigee     = %g°" % argument_perigee
    print "right_ascension = %g°" % right_ascension
    print "true_anomaly    = %g°" % true_anomaly

def doChecksum(line):
    """The checksums for each line are calculated by adding the all numerical digits on that line, including the 
       line number. One is added to the checksum for each negative sign (-) on that line. All other non-digit 
       characters are ignored.
       @note this excludes last char for the checksum thats already there."""
    return sum(map(int, filter(lambda c: c >= '0' and c <= '9', line[:-1].replace('-','1')))) % 10


# ang_momentum_vec = npa([1,0,0])
# h = npa([1,0,0])
# print "Inclination: %s" % getInclination(h, ang_momentum_vec)


pretty_print(elem1)

# EOF
