"""Limited imports from VTK (excludes any GL-dependent).

These are the modules within VTK that must be loaded across pyvista's
core API. Here, we attempt to import modules using the ``vtkmodules``
package, which lets us only have to import from select modules and not
the entire library.

"""

from __future__ import annotations

import contextlib
from typing import NamedTuple
import warnings

from vtkmodules.vtkCommonCore import vtkVersion as vtkVersion
from vtkmodules.vtkImagingSources import vtkImageEllipsoidSource as vtkImageEllipsoidSource
from vtkmodules.vtkImagingSources import vtkImageGaussianSource as vtkImageGaussianSource
from vtkmodules.vtkImagingSources import vtkImageGridSource as vtkImageGridSource
from vtkmodules.vtkImagingSources import vtkImageMandelbrotSource as vtkImageMandelbrotSource
from vtkmodules.vtkImagingSources import vtkImageNoiseSource as vtkImageNoiseSource
from vtkmodules.vtkImagingSources import vtkImageSinusoidSource as vtkImageSinusoidSource

# vtkExtractEdges moved from vtkFiltersExtraction to vtkFiltersCore in
# VTK commit d9981b9aeb93b42d1371c6e295d76bfdc18430bd
try:
    from vtkmodules.vtkFiltersCore import vtkExtractEdges as vtkExtractEdges
except ImportError:
    from vtkmodules.vtkFiltersExtraction import (  # type: ignore[attr-defined, no-redef]
        vtkExtractEdges as vtkExtractEdges,
    )

# vtkCellTreeLocator moved from vtkFiltersGeneral to vtkCommonDataModel in
# VTK commit 4a29e6f7dd9acb460644fe487d2e80aac65f7be9
try:
    from vtkmodules.vtkCommonDataModel import vtkCellTreeLocator as vtkCellTreeLocator
except ImportError:
    from vtkmodules.vtkFiltersGeneral import vtkCellTreeLocator

