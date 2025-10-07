import numpy as np
from eigsep_terrain.marjum_dem import MarjumDEM as DEM

class Image:
    def __init__(self, pathname, label, lat, lon, alt, roll, heading=None, 
                 angle_up=None, hor_weight=None, ver_weight=None, dis_weight=None) -> None:
        '''
        constructor for image class

        parameters
        ----------
        pathname : str
            path to image
        label : str
            name for image
        lat : float
            latitude the photo was taken at
        lon : float
            longitude the photo was taken at
        alt : float
            altitude the photo was taken at [m]
        roll : float
            degrees
        heading : float, optional
            degrees from north the camera was facing
            north as 0° (or 360°), east as 90°, south as 180°, and west as 270°
        angle_up : float, optional
            angle above the horizontal the camera was pointed [deg]
        hor_weight : float, optional
            indicates accuracy of the crosshair along the vertical axis,
            equal to 1/antentta's nonzero distance in pixels from vertical bar
            (ie: higher hor_weight means more accurate)
        ver_weight : float, optional
            indicates accuracy of the crosshair along the horizontal axis,
            equal to 1/antentta's nonzero distance in pixels from horizontal bar
            (ie: higher ver_weight means more accurate)
        dis_weight : float, optional
            indicates accuracy of the photo based on distance to the antenna,
            equal to area the antenna takes up on the screen in pixels^2
            (ie: higher dis_weight means more accurate)
        '''
        
        self.photo = pathname
        self.label = label
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.heading = heading
        self.angle_up = angle_up
        self.ver_weight = ver_weight
        self.hor_weight = hor_weight
        self.dis_weight = dis_weight
        self.roll = roll

    def check_valid_position(self, lat=None, lon=None, alt=None) -> bool:
        '''
        checks if a position on the canyon is valid (ie: not falling off a cliff, 
        entombed in stone, or other such unfortunate places to be taking a photo)
        via comparison to terrain maps.
        default paramters are the image's attributes but optional other parameters can be passed in

        parameters
        ----------
        lat : float, optional
            latitude the photo was taken at
        lon : float, optional
            longitude the photo was taken at
        alt : float, optional
            altitude the photo was taken at

        returns
        ----------
        valid : bool
            True if the position is valid, False if not
        '''

        # use the lat and lon to find the correct altitude and see if the given alt is acceptable (+- 5m)
        if not lat:
            lat = self.lat
        if not lon:
            lon = self.lon
        if not alt:
            alt = self.alt

        assert lat is not None
        assert lon is not None
        assert alt is not None

        # lla to emu
        enus = DEM.latlon_to_enu(lat, lon, alt)

        # correct alt
        interped_alt = DEM.interp_alt(**enus)
        acceptable_offset = 10 #m

        return interped_alt - acceptable_offset < alt < interped_alt + acceptable_offset
    
    def open(self) -> None:
        '''
        function to open the photo
        TODO: think about use cases, maybe healpy related or something
        '''
        pass
