'''OpenGL extension SGIX.texture_coordinate_clamp

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
EXTENSION_NAME = 'GL_SGIX_texture_coordinate_clamp'
_DEPRECATED = False
GL_TEXTURE_MAX_CLAMP_S_SGIX = constant.Constant( 'GL_TEXTURE_MAX_CLAMP_S_SGIX', 0x8369 )
GL_TEXTURE_MAX_CLAMP_T_SGIX = constant.Constant( 'GL_TEXTURE_MAX_CLAMP_T_SGIX', 0x836A )
GL_TEXTURE_MAX_CLAMP_R_SGIX = constant.Constant( 'GL_TEXTURE_MAX_CLAMP_R_SGIX', 0x836B )


def glInitTextureCoordinateClampSGIX():
    '''Return boolean indicating whether this extension is available'''
    return extensions.hasGLExtension( EXTENSION_NAME )
