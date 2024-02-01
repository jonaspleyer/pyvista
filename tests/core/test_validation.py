from collections import namedtuple
from numbers import Real
from re import escape
import sys
from typing import Union, get_args, get_origin

import numpy as np
import pytest
from vtk import vtkTransform

from pyvista.core import pyvista_ndarray
from pyvista.core.utilities.arrays import cast_to_tuple_array, vtkmatrix_from_array
from pyvista.core.validation import (
    check_contains,
    check_finite,
    check_greater_than,
    check_instance,
    check_integerlike,
    check_iterable,
    check_iterable_items,
    check_length,
    check_less_than,
    check_nonnegative,
    check_number,
    check_numeric,
    check_range,
    check_real,
    check_scalar,
    check_sequence,
    check_shape,
    check_sorted,
    check_string,
    check_subdtype,
    check_type,
    validate_array,
    validate_array3,
    validate_arrayN,
    validate_arrayN_uintlike,
    validate_arrayNx3,
    validate_axes,
    validate_data_range,
    validate_number,
    validate_transform3x3,
    validate_transform4x4,
)
from pyvista.core.validation._array_wrapper import (
    _ArrayLikeWrapper,
    _NumberWrapper,
    _NumpyArrayWrapper,
    _Sequence1DWrapper,
    _Sequence2DWrapper,
)
from pyvista.core.validation.check import _validate_shape_value
from pyvista.core.validation.validate import _set_default_kwarg_mandatory


@pytest.mark.parametrize(
    'transform_like',
    [
        np.eye(3),
        np.eye(4),
        np.eye(3).tolist(),
        np.eye(4).tolist(),
        vtkmatrix_from_array(np.eye(3)),
        vtkmatrix_from_array(np.eye(4)),
        vtkTransform(),
    ],
)
def test_validate_transform4x4(transform_like):
    result = validate_transform4x4(transform_like)
    assert type(result) is np.ndarray
    assert np.array_equal(result, np.eye(4))


def test_validate_transform4x4_raises():
    with pytest.raises(TypeError, match=escape("Input transform must be one of")):
        validate_transform4x4(np.array([1, 2, 3]))
    with pytest.raises(TypeError, match="must have real numbers"):
        validate_transform4x4("abc")


@pytest.mark.parametrize(
    'transform_like',
    [
        np.eye(3),
        np.eye(3).tolist(),
        vtkmatrix_from_array(np.eye(3)),
    ],
)
def test_validate_transform3x3(transform_like):
    result = validate_transform3x3(transform_like)
    assert type(result) is np.ndarray
    assert np.array_equal(result, np.eye(3))


def test_validate_transform3x3_raises():
    with pytest.raises(TypeError, match=escape("Input transform must be one of")):
        validate_transform3x3(np.array([1, 2, 3]))
    with pytest.raises(TypeError, match="must have real numbers."):
        validate_transform3x3("abc")


def test_check_subdtype():
    check_subdtype(int, np.integer)
    check_subdtype(np.dtype(int), np.integer)
    check_subdtype(np.array([1, 2, 3]), np.integer)
    check_subdtype([1.0, 2, 3], float)
    check_subdtype(np.array([1.0, 2, 3], dtype='uint8'), 'uint8')
    check_subdtype(np.array([1.0, 2, 3]), ('uint8', float))
    msg = "Input has incorrect dtype of dtype('int32'). The dtype must be a subtype of <class 'float'>."
    with pytest.raises(TypeError, match=escape(msg)):
        check_subdtype(np.array([1, 2, 3]).astype('int32'), float)
    msg = "Input has incorrect dtype of dtype('complex128'). The dtype must be a subtype of at least one of \n(<class 'numpy.integer'>, <class 'numpy.floating'>)."
    with pytest.raises(TypeError, match=escape(msg)):
        check_subdtype(np.array([1 + 1j, 2, 3]), (np.integer, np.floating))


def test_check_subdtype_changes_type():
    # test coercing some types (e.g. np.number) can lead to unexpected
    # failed `np.issubtype` checks due to an implicit change of type
    int_array = np.array([1, 2, 3])
    dtype_expected = np.number
    check_subdtype(int_array, dtype_expected)  # int is subtype of np.number

    dtype_coerced = np.dtype(dtype_expected)
    assert dtype_coerced.type is np.float64  # np.number is coerced (by NumPy) as a float
    with pytest.raises(TypeError):
        # this check will now fail since int is not subtype of float
        check_subdtype(int_array, dtype_coerced)


def test_validate_number():
    validate_number([2.0])
    num = validate_number(1)
    assert num == 1
    assert isinstance(num, int)

    num = validate_number(2.0, to_list=False, must_have_shape=(), reshape=False)
    assert num == 2.0
    assert type(num) is np.ndarray
    assert num.dtype.type is np.float64

    msg = (
        "Parameter 'must_have_shape' cannot be set for function `validate_number`.\n"
        "Its value is automatically set to `()`."
    )
    with pytest.raises(ValueError, match=escape(msg)):
        validate_number(1, must_have_shape=2, reshape=False)


def test_validate_data_range():
    rng = validate_data_range([0, 1])
    assert rng == (0, 1)

    rng = validate_data_range((0, 2.5), to_list=True)
    assert rng == [0.0, 2.5]

    rng = validate_data_range((-10, -10), to_tuple=False, must_have_shape=2)
    assert type(rng) is np.ndarray

    msg = "Data Range [1 0] must be sorted in ascending order."
    with pytest.raises(ValueError, match=escape(msg)):
        validate_data_range((1, 0))

    msg = (
        "Parameter 'must_have_shape' cannot be set for function `validate_data_range`.\n"
        "Its value is automatically set to `2`."
    )
    with pytest.raises(ValueError, match=msg):
        validate_data_range((0, 1), must_have_shape=3)


