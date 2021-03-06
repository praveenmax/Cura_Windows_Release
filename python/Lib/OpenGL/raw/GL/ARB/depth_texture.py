'''OpenGL extension ARB.depth_texture

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
EXTENSION_NAME = 'GL_ARB_depth_texture'
_DEPRECATED = False
GL_DEPTH_COMPONENT16_ARB = constant.Constant( 'GL_DEPTH_COMPONENT16_ARB', 0x81A5 )
GL_DEPTH_COMPONENT24_ARB = constant.Constant( 'GL_DEPTH_COMPONENT24_ARB', 0x81A6 )
GL_DEPTH_COMPONENT32_ARB = constant.Constant( 'GL_DEPTH_COMPONENT32_ARB', 0x81A7 )
GL_TEXTURE_DEPTH_SIZE_ARB = constant.Constant( 'GL_TEXTURE_DEPTH_SIZE_ARB', 0x884A )
GL_DEPTH_TEXTURE_MODE_ARB = constant.Constant( 'GL_DEPTH_TEXTURE_MODE_ARB', 0x884B )


def glInitDepthTextureARB():
    '''Return boolean indicating whether this extension is available'''
    return extensions.hasGLExtension( EXTENSION_NAME )