from vtkmodules.numpy_interface.dataset_adapter import VTKArray
from vtkmodules.numpy_interface.dataset_adapter import VTKObjectWrapper
from vtkmodules.numpy_interface.dataset_adapter import numpyTovtkDataArray
from vtkmodules.util.numpy_support import get_vtk_array_type
from vtkmodules.util.numpy_support import numpy_to_vtk
from vtkmodules.util.numpy_support import numpy_to_vtkIdTypeArray
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtkmodules.vtkCommonComputationalGeometry import vtkKochanekSpline
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricBohemianDome
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricBour
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricBoy
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricCatalanMinimal
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricConicSpiral
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricCrossCap
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricDini
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricEllipsoid
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricEnneper
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricFigure8Klein
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricFunction
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricHenneberg
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricKlein
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricKuen
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricMobius
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricPluckerConoid
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricPseudosphere
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricRandomHills
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricRoman
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricSpline
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricSuperEllipsoid
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricSuperToroid
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricTorus
from vtkmodules.vtkCommonCore import VTK_ARIAL
from vtkmodules.vtkCommonCore import VTK_COURIER
from vtkmodules.vtkCommonCore import VTK_FONT_FILE
from vtkmodules.vtkCommonCore import VTK_TIMES
from vtkmodules.vtkCommonCore import VTK_UNSIGNED_CHAR
from vtkmodules.vtkCommonCore import buffer_shared
from vtkmodules.vtkCommonCore import mutable
from vtkmodules.vtkCommonCore import reference
from vtkmodules.vtkCommonCore import vtkAbstractArray
from vtkmodules.vtkCommonCore import vtkBitArray
from vtkmodules.vtkCommonCore import vtkCharArray
from vtkmodules.vtkCommonCore import vtkCommand
from vtkmodules.vtkCommonCore import vtkDataArray
from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonCore import vtkFileOutputWindow
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonCore import vtkIdList
from vtkmodules.vtkCommonCore import vtkIdTypeArray
from vtkmodules.vtkCommonCore import vtkLogger
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkCommonCore import vtkOutputWindow
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonCore import vtkSignedCharArray
from vtkmodules.vtkCommonCore import vtkStringArray
from vtkmodules.vtkCommonCore import vtkStringOutputWindow
from vtkmodules.vtkCommonCore import vtkTypeInt32Array
from vtkmodules.vtkCommonCore import vtkTypeInt64Array
from vtkmodules.vtkCommonCore import vtkTypeUInt32Array
from vtkmodules.vtkCommonCore import vtkUnsignedCharArray
from vtkmodules.vtkCommonCore import vtkWeakReference
from vtkmodules.vtkCommonDataModel import VTK_BEZIER_CURVE
from vtkmodules.vtkCommonDataModel import VTK_BEZIER_HEXAHEDRON
from vtkmodules.vtkCommonDataModel import VTK_BEZIER_PYRAMID
from vtkmodules.vtkCommonDataModel import VTK_BEZIER_QUADRILATERAL
from vtkmodules.vtkCommonDataModel import VTK_BEZIER_TETRAHEDRON
from vtkmodules.vtkCommonDataModel import VTK_BEZIER_TRIANGLE
from vtkmodules.vtkCommonDataModel import VTK_BEZIER_WEDGE
from vtkmodules.vtkCommonDataModel import VTK_BIQUADRATIC_QUAD
from vtkmodules.vtkCommonDataModel import VTK_BIQUADRATIC_QUADRATIC_HEXAHEDRON
from vtkmodules.vtkCommonDataModel import VTK_BIQUADRATIC_QUADRATIC_WEDGE
from vtkmodules.vtkCommonDataModel import VTK_BIQUADRATIC_TRIANGLE
from vtkmodules.vtkCommonDataModel import VTK_CONVEX_POINT_SET
from vtkmodules.vtkCommonDataModel import VTK_CUBIC_LINE
from vtkmodules.vtkCommonDataModel import VTK_EMPTY_CELL
from vtkmodules.vtkCommonDataModel import VTK_HEXAGONAL_PRISM
from vtkmodules.vtkCommonDataModel import VTK_HEXAHEDRON
from vtkmodules.vtkCommonDataModel import VTK_HIGHER_ORDER_EDGE
from vtkmodules.vtkCommonDataModel import VTK_HIGHER_ORDER_HEXAHEDRON
from vtkmodules.vtkCommonDataModel import VTK_HIGHER_ORDER_POLYGON
from vtkmodules.vtkCommonDataModel import VTK_HIGHER_ORDER_PYRAMID
from vtkmodules.vtkCommonDataModel import VTK_HIGHER_ORDER_QUAD
from vtkmodules.vtkCommonDataModel import VTK_HIGHER_ORDER_TETRAHEDRON
from vtkmodules.vtkCommonDataModel import VTK_HIGHER_ORDER_TRIANGLE
from vtkmodules.vtkCommonDataModel import VTK_HIGHER_ORDER_WEDGE
from vtkmodules.vtkCommonDataModel import VTK_LAGRANGE_CURVE
from vtkmodules.vtkCommonDataModel import VTK_LAGRANGE_HEXAHEDRON
from vtkmodules.vtkCommonDataModel import VTK_LAGRANGE_PYRAMID
from vtkmodules.vtkCommonDataModel import VTK_LAGRANGE_QUADRILATERAL
from vtkmodules.vtkCommonDataModel import VTK_LAGRANGE_TETRAHEDRON
from vtkmodules.vtkCommonDataModel import VTK_LAGRANGE_TRIANGLE
from vtkmodules.vtkCommonDataModel import VTK_LAGRANGE_WEDGE
from vtkmodules.vtkCommonDataModel import VTK_LINE
from vtkmodules.vtkCommonDataModel import VTK_PARAMETRIC_CURVE
from vtkmodules.vtkCommonDataModel import VTK_PARAMETRIC_HEX_REGION
from vtkmodules.vtkCommonDataModel import VTK_PARAMETRIC_QUAD_SURFACE
from vtkmodules.vtkCommonDataModel import VTK_PARAMETRIC_SURFACE
from vtkmodules.vtkCommonDataModel import VTK_PARAMETRIC_TETRA_REGION
from vtkmodules.vtkCommonDataModel import VTK_PARAMETRIC_TRI_SURFACE
from vtkmodules.vtkCommonDataModel import VTK_PENTAGONAL_PRISM
from vtkmodules.vtkCommonDataModel import VTK_PIXEL
from vtkmodules.vtkCommonDataModel import VTK_POLY_LINE
from vtkmodules.vtkCommonDataModel import VTK_POLY_VERTEX
from vtkmodules.vtkCommonDataModel import VTK_POLYGON
from vtkmodules.vtkCommonDataModel import VTK_POLYHEDRON
from vtkmodules.vtkCommonDataModel import VTK_PYRAMID
from vtkmodules.vtkCommonDataModel import VTK_QUAD
from vtkmodules.vtkCommonDataModel import VTK_QUADRATIC_EDGE
from vtkmodules.vtkCommonDataModel import VTK_QUADRATIC_HEXAHEDRON
from vtkmodules.vtkCommonDataModel import VTK_QUADRATIC_LINEAR_QUAD
from vtkmodules.vtkCommonDataModel import VTK_QUADRATIC_LINEAR_WEDGE
from vtkmodules.vtkCommonDataModel import VTK_QUADRATIC_POLYGON
from vtkmodules.vtkCommonDataModel import VTK_QUADRATIC_PYRAMID
from vtkmodules.vtkCommonDataModel import VTK_QUADRATIC_QUAD
from vtkmodules.vtkCommonDataModel import VTK_QUADRATIC_TETRA
from vtkmodules.vtkCommonDataModel import VTK_QUADRATIC_TRIANGLE
from vtkmodules.vtkCommonDataModel import VTK_QUADRATIC_WEDGE
from vtkmodules.vtkCommonDataModel import VTK_TETRA
from vtkmodules.vtkCommonDataModel import VTK_TRIANGLE
from vtkmodules.vtkCommonDataModel import VTK_TRIANGLE_STRIP
from vtkmodules.vtkCommonDataModel import VTK_TRIQUADRATIC_HEXAHEDRON
from vtkmodules.vtkCommonDataModel import VTK_VERTEX
from vtkmodules.vtkCommonDataModel import VTK_VOXEL
from vtkmodules.vtkCommonDataModel import VTK_WEDGE
from vtkmodules.vtkCommonDataModel import vtkCell
from vtkmodules.vtkCommonDataModel import vtkCellArray
from vtkmodules.vtkCommonDataModel import vtkCellLocator
from vtkmodules.vtkCommonDataModel import vtkColor3ub
from vtkmodules.vtkCommonDataModel import vtkCompositeDataSet
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkCommonDataModel import vtkDataSet
from vtkmodules.vtkCommonDataModel import vtkDataSetAttributes
from vtkmodules.vtkCommonDataModel import vtkExplicitStructuredGrid
from vtkmodules.vtkCommonDataModel import vtkFieldData
from vtkmodules.vtkCommonDataModel import vtkGenericCell
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkCommonDataModel import vtkImplicitFunction
from vtkmodules.vtkCommonDataModel import vtkIterativeClosestPointTransform
from vtkmodules.vtkCommonDataModel import vtkMolecule
from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet
from vtkmodules.vtkCommonDataModel import vtkNonMergingPointLocator
from vtkmodules.vtkCommonDataModel import vtkPartitionedDataSet
from vtkmodules.vtkCommonDataModel import vtkPerlinNoise
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkCommonDataModel import vtkPlaneCollection
from vtkmodules.vtkCommonDataModel import vtkPlanes
from vtkmodules.vtkCommonDataModel import vtkPointLocator
from vtkmodules.vtkCommonDataModel import vtkPointSet
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonDataModel import vtkPolyLine
from vtkmodules.vtkCommonDataModel import vtkPolyPlane
from vtkmodules.vtkCommonDataModel import vtkPyramid
from vtkmodules.vtkCommonDataModel import vtkQuadraticEdge
from vtkmodules.vtkCommonDataModel import vtkQuadraticHexahedron
from vtkmodules.vtkCommonDataModel import vtkQuadraticQuad
from vtkmodules.vtkCommonDataModel import vtkQuadraticTetra
from vtkmodules.vtkCommonDataModel import vtkQuadraticTriangle
from vtkmodules.vtkCommonDataModel import vtkQuadraticWedge
from vtkmodules.vtkCommonDataModel import vtkRectf
from vtkmodules.vtkCommonDataModel import vtkRectilinearGrid
from vtkmodules.vtkCommonDataModel import vtkSelection
from vtkmodules.vtkCommonDataModel import vtkSelectionNode
from vtkmodules.vtkCommonDataModel import vtkStaticCellLocator
from vtkmodules.vtkCommonDataModel import vtkStaticPointLocator
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid

with contextlib.suppress(ImportError):
    from vtkmodules.util.pickle_support import (
        serialize_VTK_data_object as serialize_VTK_data_object,
    )

from vtkmodules.vtkCommonDataModel import vtkAbstractCellLocator as vtkAbstractCellLocator
from vtkmodules.vtkCommonDataModel import vtkBiQuadraticQuad as vtkBiQuadraticQuad
from vtkmodules.vtkCommonDataModel import (
    vtkBiQuadraticQuadraticHexahedron as vtkBiQuadraticQuadraticHexahedron,
)
from vtkmodules.vtkCommonDataModel import (
    vtkBiQuadraticQuadraticWedge as vtkBiQuadraticQuadraticWedge,
)
from vtkmodules.vtkCommonDataModel import vtkBiQuadraticTriangle as vtkBiQuadraticTriangle
from vtkmodules.vtkCommonDataModel import vtkConvexPointSet as vtkConvexPointSet
from vtkmodules.vtkCommonDataModel import vtkCubicLine as vtkCubicLine
from vtkmodules.vtkCommonDataModel import vtkEmptyCell as vtkEmptyCell
from vtkmodules.vtkCommonDataModel import vtkHexagonalPrism as vtkHexagonalPrism
from vtkmodules.vtkCommonDataModel import vtkHexahedron as vtkHexahedron
from vtkmodules.vtkCommonDataModel import vtkLine as vtkLine
from vtkmodules.vtkCommonDataModel import vtkPentagonalPrism as vtkPentagonalPrism
from vtkmodules.vtkCommonDataModel import vtkPixel as vtkPixel
from vtkmodules.vtkCommonDataModel import vtkPolygon as vtkPolygon
from vtkmodules.vtkCommonDataModel import vtkPolyhedron as vtkPolyhedron
from vtkmodules.vtkCommonDataModel import vtkPolyVertex as vtkPolyVertex
from vtkmodules.vtkCommonDataModel import vtkQuad as vtkQuad
from vtkmodules.vtkCommonDataModel import vtkQuadraticLinearQuad as vtkQuadraticLinearQuad
from vtkmodules.vtkCommonDataModel import vtkQuadraticLinearWedge as vtkQuadraticLinearWedge
from vtkmodules.vtkCommonDataModel import vtkQuadraticPolygon as vtkQuadraticPolygon
from vtkmodules.vtkCommonDataModel import vtkQuadraticPyramid as vtkQuadraticPyramid
from vtkmodules.vtkCommonDataModel import vtkStructuredPoints as vtkStructuredPoints
from vtkmodules.vtkCommonDataModel import vtkTetra as vtkTetra
from vtkmodules.vtkCommonDataModel import vtkTriangle as vtkTriangle
from vtkmodules.vtkCommonDataModel import vtkTriangleStrip as vtkTriangleStrip
from vtkmodules.vtkCommonDataModel import vtkTriQuadraticHexahedron as vtkTriQuadraticHexahedron
from vtkmodules.vtkCommonDataModel import vtkVertex as vtkVertex
from vtkmodules.vtkCommonDataModel import vtkVoxel as vtkVoxel
from vtkmodules.vtkCommonDataModel import vtkWedge as vtkWedge