def test_set_default_kwarg_mandatory():
    default_value = 1
    default_key = 'k'

    # Test parameter unset
    kwargs = {}
    _set_default_kwarg_mandatory(kwargs, default_key, default_value)
    assert kwargs[default_key] == default_value

    # Test parameter already set to default
    kwargs = {}
    kwargs[default_key] = default_value
    _set_default_kwarg_mandatory(kwargs, default_key, default_value)
    assert kwargs[default_key] == default_value

    # Test parameter set to non-default
    kwargs = {}
    kwargs[default_key] = default_value * 2
    msg = (
        "Parameter 'k' cannot be set for function `test_set_default_kwarg_mandatory`.\n"
        "Its value is automatically set to `1`."
    )
    with pytest.raises(ValueError, match=msg):
        _set_default_kwarg_mandatory(kwargs, default_key, default_value)


def test_check_shape():
    check_shape(0, ())
    check_shape(0, [(), 2])
    check_shape((1, 2, 3), [(), 3])
    check_shape((1, 2, 3), [-1])
    check_shape((1, 2, 3), -1)

    msg = 'Input has shape (3,) which is not allowed. Shape must be 0.'
    with pytest.raises(ValueError, match=escape(msg)):
        check_shape((1, 2, 3), 0, name="Input")

    msg = 'Array has shape (3,) which is not allowed. Shape must be one of [(), (4, 5)].'
    with pytest.raises(ValueError, match=escape(msg)):
        check_shape((1, 2, 3), [(), (4, 5)])


def test_validate_shape_value():
    msg = "`None` is not a valid shape. Use `()` instead."
    with pytest.raises(TypeError, match=escape(msg)):
        _validate_shape_value(None)
    shape = _validate_shape_value(())
    assert shape == ()
    shape = _validate_shape_value(1)
    assert shape == (1,)
    shape = _validate_shape_value(-1)
    assert shape == (-1,)
    shape = _validate_shape_value((1, 2, 3))
    assert shape == (
        1,
        2,
        3,
    )
    shape = _validate_shape_value((-1, 2, -1))
    assert shape == (-1, 2, -1)

    msg = (
        "Shape must be an instance of any type (<class 'int'>, <class 'tuple'>). "
        "Got <class 'float'> instead."
    )
    with pytest.raises(TypeError, match=escape(msg)):
        _validate_shape_value(1.0)

    msg = "Shape values must all be greater than or equal to -1."
    with pytest.raises(ValueError, match=msg):
        _validate_shape_value(-2)

    msg = "All items of Shape must be an instance of <class 'int'>. " "Got <class 'tuple'> instead."
    with pytest.raises(TypeError, match=msg):
        _validate_shape_value(((1, 2), (3, 4)))


@pytest.mark.parametrize('reshape', [True, False])
def test_validate_arrayNx3(reshape):
    arr = validate_arrayNx3((1, 2, 3))
    assert arr.shape == (1, 3)
    assert np.array_equal(arr, [[1, 2, 3]])

    if not reshape:
        msg = "Array has shape (3,) which is not allowed. Shape must be (-1, 3)."
        with pytest.raises(ValueError, match=escape(msg)):
            validate_arrayNx3((1, 2, 3), reshape=False)

    arr = validate_arrayNx3([(1, 2, 3), (4, 5, 6)], reshape=reshape)
    assert arr.shape == (2, 3)

    msg = (
        "Parameter 'must_have_shape' cannot be set for function `validate_arrayNx3`.\n"
        "Its value is automatically set to `[3, (-1, 3)]`."
    )
    with pytest.raises(ValueError, match=escape(msg)):
        validate_arrayNx3((1, 2, 3), must_have_shape=1)
    msg = "Array has shape () which is not allowed. Shape must be one of [3, (-1, 3)]."
    with pytest.raises(ValueError, match=escape(msg)):
        validate_arrayNx3(0)
    with pytest.raises(ValueError, match="_input"):
        validate_arrayNx3([1, 2, 3, 4], name="_input")


@pytest.mark.parametrize('reshape', [True, False])
def test_validate_arrayN(reshape):
    # test 0D input is reshaped to 1D by default
    arr = validate_arrayN(0)
    assert arr.shape == (1,)
    assert np.array_equal(arr, [0])

    # test 2D input is reshaped to 1D by default
    arr = validate_arrayN([[1, 2, 3]])
    assert arr.shape == (3,)
    assert np.array_equal(arr, [1, 2, 3])

    arr = validate_arrayN([[1], [2], [3]])
    assert arr.shape == (3,)
    assert np.array_equal(arr, [1, 2, 3])

    if not reshape:
        msg = 'Array has shape () which is not allowed. Shape must be -1.'
        with pytest.raises(ValueError, match=escape(msg)):
            validate_arrayN(0, reshape=False)

        msg = 'Array has shape (1, 3) which is not allowed. Shape must be -1.'
        with pytest.raises(ValueError, match=escape(msg)):
            validate_arrayN([[1, 2, 3]], reshape=False)

    arr = validate_arrayN((1, 2, 3, 4, 5, 6), reshape=reshape)
    assert arr.shape == (6,)

    msg = (
        "Parameter 'must_have_shape' cannot be set for function `validate_arrayN`.\n"
        "Its value is automatically set to `[(), -1, (1, -1), (-1, 1)]`."
    )
    with pytest.raises(ValueError, match=escape(msg)):
        validate_arrayN((1, 2, 3), must_have_shape=1)

    msg = 'Array has shape (2, 2) which is not allowed. Shape must be one of [(), -1, (1, -1), (-1, 1)].'
    with pytest.raises(ValueError, match=escape(msg)):
        validate_arrayN(((1, 2), (3, 4)))
    with pytest.raises(ValueError, match="_input"):
        validate_arrayN(((1, 2), (3, 4)), name="_input")


