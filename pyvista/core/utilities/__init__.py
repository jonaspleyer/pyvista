"""Utilities routines."""

from __future__ import annotations

import contextlib

from .arrays import FieldAssociation as FieldAssociation
from .arrays import array_from_vtkmatrix as array_from_vtkmatrix
from .arrays import cell_array as cell_array
from .arrays import convert_array as convert_array
from .arrays import convert_string_array as convert_string_array
from .arrays import field_array as field_array
from .arrays import get_array as get_array
from .arrays import get_array_association as get_array_association
from .arrays import get_vtk_type as get_vtk_type
from .arrays import parse_field_choice as parse_field_choice
from .arrays import point_array as point_array
from .arrays import raise_has_duplicates as raise_has_duplicates
from .arrays import raise_not_matching as raise_not_matching
from .arrays import row_array as row_array
from .arrays import set_default_active_scalars as set_default_active_scalars
from .arrays import set_default_active_vectors as set_default_active_vectors
from .arrays import vtk_bit_array_to_char as vtk_bit_array_to_char
from .arrays import vtk_id_list_to_array as vtk_id_list_to_array
from .arrays import vtkmatrix_from_array as vtkmatrix_from_array
from .cells import create_mixed_cells as create_mixed_cells
from .cells import get_mixed_cells as get_mixed_cells
from .cells import ncells_from_cells as ncells_from_cells
from .cells import numpy_to_idarr as numpy_to_idarr
from .features import cartesian_to_spherical as cartesian_to_spherical
from .features import create_grid as create_grid
from .features import grid_from_sph_coords as grid_from_sph_coords
from .features import merge as merge
from .features import perlin_noise as perlin_noise
from .features import sample_function as sample_function
from .features import spherical_to_cartesian as spherical_to_cartesian
from .features import transform_vectors_sph_to_cart as transform_vectors_sph_to_cart
from .features import voxelize as voxelize
from .features import voxelize_unstructured_grid as voxelize_unstructured_grid
from .features import voxelize_volume as voxelize_volume
from .fileio import from_meshio as from_meshio
from .fileio import get_ext as get_ext
from .fileio import is_meshio_mesh as is_meshio_mesh
from .fileio import read as read
from .fileio import read_exodus as read_exodus
from .fileio import read_grdecl as read_grdecl
from .fileio import read_meshio as read_meshio
from .fileio import read_pickle as read_pickle
from .fileio import read_texture as read_texture
from .fileio import save_meshio as save_meshio
from .fileio import save_pickle as save_pickle
from .fileio import set_pickle_format as set_pickle_format
from .fileio import set_vtkwriter_mode as set_vtkwriter_mode
from .geometric_objects import NORMALS as NORMALS
from .geometric_objects import Arrow as Arrow
from .geometric_objects import Box as Box
from .geometric_objects import Capsule as Capsule
from .geometric_objects import Circle as Circle
from .geometric_objects import CircularArc as CircularArc
from .geometric_objects import CircularArcFromNormal as CircularArcFromNormal
from .geometric_objects import Cone as Cone
from .geometric_objects import Cube as Cube
from .geometric_objects import Cylinder as Cylinder
from .geometric_objects import CylinderStructured as CylinderStructured
from .geometric_objects import Disc as Disc
from .geometric_objects import Dodecahedron as Dodecahedron
from .geometric_objects import Ellipse as Ellipse
from .geometric_objects import Icosahedron as Icosahedron
from .geometric_objects import Icosphere as Icosphere
from .geometric_objects import Line as Line
from .geometric_objects import MultipleLines as MultipleLines
from .geometric_objects import Octahedron as Octahedron
from .geometric_objects import Plane as Plane
from .geometric_objects import PlatonicSolid as PlatonicSolid
from .geometric_objects import Polygon as Polygon
from .geometric_objects import Pyramid as Pyramid
from .geometric_objects import Quadrilateral as Quadrilateral
from .geometric_objects import Rectangle as Rectangle
from .geometric_objects import SolidSphere as SolidSphere
from .geometric_objects import SolidSphereGeneric as SolidSphereGeneric
from .geometric_objects import Sphere as Sphere
from .geometric_objects import Superquadric as Superquadric
from .geometric_objects import Tetrahedron as Tetrahedron
from .geometric_objects import Text3D as Text3D
from .geometric_objects import Triangle as Triangle
from .geometric_objects import Tube as Tube
from .geometric_objects import Wavelet as Wavelet
from .geometric_sources import ArrowSource as ArrowSource
from .geometric_sources import AxesGeometrySource as AxesGeometrySource
from .geometric_sources import BoxSource as BoxSource
from .geometric_sources import ConeSource as ConeSource
from .geometric_sources import CubeFacesSource as CubeFacesSource
from .geometric_sources import CubeSource as CubeSource
from .geometric_sources import CylinderSource as CylinderSource
from .geometric_sources import DiscSource as DiscSource
from .geometric_sources import LineSource as LineSource
from .geometric_sources import MultipleLinesSource as MultipleLinesSource
from .geometric_sources import OrthogonalPlanesSource as OrthogonalPlanesSource
from .geometric_sources import PlaneSource as PlaneSource
from .geometric_sources import PlatonicSolidSource as PlatonicSolidSource
from .geometric_sources import PolygonSource as PolygonSource
from .geometric_sources import SphereSource as SphereSource
from .geometric_sources import SuperquadricSource as SuperquadricSource
from .geometric_sources import Text3DSource as Text3DSource
from .geometric_sources import translate as translate
from .image_sources import ImageEllipsoidSource as ImageEllipsoidSource
from .image_sources import ImageGaussianSource as ImageGaussianSource
from .image_sources import ImageGridSource as ImageGridSource
from .image_sources import ImageMandelbrotSource as ImageMandelbrotSource
from .image_sources import ImageNoiseSource as ImageNoiseSource
from .image_sources import ImageSinusoidSource as ImageSinusoidSource

