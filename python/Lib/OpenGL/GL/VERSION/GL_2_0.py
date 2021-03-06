'''OpenGL extension VERSION.GL_2_0

This module customises the behaviour of the 
OpenGL.raw.GL.VERSION.GL_2_0 to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/VERSION/GL_2_0.txt
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL.VERSION.GL_2_0 import *
### END AUTOGENERATED SECTION
import OpenGL
from OpenGL.raw.GL.ARB.shader_objects import GL_OBJECT_COMPILE_STATUS_ARB as GL_OBJECT_COMPILE_STATUS
from OpenGL.raw.GL.ARB.shader_objects import GL_OBJECT_LINK_STATUS_ARB as GL_OBJECT_LINK_STATUS
from OpenGL.raw.GL.ARB.shader_objects import GL_OBJECT_ACTIVE_UNIFORMS_ARB as GL_OBJECT_ACTIVE_UNIFORMS
from OpenGL.raw.GL.ARB.shader_objects import GL_OBJECT_ACTIVE_UNIFORM_MAX_LENGTH_ARB as GL_OBJECT_ACTIVE_UNIFORM_MAX_LENGTH
from OpenGL.GL.ARB.shader_objects import glGetInfoLogARB as glGetInfoLog
from OpenGL.lazywrapper import lazy

from OpenGL import converters, error, contextdata
from OpenGL.arrays.arraydatatype import ArrayDatatype, GLenumArray
GL_INFO_LOG_LENGTH = constant.Constant( 'GL_INFO_LOG_LENGTH', 0x8B84 )

glShaderSource = platform.createExtensionFunction( 
    'glShaderSource', dll=platform.GL,
    resultType=None, 
    argTypes=(constants.GLhandle, constants.GLsizei, ctypes.POINTER(ctypes.c_char_p), arrays.GLintArray,),
    doc = 'glShaderSource( GLhandle(shaderObj),[str(string),...]) -> None',
    argNames = ('shaderObj', 'count', 'string', 'length',),
    extension = EXTENSION_NAME,
)
conv = converters.StringLengths( name='string' )
glShaderSource = wrapper.wrapper(
    glShaderSource
).setPyConverter(
    'count' # number of strings
).setPyConverter( 
    'length' # lengths of strings
).setPyConverter(
    'string', conv.stringArray
).setCResolver(
    'string', conv.stringArrayForC,
).setCConverter(
    'length', conv,
).setCConverter(
    'count', conv.totalCount,
)
del conv

for size in (1,2,3,4):
    for format,arrayType in (
        ('f',arrays.GLfloatArray),
        ('i',arrays.GLintArray),
    ):
        name = 'glUniform%(size)s%(format)sv'%globals()
        globals()[name] = arrays.setInputArraySizeType(
            globals()[name],
            None, # don't want to enforce size...
            arrayType, 
            'value',
        )
        del format, arrayType
    del size,name

@lazy( glGetShaderiv )
def glGetShaderiv( baseOperation, shader, pname, status=None ):
    """Retrieve the integer parameter for the given shader
    
    shader -- shader ID to query 
    pname -- parameter name 
    status -- pointer to integer to receive status or None to 
        return the parameter as an integer value 
    
    returns 
        integer if status parameter is None
        status if status parameter is not None
    """
    if status is None:
        status = arrays.GLintArray.zeros( (1,))
        status[0] = 1 
        baseOperation(
            shader, pname, status
        )
        return status[0]
    else:
        baseOperation(
            shader, pname, status
        )
        return status
@lazy( glGetProgramiv )
def glGetProgramiv( baseOperation, program, pname, params=None ):
    """Will automatically allocate params if not provided"""
    if params is None:
        params = arrays.GLintArray.zeros( (1,))
        baseOperation( program, pname, params )
        return params[0]
    else:
        baseOperation( program,pname, params )
        return params

def _afterCheck( key ):
    """Generate an error-checking function for compilation operations"""
    if key == GL_OBJECT_COMPILE_STATUS:
        getter = glGetShaderiv
    else:
        getter = glGetProgramiv
    def GLSLCheckError( 
        result,
        baseOperation=None,
        cArguments=None,
        *args
    ):
        result = error.glCheckError( result, baseOperation, cArguments, *args )
        status = ctypes.c_int()
        getter( cArguments[0], key, ctypes.byref(status))
        status = status.value
        if not status:
            raise error.GLError( 
                result = result,
                baseOperation = baseOperation,
                cArguments = cArguments,
                description= glGetInfoLog( cArguments[0] )
            )
        return result
    return GLSLCheckError

if OpenGL.ERROR_CHECKING:
    glCompileShader.errcheck = _afterCheck( GL_OBJECT_COMPILE_STATUS )
if OpenGL.ERROR_CHECKING:
    glLinkProgram.errcheck = _afterCheck( GL_OBJECT_LINK_STATUS )
## Not sure why, but these give invalid operation :(
##if glValidateProgram and OpenGL.ERROR_CHECKING:
##	glValidateProgram.errcheck = _afterCheck( GL_OBJECT_VALIDATE_STATUS )

@lazy( glGetShaderInfoLog )
def glGetShaderInfoLog( baseOperation, obj ):
    """Retrieve the shader's error messages as a Python string
    
    returns string which is '' if no message
    """
    length = int(glGetShaderiv(obj, GL_INFO_LOG_LENGTH))
    if length > 0:
        log = ctypes.create_string_buffer(length)
        baseOperation(obj, length, None, log)
        return log.value.strip('\000') # null-termination
    return ''
@lazy( glGetProgramInfoLog )
def glGetProgramInfoLog( baseOperation, obj ):
    """Retrieve the shader program's error messages as a Python string
    
    returns string which is '' if no message
    """
    length = int(glGetProgramiv(obj, GL_INFO_LOG_LENGTH))
    if length > 0:
        log = ctypes.create_string_buffer(length)
        baseOperation(obj, length, None, log)
        return log.value.strip('\000') # null-termination
    return ''

@lazy( glGetAttachedShaders )
def glGetAttachedShaders( baseOperation, obj ):
    """Retrieve the attached objects as an array of GLhandle instances"""
    length= glGetProgramiv( obj, GL_ATTACHED_SHADERS )
    if length > 0:
        storage = arrays.GLuintArray.zeros( (length,))
        baseOperation( obj, length, None, storage )
        return storage
    return arrays.GLuintArray.zeros( (0,))


@lazy( glGetShaderSource )
def glGetShaderSource( baseOperation, obj ):
    """Retrieve the program/shader's source code as a Python string
    
    returns string which is '' if no source code
    """
    length = int(glGetShaderiv(obj, GL_OBJECT_SHADER_SOURCE_LENGTH))
    if length > 0:
        source = ctypes.create_string_buffer(length)
        baseOperation(obj, length, None, source)
        return source.value.strip('\000') # null-termination
    return ''

@lazy( glGetActiveUniform )
def glGetActiveUniform(baseOperation,program, index):
    """Retrieve the name, size and type of the uniform of the index in the program"""
    max_index = int(glGetProgramiv( program, GL_OBJECT_ACTIVE_UNIFORMS ))
    length = int(glGetProgramiv( program, GL_OBJECT_ACTIVE_UNIFORM_MAX_LENGTH))
    if index < max_index and index >= 0:
        if length > 0:
            name = ctypes.create_string_buffer(length)
            size = arrays.GLintArray.zeros( (1,))
            gl_type = arrays.GLenumArray.zeros( (1,))
            namelen = arrays.GLsizeiArray.zeros( (1,))
            baseOperation(program, index, length, namelen, size, gl_type, name)
            return name.value[:int(namelen[0])], size[0], gl_type[0]
        raise ValueError( """No currently specified uniform names""" )
    raise IndexError, 'Index %s out of range 0 to %i' % (index, max_index - 1, )

@lazy( glGetUniformLocation )
def glGetUniformLocation( baseOperation, program, name ):
    """Check that name is a string with a null byte at the end of it"""
    if not name:
        raise ValueError( """Non-null name required""" )
    elif name[-1] != '\000':
        name = name + '\000'
    return baseOperation( program, name )
@lazy( glGetAttribLocation )
def glGetAttribLocation( baseOperation, program, name ):
    """Check that name is a string with a null byte at the end of it"""
    if not name:
        raise ValueError( """Non-null name required""" )
    elif name[-1] != '\000':
        name = name + '\000'
    return baseOperation( program, name )

@lazy( glVertexAttribPointer )
def glVertexAttribPointer( 
    baseOperation, index, size, type,
    normalized, stride, pointer,
):
    """Set an attribute pointer for a given shader (index)
    
    index -- the index of the generic vertex to bind, see 
        glGetAttribLocation for retrieval of the value,
        note that index is a global variable, not per-shader
    size -- number of basic elements per record, 1,2,3, or 4
    type -- enum constant for data-type 
    normalized -- whether to perform int to float 
        normalization on integer-type values
    stride -- stride in machine units (bytes) between 
        consecutive records, normally used to create 
        "interleaved" arrays 
    pointer -- data-pointer which provides the data-values,
        normally a vertex-buffer-object or offset into the 
        same.
    
    This implementation stores a copy of the data-pointer 
    in the contextdata structure in order to prevent null-
    reference errors in the renderer.
    """
    array = ArrayDatatype.asArray( pointer )
    key = ('vertex-attrib',index)
    contextdata.setValue( key, array )
    return baseOperation(
        index, size, type,
        normalized, stride, 
        ArrayDatatype.voidDataPointer( array ) 
    )

@lazy( glDrawBuffers )
def glDrawBuffers( baseOperation, n=None, bufs=None ):
    """glDrawBuffers( bufs ) -> bufs 
    
    Wrapper will calculate n from dims of bufs if only 
    one argument is provided...
    """
    if bufs is None:
        bufs = n
        n = None
    bufs = arrays.GLenumArray.asArray( bufs )
    if n is None:
        n = arrays.GLenumArray.arraySize( bufs )
    return baseOperation( n,bufs )