@pytest.mark.parametrize('reshape', [True, False])
def test_validate_arrayN_uintlike(reshape):
    # test 0D input is reshaped to 1D by default
    arr = validate_arrayN_uintlike(0.0)
    assert arr.shape == (1,)
    assert np.array_equal(arr, [0])
    assert arr.dtype.type is np.int32 or arr.dtype.type is np.int64

    arr = validate_arrayN_uintlike(0.0, dtype_out='uint8')
    assert arr.dtype.type is np.uint8

    with pytest.raises(ValueError, match="Shape must be -1."):
        validate_arrayN_uintlike(0.0, reshape=False)

    msg = '_input values must all be greater than or equal to 0.'
    with pytest.raises(ValueError, match=msg):
        validate_arrayN_uintlike([-1, 1], name="_input")


@pytest.mark.parametrize('reshape', [True, False])
def test_validate_array3(reshape):
    # test 0D input is reshaped to len-3 1D vector with broadcasting enabled
    arr = validate_array3(0, broadcast=True)
    assert arr.shape == (3,)
    assert np.array_equal(arr, [0, 0, 0])

    # test 2D input is reshaped to 1D by default
    arr = validate_array3([[1, 2, 3]])
    assert arr.shape == (3,)
    assert np.array_equal(arr, [1, 2, 3])

    arr = validate_array3([[1], [2], [3]])
    assert arr.shape == (3,)
    assert np.array_equal(arr, [1, 2, 3])

    if not reshape:
        # test check fails with 2D input and no reshape
        msg = 'Array has shape (1, 3) which is not allowed. Shape must be (3,).'
        with pytest.raises(ValueError, match=escape(msg)):
            validate_array3([[1, 2, 3]], reshape=reshape)

        # test correct shape with broadcast and no reshape
        msg = "Shape must be one of [(3,), (), (1,)]."
        with pytest.raises(ValueError, match=escape(msg)):
            validate_array3((1, 2, 3, 4, 5, 6), reshape=reshape, broadcast=True)
    else:
        # test error msg shows correct shape with broadcast and with reshape
        msg = "Shape must be one of [(3,), (1, 3), (3, 1), (), (1,)]"
        with pytest.raises(ValueError, match=escape(msg)):
            validate_array3((1, 2, 3, 4, 5, 6), reshape=reshape, broadcast=True)

    # test shape cannot be overridden
    msg = (
        "Parameter 'must_have_shape' cannot be set for function `validate_array3`.\n"
        "Its value is automatically set to `[(3,), (1, 3), (3, 1)]`."
    )
    with pytest.raises(ValueError, match=escape(msg)):
        validate_array3((1, 2, 3), must_have_shape=3)


def test_check_range():
    check_range((1, 2, 3), [1, 3])

    msg = "Array values must all be less than or equal to 2."
    with pytest.raises(ValueError, match=msg):
        check_range((1, 2, 3), [1, 2])

    msg = "Input values must all be greater than or equal to 2."
    with pytest.raises(ValueError, match=msg):
        check_range((1, 2, 3), [2, 3], name='Input')

    # Test strict bounds
    msg = "Array values must all be less than 3."
    with pytest.raises(ValueError, match=msg):
        check_range((1, 2, 3), [1, 3], strict_upper=True)

    msg = "Array values must all be greater than 1."
    with pytest.raises(ValueError, match=msg):
        check_range((1, 2, 3), [1, 3], strict_lower=True)


def numeric_array_test_cases():
    Case = namedtuple("Case", ["kwarg", "valid_array", "invalid_array", "error_type", "error_msg"])
    return (
        Case(
            dict(
                must_be_finite=True, must_be_real=False
            ),  # must be real is only added for extra coverage
            0,
            np.inf,
            ValueError,
            'must have finite values',
        ),
        Case(dict(must_be_real=True), 0, 1 + 1j, TypeError, 'must have real numbers'),
        Case(
            dict(must_be_integer_like=True), 0.0, 0.1, ValueError, 'must have integer-like values'
        ),
        Case(dict(must_be_sorted=True), [0, 1], [1, 0], ValueError, 'must be sorted'),
        Case(
            dict(must_be_sorted=dict(ascending=True, strict=False, axis=-1)),
            [0, 1],
            [1, 0],
            ValueError,
            'must be sorted',
        ),
    )


