from typing import Any, Dict, List

from super_scad.boolean.Difference import Difference
from super_scad.boolean.Union import Union
from super_scad.d2.Circle import Circle
from super_scad.d2.Rectangle import Rectangle
from super_scad.d3.LinearExtrude import LinearExtrude
from super_scad.d3.RotateExtrude import RotateExtrude
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Flip2D import Flip2D
from super_scad.transformation.Rotate3D import Rotate3D
from super_scad.transformation.Translate2D import Translate2D
from super_scad.transformation.Translate3D import Translate3D
from super_scad.util.Radius2Sides4n import Radius2Sides4n
from super_scad_smooth_profile.Rough import Rough
from super_scad_smooth_profile.SmoothProfile3D import SmoothProfile3D
from super_scad_smooth_profile.SmoothProfileParams import SmoothProfileParams

from super_scad_hole.Hole import Hole
from super_scad_hole.HoleAlignment import HoleAlignment


class HoleSlotted(Hole):
    """
    Widget for creating slotted holes.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 height: float,
                 radius: float | None = None,
                 diameter: float | None = None,
                 overall_length: float | None = None,
                 center_to_center: float | None = None,
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
        :param overall_length: The overall length of the hole.
        :param center_to_center: The distance between two centers of the two circles of the hole.
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
        Hole.__init__(self,
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

        self._height: float | None = height
        """
        The height of the hole.
        """

        self._radius: float | None = radius
        """
        The radius of the hole.
        """

        self._diameter: float | None = diameter
        """
        The diameter of the hole.
        """

        self._overall_length: float | None = overall_length
        """
        The overall length of the hole. 
        """

        self._center_to_center: float | None = center_to_center
        """
        The distance between two centers of the two circles of the hole.
        """

        self.__validate_arguments(locals())

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __validate_arguments(args: Dict[str, Any]) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.

        :param args: The arguments supplied to the constructor.
        """
        validator = ArgumentValidator(args)
        validator.validate_exclusive({'radius'}, {'diameter'})
        validator.validate_exclusive({'center_to_center'}, {'overall_length'})
        validator.validate_required({'height'},
                                    {'center_to_center', 'overall_length'},
                                    {'radius', 'diameter'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def height(self) -> float:
        """
        Returns the height/length of the hole.
        """
        return self._height

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float:
        """
        Returns the radius of the hole.
        """
        if self._radius is None:
            self._radius = 0.5 * self._diameter

        return self._radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter(self) -> float:
        """
        Returns the diameter of the hole.
        """
        if self._diameter is None:
            self._diameter = 2.0 * self._radius

        return self._diameter

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def overall_length(self) -> float:
        """
        Returns the overall length of the hole.
        """
        if self._overall_length is None:
            self._overall_length = self.center_to_center + self.diameter

        return self._overall_length

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center_to_center(self) -> float:
        """
        Returns the distance between two centers of the two circles of the hole.
        """
        if self._center_to_center is None:
            self._center_to_center = self._overall_length - self.diameter

        return self._center_to_center

    # ------------------------------------------------------------------------------------------------------------------
    def real_fn(self, context: Context) -> int | None:
        """
        Returns the real fixed number of fragments in 360 degrees.
        """
        if self.fn4n:
            return Radius2Sides4n.r2sides4n(context, self.radius)

        return self.fn

    # ------------------------------------------------------------------------------------------------------------------
    def _build_extrude(self, context: Context) -> ScadWidget:
        """
        Build a simple hole without a top and a bottom profile.

        :param context: The build context.
        """
        circle = Circle(diameter=self.diameter,
                        fa=self.fa,
                        fs=self.fs,
                        fn=self.fn,
                        fn4n=self.fn4n,
                        extend_by_eps_radius=self.extend_by_eps_boundary)
        circle1 = Translate2D(y=-0.5 * self.center_to_center, child=circle)
        middle = Rectangle(width=self.diameter,
                           depth=self.center_to_center,
                           center=True,
                           extend_by_eps_sides=self.extend_by_eps_boundary)
        circle2 = Translate2D(y=0.5 * self.center_to_center, child=circle)
        slot = Union(children=[circle1, middle, circle2])

        hole = LinearExtrude(height=self.height,
                             center=self.alignment == HoleAlignment.CENTER,
                             fa=self.fa,
                             fs=self.fs,
                             fn=self.real_fn(context),
                             extend_by_eps_top=self.extend_by_eps_top,
                             extend_by_eps_bottom=self.extend_by_eps_bottom,
                             child=slot)

        if self.alignment == HoleAlignment.TOP:
            hole = Translate3D(z=-self.height, child=hole)

        return hole

    # ------------------------------------------------------------------------------------------------------------------
    def _build_rotate_extrude_profile(self, context: Context) -> ScadWidget:
        """

        :param context:
        """
        profile = Rectangle(width=self.radius,
                            depth=self.height,
                            extend_by_eps_sides=[False,
                                                 self.extend_by_eps_top,
                                                 self.extend_by_eps_boundary,
                                                 self.extend_by_eps_bottom])
        left_halve = Rectangle(width=self.radius + context.eps,
                               depth=self.height + 2 * context.eps,
                               extend_by_eps_sides=[True, True, False, True])
        left_halve = Translate2D(x=-self.radius - context.eps, y=-context.eps, child=left_halve)
        negatives: List[ScadWidget] = [left_halve]
        positives: List[ScadWidget] = []

        nodes = profile.nodes
        params = SmoothProfileParams(inner_angle=90.0,
                                     normal_angle=225.0,
                                     position=nodes[2],
                                     edge1_is_extended_by_eps=self.extend_by_eps_top,
                                     edge2_is_extended_by_eps=self.extend_by_eps_boundary)
        negative, positive = self.profile_top.create_smooth_profiles(params=params)
        if negative is not None:
            negatives.append(negative)
        if positive is not None:
            positives.append(positive)

        nodes = profile.nodes
        params = SmoothProfileParams(inner_angle=90.0,
                                     normal_angle=135.0,
                                     position=nodes[3],
                                     edge1_is_extended_by_eps=self.extend_by_eps_boundary,
                                     edge2_is_extended_by_eps=self.extend_by_eps_bottom)
        negative, positive = self.profile_bottom.create_smooth_profiles(params=params)

        if negative is not None:
            negatives.append(negative)
        if positive is not None:
            positives.append(positive)

        if positives:
            profile = Union(children=[profile, *positives])
        if negatives:
            profile = Difference(children=[profile, *negatives])

        return profile

    # ------------------------------------------------------------------------------------------------------------------
    def _build_rotate_extrude(self, context: Context) -> ScadWidget:
        """
        Build a simple hole with a top or a bottom profile.

        :param context The build context.
        """
        profile = self._build_rotate_extrude_profile(context)

        hole = RotateExtrude(convexity=2,
                             fa=self.fa,
                             fs=self.fs,
                             fn=self.real_fn(context),
                             child=profile)
        hole1 = Translate3D(y=0.5 * self.center_to_center, child=hole)
        hole2 = Translate3D(y=-0.5 * self.center_to_center, child=hole)

        profile = Union(children=[profile, Flip2D(horizontal=True, child=profile)])
        slot = LinearExtrude(height=self.center_to_center, center=True, child=profile, convexity=4)
        slot = Rotate3D(angle_x=90.0, child=slot)

        hole = Union(children=[hole1, slot, hole2])

        if self.alignment == HoleAlignment.TOP:
            hole = Translate3D(z=-self.height, child=hole)
        elif self.alignment == HoleAlignment.CENTER:
            hole = Translate3D(z=-0.5 * self.height, child=hole)
        elif self.alignment == HoleAlignment.BOTTOM:
            pass
        else:
            raise ValueError(f'Unknown alignment {self.alignment}')

        return hole

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        if isinstance(self.profile_top, Rough) and isinstance(self.profile_bottom, Rough):
            return self._build_extrude(context)

        return self._build_rotate_extrude(context)

# ----------------------------------------------------------------------------------------------------------------------