with contextlib.suppress(ImportError):  # Introduced prior to VTK 9.2
    from vtkmodules.vtkCommonDataModel import VTK_TRIQUADRATIC_PYRAMID as VTK_TRIQUADRATIC_PYRAMID
    from vtkmodules.vtkCommonDataModel import vtkTriQuadraticPyramid as vtkTriQuadraticPyramid

from vtkmodules.vtkCommonExecutionModel import vtkAlgorithm as vtkAlgorithm
from vtkmodules.vtkCommonExecutionModel import vtkAlgorithmOutput as vtkAlgorithmOutput
from vtkmodules.vtkCommonExecutionModel import vtkCompositeDataPipeline as vtkCompositeDataPipeline
from vtkmodules.vtkCommonExecutionModel import vtkImageToStructuredGrid as vtkImageToStructuredGrid
from vtkmodules.vtkCommonMath import vtkMatrix3x3 as vtkMatrix3x3
from vtkmodules.vtkCommonMath import vtkMatrix4x4 as vtkMatrix4x4
from vtkmodules.vtkCommonTransforms import vtkTransform as vtkTransform
from vtkmodules.vtkDomainsChemistry import vtkProteinRibbonFilter as vtkProteinRibbonFilter
from vtkmodules.vtkFiltersCore import VTK_BEST_FITTING_PLANE as VTK_BEST_FITTING_PLANE
from vtkmodules.vtkFiltersCore import vtkAppendArcLength as vtkAppendArcLength
from vtkmodules.vtkFiltersCore import vtkAppendFilter as vtkAppendFilter
from vtkmodules.vtkFiltersCore import vtkAppendPolyData as vtkAppendPolyData
from vtkmodules.vtkFiltersCore import vtkCellCenters as vtkCellCenters
from vtkmodules.vtkFiltersCore import vtkCellDataToPointData as vtkCellDataToPointData
from vtkmodules.vtkFiltersCore import vtkCenterOfMass as vtkCenterOfMass
from vtkmodules.vtkFiltersCore import vtkCleanPolyData as vtkCleanPolyData
from vtkmodules.vtkFiltersCore import vtkClipPolyData as vtkClipPolyData
from vtkmodules.vtkFiltersCore import vtkConnectivityFilter as vtkConnectivityFilter
from vtkmodules.vtkFiltersCore import vtkContourFilter as vtkContourFilter
from vtkmodules.vtkFiltersCore import vtkCutter as vtkCutter
from vtkmodules.vtkFiltersCore import vtkDecimatePolylineFilter as vtkDecimatePolylineFilter
from vtkmodules.vtkFiltersCore import vtkDecimatePro as vtkDecimatePro
from vtkmodules.vtkFiltersCore import vtkDelaunay2D as vtkDelaunay2D
from vtkmodules.vtkFiltersCore import vtkDelaunay3D as vtkDelaunay3D
from vtkmodules.vtkFiltersCore import vtkElevationFilter as vtkElevationFilter
from vtkmodules.vtkFiltersCore import (
    vtkExplicitStructuredGridToUnstructuredGrid as vtkExplicitStructuredGridToUnstructuredGrid,
)
from vtkmodules.vtkFiltersCore import vtkFeatureEdges as vtkFeatureEdges
from vtkmodules.vtkFiltersCore import vtkFlyingEdges3D as vtkFlyingEdges3D
from vtkmodules.vtkFiltersCore import vtkGlyph3D as vtkGlyph3D
from vtkmodules.vtkFiltersCore import vtkImplicitPolyDataDistance as vtkImplicitPolyDataDistance
from vtkmodules.vtkFiltersCore import vtkMarchingCubes as vtkMarchingCubes
from vtkmodules.vtkFiltersCore import vtkMassProperties as vtkMassProperties
from vtkmodules.vtkFiltersCore import vtkPointDataToCellData as vtkPointDataToCellData
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals as vtkPolyDataNormals
from vtkmodules.vtkFiltersCore import vtkQuadricDecimation as vtkQuadricDecimation
from vtkmodules.vtkFiltersCore import vtkResampleWithDataSet as vtkResampleWithDataSet
from vtkmodules.vtkFiltersCore import vtkReverseSense as vtkReverseSense
from vtkmodules.vtkFiltersCore import vtkSmoothPolyDataFilter as vtkSmoothPolyDataFilter
from vtkmodules.vtkFiltersCore import vtkStripper as vtkStripper
from vtkmodules.vtkFiltersCore import vtkThreshold as vtkThreshold
from vtkmodules.vtkFiltersCore import vtkTriangleFilter as vtkTriangleFilter
from vtkmodules.vtkFiltersCore import vtkTubeFilter as vtkTubeFilter
from vtkmodules.vtkFiltersCore import (
    vtkUnstructuredGridToExplicitStructuredGrid as vtkUnstructuredGridToExplicitStructuredGrid,
)
from vtkmodules.vtkFiltersCore import vtkWindowedSincPolyDataFilter as vtkWindowedSincPolyDataFilter
from vtkmodules.vtkFiltersExtraction import vtkExtractCellsByType as vtkExtractCellsByType
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry as vtkExtractGeometry
from vtkmodules.vtkFiltersExtraction import vtkExtractGrid as vtkExtractGrid
from vtkmodules.vtkFiltersExtraction import vtkExtractSelection as vtkExtractSelection
from vtkmodules.vtkFiltersFlowPaths import (
    vtkEvenlySpacedStreamlines2D as vtkEvenlySpacedStreamlines2D,
)
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer as vtkStreamTracer