@pytest.mark.parametrize('name', ["_array", "_input"])
@pytest.mark.parametrize('copy', [True, False])
@pytest.mark.parametrize('as_any', [True, False])
@pytest.mark.parametrize('to_list', [True, False])
@pytest.mark.parametrize('to_tuple', [True, False])
@pytest.mark.parametrize('dtype_out', [np.float32, np.float64])
@pytest.mark.parametrize('case', numeric_array_test_cases())
@pytest.mark.parametrize('stack_input', [True, False])
@pytest.mark.parametrize('input_type', [tuple, list, np.ndarray, pyvista_ndarray])
def test_validate_array(
    name, copy, as_any, to_list, to_tuple, dtype_out, case, stack_input, input_type
):
    # Set up
    valid_array = np.array(case.valid_array)
    invalid_array = np.array(case.invalid_array)

    # Inputs may be scalar, use stacking to ensure we have test cases
    # with multidimensional arrays
    if stack_input:
        valid_array = np.stack((valid_array, valid_array), axis=0)
        valid_array = np.stack((valid_array, valid_array), axis=1)
        invalid_array = np.stack((invalid_array, invalid_array), axis=0)
        invalid_array = np.stack((invalid_array, invalid_array), axis=1)

    if input_type is tuple:
        valid_array = cast_to_tuple_array(valid_array)
        invalid_array = cast_to_tuple_array(invalid_array)
    elif input_type is list:
        valid_array = valid_array.tolist()
        invalid_array = invalid_array.tolist()
    elif input_type is np.ndarray:
        valid_array = np.asarray(valid_array)
        invalid_array = np.asarray(invalid_array)
    else:  # pyvista_ndarray:
        valid_array = pyvista_ndarray(valid_array)
        invalid_array = pyvista_ndarray(invalid_array)

    shape = np.array(valid_array).shape
    common_kwargs = dict(
        **case.kwarg,
        name=name,
        copy=copy,
        as_any=as_any,
        to_list=to_list,
        to_tuple=to_tuple,
        must_have_dtype=np.number,
        dtype_out=dtype_out,
        must_have_length=range(np.array(valid_array).size + 1),
        must_have_min_length=1,
        must_have_max_length=np.array(valid_array).size,
        must_have_shape=shape,
        reshape_to=shape,
        broadcast_to=shape,
        must_be_in_range=(np.min(valid_array), np.max(valid_array)),
        must_be_nonnegative=np.all(np.array(valid_array) > 0),
    )

    # Test raises correct error with invalid input
    with pytest.raises(case.error_type, match=case.error_msg):
        validate_array(invalid_array, **common_kwargs)
    # Test error has correct name
    with pytest.raises(case.error_type, match=name):
        validate_array(invalid_array, **common_kwargs)

    # Test no error with valid input
    array_in = valid_array
    array_out = validate_array(array_in, **common_kwargs)
    assert np.array_equal(array_out, array_in)

    # Check output
    if np.array(array_in).ndim == 0 and (to_tuple or to_list):
        # test scalar input results in scalar output
        assert isinstance(array_out, float) or isinstance(array_out, int)
    elif to_tuple:
        assert type(array_out) is tuple
    elif to_list:
        assert isinstance(array_out, list)
    else:
        assert isinstance(array_out, np.ndarray)
        assert array_out.dtype.type is dtype_out
        if as_any:
            if input_type is pyvista_ndarray:
                assert type(array_out) is pyvista_ndarray
            elif input_type is np.ndarray:
                assert type(array_out) is np.ndarray
            if (
                not copy
                and isinstance(array_in, np.ndarray)
                and np.dtype(dtype_out) is array_in.dtype
            ):
                assert array_out is array_in
            else:
                assert array_out is not array_in
        else:
            assert type(array_out) is np.ndarray

    if copy:
        assert array_out is not array_in


@pytest.mark.parametrize('obj', [0, 0.0, "0"])
@pytest.mark.parametrize('classinfo', [int, (int, float), [int, float]])
@pytest.mark.parametrize('allow_subclass', [True, False])
@pytest.mark.parametrize('name', ["_input", "_object"])
def test_check_instance(obj, classinfo, allow_subclass, name):
    if isinstance(classinfo, list):
        with pytest.raises(TypeError):
            check_instance(obj, classinfo)
        return

    if allow_subclass:
        if isinstance(obj, classinfo):
            check_instance(obj, classinfo)
        else:
            with pytest.raises(TypeError, match='Object must be an instance of'):
                check_instance(obj, classinfo)
            with pytest.raises(TypeError, match=f'{name} must be an instance of'):
                check_instance(obj, classinfo, name=name)

    else:
        if type(classinfo) is tuple:
            if type(obj) in classinfo:
                check_type(obj, classinfo)
            else:
                with pytest.raises(TypeError, match=f'{name} must have one of the following types'):
                    check_type(obj, classinfo, name=name)
                with pytest.raises(TypeError, match='Object must have one of the following types'):
                    check_type(obj, classinfo)
        elif get_origin(classinfo) is Union:
            if type(obj) in get_args(classinfo):
                check_type(obj, classinfo)
            else:
                with pytest.raises(TypeError, match=f'{name} must have one of the following types'):
                    check_type(obj, classinfo, name=name)
                with pytest.raises(TypeError, match='Object must have one of the following types'):
                    check_type(obj, classinfo)
        else:
            if type(obj) is classinfo:
                check_type(obj, classinfo)
            else:
                with pytest.raises(TypeError, match=f'{name} must have type'):
                    check_type(obj, classinfo, name=name)
                with pytest.raises(TypeError, match='Object must have type'):
                    check_type(obj, classinfo)

    msg = "Name must be a string, got <class 'int'> instead."
    with pytest.raises(TypeError, match=msg):
        check_instance(0, int, name=0)


def test_check_type():
    check_type(0, int, name='abc')
    check_type(0, Union[int])
    with pytest.raises(TypeError):
        check_type("str", int)
    with pytest.raises(TypeError):
        check_type(0, int, name=1)
        check_type(0, Union[int, float])


