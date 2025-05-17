from super_scad_smooth_profile.SmoothProfile3D import SmoothProfile3D

from super_scad_hole.HoleAlignment import HoleAlignment
from super_scad_hole.HoleCounterdrilled import HoleCounterdrilled


class HoleCountersunk(HoleCounterdrilled):
    """
    Widget for creating countersunk holes.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 height: float,
                 radius: float | None = None,
                 diameter: float | None = None,
                 countersink_radius: float | None = None,
                 countersink_diameter: float | None = None,
                 countersink_angle: float | None = 90.0,
                 countersink_height: float | None = None,
                 alignment: HoleAlignment,
                 profile_top: SmoothProfile3D | None = None,
                 profile_bottom: SmoothProfile3D | None = None,
                 extend_by_eps_top: bool = True,
                 extend_by_eps_bottom: bool = True,
                 extend_by_eps_boundary: bool = False,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 fn4n: bool | None = None):
        """
        Object constructor.

        :param height: The height of the hole.
        :param radius: The radius of the hole.
        :param diameter: The diameter of the hole.
        :param countersink_radius: The radius at the top of the countersink.
        :param countersink_diameter: The diameter at the top of the countersink.
        :param countersink_angle: The angle of the countersink.
        :param countersink_height: The height of the countersink.
        :param alignment: The alignment of the whole relative to the xy-plane.
        :param profile_top: The profile of the top of the hole.
        :param profile_bottom: The profile of the bottom of the hole.
        :param extend_by_eps_top: Whether to extend the top of the hole by eps for a clear overlap.
        :param extend_by_eps_bottom: Whether to extend the bottom of the hole by eps for a clear overlap.
        :param extend_by_eps_boundary: Whether to extend the radius of the hole by eps for a clear overlap.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param fn4n: Whether to create a hole with a multiple of 4 vertices.
        """
        HoleCounterdrilled.__init__(self,
                                    height=height,
                                    radius=radius,
                                    diameter=diameter,
                                    countersink_radius=countersink_radius,
                                    countersink_diameter=countersink_diameter,
                                    countersink_angle=countersink_angle,
                                    countersink_height=countersink_height,
                                    counterdrill_height=0.0,
                                    alignment=alignment,
                                    profile_top=profile_top,
                                    profile_bottom=profile_bottom,
                                    extend_by_eps_top=extend_by_eps_top,
                                    extend_by_eps_bottom=extend_by_eps_bottom,
                                    extend_by_eps_boundary=extend_by_eps_boundary,
                                    fa=fa,
                                    fs=fs,
                                    fn=fn,
                                    fn4n=fn4n)

# ----------------------------------------------------------------------------------------------------------------------
