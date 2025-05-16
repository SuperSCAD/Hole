// Unit of length: Unit.MM
$fn = 60;

union()
{
   translate(v = [0.0, 0.0, -10.0])
   {
      translate(v = [0.0, 0.0, -0.314])
      {
         linear_extrude(height = 10.628, center = false, twist = 0.0, scale = 1.0)
         {
            union()
            {
               translate(v = [0.0, -1.5])
               {
                  circle(d = 1.0);
               }
               square(size = [1.0, 3.0], center = true);
               translate(v = [0.0, 1.5])
               {
                  circle(d = 1.0);
               }
            }
         }
      }
   }
   translate(v = [5.0, 0.0, 0.0])
   {
      linear_extrude(height = 10.628, center = true, twist = 0.0, scale = 1.0)
      {
         union()
         {
            translate(v = [0.0, -1.5])
            {
               circle(d = 1.0);
            }
            square(size = [1.0, 3.0], center = true);
            translate(v = [0.0, 1.5])
            {
               circle(d = 1.0);
            }
         }
      }
   }
   translate(v = [10.0, 0.0, 0.0])
   {
      translate(v = [0.0, 0.0, -0.314])
      {
         linear_extrude(height = 10.628, center = false, twist = 0.0, scale = 1.0)
         {
            union()
            {
               translate(v = [0.0, -1.5])
               {
                  circle(d = 1.0);
               }
               square(size = [1.0, 3.0], center = true);
               translate(v = [0.0, 1.5])
               {
                  circle(d = 1.0);
               }
            }
         }
      }
   }
}