@pytest.mark.skipif(
    sys.version_info < (3, 10), reason="Union type input requires python3.10 or higher"
)
def test_check_type_union():
    check_type(0, Union[int, float])


def test_check_string():
    check_string("abc")
    check_string("abc", name='123')
    msg = "Value must be an instance of <class 'str'>. Got <class 'int'> instead."
    with pytest.raises(TypeError, match=msg):
        check_string(0, name='Value')
    msg = "Object must be an instance of <class 'str'>. Got <class 'int'> instead."
    with pytest.raises(TypeError, match=msg):
        check_string(0)
    msg = "Name must be a string, got <class 'float'> instead."
    with pytest.raises(TypeError, match=msg):
        check_string("abc", name=0.0)

    class str_subclass(str):
        pass

    check_string(str_subclass(), allow_subclass=True)
    with pytest.raises(TypeError, match="Object must have type <class 'str'>."):
        check_string(str_subclass(), allow_subclass=False)


def test_check_less_than():
    check_less_than([0], 1)
    check_less_than(np.eye(3), 1, strict=False)
    msg = "Array values must all be less than 0."
    with pytest.raises(ValueError, match=msg):
        check_less_than(0, 0, strict=True)
    msg = "_input values must all be less than or equal to 0."
    with pytest.raises(ValueError, match=msg):
        check_less_than(1, 0, strict=False, name="_input")


def test_check_greater_than():
    check_greater_than([1], 0)
    check_greater_than(np.eye(3), 0, strict=False)
    msg = "Array values must all be greater than 0."
    with pytest.raises(ValueError, match=msg):
        check_greater_than(0, 0, strict=True)
    msg = "_input values must all be greater than or equal to 0."
    with pytest.raises(ValueError, match=msg):
        check_greater_than(-1, 0, strict=False, name="_input")


def test_check_real():
    check_real(1)
    check_real(-2.0)
    check_real(np.array(-2.0, dtype="uint8"))
    msg = 'Array must have real numbers.'
    with pytest.raises(TypeError, match=msg):
        check_real(1 + 1j)
    msg = '_input must have real numbers.'
    with pytest.raises(TypeError, match=msg):
        check_real(1 + 1j, name="_input")


def test_check_numeric():
    check_numeric(1)
    check_numeric(-2.0)
    check_numeric(np.array(-2.0, dtype="uint8"))
    msg = 'Array must be numeric.'
    with pytest.raises(TypeError, match=msg):
        check_numeric('abc')
    msg = '_input must be numeric.'
    with pytest.raises(TypeError, match=msg):
        check_numeric(tuple('s'), name="_input")


def test_check_finite():
    check_finite(0)
    msg = '_input must have finite values.'
    with pytest.raises(ValueError, match=msg):
        check_finite(np.nan, name="_input")


def test_check_integerlike():
    check_integerlike(1)
    check_integerlike([2, 3.0])
    msg = "Input has incorrect dtype of <class 'float'>. The dtype must be a subtype of <class 'numpy.integer'>."
    with pytest.raises(TypeError, match=msg):
        check_integerlike([2, 3.0], strict=True, name="_input")
    msg = "_input must have integer-like values."
    with pytest.raises(ValueError, match=msg):
        check_integerlike([2, 3.4], strict=False, name="_input")


def test_check_sequence():
    check_sequence((1,), name='abc')
    check_sequence(range(3))
    check_sequence("abc")
    with pytest.raises(TypeError, match="_input"):
        check_sequence(np.array(1), name="_input")


def test_check_iterable():
    check_iterable((1,), name='abc')
    check_iterable(range(3))
    check_iterable("abc")
    check_iterable(np.array(1))
    with pytest.raises(TypeError, match="_input"):
        check_iterable(1, name="_input")


def test_check_length():
    check_length((1,))
    check_length(
        [
            1,
        ]
    )
    check_length(np.ndarray((1,)))
    check_length((1,), exact_length=1, min_length=1, max_length=1, must_be_1d=True)
    check_length((1,), exact_length=[1, 2.0])

    with pytest.raises(ValueError, match="'exact_length' must have integer-like values."):
        check_length((1,), exact_length=(1, 2.4), name="_input")

    msg = '_input must have a length equal to any of: 1. Got length 2 instead.'
    with pytest.raises(ValueError, match=msg):
        check_length((1, 2), exact_length=1, name="_input")
    msg = '_input must have a length equal to any of: [3 4]. Got length 2 instead.'
    with pytest.raises(ValueError, match=escape(msg)):
        check_length((1, 2), exact_length=[3, 4], name="_input")

    msg = "_input must have a maximum length of 1. Got length 2 instead."
    with pytest.raises(ValueError, match=msg):
        check_length((1, 2), max_length=1, name="_input")

    msg = "_input must have a minimum length of 2. Got length 1 instead."
    with pytest.raises(ValueError, match=msg):
        check_length((1,), min_length=2, name="_input")

    msg = "Range [4 2] must be sorted in ascending order."
    with pytest.raises(ValueError, match=escape(msg)):
        check_length(
            (
                1,
                2,
                3,
            ),
            min_length=4,
            max_length=2,
        )

    msg = "Shape must be -1."
    with pytest.raises(ValueError, match=escape(msg)):
        check_length(((1, 2), (3, 4)), must_be_1d=True)


def test_check_nonnegative():
    check_nonnegative(0)
    check_nonnegative(np.eye(3))
    msg = "Array values must all be greater than or equal to 0."
    with pytest.raises(ValueError, match=msg):
        check_nonnegative(-1)