with contextlib.suppress(ImportError):
    from .geometric_sources import CapsuleSource as CapsuleSource

from .helpers import axis_rotation as axis_rotation
from .helpers import generate_plane as generate_plane
from .helpers import is_inside_bounds as is_inside_bounds
from .helpers import is_pyvista_dataset as is_pyvista_dataset
from .helpers import wrap as wrap
from .misc import AnnotatedIntEnum as AnnotatedIntEnum
from .misc import abstract_class as abstract_class
from .misc import assert_empty_kwargs as assert_empty_kwargs
from .misc import check_valid_vector as check_valid_vector
from .misc import conditional_decorator as conditional_decorator
from .misc import has_module as has_module
from .misc import threaded as threaded
from .misc import try_callback as try_callback
from .observers import Observer as Observer
from .observers import ProgressMonitor as ProgressMonitor
from .observers import VtkErrorCatcher as VtkErrorCatcher
from .observers import send_errors_to_logging as send_errors_to_logging
from .observers import set_error_output_file as set_error_output_file
from .parametric_objects import KochanekSpline as KochanekSpline
from .parametric_objects import ParametricBohemianDome as ParametricBohemianDome
from .parametric_objects import ParametricBour as ParametricBour
from .parametric_objects import ParametricBoy as ParametricBoy
from .parametric_objects import ParametricCatalanMinimal as ParametricCatalanMinimal
from .parametric_objects import ParametricConicSpiral as ParametricConicSpiral
from .parametric_objects import ParametricCrossCap as ParametricCrossCap
from .parametric_objects import ParametricDini as ParametricDini
from .parametric_objects import ParametricEllipsoid as ParametricEllipsoid
from .parametric_objects import ParametricEnneper as ParametricEnneper
from .parametric_objects import ParametricFigure8Klein as ParametricFigure8Klein
from .parametric_objects import ParametricHenneberg as ParametricHenneberg
from .parametric_objects import ParametricKlein as ParametricKlein
from .parametric_objects import ParametricKuen as ParametricKuen
from .parametric_objects import ParametricMobius as ParametricMobius
from .parametric_objects import ParametricPluckerConoid as ParametricPluckerConoid
from .parametric_objects import ParametricPseudosphere as ParametricPseudosphere
from .parametric_objects import ParametricRandomHills as ParametricRandomHills
from .parametric_objects import ParametricRoman as ParametricRoman
from .parametric_objects import ParametricSuperEllipsoid as ParametricSuperEllipsoid
from .parametric_objects import ParametricSuperToroid as ParametricSuperToroid
from .parametric_objects import ParametricTorus as ParametricTorus
from .parametric_objects import Spline as Spline
from .parametric_objects import parametric_keywords as parametric_keywords
from .parametric_objects import surface_from_para as surface_from_para
from .points import fit_line_to_points as fit_line_to_points
from .points import fit_plane_to_points as fit_plane_to_points
from .points import line_segments_from_points as line_segments_from_points
from .points import lines_from_points as lines_from_points
from .points import make_tri_mesh as make_tri_mesh
from .points import principal_axes as principal_axes
from .points import vector_poly_data as vector_poly_data
from .points import vtk_points as vtk_points
from .reader import AVSucdReader as AVSucdReader
from .reader import BaseReader as BaseReader
from .reader import BinaryMarchingCubesReader as BinaryMarchingCubesReader
from .reader import BMPReader as BMPReader
from .reader import BYUReader as BYUReader
from .reader import CGNSReader as CGNSReader
from .reader import DEMReader as DEMReader
from .reader import DICOMReader as DICOMReader
from .reader import EnSightReader as EnSightReader
from .reader import ExodusIIReader as ExodusIIReader
from .reader import FacetReader as FacetReader
from .reader import FLUENTCFFReader as FLUENTCFFReader
from .reader import FluentReader as FluentReader
from .reader import GambitReader as GambitReader
from .reader import GaussianCubeReader as GaussianCubeReader
from .reader import GESignaReader as GESignaReader
from .reader import GIFReader as GIFReader
from .reader import GLTFReader as GLTFReader
from .reader import HDFReader as HDFReader
from .reader import HDRReader as HDRReader
from .reader import JPEGReader as JPEGReader
from .reader import MetaImageReader as MetaImageReader
from .reader import MFIXReader as MFIXReader
from .reader import MINCImageReader as MINCImageReader
from .reader import MultiBlockPlot3DReader as MultiBlockPlot3DReader
from .reader import Nek5000Reader as Nek5000Reader
from .reader import NIFTIReader as NIFTIReader
from .reader import NRRDReader as NRRDReader
from .reader import OBJReader as OBJReader
from .reader import OpenFOAMReader as OpenFOAMReader
from .reader import ParticleReader as ParticleReader
from .reader import PDBReader as PDBReader
from .reader import Plot3DFunctionEnum as Plot3DFunctionEnum
from .reader import Plot3DMetaReader as Plot3DMetaReader
from .reader import PLYReader as PLYReader
from .reader import PNGReader as PNGReader
from .reader import PNMReader as PNMReader
from .reader import PointCellDataSelection as PointCellDataSelection
from .reader import POpenFOAMReader as POpenFOAMReader
from .reader import ProStarReader as ProStarReader
from .reader import PTSReader as PTSReader
from .reader import PVDDataSet as PVDDataSet
from .reader import PVDReader as PVDReader
from .reader import SegYReader as SegYReader
from .reader import SLCReader as SLCReader
from .reader import STLReader as STLReader
from .reader import TecplotReader as TecplotReader
from .reader import TIFFReader as TIFFReader
from .reader import TimeReader as TimeReader
from .reader import VTKDataSetReader as VTKDataSetReader
from .reader import VTKPDataSetReader as VTKPDataSetReader
from .reader import XdmfReader as XdmfReader
from .reader import XMLImageDataReader as XMLImageDataReader
from .reader import XMLMultiBlockDataReader as XMLMultiBlockDataReader
from .reader import XMLPartitionedDataSetReader as XMLPartitionedDataSetReader
from .reader import XMLPImageDataReader as XMLPImageDataReader
from .reader import XMLPolyDataReader as XMLPolyDataReader
from .reader import XMLPRectilinearGridReader as XMLPRectilinearGridReader
from .reader import XMLPUnstructuredGridReader as XMLPUnstructuredGridReader
from .reader import XMLRectilinearGridReader as XMLRectilinearGridReader
from .reader import XMLStructuredGridReader as XMLStructuredGridReader
from .reader import XMLUnstructuredGridReader as XMLUnstructuredGridReader
from .reader import get_reader as get_reader
from .transform import Transform as Transform
