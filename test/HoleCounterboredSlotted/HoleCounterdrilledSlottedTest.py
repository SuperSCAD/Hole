from super_scad.boolean.Compound import Compound
from super_scad.scad.Context import Context
from super_scad.scad.Scad import Scad
from super_scad.transformation.Translate3D import Translate3D
from super_scad.type import Vector3
from super_scad_smooth_profiles.Chamfer import Chamfer
from super_scad_smooth_profiles.Fillet import Fillet

from super_scad_hole.HoleAlignment import HoleAlignment
from super_scad_hole.HoleCounterboredSlotted import HoleCounterboredSlotted
from test.ScadTestCase import ScadTestCase


class HoleCounterboredSlottedTest(ScadTestCase):
    """
    Test cases for HoleCounterboredSlotted.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def test_alignment(self):
        """
        Test the alignment of a slotted counterbored hole.
        """
        scad = Scad(context=Context(fn=360, eps=0.35, vpr=Vector3(90.0, 0.0, 0.0)))

        hole1 = HoleCounterboredSlotted(height=10.0,
                                        diameter=1.0,
                                        counterbore_diameter=3.0,
                                        counterbore_height=1.5,
                                        center_to_center=6.0,
                                        alignment=HoleAlignment.TOP)

        hole2 = HoleCounterboredSlotted(height=10.0,
                                        diameter=1.0,
                                        counterbore_diameter=3.0,
                                        counterbore_height=1.5,
                                        center_to_center=6.0,
                                        alignment=HoleAlignment.CENTER)
        hole2 = Translate3D(x=5.0, child=hole2)

        hole3 = HoleCounterboredSlotted(height=10.0,
                                        diameter=1.0,
                                        counterbore_diameter=3.0,
                                        counterbore_height=1.5,
                                        center_to_center=6.0,
                                        alignment=HoleAlignment.BOTTOM)
        hole3 = Translate3D(x=10.0, child=hole3)

        holes = Compound(children=[hole1, hole2, hole3])

        path_actual, path_expected = self.paths()
        scad.run_super_scad(holes, path_actual)
        actual = path_actual.read_text()
        expected = path_expected.read_text()
        self.assertEqual(expected, actual)

    # ------------------------------------------------------------------------------------------------------------------
    def test_alignment_with_profiles(self):
        """
        Test the alignment of a slotted counterbored hole with profiles.
        """
        scad = Scad(context=Context(fn=360, eps=0.1, vpr=Vector3(90.0, 0.0, 0.0)))

        hole1 = HoleCounterboredSlotted(height=10.0,
                                        diameter=2.0,
                                        counterbore_diameter=4.0,
                                        counterbore_angle=None,
                                        counterbore_height=2.0,
                                        center_to_center=6.0,
                                        alignment=HoleAlignment.TOP,
                                        profile_top=Fillet(radius=1.0, side=2),
                                        profile_bottom=Chamfer(skew_length=0.2, side=1))

        hole2 = HoleCounterboredSlotted(height=10.0,
                                        diameter=2.0,
                                        counterbore_diameter=4.0,
                                        counterbore_height=2.0,
                                        center_to_center=6.0,
                                        alignment=HoleAlignment.CENTER,
                                        profile_top=Fillet(radius=1.0, side=2),
                                        profile_bottom=Chamfer(skew_length=0.2, side=1))
        hole2 = Translate3D(x=5.0, child=hole2)

        hole3 = HoleCounterboredSlotted(height=10.0,
                                        diameter=2.0,
                                        counterbore_diameter=4.0,
                                        counterbore_height=2.0,
                                        center_to_center=6.0,
                                        alignment=HoleAlignment.BOTTOM,
                                        profile_top=Fillet(radius=1.0, side=2),
                                        profile_bottom=Chamfer(skew_length=0.2, side=1))
        hole3 = Translate3D(x=10.0, child=hole3)

        holes = Compound(children=[hole1, hole2, hole3])

        path_actual, path_expected = self.paths()
        scad.run_super_scad(holes, path_actual)
        actual = path_actual.read_text()
        expected = path_expected.read_text()
        self.assertEqual(expected, actual)

# ----------------------------------------------------------------------------------------------------------------------