@pytest.mark.parametrize('shape', [(), (8,), (4, 6), (2, 3, 4)])
@pytest.mark.parametrize('axis', [None, -1, -2, -3, 0, 1, 2, 3])
@pytest.mark.parametrize('ascending', [True, False])
@pytest.mark.parametrize('strict', [True, False])
def test_check_sorted(shape, axis, ascending, strict):
    def _check_sorted_params(arr):
        check_sorted(arr, axis=axis, strict=strict, ascending=ascending)

    if shape == ():
        # test always succeeds with scalar
        _check_sorted_params(0)
        return

    # Create ascending array with unique values
    num_elements = np.prod(shape)
    arr_strict_ascending = np.arange(num_elements).reshape(shape)

    # needed to support numpy <1.25
    # needed to support vtk 9.0.3
    # check for removal when support for vtk 9.0.3 is removed
    try:
        AxisError = np.exceptions.AxisError
    except AttributeError:
        AxisError = np.AxisError

    try:
        # Create ascending array with duplicate values
        arr_ascending = np.repeat(arr_strict_ascending, 2, axis=axis)
        # Create descending arrays
        arr_descending = np.flip(arr_ascending, axis=axis)
        arr_strict_descending = np.flip(arr_strict_ascending, axis=axis)
    except AxisError:
        # test ValueError is raised whenever an AxisError would otherwise be raised
        with pytest.raises(
            ValueError, match=f'Axis {axis} is out of bounds for ndim {arr_strict_ascending.ndim}'
        ):
            _check_sorted_params(arr_strict_ascending)
        return

    if axis is None and arr_ascending.ndim > 1:
        # test that axis=None will flatten array and cause it not to be sorted for higher dimension arrays
        with pytest.raises(ValueError):
            _check_sorted_params(arr_ascending)
        return

    if strict and ascending:
        _check_sorted_params(arr_strict_ascending)
        for a in [arr_ascending, arr_descending, arr_strict_descending]:
            with pytest.raises(ValueError, match="must be sorted in strict ascending order"):
                _check_sorted_params(a)

    elif not strict and ascending:
        _check_sorted_params(arr_ascending)
        _check_sorted_params(arr_strict_ascending)
        for a in [arr_descending, arr_strict_descending]:
            with pytest.raises(ValueError, match="must be sorted in ascending order"):
                _check_sorted_params(a)

    elif strict and not ascending:
        _check_sorted_params(arr_strict_descending)
        for a in [arr_ascending, arr_strict_ascending, arr_descending]:
            with pytest.raises(ValueError, match="must be sorted in strict descending order"):
                _check_sorted_params(a)

    elif not strict and not ascending:
        _check_sorted_params(arr_descending)
        _check_sorted_params(arr_strict_descending)
        for a in [arr_ascending, arr_strict_ascending]:
            with pytest.raises(ValueError, match="must be sorted in descending order"):
                _check_sorted_params(a)


def test_check_iterable_items():
    check_iterable_items([1, 2, 3], int)
    check_iterable_items(("a", "b", "c"), str)
    check_iterable_items("abc", str)
    check_iterable_items(range(10), int)
    msg = "All items of Iterable must be an instance of <class 'str'>. Got <class 'int'> instead."
    with pytest.raises(TypeError, match=escape(msg)):
        check_iterable_items(["abc", 1], str)
    with pytest.raises(TypeError, match="All items of _input"):
        check_iterable_items(["abc", 1], str, name="_input")


@pytest.mark.parametrize('number', [1, 1.0, True, 1 + 1j])
@pytest.mark.parametrize('definition', ['builtin', 'numpy'])
@pytest.mark.parametrize('must_be_real', [True, False])
def test_check_number(number, definition, must_be_real):
    if definition == 'numpy':
        number = np.array([number])[0]

    if isinstance(number, np.bool_) or (not isinstance(number, Real) and must_be_real):
        # Test bool types always raise an error
        # Test complex types raise an error when `must_be_real` is True
        with pytest.raises(TypeError):
            check_number(number, must_be_real=must_be_real)
    else:
        # All other cases should succeed
        check_number(number, must_be_real=must_be_real)

    if definition == 'numpy':
        # Test numpy types raise an error when definition is 'builtin'
        if isinstance(number, float) or (isinstance(number, complex) and not must_be_real):
            # np.float_ and np.complex_ subclass float and complex, respectively,
            # so no error is raised
            check_number(number, must_be_real=must_be_real, definition='builtin')
        else:
            with pytest.raises(TypeError):
                check_number(number, must_be_real=must_be_real, definition='builtin')
    elif definition == 'builtin':
        # Test builtin types raise an error when definition is 'numpy'
        with pytest.raises(TypeError):
            check_number(number, must_be_real=must_be_real, definition='numpy')


def test_check_number_raises():
    msg = (
        "_input must be an instance of <class 'numbers.Real'>. Got <class 'numpy.ndarray'> instead."
    )
    with pytest.raises(TypeError, match=msg):
        check_number(np.array(0), name='_input')
    msg = "Object must be"
    with pytest.raises(TypeError, match=msg):
        check_number(np.array(0))
    msg = "Object must be"
    with pytest.raises(TypeError, match=msg):
        check_number(1 + 1j, must_be_real=True)


def test_check_scalar():
    check_scalar(1)
    check_scalar(np.array(0))
    check_scalar(np.array(1 + 2j), must_be_real=False)

    msg = "Got <class 'list'> instead."
    with pytest.raises(TypeError, match=msg):
        check_scalar([1, 2])

    msg = "Scalar must be a 0-dimensional array, got `ndim=1` instead."
    with pytest.raises(ValueError, match=escape(msg)):
        check_scalar(np.array([1]))


