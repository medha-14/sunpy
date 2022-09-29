"""Yohkoh SXT Map subclass definitions"""

__author__ = "Jack Ireland"
__email__ = "jack.ireland@nasa.gov"


from astropy.visualization import PowerStretch
from astropy.visualization.mpl_normalize import ImageNormalize

from sunpy.map import GenericMap
from sunpy.map.sources.source_type import source_stretch

__all__ = ['SXTMap']


class SXTMap(GenericMap):
    """Yohkoh SXT Image Map

    The Yohkoh Soft X-ray Telescope (SXT) observed the full solar disk
    (42 x 42 arcminutes) in the 0.25 - 4.0 keV range.
    It consisted of a glancing incidence mirror and a CCD sensor and
    used thin metallic filters to acquire images in restricted
    portions of its energy range.
    SXT could resolve features down to 2.5 arcseconds.
    Information about the temperature and density of the plasma
    emitting the observed x-rays was obtained by comparing images acquired with
    the different filters.
    Images could be obtained every 2 to 8 seconds.
    Smaller images with a single filter could be obtained as frequently as
    once every 0.5 seconds.
    Yohkoh was launched on 30 August 1991 and ceased operations on
    14 December 2001.

    References
    ----------
    * `Yohkoh Mission Page <http://solar.physics.montana.edu/sxt/>`_
    * `Fits header reference <http://proba2.oma.be/data/SWAP/level0>`_
    * `Yohkoh Analysis Guide <http://ylstone.physics.montana.edu/ylegacy/yag.html>`_
    """

    def __init__(self, data, header, **kwargs):
        super().__init__(data, header, **kwargs)

        self.plot_settings['cmap'] = 'yohkohsxt' + self.measurement[0:2].lower()
        self.plot_settings['norm'] = ImageNormalize(
            stretch=source_stretch(self.meta, PowerStretch(0.5)), clip=False)

    @property
    def observatory(self):
        return "Yohkoh"

    @property
    def detector(self):
        return "SXT"

    @property
    def measurement(self):
        s = self.meta.get('wavelnth', '')
        if s == 'Al.1':
            s = 'Al01'
        elif s.lower() == 'open':
            s = 'white-light'
        return s

    @property
    def wavelength(self):
        """
        Returns `None`, as SXT is a broadband imager.
        """

    @classmethod
    def is_datasource_for(cls, data, header, **kwargs):
        """Determines if header corresponds to an SXT image"""
        return header.get('instrume') == 'SXT'
