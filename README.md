## README — Triangular Prism Add-on

Short: adds Shift+A → Mesh → "Add Triangular Prism (with horizontal bevel)" and creates a triangular prism with an optional horizontal bevel.

## Features

-  Creates a triangular prism with configurable width, height, and depth.
-  Selects nearly-horizontal edges (along X) and applies a bevel to them.
-  Bevel parameters: amount and segments (profile fixed at 0.5 in code).
-  Option to enter Edit Mode after creation.

## Installation

1. Save the script as triangular_prism_addon.py (or any .py filename).
2. In Blender: Edit → Preferences → Add-ons → Install → select the file → Enable.

## Usage

1. Shift+A → Mesh → Add Triangular Prism (with horizontal bevel).
2. Adjust operator options in the lower-left operator panel (or press F9):
   -  Width — prism width
   -  Height — prism height
   -  Depth — prism depth
   -  Bevel Amount — bevel offset
   -  Bevel Segments — bevel subdivision
   -  Enter Edit Mode — toggle entering Edit Mode after creation

## Default Parameters

-  width: 2.0
-  height: 1.732
-  depth: 2.0
-  bevel_amount: 0.2
-  bevel_segments: 3

## Technical Notes

-  Horizontal-edge detection: compares X difference to horizontal_x_tol (1e-3) and checks vertical component ≤ max_vertical_component (0.01 by default).
-  Bevel is applied in Edit Mode using bpy.ops.mesh.bevel.
-  Mesh is created with 6 verts and 5 faces (two triangular caps + three quad side faces).
-  Compatible with Blender 3.0+ (see bl_info).

## License

Add a LICENSE file (e.g., MIT) when publishing.

## Optional Extensions

-  Expose bevel profile as a UI parameter.
-  Add location/rotation parameters to the operator UI.
-  Register custom icons and a dedicated UI panel.

I can prepare a ZIP with the add-on and a LICENSE file if you want.