def test_check_contains():
    check_contains("foo", ["foo", "bar"])
    msg = "Input 'foo' is not valid. Input must be one of: \n\t['cat', 'bar']"
    with pytest.raises(ValueError, match=escape(msg)):
        check_contains("foo", ["cat", "bar"])
    msg = "_input '5' is not valid. _input must be in: \n\trange(0, 4)"
    with pytest.raises(ValueError, match=escape(msg)):
        check_contains(5, range(4), name="_input")


@pytest.mark.parametrize('name', ['_input', 'Axes'])
def test_validate_axes(name):
    axes_right = np.eye(3)
    axes_left = np.array([[1, 0.0, 0], [0, 1, 0], [0, 0, -1]])

    # test different input args
    axes = validate_axes(axes_right)
    assert np.array_equal(axes, axes_right)
    axes = validate_axes(
        [[1], [0], [0]], [[0, 1, 0]], must_have_orientation='right', must_be_orthogonal=True
    )
    assert np.array_equal(axes, axes_right)
    axes = validate_axes([1, 0, 0], [[0, 1, 0]], (0, 0, 1))
    assert np.array_equal(axes, axes_right)
    assert np.issubdtype(axes.dtype, np.floating)

    axes = validate_axes(np.eye(3).astype(int))
    assert np.array_equal(axes, axes_right)
    assert np.issubdtype(axes.dtype, np.floating)

    # test bad input
    with pytest.raises(ValueError, match=f"{name} cannot be parallel."):
        validate_axes([[1, 0, 0], [1, 0, 0], [0, 1, 0]], name=name)
    with pytest.raises(ValueError, match="Axes cannot be parallel."):
        validate_axes([[0, 1, 0], [1, 0, 0], [0, 1, 0]])
    with pytest.raises(ValueError, match=f"{name} cannot be zeros."):
        validate_axes([[1, 0, 0], [0, 1, 0], [0, 0, 0]], name=name)
    with pytest.raises(ValueError, match="Axes cannot be zeros."):
        validate_axes([[1, 0, 0], [0, 0, 0], [0, 0, 1]])
    with pytest.raises(ValueError, match="Axes cannot be zeros."):
        validate_axes([[0, 0, 0], [0, 1, 0], [0, 0, 1]])

    # test normalize
    axes_scaled = axes_right * 2
    axes = validate_axes(axes_scaled, normalize=False)
    assert np.array_equal(axes, axes_scaled)
    axes = validate_axes(axes_scaled, normalize=True)
    assert np.array_equal(axes, axes_right)

    # test orientation
    validate_axes([1, 0, 0], [0, 1, 0], must_have_orientation='left')
    validate_axes(axes_left, must_have_orientation=None)
    validate_axes(axes_left, must_have_orientation='left')
    with pytest.raises(ValueError, match=f"{name} do not have a right-handed orientation."):
        validate_axes(axes_left, must_have_orientation='right', name=name)

    validate_axes(axes_right, must_have_orientation=None)
    validate_axes(axes_right, must_have_orientation='right')
    with pytest.raises(ValueError, match=f"{name} do not have a left-handed orientation."):
        validate_axes(axes_right, must_have_orientation='left', name=name)

    # test specifying two vectors without orientation raises error (3rd cannot be computed)
    with pytest.raises(
        ValueError, match=f"{name} orientation must be specified when only two vectors are given."
    ):
        validate_axes([1, 0, 0], [0, 1, 0], must_have_orientation=None, name=name)


@pytest.mark.parametrize('bias_index', [(0, 1), (1, 0), (2, 0)])
def test_validate_axes_orthogonal(bias_index):
    axes_right = np.eye(3)
    axes_right[bias_index[0], bias_index[1]] = 0.1
    axes_left = np.array([[1, 0.0, 0], [0, 1, 0], [0, 0, -1]])
    axes_left[bias_index[0], bias_index[1]] = 0.1

    msg = "Axes are not orthogonal."
    axes = validate_axes(
        axes_right, must_be_orthogonal=False, normalize=False, must_have_orientation='right'
    )
    assert np.array_equal(axes, axes_right)
    with pytest.raises(ValueError, match=msg):
        validate_axes(axes_right, must_be_orthogonal=True)

    axes = validate_axes(
        axes_left, must_be_orthogonal=False, normalize=False, must_have_orientation='left'
    )
    assert np.array_equal(axes, axes_left)
    with pytest.raises(ValueError, match=msg):
        validate_axes(axes_left, must_be_orthogonal=True)


arraylike_shapes = [
    (),
    (0,),
    (1,),
    (
        1,
        0,
    ),
    (1, 1, 0),
    (1, 1, 1, 0),
    (
        1,
        2,
    ),
    (1, 2, 3),
    (
        1,
        2,
        3,
        4,
    ),
]

ArrayLikePropsTuple = namedtuple(
    'ArrayLikeTuple', ['array', 'shape', 'dtype', 'ndim', 'wrapper', 'return_original']
)


from enum import Enum


class arraylike_types(Enum):
    Number = 0
    NumpyArraySequence = 1
    NumberSequence1D = 2
    NumberSequence2D = 2
    NumpyArray = 3