with contextlib.suppress(ImportError):  # Introduced VTK v9.1.0
    from vtkmodules.vtkFiltersGeneral import vtkRemovePolyData as vtkRemovePolyData

from vtkmodules.vtkFiltersGeneral import vtkAxes as vtkAxes
from vtkmodules.vtkFiltersGeneral import (
    vtkBooleanOperationPolyDataFilter as vtkBooleanOperationPolyDataFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkBoxClipDataSet as vtkBoxClipDataSet
from vtkmodules.vtkFiltersGeneral import vtkClipClosedSurface as vtkClipClosedSurface
from vtkmodules.vtkFiltersGeneral import vtkContourTriangulator as vtkContourTriangulator
from vtkmodules.vtkFiltersGeneral import vtkCursor3D as vtkCursor3D
from vtkmodules.vtkFiltersGeneral import vtkCurvatures as vtkCurvatures
from vtkmodules.vtkFiltersGeneral import vtkDataSetTriangleFilter as vtkDataSetTriangleFilter
from vtkmodules.vtkFiltersGeneral import vtkGradientFilter as vtkGradientFilter
from vtkmodules.vtkFiltersGeneral import (
    vtkIntersectionPolyDataFilter as vtkIntersectionPolyDataFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkOBBTree as vtkOBBTree
from vtkmodules.vtkFiltersGeneral import (
    vtkRectilinearGridToPointSet as vtkRectilinearGridToPointSet,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkRectilinearGridToTetrahedra as vtkRectilinearGridToTetrahedra,
)
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter as vtkShrinkFilter
from vtkmodules.vtkFiltersGeneral import vtkTableBasedClipDataSet as vtkTableBasedClipDataSet
from vtkmodules.vtkFiltersGeneral import vtkTableToPolyData as vtkTableToPolyData
from vtkmodules.vtkFiltersGeneral import vtkTessellatorFilter as vtkTessellatorFilter
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter as vtkTransformFilter
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar as vtkWarpScalar
from vtkmodules.vtkFiltersGeneral import vtkWarpVector as vtkWarpVector
from vtkmodules.vtkFiltersGeometry import (
    vtkCompositeDataGeometryFilter as vtkCompositeDataGeometryFilter,
)
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter as vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter as vtkGeometryFilter
from vtkmodules.vtkFiltersGeometry import (
    vtkStructuredGridGeometryFilter as vtkStructuredGridGeometryFilter,
)
from vtkmodules.vtkFiltersHybrid import vtkPolyDataSilhouette as vtkPolyDataSilhouette
from vtkmodules.vtkFiltersModeling import (
    vtkAdaptiveSubdivisionFilter as vtkAdaptiveSubdivisionFilter,
)
from vtkmodules.vtkFiltersModeling import (
    vtkBandedPolyDataContourFilter as vtkBandedPolyDataContourFilter,
)
from vtkmodules.vtkFiltersModeling import (
    vtkButterflySubdivisionFilter as vtkButterflySubdivisionFilter,
)
from vtkmodules.vtkFiltersModeling import vtkCollisionDetectionFilter as vtkCollisionDetectionFilter
from vtkmodules.vtkFiltersModeling import (
    vtkDijkstraGraphGeodesicPath as vtkDijkstraGraphGeodesicPath,
)
from vtkmodules.vtkFiltersModeling import vtkFillHolesFilter as vtkFillHolesFilter
from vtkmodules.vtkFiltersModeling import vtkLinearExtrusionFilter as vtkLinearExtrusionFilter
from vtkmodules.vtkFiltersModeling import vtkLinearSubdivisionFilter as vtkLinearSubdivisionFilter
from vtkmodules.vtkFiltersModeling import vtkLoopSubdivisionFilter as vtkLoopSubdivisionFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter as vtkOutlineFilter
from vtkmodules.vtkFiltersModeling import vtkRibbonFilter as vtkRibbonFilter
from vtkmodules.vtkFiltersModeling import (
    vtkRotationalExtrusionFilter as vtkRotationalExtrusionFilter,
)
from vtkmodules.vtkFiltersModeling import vtkRuledSurfaceFilter as vtkRuledSurfaceFilter
from vtkmodules.vtkFiltersModeling import vtkSelectEnclosedPoints as vtkSelectEnclosedPoints
from vtkmodules.vtkFiltersModeling import vtkSubdivideTetra as vtkSubdivideTetra
from vtkmodules.vtkFiltersModeling import vtkTrimmedExtrusionFilter as vtkTrimmedExtrusionFilter
from vtkmodules.vtkFiltersParallel import vtkIntegrateAttributes as vtkIntegrateAttributes

with contextlib.suppress(ImportError):
    # `vtkmodules.vtkFiltersParallelDIY2` is unavailable in some versions of `vtk` from conda-forge
    from vtkmodules.vtkFiltersParallelDIY2 import (
        vtkRedistributeDataSetFilter as vtkRedistributeDataSetFilter,
    )

from vtkmodules.vtkFiltersPoints import vtkGaussianKernel as vtkGaussianKernel
from vtkmodules.vtkFiltersPoints import vtkPointInterpolator as vtkPointInterpolator
from vtkmodules.vtkFiltersSources import vtkArcSource as vtkArcSource
from vtkmodules.vtkFiltersSources import vtkArrowSource as vtkArrowSource
from vtkmodules.vtkFiltersSources import vtkCapsuleSource as vtkCapsuleSource
from vtkmodules.vtkFiltersSources import vtkConeSource as vtkConeSource
from vtkmodules.vtkFiltersSources import vtkCubeSource as vtkCubeSource
from vtkmodules.vtkFiltersSources import vtkCylinderSource as vtkCylinderSource
from vtkmodules.vtkFiltersSources import vtkDiskSource as vtkDiskSource
from vtkmodules.vtkFiltersSources import vtkFrustumSource as vtkFrustumSource
from vtkmodules.vtkFiltersSources import vtkLineSource as vtkLineSource
from vtkmodules.vtkFiltersSources import vtkOutlineCornerFilter as vtkOutlineCornerFilter
from vtkmodules.vtkFiltersSources import vtkOutlineCornerSource as vtkOutlineCornerSource
from vtkmodules.vtkFiltersSources import vtkParametricFunctionSource as vtkParametricFunctionSource
from vtkmodules.vtkFiltersSources import vtkPlaneSource as vtkPlaneSource
from vtkmodules.vtkFiltersSources import vtkPlatonicSolidSource as vtkPlatonicSolidSource
from vtkmodules.vtkFiltersSources import vtkPointSource as vtkPointSource
from vtkmodules.vtkFiltersSources import vtkRegularPolygonSource as vtkRegularPolygonSource
from vtkmodules.vtkFiltersSources import vtkSphereSource as vtkSphereSource
from vtkmodules.vtkFiltersSources import vtkSuperquadricSource as vtkSuperquadricSource
from vtkmodules.vtkFiltersSources import vtkTessellatedBoxSource as vtkTessellatedBoxSource
from vtkmodules.vtkFiltersStatistics import vtkComputeQuartiles as vtkComputeQuartiles

with contextlib.suppress(ImportError):
    from vtkmodules.vtkFiltersStatistics import vtkLengthDistribution as vtkLengthDistribution
from vtkmodules.vtkFiltersTexture import vtkTextureMapToPlane as vtkTextureMapToPlane
from vtkmodules.vtkFiltersTexture import vtkTextureMapToSphere as vtkTextureMapToSphere
from vtkmodules.vtkFiltersVerdict import vtkCellQuality as vtkCellQuality
from vtkmodules.vtkFiltersVerdict import vtkCellSizeFilter as vtkCellSizeFilter

with contextlib.suppress(ImportError):
    from vtkmodules.vtkFiltersVerdict import vtkBoundaryMeshQuality as vtkBoundaryMeshQuality

from vtkmodules.vtkImagingCore import vtkAbstractImageInterpolator as vtkAbstractImageInterpolator
from vtkmodules.vtkImagingCore import vtkExtractVOI as vtkExtractVOI
from vtkmodules.vtkImagingCore import vtkImageConstantPad as vtkImageConstantPad
from vtkmodules.vtkImagingCore import vtkImageDifference as vtkImageDifference
from vtkmodules.vtkImagingCore import vtkImageExtractComponents as vtkImageExtractComponents
from vtkmodules.vtkImagingCore import vtkImageFlip as vtkImageFlip
from vtkmodules.vtkImagingCore import vtkImageInterpolator as vtkImageInterpolator
from vtkmodules.vtkImagingCore import vtkImageMirrorPad as vtkImageMirrorPad
from vtkmodules.vtkImagingCore import vtkImageResize as vtkImageResize
from vtkmodules.vtkImagingCore import vtkImageSincInterpolator as vtkImageSincInterpolator
from vtkmodules.vtkImagingCore import vtkImageThreshold as vtkImageThreshold
from vtkmodules.vtkImagingCore import vtkImageWrapPad as vtkImageWrapPad
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource as vtkRTAnalyticSource
from vtkmodules.vtkImagingGeneral import vtkImageGaussianSmooth as vtkImageGaussianSmooth
from vtkmodules.vtkImagingGeneral import vtkImageMedian3D as vtkImageMedian3D
from vtkmodules.vtkImagingHybrid import vtkSampleFunction as vtkSampleFunction
from vtkmodules.vtkImagingHybrid import (
    vtkSurfaceReconstructionFilter as vtkSurfaceReconstructionFilter,
)
from vtkmodules.vtkImagingMorphological import (
    vtkImageConnectivityFilter as vtkImageConnectivityFilter,
)
from vtkmodules.vtkImagingStencil import vtkImageStencil as vtkImageStencil
from vtkmodules.vtkImagingStencil import vtkPolyDataToImageStencil as vtkPolyDataToImageStencil
from vtkmodules.vtkIOGeometry import vtkHoudiniPolyDataWriter as vtkHoudiniPolyDataWriter
from vtkmodules.vtkIOGeometry import vtkIVWriter as vtkIVWriter
from vtkmodules.vtkIOGeometry import vtkOBJWriter as vtkOBJWriter
from vtkmodules.vtkIOGeometry import vtkProStarReader as vtkProStarReader
from vtkmodules.vtkIOGeometry import vtkSTLWriter as vtkSTLWriter
from vtkmodules.vtkIOInfovis import vtkDelimitedTextReader as vtkDelimitedTextReader
from vtkmodules.vtkIOLegacy import vtkDataReader as vtkDataReader
from vtkmodules.vtkIOLegacy import vtkDataSetReader as vtkDataSetReader
from vtkmodules.vtkIOLegacy import vtkDataSetWriter as vtkDataSetWriter
from vtkmodules.vtkIOLegacy import vtkDataWriter as vtkDataWriter
from vtkmodules.vtkIOLegacy import vtkPolyDataReader as vtkPolyDataReader
from vtkmodules.vtkIOLegacy import vtkPolyDataWriter as vtkPolyDataWriter
from vtkmodules.vtkIOLegacy import vtkRectilinearGridReader as vtkRectilinearGridReader
from vtkmodules.vtkIOLegacy import vtkRectilinearGridWriter as vtkRectilinearGridWriter
from vtkmodules.vtkIOLegacy import vtkSimplePointsWriter as vtkSimplePointsWriter
from vtkmodules.vtkIOLegacy import vtkStructuredGridReader as vtkStructuredGridReader
from vtkmodules.vtkIOLegacy import vtkStructuredGridWriter as vtkStructuredGridWriter
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader as vtkUnstructuredGridReader
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridWriter as vtkUnstructuredGridWriter
from vtkmodules.vtkIOPLY import vtkPLYReader as vtkPLYReader
from vtkmodules.vtkIOPLY import vtkPLYWriter as vtkPLYWriter
from vtkmodules.vtkIOXML import vtkXMLImageDataReader as vtkXMLImageDataReader
from vtkmodules.vtkIOXML import vtkXMLImageDataWriter as vtkXMLImageDataWriter
from vtkmodules.vtkIOXML import vtkXMLMultiBlockDataReader as vtkXMLMultiBlockDataReader
from vtkmodules.vtkIOXML import vtkXMLMultiBlockDataWriter as vtkXMLMultiBlockDataWriter
from vtkmodules.vtkIOXML import vtkXMLPartitionedDataSetReader as vtkXMLPartitionedDataSetReader
from vtkmodules.vtkIOXML import vtkXMLPImageDataReader as vtkXMLPImageDataReader
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader as vtkXMLPolyDataReader
from vtkmodules.vtkIOXML import vtkXMLPolyDataWriter as vtkXMLPolyDataWriter
from vtkmodules.vtkIOXML import vtkXMLPRectilinearGridReader as vtkXMLPRectilinearGridReader
from vtkmodules.vtkIOXML import vtkXMLPUnstructuredGridReader as vtkXMLPUnstructuredGridReader
from vtkmodules.vtkIOXML import vtkXMLReader as vtkXMLReader
from vtkmodules.vtkIOXML import vtkXMLRectilinearGridReader as vtkXMLRectilinearGridReader
from vtkmodules.vtkIOXML import vtkXMLRectilinearGridWriter as vtkXMLRectilinearGridWriter
from vtkmodules.vtkIOXML import vtkXMLStructuredGridReader as vtkXMLStructuredGridReader
from vtkmodules.vtkIOXML import vtkXMLStructuredGridWriter as vtkXMLStructuredGridWriter
from vtkmodules.vtkIOXML import vtkXMLTableReader as vtkXMLTableReader
from vtkmodules.vtkIOXML import vtkXMLTableWriter as vtkXMLTableWriter
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader as vtkXMLUnstructuredGridReader
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter as vtkXMLUnstructuredGridWriter
from vtkmodules.vtkIOXML import vtkXMLWriter as vtkXMLWriter

with contextlib.suppress(ImportError):
    from vtkmodules.vtkImagingMorphological import vtkImageDilateErode3D as vtkImageDilateErode3D

try:
    from vtkmodules.vtkPythonContext2D import vtkPythonItem as vtkPythonItem
except ImportError:  # pragma: no cover
    # `vtkmodules.vtkPythonContext2D` is unavailable in some versions of `vtk` (see #3224)

    class vtkPythonItem:  # type: ignore[no-redef]
        """Empty placeholder."""

        def __init__(self):  # pragma: no cover
            """Raise version error on init."""
            from pyvista.core.errors import VTKVersionError

            raise VTKVersionError('Chart backgrounds require the vtkPythonContext2D module')


from vtkmodules.vtkImagingFourier import vtkImageButterworthHighPass as vtkImageButterworthHighPass
from vtkmodules.vtkImagingFourier import vtkImageButterworthLowPass as vtkImageButterworthLowPass
from vtkmodules.vtkImagingFourier import vtkImageFFT as vtkImageFFT
from vtkmodules.vtkImagingFourier import vtkImageRFFT as vtkImageRFFT

# 9.1+ imports
with contextlib.suppress(ImportError):
    from vtkmodules.vtkFiltersPoints import vtkConvertToPointCloud as vtkConvertToPointCloud

with contextlib.suppress(ImportError):  # Introduced prior to VTK 9.3
    from vtkmodules.vtkRenderingCore import vtkViewport as vtkViewport

# 9.3+ imports
with contextlib.suppress(ImportError):
    from vtkmodules.vtkFiltersCore import vtkPackLabels as vtkPackLabels
    from vtkmodules.vtkFiltersCore import vtkSurfaceNets3D as vtkSurfaceNets3D

# 9.1+ imports
with contextlib.suppress(ImportError):
    from vtkmodules.vtkIOParallelXML import (
        vtkXMLPartitionedDataSetWriter as vtkXMLPartitionedDataSetWriter,
    )


class VersionInfo(NamedTuple):
    """Version information as a named tuple."""

    major: int
    minor: int
    micro: int


def VTKVersionInfo():
    """Return the vtk version as a namedtuple.

    Returns
    -------
    VersionInfo
        Version information as a named tuple.

    """
    try:
        ver = vtkVersion()
        major = ver.GetVTKMajorVersion()
        minor = ver.GetVTKMinorVersion()
        micro = ver.GetVTKBuildVersion()
    except AttributeError:  # pragma: no cover
        warnings.warn('Unable to detect VTK version. Defaulting to v4.0.0')
        major, minor, micro = (4, 0, 0)

    return VersionInfo(major, minor, micro)


vtk_version_info = VTKVersionInfo()
