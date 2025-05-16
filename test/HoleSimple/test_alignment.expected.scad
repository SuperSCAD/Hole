// Unit of length: Unit.MM
$fn = 360;
$vpr = [90.0, 0.0, 0.0];

union()
{
   translate(v = [0.0, 0.0, -10.0])
   {
      translate(v = [0.0, 0.0, -0.35])
      {
         cylinder(h = 10.7, d = 1.0, center = false);
      }
   }
   translate(v = [5.0, 0.0, 0.0])
   {
      cylinder(h = 10.7, d = 1.0, center = true);
   }
   translate(v = [10.0, 0.0, 0.0])
   {
      translate(v = [0.0, 0.0, -0.35])
      {
         cylinder(h = 10.7, d = 1.0, center = false);
      }
   }
}