@pytest.mark.parametrize('arraylike_type', arraylike_types)
@pytest.mark.parametrize('shape_in', arraylike_shapes)
@pytest.mark.parametrize('dtype_in', [float, int, bool, np.float64, np.int_, np.bool_, np.uint8])
def test_array_wrappers(arraylike_type, shape_in, dtype_in):
    # Skip tests for impossible scalar cases
    is_scalar = shape_in == ()
    is_sequence_type = arraylike_type in [
        arraylike_types.NumpyArraySequence,
        arraylike_types.NumberSequence1D,
        arraylike_types.NumberSequence2D,
    ]
    is_scalar_type = arraylike_type is arraylike_types.Number
    if (is_scalar and is_sequence_type) or (not is_scalar and is_scalar_type):
        pytest.skip("Scalar cannot be a sequence")

    # Skip tests for sequences of numpy dtypes
    # This is done since sequences are generated using `array.tolist()`
    # which will cast numpy dtypes to builtin types (which are tested separately)
    if arraylike_type in [
        arraylike_types.NumberSequence1D,
        arraylike_types.NumberSequence2D,
    ] and issubclass(dtype_in, np.generic):
        pytest.skip("No tests for sequences of numpy dtypes.")

    # Set up test array and keep track of special empty sequence cases
    if is_scalar:
        initial_array = dtype_in(0)
        is_empty = False
    else:
        initial_array = np.zeros(shape=shape_in, dtype=dtype_in)
        is_empty = initial_array.shape[-1] == 0

    if arraylike_type is arraylike_types.Number:
        array_before_wrap = initial_array
        expected = ArrayLikePropsTuple(
            array=array_before_wrap,
            shape=shape_in,
            dtype=dtype_in,
            ndim=0,
            wrapper=_NumberWrapper,
            return_original=True,
        )
    elif arraylike_type is arraylike_types.NumpyArray:
        array_before_wrap = np.array(initial_array)
        expected = ArrayLikePropsTuple(
            array=array_before_wrap,
            shape=shape_in,
            dtype=np.dtype(dtype_in),
            ndim=array_before_wrap.ndim,
            wrapper=_NumpyArrayWrapper,
            return_original=True,
        )
    elif arraylike_type is arraylike_types.NumpyArraySequence:
        # convert to list array and replace items with numpy arrays
        depth = initial_array.ndim
        if depth == 4:
            array_before_wrap = [[[[initial_array]]]]
            shape_out = (1, 1, 1, 1, *shape_in)
        elif depth == 3:
            array_before_wrap = [[[initial_array]]]
            shape_out = (1, 1, 1, *shape_in)
        elif depth == 2:
            array_before_wrap = [[initial_array]]
            shape_out = (1, 1, *shape_in)
        elif depth == 1:
            array_before_wrap = [initial_array]
            shape_out = (1, *shape_in)
        else:
            raise RuntimeError('Unexpected test case.')

        expected = ArrayLikePropsTuple(
            array=np.array(array_before_wrap),
            shape=shape_out,
            dtype=np.array(array_before_wrap).dtype,
            ndim=np.array(array_before_wrap).ndim,
            wrapper=_NumpyArrayWrapper,
            return_original=False,
        )

    elif arraylike_type in [arraylike_types.NumberSequence1D, arraylike_types.NumberSequence2D]:
        if is_empty:
            # Cannot infer dtype from an empty sequence at runtime,
            # so we assume the dtype is float by default
            dtype_out = float
            # Check this matches default numpy behavior
            assert np.array([()]).dtype.type is np.float64
        else:
            dtype_out = dtype_in
        depth = initial_array.ndim
        array_before_wrap = initial_array.tolist()
        if depth in (1, 2):
            if depth == 1:
                wrapper = _Sequence1DWrapper
            else:
                wrapper = _Sequence2DWrapper

            # sequence is expected as-is
            expected = ArrayLikePropsTuple(
                array=array_before_wrap,
                shape=shape_in,
                dtype=dtype_out,
                ndim=depth,
                wrapper=wrapper,
                return_original=True,
            )
        else:
            # cast to a numpy array
            expected = ArrayLikePropsTuple(
                array=np.asarray(array_before_wrap),
                shape=shape_in,
                dtype=dtype_out,
                ndim=depth,
                wrapper=_NumpyArrayWrapper,
                return_original=False,
            )
    else:
        raise RuntimeError("Unexpected test case.")

    # Test abstract wrapper
    actual = _ArrayLikeWrapper(array_before_wrap)
    assert np.array_equal(actual._array, expected.array)
    assert actual.shape == expected.shape
    assert actual.dtype == expected.dtype
    assert actual.ndim == expected.ndim
    assert type(actual) is expected.wrapper

    # Test child wrapper
    actual = expected.wrapper(array_before_wrap)
    assert np.array_equal(actual._array, expected.array)
    assert actual.shape == expected.shape
    assert actual.dtype == expected.dtype
    assert actual.ndim == expected.ndim
    assert type(actual) is expected.wrapper


ragged_arrays = (
    [[1, 2, 3], [4, 5], [6, 7, 8, 9]],
    [np.array([1, 2, 3]), np.array([4, 5]), np.array([6, 7, 8, 9])],
)


@pytest.mark.skipif(
    sys.platform == 'linux' and sys.version_info < (3, 9, 0),
    reason="Numpy raise a warning, not an error.",
)
@pytest.mark.parametrize('ragged_array', ragged_arrays)
def test_get_sequence_shape_raises_error_for_ragged_arrays(ragged_array):
    match = 'inhomogeneous shape'
    with pytest.raises(ValueError, match=match):
        _ArrayLikeWrapper(ragged_array)
    # test this matches numpy array behavior
    with pytest.raises(ValueError, match=match):
        np.array(ragged_array)
